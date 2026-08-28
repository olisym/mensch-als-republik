"""Golden-Tests gegen Anhang C Vektoren."""

import json
from pathlib import Path

import pytest

from tests.vectors.gen import build_vectors

GOLDEN = {
    "TV1": "f95d430e40df736cbdffd7bf82af4f77e0c7af8692565f3b2a151c2c1ae8660c",
    "TV2": "29b66881810bbbf1e254e061c35395e15da6c064327c2d33dfa6aa29d47dc2a6",
    "TV3": "8e76a2a9ee6677e6959bf9868dc6d162e5ff7e464a6bb4c6b839f89713e54629",
    "TV4": "0bd77591da5e480a8c9a573382d14407a1770e0a7f6d2d09776b630fbd7ca01c",
    "NV1": "9b25020fee7da6832416f8bcb61e4a05329776d051a4da282db7e973eb96c453",
    "NV3": "e14ebd82eb172672a4a3ccbc330fef64fecd86e4664f72eab538855c9cef5c8b",
    "TV5": "8b19196274b2a8ac08e9a34337de5f445e6efd19fb75155eb187b069f5fd8022",
}

GOLDEN_SIGMA = {
    "TV1": (
        "ef3b6674898a1f037bdb58dc485926b4f0de01ef995d6cbf7d6387c4dd33679f"
        "63da403f2f2d1c4bb39513484dee2c74387ec904bbab0aa22b8bdb376fb1c401"
    ),
}


@pytest.fixture(scope="module")
def vectors_file():
    path = Path(__file__).resolve().parent / "vectors" / "vectors_01.json"
    return json.loads(path.read_text())


@pytest.fixture(scope="module")
def regenerated():
    return build_vectors()


def test_vectors_json_exists(vectors_file):
    assert vectors_file["params"]["N"] == (
        "65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557"
    )


@pytest.mark.parametrize("name", list(GOLDEN.keys()))
def test_claim_id_matches_golden(name: str, regenerated: dict):
    vec = next(v for v in regenerated["vectors"] if v.get("name") == name)
    assert vec["claim_id"] == GOLDEN[name]


def test_tv1_core_bytes_match_spec(regenerated: dict):
    tv1 = next(v for v in regenerated["vectors"] if v["name"] == "TV1")
    expected_core = (
        "a900010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c"
        "02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394"
        "03784c6e75633a363533303966653233336461333066646130363164376335656630303262"
        "366238306534323638326364353464373033616231336662366337643266353535372f766f"
        "75636840310444a100186405582065309fe233da30fda061d7c5ef002b6b80e42682cd54d"
        "703ab13fb6c7d2f5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371"
        "d631845fdd5858dd94c37d327a28f73b25625430"
    )
    assert tv1["core_bytes"] == expected_core


def test_tv1_sigma_matches_spec(regenerated: dict):
    tv1 = next(v for v in regenerated["vectors"] if v["name"] == "TV1")
    assert tv1["sigma"] == GOLDEN_SIGMA["TV1"]
