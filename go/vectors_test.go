package main

import (
	"bytes"
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/hex"
)

const (
	aliceIHex       = "8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c"
	bobIHex         = "8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394"
	scopeNHex       = "65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557"
	aliceGenesisHex = "62db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f73b25625430"
	bobGenesisHex   = "d507038f3b07c8642b65e9b3cf559204d9ad7aa0a3faee674d4284a5d9e43abe"
	tv1ClaimIDHex   = "f95d430e40df736cbdffd7bf82af4f77e0c7af8692565f3b2a151c2c1ae8660c"
	tv1SigHex       = "ef3b6674898a1f037bdb58dc485926b4f0de01ef995d6cbf7d6387c4dd33679f" +
		"63da403f2f2d1c4bb39513484dee2c74387ec904bbab0aa22b8bdb376fb1c401"
	tv1CoreHex = "a900010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374" +
		"8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4" +
		"ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330" +
		"6664613036316437633565663030326236623830653432363832636435346437" +
		"3033616231336662366337643266353535372f766f75636840310444a1001864" +
		"05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d" +
		"2f5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d631" +
		"845fdd5858dd94c37d327a28f73b25625430"
	tv1Pred = "nuc:65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557/vouch@1"
)

func aliceSeed() []byte { return bytes.Repeat([]byte{0x01}, 32) }
func bobSeed() []byte   { return bytes.Repeat([]byte{0x02}, 32) }

func alicePub() []byte {
	return ed25519.NewKeyFromSeed(aliceSeed()).Public().(ed25519.PublicKey)
}
func bobPub() []byte {
	return ed25519.NewKeyFromSeed(bobSeed()).Public().(ed25519.PublicKey)
}

func genesisAnchor(identity []byte) []byte {
	sum := sha256.Sum256(append([]byte(domIDGen), identity...))
	out := make([]byte, 32)
	copy(out, sum[:])
	return out
}

func mustHex(s string) []byte {
	b, err := hex.DecodeString(s)
	if err != nil {
		panic(err)
	}
	return b
}

func tv1CoreFields() map[uint64]cborValue {
	return map[uint64]cborValue{
		0: cborUintVal(1),
		1: cborBytesVal(mustHex(aliceIHex)),
		2: cborArrayVal(cborUintVal(1), cborBytesVal(mustHex(bobIHex))),
		3: cborTextVal(tv1Pred),
		4: cborBytesVal(mustHex("a1001864")),
		5: cborBytesVal(mustHex(scopeNHex)),
		6: cborUintVal(1700000000),
		7: cborUintVal(1735689600),
		8: cborBytesVal(mustHex(aliceGenesisHex)),
	}
}

func tv1FullClaim() []byte {
	fields := tv1CoreFields()
	fields[9] = cborBytesVal(mustHex(tv1SigHex))
	return encodeCBOR(cborMapUint(fields))
}

func signFields(seed []byte, fields map[uint64]cborValue) []byte {
	core := encodeCBOR(cborMapUint(fields))
	priv := ed25519.NewKeyFromSeed(seed)
	sig := ed25519.Sign(priv, append([]byte(domSIG), core...))
	full := make(map[uint64]cborValue, len(fields)+1)
	for k, v := range fields {
		full[k] = v
	}
	full[9] = cborBytesVal(sig)
	return encodeCBOR(cborMapUint(full))
}

func baseNucFields(p string, n []byte) map[uint64]cborValue {
	m := map[uint64]cborValue{
		0: cborUintVal(1),
		1: cborBytesVal(alicePub()),
		2: cborArrayVal(cborUintVal(1), cborBytesVal(bobPub())),
		3: cborTextVal(p),
		6: cborUintVal(1700000000),
		8: cborBytesVal(genesisAnchor(alicePub())),
	}
	if n != nil {
		m[5] = cborBytesVal(n)
	}
	return m
}

func baseCoreFields(pred string, jTag uint64, jVal []byte) map[uint64]cborValue {
	return map[uint64]cborValue{
		0: cborUintVal(1),
		1: cborBytesVal(alicePub()),
		2: cborArrayVal(cborUintVal(jTag), cborBytesVal(jVal)),
		3: cborTextVal(pred),
		6: cborUintVal(1700000000),
		8: cborBytesVal(genesisAnchor(alicePub())),
	}
}
