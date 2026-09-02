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
    "NV4": "382810f6d71a1767c96e678a05519da48713a556f0277f8a97732b9d9714bf09",
    "NV5": "341cd38cebb06e8b9b2b33c10def16530df4576862c5dc92d98dc9fecadd8a7d",
    "NV6": "e9a3dbb5903dba124c2c746e4a8a2180454fba7527ac406e57af40bfd8c9824a",
    "NV7": "0c9b903b704dd4f996522cef13f96bfa2fb9f553196579981ba58d39801c3099",
    "NV8": "52c26cea614c8460f859a6e0756eb8cbb6e3cf7b8409547f3f41e5d727af60b5",
    "NV9": "614aab79e4bea65dd486b46f95a4d1f50ad03205f92aac14e454b4446fd71969",
    "NV10": "f4541adfc37c1d42b880cee040c1018772f47020736bc02ed3d4b21fed7b611b",
    "NV11": "32dd820ac291f75319369563f9eb10fe30de77607cb24cbb5a6778798a57ff3c",
    "TV6": "990b870c9e1c92d7fc442c70cdfe3b2d06d04ca41c522c6efe9e0834902d952e",
    "NV12": "8d253635ff9d59cca68fa760c589a3393551053a4ea08a5c78ce936d7541bddc",
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


def test_vectors_file_matches_build_vectors(vectors_file: dict, regenerated: dict):
    assert vectors_file == regenerated
