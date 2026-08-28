package main

import (
	"bytes"
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/hex"
	"strings"
)

const (
	classUnsupportedVersion    = "UNSUPPORTED_VERSION"
	classNonCanonicalEncoding  = "NON_CANONICAL_ENCODING"
	classMalformedCBOR         = "MALFORMED_CBOR"
	classUnknownJTag           = "UNKNOWN_J_TAG"
	classUnknownNamespace      = "UNKNOWN_NAMESPACE"
	classBadScopeBinding       = "BAD_SCOPE_BINDING"
	classReservedCorePredicate = "RESERVED_CORE_PREDICATE"
	classForeignLifecycle      = "FOREIGN_LIFECYCLE"
	classBadSignature          = "BAD_SIGNATURE"
	classInvalidGenesisAnchor  = "INVALID_GENESIS_ANCHOR"
	classIncoherentExpiry      = "INCOHERENT_EXPIRY"
)

const (
	domSIG   = "claim-atom/v1/sig"
	domCID   = "claim-atom/v1/cid"
	domIDGen = "claim-atom/v1/id-genesis"
)

type outcome struct {
	accept bool
	id     []byte
	reject string
}

func (o outcome) line() string {
	if o.accept {
		return "ok " + hex.EncodeToString(o.id)
	}
	return "reject " + o.reject
}

func reject(class string) outcome {
	return outcome{reject: class}
}

func verifyHex(line string) outcome {
	line = strings.TrimSpace(line)
	raw, err := hex.DecodeString(line)
	if err != nil {
		return reject(classMalformedCBOR)
	}
	return verify(raw)
}

func verify(raw []byte) outcome {
	v, err := decodeCBOR(raw)
	if err != nil {
		return reject(classMalformedCBOR)
	}
	if !bytes.Equal(encodeCBOR(v), raw) {
		return reject(classNonCanonicalEncoding)
	}

	fields, extra, ok := uintKeyMap(v)
	if !ok {
		return reject(classMalformedCBOR)
	}

	ver, ok := asUint(fields, 0)
	if !ok {
		return reject(classMalformedCBOR)
	}
	if ver != 1 {
		return reject(classUnsupportedVersion)
	}
	if extra {
		return reject(classMalformedCBOR)
	}

	c, errClass := parseV1Claim(fields)
	if errClass != "" {
		return reject(errClass)
	}

	if c.jTag != 1 && c.jTag != 2 && c.jTag != 3 {
		return reject(classUnknownJTag)
	}

	pred, errClass := parsePredicate(c.p)
	if errClass != "" {
		return reject(errClass)
	}

	switch pred.kind {
	case predCore:
		if c.jTag != 2 {
			return reject(classForeignLifecycle)
		}
	case predNucCanonical:
		if !c.hasN || !bytes.Equal(c.n, pred.scopeID) {
			return reject(classBadScopeBinding)
		}
	case predNucAlias:
		if !c.hasN {
			return reject(classBadScopeBinding)
		}
	}

	if isZero32(c.hPrev) {
		return reject(classInvalidGenesisAnchor)
	}

	if c.hasTExp && pred.kind != predCore && c.t >= c.tExp {
		return reject(classIncoherentExpiry)
	}

	core := cborMapUint(coreFields(fields))
	coreBytes := encodeCBOR(core)
	msg := append([]byte(domSIG), coreBytes...)
	if !ed25519.Verify(ed25519.PublicKey(c.i), msg, c.sig) {
		return reject(classBadSignature)
	}

	sum := sha256.Sum256(append([]byte(domCID), coreBytes...))
	id := make([]byte, 32)
	copy(id, sum[:])
	return outcome{accept: true, id: id}
}

type claim struct {
	i       []byte
	jTag    uint64
	jVal    []byte
	p       string
	hasN    bool
	n       []byte
	t       uint64
	hasTExp bool
	tExp    uint64
	hPrev   []byte
	sig     []byte
}

func parseV1Claim(fields map[uint64]cborValue) (claim, string) {
	required := []uint64{1, 2, 3, 6, 8, 9}
	for _, k := range required {
		if _, ok := fields[k]; !ok {
			return claim{}, classMalformedCBOR
		}
	}

	var c claim
	var ok bool

	c.i, ok = asBytesLen(fields, 1, 32)
	if !ok {
		return claim{}, classMalformedCBOR
	}

	j, ok := fields[2]
	if !ok || j.kind != cborArray || len(j.a) != 2 {
		return claim{}, classMalformedCBOR
	}
	if j.a[0].kind != cborUint {
		return claim{}, classMalformedCBOR
	}
	c.jTag = j.a[0].u
	if j.a[1].kind != cborBytes || len(j.a[1].b) != 32 {
		return claim{}, classMalformedCBOR
	}
	c.jVal = j.a[1].b

	if fields[3].kind != cborText {
		return claim{}, classMalformedCBOR
	}
	c.p = fields[3].t

	if v, present := fields[4]; present {
		if v.kind != cborBytes {
			return claim{}, classMalformedCBOR
		}
	}

	if n, present := fields[5]; present {
		if n.kind != cborBytes || len(n.b) != 32 {
			return claim{}, classMalformedCBOR
		}
		c.hasN = true
		c.n = n.b
	}

	c.t, ok = asUint(fields, 6)
	if !ok {
		return claim{}, classMalformedCBOR
	}

	if tExp, present := fields[7]; present {
		if tExp.kind != cborUint {
			return claim{}, classMalformedCBOR
		}
		c.hasTExp = true
		c.tExp = tExp.u
	}

	c.hPrev, ok = asBytesLen(fields, 8, 32)
	if !ok {
		return claim{}, classMalformedCBOR
	}
	c.sig, ok = asBytesLen(fields, 9, 64)
	if !ok {
		return claim{}, classMalformedCBOR
	}
	return c, ""
}

func uintKeyMap(v cborValue) (map[uint64]cborValue, bool, bool) {
	if v.kind != cborMap {
		return nil, false, false
	}
	out := make(map[uint64]cborValue, len(v.m))
	extra := false
	for _, p := range v.m {
		if p.k.kind != cborUint {
			return nil, false, false
		}
		out[p.k.u] = p.v
		if p.k.u > 9 {
			extra = true
		}
	}
	return out, extra, true
}

func asUint(fields map[uint64]cborValue, k uint64) (uint64, bool) {
	v, ok := fields[k]
	if !ok || v.kind != cborUint {
		return 0, false
	}
	return v.u, true
}

func asBytesLen(fields map[uint64]cborValue, k uint64, n int) ([]byte, bool) {
	v, ok := fields[k]
	if !ok || v.kind != cborBytes || len(v.b) != n {
		return nil, false
	}
	return v.b, true
}

func coreFields(fields map[uint64]cborValue) map[uint64]cborValue {
	out := make(map[uint64]cborValue, len(fields))
	for k, v := range fields {
		if k == 9 {
			continue
		}
		out[k] = v
	}
	return out
}

func isZero32(b []byte) bool {
	for _, x := range b {
		if x != 0 {
			return false
		}
	}
	return len(b) == 32
}

type predKind int

const (
	predCore predKind = iota
	predNucCanonical
	predNucAlias
)

type parsedPred struct {
	kind    predKind
	scopeID []byte
}

func parsePredicate(p string) (parsedPred, string) {
	ns, rest, ok := splitOnce(p, '/')
	if !ok {
		return parsedPred{}, classUnknownNamespace
	}
	name, ver, ok := splitOnce(rest, '@')
	if !ok {
		if ns == "core" {
			return parsedPred{}, classReservedCorePredicate
		}
		return parsedPred{}, classUnknownNamespace
	}

	if ns == "core" {
		if !validName(name) || !validVersion(ver) || ver != "1" || (name != "revoke" && name != "supersede") {
			return parsedPred{}, classReservedCorePredicate
		}
		return parsedPred{kind: predCore}, ""
	}

	if strings.HasPrefix(ns, "nuc:") {
		if !validName(name) || !validVersion(ver) {
			return parsedPred{}, classUnknownNamespace
		}
		scope := ns[len("nuc:"):]
		if validCanonicalScope(scope) {
			id, err := hex.DecodeString(scope)
			if err != nil || len(id) != 32 {
				return parsedPred{}, classUnknownNamespace
			}
			return parsedPred{kind: predNucCanonical, scopeID: id}, ""
		}
		if validAliasScope(scope) {
			return parsedPred{kind: predNucAlias}, ""
		}
		return parsedPred{}, classUnknownNamespace
	}

	return parsedPred{}, classUnknownNamespace
}

func splitOnce(s string, sep byte) (string, string, bool) {
	i := strings.IndexByte(s, sep)
	if i < 0 {
		return "", "", false
	}
	return s[:i], s[i+1:], true
}

func validName(s string) bool {
	if s == "" {
		return false
	}
	for i := 0; i < len(s); i++ {
		if !isNameChar(s[i]) {
			return false
		}
	}
	return true
}

func validVersion(s string) bool {
	if s == "" || s[0] < '1' || s[0] > '9' {
		return false
	}
	for i := 1; i < len(s); i++ {
		if s[i] < '0' || s[i] > '9' {
			return false
		}
	}
	return true
}

func validCanonicalScope(s string) bool {
	if len(s) != 64 {
		return false
	}
	for i := 0; i < 64; i++ {
		c := s[i]
		if (c < '0' || c > '9') && (c < 'a' || c > 'f') {
			return false
		}
	}
	return true
}

func validAliasScope(s string) bool {
	if !validName(s) {
		return false
	}
	return !validCanonicalScope(s)
}

func isNameChar(c byte) bool {
	return (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == '-' || c == '_'
}
