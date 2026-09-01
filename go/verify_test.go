package main

import (
	"bytes"
	"encoding/hex"
	"strings"
	"testing"
)

func TestTV1Accept(t *testing.T) {
	raw := tv1FullClaim()
	o := verify(raw)
	if !o.accept {
		t.Fatalf("rejected TV1: %s", o.reject)
	}
	if hex.EncodeToString(o.id) != tv1ClaimIDHex {
		t.Fatalf("claim_id got %x want %s", o.id, tv1ClaimIDHex)
	}
	line := o.line()
	want := "ok " + tv1ClaimIDHex
	if line != want {
		t.Fatalf("line got %q want %q", line, want)
	}
}

func TestTV1HexRoundtrip(t *testing.T) {
	raw := tv1FullClaim()
	o := verifyHex(hex.EncodeToString(raw))
	if !o.accept {
		t.Fatalf("rejected: %s", o.reject)
	}
	o2 := verifyHex(strings.ToUpper(hex.EncodeToString(raw)))
	if !o2.accept {
		t.Fatalf("uppercase hex rejected: %s", o2.reject)
	}
}

func TestVerifyTable(t *testing.T) {
	n := mustHex(scopeNHex)
	canonicalP := tv1Pred
	aliasP := "nuc:hasenpfote/vouch@1"
	target := bytes.Repeat([]byte{0xab}, 32)

	cases := []struct {
		name string
		raw  []byte
		hex  string
		want string
	}{
		{
			name: "empty input",
			hex:  "",
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "odd hex",
			hex:  "abc",
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "invalid hex",
			hex:  "zz",
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "interior whitespace in hex",
			hex:  "a9 00",
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "truncated cbor",
			raw:  []byte{0xa9},
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "trailing bytes",
			raw:  append(tv1FullClaim(), 0x00),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "top-level array",
			raw:  []byte{0x80},
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "empty map",
			raw:  []byte{0xa0},
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "duplicate keys",
			raw:  mustHex("a200010001"),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "text map key",
			raw:  mustHex("a1616101"), // {"a": 1}
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "float64",
			raw:  []byte{0xfb, 0x3f, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00},
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "tag 0",
			raw:  []byte{0xc0, 0x00},
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "true",
			raw:  []byte{0xf5},
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "unterminated indefinite array",
			raw:  []byte{0x9f, 0x01},
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "break in value position",
			raw:  []byte{0x81, 0xff},
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "I length 31",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()[:31]),
				2: cborArrayVal(cborUintVal(1), cborBytesVal(bobPub())),
				3: cborTextVal(canonicalP),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(genesisAnchor(alicePub())),
			}),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "J length 1",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(1)),
				3: cborTextVal(canonicalP),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(genesisAnchor(alicePub())),
			}),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "J value length 31",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(1), cborBytesVal(bobPub()[:31])),
				3: cborTextVal(canonicalP),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(genesisAnchor(alicePub())),
			}),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "p is bytes not text",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(1), cborBytesVal(bobPub())),
				3: cborBytesVal([]byte(canonicalP)),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(genesisAnchor(alicePub())),
			}),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "missing sigma",
			raw:  encodeCBOR(cborMapUint(tv1CoreFields())),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "sigma length 63",
			raw: func() []byte {
				fields := tv1CoreFields()
				fields[9] = cborBytesVal(mustHex(tv1SigHex)[:63])
				return encodeCBOR(cborMapUint(fields))
			}(),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "extra key 10",
			raw: signFields(aliceSeed(), func() map[uint64]cborValue {
				m := tv1CoreFields()
				m[10] = cborUintVal(0)
				return m
			}()),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "version as text",
			raw:  mustHex("a1617601"), // {"v": 1} not even key 0
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "t as negative",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(1), cborBytesVal(bobPub())),
				3: cborTextVal(canonicalP),
				5: cborBytesVal(n),
				6: {kind: cborNint, u: 0}, // -1
				8: cborBytesVal(genesisAnchor(alicePub())),
			}),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "non-shortest version integer",
			raw: func() []byte {
				good := tv1FullClaim()
				// key 0 value 1 is 0x00 0x01 at the start after map head aa
				// aa 00 01 ... → replace 01 with 18 01
				out := make([]byte, 0, len(good)+1)
				out = append(out, good[0]) // aa
				if good[1] != 0x00 || good[2] != 0x01 {
					panic("unexpected TV1 prefix")
				}
				out = append(out, 0x00, 0x18, 0x01)
				out = append(out, good[3:]...)
				return out
			}(),
			want: "reject NON_CANONICAL_ENCODING",
		},
		{
			name: "unsorted map keys",
			raw:  mustHex("a201010001"), // {1:1, 0:1}
			want: "reject NON_CANONICAL_ENCODING",
		},
		{
			name: "indefinite array as top-level",
			raw:  []byte{0x9f, 0x01, 0xff},
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "indefinite map with text key",
			raw:  mustHex("bf616100ff"),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "indefinite J array",
			raw: func() []byte {
				good := tv1FullClaim()
				idx := bytes.Index(good, []byte{0x02, 0x82, 0x01, 0x58, 0x20})
				if idx < 0 {
					panic("J prefix not found")
				}
				jValStart := idx + 5
				jValEnd := jValStart + 32
				out := append([]byte{}, good[:idx+1]...)
				out = append(out, 0x9f, 0x01, 0x58, 0x20)
				out = append(out, good[jValStart:jValEnd]...)
				out = append(out, 0xff)
				out = append(out, good[jValEnd:]...)
				return out
			}(),
			want: "reject NON_CANONICAL_ENCODING",
		},
		{
			name: "indefinite byte string for I",
			raw: func() []byte {
				good := tv1FullClaim()
				// 01 58 20 <32 I bytes>
				idx := bytes.Index(good, append([]byte{0x01, 0x58, 0x20}, alicePub()...))
				if idx < 0 {
					panic("I prefix not found")
				}
				out := append([]byte{}, good[:idx+1]...)
				out = append(out, 0x5f, 0x58, 0x20)
				out = append(out, alicePub()...)
				out = append(out, 0xff)
				out = append(out, good[idx+2+1+32:]...)
				return out
			}(),
			want: "reject NON_CANONICAL_ENCODING",
		},
		{
			name: "version 2 only",
			raw:  encodeCBOR(cborMapUint(map[uint64]cborValue{0: cborUintVal(2)})),
			want: "reject UNSUPPORTED_VERSION",
		},
		{
			name: "version 0",
			raw:  encodeCBOR(cborMapUint(map[uint64]cborValue{0: cborUintVal(0)})),
			want: "reject UNSUPPORTED_VERSION",
		},
		{
			name: "version 2 extra keys still unsupported",
			raw: encodeCBOR(cborMapUint(map[uint64]cborValue{
				0:  cborUintVal(2),
				10: cborUintVal(0),
			})),
			want: "reject UNSUPPORTED_VERSION",
		},
		{
			name: "unknown J tag 0",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(0), cborBytesVal(bobPub())),
				3: cborTextVal(canonicalP),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(genesisAnchor(alicePub())),
			}),
			want: "reject UNKNOWN_J_TAG",
		},
		{
			name: "unknown J tag 4",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(4), cborBytesVal(bobPub())),
				3: cborTextVal(canonicalP),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(genesisAnchor(alicePub())),
			}),
			want: "reject UNKNOWN_J_TAG",
		},
		{
			name: "unknown namespace foo",
			raw:  signFields(aliceSeed(), baseNucFields("foo/bar@1", n)),
			want: "reject UNKNOWN_NAMESPACE",
		},
		{
			name: "unknown namespace nuc-missing-colon",
			raw:  signFields(aliceSeed(), baseNucFields("nuc/vouch@1", n)),
			want: "reject UNKNOWN_NAMESPACE",
		},
		{
			name: "uppercase CORE",
			raw:  signFields(aliceSeed(), baseCoreFields("CORE/revoke@1", 2, target)),
			want: "reject UNKNOWN_NAMESPACE",
		},
		{
			name: "predicate without slash",
			raw:  signFields(aliceSeed(), baseNucFields("vouch@1", n)),
			want: "reject UNKNOWN_NAMESPACE",
		},
		{
			name: "nuc empty scope",
			raw:  signFields(aliceSeed(), baseNucFields("nuc:/vouch@1", n)),
			want: "reject INVALID_PREDICATE",
		},
		{
			name: "nuc uppercase hex scope",
			raw: signFields(aliceSeed(), baseNucFields(
				"nuc:"+strings.ToUpper(scopeNHex)+"/vouch@1", n)),
			want: "reject INVALID_PREDICATE",
		},
		{
			name: "nuc version leading zero",
			raw:  signFields(aliceSeed(), baseNucFields("nuc:hasenpfote/vouch@01", n)),
			want: "reject INVALID_PREDICATE",
		},
		{
			name: "nuc name uppercase",
			raw:  signFields(aliceSeed(), baseNucFields("nuc:hasenpfote/Vouch@1", n)),
			want: "reject INVALID_PREDICATE",
		},
		{
			name: "nuc without slash",
			raw:  signFields(aliceSeed(), baseNucFields("nuc:hasenpfote", n)),
			want: "reject INVALID_PREDICATE",
		},
		{
			name: "reserved core foo",
			raw:  signFields(aliceSeed(), baseCoreFields("core/foo@1", 2, target)),
			want: "reject RESERVED_CORE_PREDICATE",
		},
		{
			name: "core revoke@2",
			raw:  signFields(aliceSeed(), baseCoreFields("core/revoke@2", 2, target)),
			want: "reject RESERVED_CORE_PREDICATE",
		},
		{
			name: "core rotate-key",
			raw:  signFields(aliceSeed(), baseCoreFields("core/rotate-key@1", 2, target)),
			want: "reject RESERVED_CORE_PREDICATE",
		},
		{
			name: "core without at-version",
			raw:  signFields(aliceSeed(), baseCoreFields("core/revoke", 2, target)),
			want: "reject RESERVED_CORE_PREDICATE",
		},
		{
			name: "canonical nuc without N",
			raw:  signFields(aliceSeed(), baseNucFields(canonicalP, nil)),
			want: "reject BAD_SCOPE_BINDING",
		},
		{
			name: "canonical nuc wrong N",
			raw:  signFields(aliceSeed(), baseNucFields(canonicalP, bytes.Repeat([]byte{0x11}, 32))),
			want: "reject BAD_SCOPE_BINDING",
		},
		{
			name: "alias without N",
			raw:  signFields(aliceSeed(), baseNucFields(aliasP, nil)),
			want: "reject BAD_SCOPE_BINDING",
		},
		{
			name: "core revoke with identity J",
			raw:  signFields(aliceSeed(), baseCoreFields("core/revoke@1", 1, bobPub())),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "core supersede with object-hash J",
			raw:  signFields(aliceSeed(), baseCoreFields("core/supersede@1", 3, target)),
			want: "reject MALFORMED_CBOR",
		},
		{
			name: "zero h_prev",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(1), cborBytesVal(bobPub())),
				3: cborTextVal(canonicalP),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(make([]byte, 32)),
			}),
			want: "reject INVALID_GENESIS_ANCHOR",
		},
		{
			name: "t equal t_exp",
			raw: signFields(aliceSeed(), func() map[uint64]cborValue {
				m := baseNucFields(canonicalP, n)
				m[6] = cborUintVal(100)
				m[7] = cborUintVal(100)
				return m
			}()),
			want: "reject INCOHERENT_EXPIRY",
		},
		{
			name: "t greater t_exp",
			raw: signFields(aliceSeed(), func() map[uint64]cborValue {
				m := baseNucFields(canonicalP, n)
				m[6] = cborUintVal(101)
				m[7] = cborUintVal(100)
				return m
			}()),
			want: "reject INCOHERENT_EXPIRY",
		},
		{
			name: "bad signature flipped bit",
			raw: func() []byte {
				raw := tv1FullClaim()
				raw[len(raw)-1] ^= 0x01
				return raw
			}(),
			want: "reject BAD_SIGNATURE",
		},
		{
			name: "wrong signer key I",
			raw: signFields(bobSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(1), cborBytesVal(bobPub())),
				3: cborTextVal(canonicalP),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(genesisAnchor(alicePub())),
			}),
			want: "reject BAD_SIGNATURE",
		},
		{
			name: "alias with N accepted",
			raw:  signFields(aliceSeed(), baseNucFields(aliasP, n)),
			want: "ok",
		},
		{
			name: "core revoke claim-ref accepted",
			raw:  signFields(aliceSeed(), baseCoreFields("core/revoke@1", 2, target)),
			want: "ok",
		},
		{
			name: "core supersede claim-ref accepted",
			raw:  signFields(aliceSeed(), baseCoreFields("core/supersede@1", 2, target)),
			want: "ok",
		},
		{
			name: "core revoke with t_exp ignored even if incoherent",
			raw: signFields(aliceSeed(), func() map[uint64]cborValue {
				m := baseCoreFields("core/revoke@1", 2, target)
				m[6] = cborUintVal(100)
				m[7] = cborUintVal(50)
				return m
			}()),
			want: "ok",
		},
		{
			name: "core with extra N allowed",
			raw: signFields(aliceSeed(), func() map[uint64]cborValue {
				m := baseCoreFields("core/revoke@1", 2, target)
				m[5] = cborBytesVal(n)
				return m
			}()),
			want: "ok",
		},
		{
			name: "non-genesis h_prev accepted stateless",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(1), cborBytesVal(bobPub())),
				3: cborTextVal(canonicalP),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(bytes.Repeat([]byte{0xcd}, 32)),
			}),
			want: "ok",
		},
		{
			name: "object-hash J on nuc",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(3), cborBytesVal(target)),
				3: cborTextVal("nuc:hasenpfote/accept-rules@1"),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(genesisAnchor(alicePub())),
			}),
			want: "ok",
		},
		{
			name: "claim-ref J on nuc",
			raw: signFields(aliceSeed(), map[uint64]cborValue{
				0: cborUintVal(1),
				1: cborBytesVal(alicePub()),
				2: cborArrayVal(cborUintVal(2), cborBytesVal(target)),
				3: cborTextVal(aliasP),
				5: cborBytesVal(n),
				6: cborUintVal(1),
				8: cborBytesVal(genesisAnchor(alicePub())),
			}),
			want: "ok",
		},
		{
			name: "t_exp greater than t",
			raw: signFields(aliceSeed(), func() map[uint64]cborValue {
				m := baseNucFields(aliasP, n)
				m[6] = cborUintVal(100)
				m[7] = cborUintVal(101)
				return m
			}()),
			want: "ok",
		},
		{
			name: "optional v absent",
			raw:  signFields(aliceSeed(), baseNucFields(aliasP, n)),
			want: "ok",
		},
		{
			name: "opaque v not parsed",
			raw: signFields(aliceSeed(), func() map[uint64]cborValue {
				m := baseNucFields(aliasP, n)
				m[4] = cborBytesVal([]byte{0xff, 0x00, 0x01})
				return m
			}()),
			want: "ok",
		},
		{
			name: "65-char hex-like alias is alias not canonical",
			raw: signFields(aliceSeed(), baseNucFields(
				"nuc:"+scopeNHex+"a/vouch@1", n)),
			want: "ok",
		},
		{
			name: "nuc version @10",
			raw:  signFields(aliceSeed(), baseNucFields("nuc:hasenpfote/vouch@10", n)),
			want: "ok",
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			var o outcome
			if tc.raw == nil {
				o = verifyHex(tc.hex)
			} else {
				o = verify(tc.raw)
			}
			got := o.line()
			if tc.want == "ok" {
				if !o.accept {
					t.Fatalf("got %s", got)
				}
				return
			}
			if got != tc.want {
				t.Fatalf("got %s want %s", got, tc.want)
			}
		})
	}
}

func TestProcessOneLinePerInput(t *testing.T) {
	raw := tv1FullClaim()
	in := hex.EncodeToString(raw) + "\n\nzz\n"
	var out bytes.Buffer
	if err := process(strings.NewReader(in), &out); err != nil {
		t.Fatal(err)
	}
	lines := strings.Split(strings.TrimRight(out.String(), "\n"), "\n")
	if len(lines) != 3 {
		t.Fatalf("got %d lines: %q", len(lines), lines)
	}
	if lines[0] != "ok "+tv1ClaimIDHex {
		t.Fatalf("line0 %q", lines[0])
	}
	if lines[1] != "reject MALFORMED_CBOR" {
		t.Fatalf("line1 %q", lines[1])
	}
	if lines[2] != "reject MALFORMED_CBOR" {
		t.Fatalf("line2 %q", lines[2])
	}
}

func TestEncodingPrecedesSemantics(t *testing.T) {
	// Non-canonical encoding of a map that would also be version 2.
	// {0:2} with 2 as 0x1802.
	raw := mustHex("a1001802")
	got := verify(raw).line()
	if got != "reject NON_CANONICAL_ENCODING" {
		t.Fatalf("got %s", got)
	}
}

func TestUnknownJTagPrecedesNamespace(t *testing.T) {
	raw := signFields(aliceSeed(), map[uint64]cborValue{
		0: cborUintVal(1),
		1: cborBytesVal(alicePub()),
		2: cborArrayVal(cborUintVal(9), cborBytesVal(bobPub())),
		3: cborTextVal("foo/bar@1"),
		6: cborUintVal(1),
		8: cborBytesVal(genesisAnchor(alicePub())),
	})
	got := verify(raw).line()
	if got != "reject UNKNOWN_J_TAG" {
		t.Fatalf("got %s", got)
	}
}
