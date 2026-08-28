package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"testing"
)

func TestEncodeShortestInteger(t *testing.T) {
	cases := []struct {
		n    uint64
		want string
	}{
		{0, "00"},
		{23, "17"},
		{24, "1818"},
		{255, "18ff"},
		{256, "190100"},
		{65535, "19ffff"},
		{65536, "1a00010000"},
		{1700000000, "1a6553f100"},
		{1735689600, "1a67748580"},
	}
	for _, tc := range cases {
		got := hex.EncodeToString(encodeCBOR(cborUintVal(tc.n)))
		if got != tc.want {
			t.Errorf("uint %d: got %s want %s", tc.n, got, tc.want)
		}
	}
}

func TestEncodeMapKeyOrder(t *testing.T) {
	v := cborMapUint(map[uint64]cborValue{
		2: cborUintVal(2),
		0: cborUintVal(0),
		1: cborUintVal(1),
	})
	got := hex.EncodeToString(encodeCBOR(v))
	want := "a3000001010202"
	if got != want {
		t.Errorf("got %s want %s", got, want)
	}
}

func TestDecodeDuplicateKeys(t *testing.T) {
	// {0:1, 0:1} with two encodings of the same key.
	raw, _ := hex.DecodeString("a200010001")
	if _, err := decodeCBOR(raw); err == nil {
		t.Fatal("expected malformed duplicate keys")
	}
	// semantically duplicate: key 1 as 0x01 and as 0x1801
	raw, _ = hex.DecodeString("a20101180101")
	if _, err := decodeCBOR(raw); err == nil {
		t.Fatal("expected malformed semantic duplicate keys")
	}
}

func TestDecodeTrailingBytes(t *testing.T) {
	if _, err := decodeCBOR([]byte{0x00, 0x00}); err != errTrailingCBOR {
		t.Fatalf("got %v want trailing", err)
	}
}

func TestDecodeInvalidUTF8(t *testing.T) {
	// text of length 1 with 0xff
	if _, err := decodeCBOR([]byte{0x61, 0xff}); err == nil {
		t.Fatal("expected malformed invalid utf-8")
	}
}

func TestDecodeUnterminatedIndefinite(t *testing.T) {
	if _, err := decodeCBOR([]byte{0x9f, 0x01}); err == nil {
		t.Fatal("expected malformed unterminated indefinite")
	}
}

func TestDecodeBreakInValuePosition(t *testing.T) {
	// definite array of 1, item is break
	if _, err := decodeCBOR([]byte{0x81, 0xff}); err == nil {
		t.Fatal("expected malformed break in value position")
	}
}

func TestIndefiniteRoundtripIsDefinite(t *testing.T) {
	// indefinite array [1, 2] → encode as definite 0x82 0x01 0x02
	raw := []byte{0x9f, 0x01, 0x02, 0xff}
	v, err := decodeCBOR(raw)
	if err != nil {
		t.Fatal(err)
	}
	got := encodeCBOR(v)
	want := []byte{0x82, 0x01, 0x02}
	if !bytes.Equal(got, want) {
		t.Fatalf("got %x want %x", got, want)
	}
}

func TestTV1CoreEncoding(t *testing.T) {
	core := encodeCBOR(cborMapUint(tv1CoreFields()))
	want, err := hex.DecodeString(tv1CoreHex)
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(core, want) {
		t.Fatalf("core encoding mismatch\ngot  %x\nwant %x", core, want)
	}
}

func TestSpecAnchors(t *testing.T) {
	alice := alicePub()
	bob := bobPub()
	if hex.EncodeToString(alice) != aliceIHex {
		t.Errorf("ALICE I: got %x", alice)
	}
	if hex.EncodeToString(bob) != bobIHex {
		t.Errorf("BOB I: got %x", bob)
	}
	got := hex.EncodeToString(genesisAnchor(alice))
	if got != aliceGenesisHex {
		t.Errorf("h_prev_genesis(ALICE): got %s", got)
	}
	got = hex.EncodeToString(genesisAnchor(bob))
	if got != bobGenesisHex {
		t.Errorf("h_prev_genesis(BOB): got %s", got)
	}
}

func TestTV1ClaimID(t *testing.T) {
	core, _ := hex.DecodeString(tv1CoreHex)
	sum := sha256.Sum256(append([]byte(domCID), core...))
	if hex.EncodeToString(sum[:]) != tv1ClaimIDHex {
		t.Fatalf("got %x want %s", sum[:], tv1ClaimIDHex)
	}
}
