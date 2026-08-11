"""Zusicherung: TV1 trägt das Vouch-Gewicht nach D37.

Ohne diesen Test belegt "61 grün" die Byte-Neutralität von D37 nicht — kein
bestehender Test dekodiert `v`, weil das Feld für das Atom opake Bytes ist.
Grün wäre a priori garantiert und damit aussagelos.
"""

import json
from pathlib import Path

import cbor2
import pytest

VECTORS = Path(__file__).resolve().parent / "vectors" / "vectors_01.json"


@pytest.fixture(scope="module")
def tv1():
    data = json.loads(VECTORS.read_text())
    return next(v for v in data["vectors"] if v["name"] == "TV1")


def test_tv1_ist_ein_vouch(tv1):
    core = cbor2.loads(bytes.fromhex(tv1["core_bytes"]))
    assert core[3].endswith("/vouch@1")


def test_tv1_payload_traegt_n(tv1):
    """v = {0: n} nach D37, nicht der alte Float-Vorschlag aus 01 §7.1."""
    core = cbor2.loads(bytes.fromhex(tv1["core_bytes"]))
    assert core[4] == bytes.fromhex("a1001864")
    assert cbor2.loads(core[4]) == {0: 100}


def test_tv1_payload_ist_kanonisch(tv1):
    """Die Payload-Bytes sind selbst kanonisches CBOR (01 §3)."""
    core = cbor2.loads(bytes.fromhex(tv1["core_bytes"]))
    assert cbor2.dumps(cbor2.loads(core[4]), canonical=True) == core[4]


def test_tv1_n_ist_default_bei_D_100(tv1):
    """n = 100 = D im example-nucleus ⇒ w = 1, der Default aus 02 §3.1."""
    core = cbor2.loads(bytes.fromhex(tv1["core_bytes"]))
    n = cbor2.loads(core[4])[0]
    D = 100
    assert 1 <= n <= D
    assert n == D
