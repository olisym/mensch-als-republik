package main

import (
	"bytes"
	"errors"
	"sort"
	"unicode/utf8"
)

// Deterministic CBOR (RFC 8949, Core Deterministic Encoding) for the claim atom.
// Decode accepts well-formed definite and indefinite items; Encode always emits
// definite-length, shortest-integer, sorted-map form. A byte-exact mismatch
// against the input is NON_CANONICAL_ENCODING.

var (
	errMalformedCBOR = errors.New("malformed CBOR")
	errTrailingCBOR  = errors.New("trailing CBOR bytes")
)

type cborKind int

const (
	cborUint cborKind = iota
	cborNint
	cborBytes
	cborText
	cborArray
	cborMap
)

type cborValue struct {
	kind cborKind
	u    uint64 // uint, or the raw n of a negative int (−1−n)
	b    []byte
	t    string
	a    []cborValue
	m    []cborPair
}

type cborPair struct {
	k, v cborValue
}

func cborUintVal(n uint64) cborValue { return cborValue{kind: cborUint, u: n} }

func cborBytesVal(b []byte) cborValue {
	cp := append([]byte(nil), b...)
	return cborValue{kind: cborBytes, b: cp}
}

func cborTextVal(s string) cborValue { return cborValue{kind: cborText, t: s} }

func cborArrayVal(elems ...cborValue) cborValue {
	a := make([]cborValue, len(elems))
	copy(a, elems)
	return cborValue{kind: cborArray, a: a}
}

func cborMapUint(m map[uint64]cborValue) cborValue {
	pairs := make([]cborPair, 0, len(m))
	for k, v := range m {
		pairs = append(pairs, cborPair{k: cborUintVal(k), v: v})
	}
	return cborValue{kind: cborMap, m: pairs}
}

func encodeCBOR(v cborValue) []byte {
	switch v.kind {
	case cborUint:
		return encodeHead(0, v.u)
	case cborNint:
		return encodeHead(1, v.u)
	case cborBytes:
		out := encodeHead(2, uint64(len(v.b)))
		return append(out, v.b...)
	case cborText:
		b := []byte(v.t)
		out := encodeHead(3, uint64(len(b)))
		return append(out, b...)
	case cborArray:
		out := encodeHead(4, uint64(len(v.a)))
		for _, e := range v.a {
			out = append(out, encodeCBOR(e)...)
		}
		return out
	case cborMap:
		type kv struct {
			encK []byte
			p    cborPair
		}
		items := make([]kv, len(v.m))
		for i, p := range v.m {
			items[i] = kv{encK: encodeCBOR(p.k), p: p}
		}
		sort.Slice(items, func(i, j int) bool {
			return bytes.Compare(items[i].encK, items[j].encK) < 0
		})
		out := encodeHead(5, uint64(len(items)))
		for _, it := range items {
			out = append(out, it.encK...)
			out = append(out, encodeCBOR(it.p.v)...)
		}
		return out
	default:
		panic("encodeCBOR: unknown kind")
	}
}

func encodeHead(major byte, n uint64) []byte {
	mt := major << 5
	switch {
	case n < 24:
		return []byte{mt | byte(n)}
	case n < 256:
		return []byte{mt | 24, byte(n)}
	case n < 65536:
		return []byte{mt | 25, byte(n >> 8), byte(n)}
	case n < 1<<32:
		return []byte{mt | 26, byte(n >> 24), byte(n >> 16), byte(n >> 8), byte(n)}
	default:
		return []byte{
			mt | 27,
			byte(n >> 56), byte(n >> 48), byte(n >> 40), byte(n >> 32),
			byte(n >> 24), byte(n >> 16), byte(n >> 8), byte(n),
		}
	}
}

type decoder struct {
	b []byte
	i int
}

func decodeCBOR(b []byte) (cborValue, error) {
	d := decoder{b: b}
	v, err := d.value(false)
	if err != nil {
		return cborValue{}, err
	}
	if d.i != len(d.b) {
		return cborValue{}, errTrailingCBOR
	}
	return v, nil
}

func (d *decoder) value(allowBreak bool) (cborValue, error) {
	if d.i >= len(d.b) {
		return cborValue{}, errMalformedCBOR
	}
	head := d.b[d.i]
	d.i++
	major := head >> 5
	ai := head & 0x1f

	if ai == 31 {
		if major == 7 {
			if !allowBreak {
				return cborValue{}, errMalformedCBOR
			}
			return cborValue{}, errBreak
		}
		return d.indefinite(major)
	}

	n, err := d.additional(ai)
	if err != nil {
		return cborValue{}, err
	}
	return d.definite(major, n)
}

var errBreak = errors.New("cbor break")

func (d *decoder) additional(ai byte) (uint64, error) {
	switch {
	case ai < 24:
		return uint64(ai), nil
	case ai == 24:
		if d.i >= len(d.b) {
			return 0, errMalformedCBOR
		}
		n := uint64(d.b[d.i])
		d.i++
		return n, nil
	case ai == 25:
		b, err := d.read(2)
		if err != nil {
			return 0, err
		}
		return uint64(b[0])<<8 | uint64(b[1]), nil
	case ai == 26:
		b, err := d.read(4)
		if err != nil {
			return 0, err
		}
		return uint64(b[0])<<24 | uint64(b[1])<<16 | uint64(b[2])<<8 | uint64(b[3]), nil
	case ai == 27:
		b, err := d.read(8)
		if err != nil {
			return 0, err
		}
		return uint64(b[0])<<56 | uint64(b[1])<<48 | uint64(b[2])<<40 | uint64(b[3])<<32 |
			uint64(b[4])<<24 | uint64(b[5])<<16 | uint64(b[6])<<8 | uint64(b[7]), nil
	default:
		return 0, errMalformedCBOR
	}
}

func (d *decoder) read(n int) ([]byte, error) {
	if n < 0 || d.i+n > len(d.b) {
		return nil, errMalformedCBOR
	}
	b := d.b[d.i : d.i+n]
	d.i += n
	return b, nil
}

func (d *decoder) definite(major byte, n uint64) (cborValue, error) {
	switch major {
	case 0:
		return cborValue{kind: cborUint, u: n}, nil
	case 1:
		return cborValue{kind: cborNint, u: n}, nil
	case 2:
		if n > uint64(len(d.b)-d.i) {
			return cborValue{}, errMalformedCBOR
		}
		b, err := d.read(int(n))
		if err != nil {
			return cborValue{}, err
		}
		cp := append([]byte(nil), b...)
		return cborValue{kind: cborBytes, b: cp}, nil
	case 3:
		if n > uint64(len(d.b)-d.i) {
			return cborValue{}, errMalformedCBOR
		}
		b, err := d.read(int(n))
		if err != nil {
			return cborValue{}, err
		}
		if !utf8.Valid(b) {
			return cborValue{}, errMalformedCBOR
		}
		return cborValue{kind: cborText, t: string(b)}, nil
	case 4:
		if n > uint64(len(d.b)-d.i) { // each item is at least one byte
			return cborValue{}, errMalformedCBOR
		}
		a := make([]cborValue, 0, int(n))
		for i := uint64(0); i < n; i++ {
			v, err := d.value(false)
			if err != nil {
				return cborValue{}, err
			}
			a = append(a, v)
		}
		return cborValue{kind: cborArray, a: a}, nil
	case 5:
		if n > uint64(len(d.b)-d.i) {
			return cborValue{}, errMalformedCBOR
		}
		m := make([]cborPair, 0, int(n))
		for i := uint64(0); i < n; i++ {
			k, err := d.value(false)
			if err != nil {
				return cborValue{}, err
			}
			v, err := d.value(false)
			if err != nil {
				return cborValue{}, err
			}
			for _, p := range m {
				if cborKeyEqual(p.k, k) {
					return cborValue{}, errMalformedCBOR
				}
			}
			m = append(m, cborPair{k: k, v: v})
		}
		return cborValue{kind: cborMap, m: m}, nil
	default:
		// Major 6 (tags) and 7 (floats / simples, including false/true/null)
		// are not used in the atom and are not needed to exhibit BV3.
		return cborValue{}, errMalformedCBOR
	}
}

func (d *decoder) indefinite(major byte) (cborValue, error) {
	switch major {
	case 2:
		var buf []byte
		for {
			if d.i >= len(d.b) {
				return cborValue{}, errMalformedCBOR
			}
			if d.b[d.i] == 0xff {
				d.i++
				return cborValue{kind: cborBytes, b: buf}, nil
			}
			head := d.b[d.i]
			if head>>5 != 2 || head&0x1f == 31 {
				return cborValue{}, errMalformedCBOR
			}
			d.i++
			n, err := d.additional(head & 0x1f)
			if err != nil {
				return cborValue{}, err
			}
			if n > uint64(len(d.b)-d.i) {
				return cborValue{}, errMalformedCBOR
			}
			b, err := d.read(int(n))
			if err != nil {
				return cborValue{}, err
			}
			buf = append(buf, b...)
		}
	case 3:
		var buf []byte
		for {
			if d.i >= len(d.b) {
				return cborValue{}, errMalformedCBOR
			}
			if d.b[d.i] == 0xff {
				d.i++
				if !utf8.Valid(buf) {
					return cborValue{}, errMalformedCBOR
				}
				return cborValue{kind: cborText, t: string(buf)}, nil
			}
			head := d.b[d.i]
			if head>>5 != 3 || head&0x1f == 31 {
				return cborValue{}, errMalformedCBOR
			}
			d.i++
			n, err := d.additional(head & 0x1f)
			if err != nil {
				return cborValue{}, err
			}
			if n > uint64(len(d.b)-d.i) {
				return cborValue{}, errMalformedCBOR
			}
			b, err := d.read(int(n))
			if err != nil {
				return cborValue{}, err
			}
			buf = append(buf, b...)
		}
	case 4:
		var a []cborValue
		for {
			v, err := d.value(true)
			if err == errBreak {
				return cborValue{kind: cborArray, a: a}, nil
			}
			if err != nil {
				return cborValue{}, err
			}
			a = append(a, v)
		}
	case 5:
		var m []cborPair
		for {
			if d.i >= len(d.b) {
				return cborValue{}, errMalformedCBOR
			}
			if d.b[d.i] == 0xff {
				d.i++
				return cborValue{kind: cborMap, m: m}, nil
			}
			k, err := d.value(false)
			if err != nil {
				return cborValue{}, err
			}
			v, err := d.value(false)
			if err != nil {
				return cborValue{}, err
			}
			for _, p := range m {
				if cborKeyEqual(p.k, k) {
					return cborValue{}, errMalformedCBOR
				}
			}
			m = append(m, cborPair{k: k, v: v})
		}
	default:
		return cborValue{}, errMalformedCBOR
	}
}

func cborKeyEqual(a, b cborValue) bool {
	if a.kind != b.kind {
		return false
	}
	switch a.kind {
	case cborUint, cborNint:
		return a.u == b.u
	case cborBytes:
		return bytes.Equal(a.b, b.b)
	case cborText:
		return a.t == b.t
	case cborArray:
		if len(a.a) != len(b.a) {
			return false
		}
		for i := range a.a {
			if !cborKeyEqual(a.a[i], b.a[i]) {
				return false
			}
		}
		return true
	case cborMap:
		if len(a.m) != len(b.m) {
			return false
		}
		// Semantic equality of maps ignores pair order.
		used := make([]bool, len(b.m))
		for _, p := range a.m {
			found := false
			for j, q := range b.m {
				if used[j] {
					continue
				}
				if cborKeyEqual(p.k, q.k) && cborKeyEqual(p.v, q.v) {
					used[j] = true
					found = true
					break
				}
			}
			if !found {
				return false
			}
		}
		return true
	default:
		return false
	}
}
