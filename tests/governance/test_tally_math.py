"""Schwellenarithmetik und threshold_for (04-golden-anchors.md §4–§5)."""

from __future__ import annotations

import math

from mensch_als_republik.governance.tally import (
    hopeless,
    ratio_max,
    reached,
    threshold_for,
)

from .fixtures import C1, C2, C2_HALF, C2_HIGH, C2_LOWER, C3, GENESIS_D


def test_reached_strict_greater() -> None:
    assert reached(3, 4, 3, 4) is False
    assert reached(4, 4, 3, 4) is True


def test_hopeless_without_full_turnout() -> None:
    assert hopeless(2, 4, 3, 4) is True
    assert hopeless(0, 4, 3, 4) is False


def test_ratio_max_lower_keeps_old() -> None:
    assert ratio_max((3, 4), (1, 2)) == (3, 4)


def test_ratio_max_raise_takes_new() -> None:
    assert ratio_max((1, 2), (4, 5)) == (4, 5)


def test_threshold_for_membership_only_participants() -> None:
    klass, applied = threshold_for(C1, C2, GENESIS_D)
    assert klass == "membership"
    assert applied == (2, 3)


def test_threshold_for_amendment_from_genesis() -> None:
    klass, applied = threshold_for(C2, C3, GENESIS_D)
    assert klass == "amendment"
    assert applied == (3, 4)


def test_threshold_for_ratio_max_on_lower() -> None:
    klass, applied = threshold_for(C2, C2_LOWER, GENESIS_D)
    assert klass == "amendment"
    assert applied == (3, 4)


def test_threshold_for_ratio_max_on_raise() -> None:
    klass, applied = threshold_for(C2_HALF, C2_HIGH, GENESIS_D)
    assert klass == "amendment"
    assert applied == (4, 5)


def test_INV_04_2_passed_and_failed_exclusive() -> None:
    for n in range(1, 13):
        for den in range(1, 9):
            for num in range(1, den):
                if math.gcd(num, den) != 1:
                    continue
                if num * 2 < den:
                    continue
                for yes in range(n + 1):
                    for no in range(n - yes + 1):
                        assert not (
                            reached(yes, n, num, den) and hopeless(no, n, num, den)
                        )


def test_INV_04_6_at_most_one_passed_if_yes_disjoint() -> None:
    for n in range(1, 13):
        for den in range(1, 9):
            for num in range(1, den):
                if math.gcd(num, den) != 1:
                    continue
                if num * 2 < den:
                    continue
                for yes_a in range(n + 1):
                    for yes_b in range(n - yes_a + 1):
                        assert not (
                            reached(yes_a, n, num, den) and reached(yes_b, n, num, den)
                        )
