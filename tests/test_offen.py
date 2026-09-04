"""Nummerierte Posten: Lücken, Dubletten, Nennungen ohne Posten (D316, D229)."""

from __future__ import annotations

from tools.offen import findings, mentioned_numbers, post_numbers


def _posts(*nums: int) -> str:
    return "".join(f"### O{n} Titel {n}\n" for n in nums)


def test_count_is_derived_from_generated_headings() -> None:
    nums = (1, 2, 3, 4)
    parsed = post_numbers(_posts(*nums))
    assert parsed == list(nums)
    assert findings(parsed, set(parsed)) == []
    assert len(parsed) == len(nums)


def test_gap_in_the_middle_is_derived() -> None:
    nums = (1, 2, 4, 5)
    parsed = post_numbers(_posts(*nums))
    missing = sorted(set(range(1, max(parsed) + 1)) - set(parsed))
    problems = findings(parsed, set(parsed))
    joined = " ".join(problems)
    assert missing
    for n in missing:
        assert f"O{n}" in joined


def test_duplicate_is_derived_from_repeated_heading() -> None:
    nums = (1, 2, 2, 3)
    parsed = post_numbers(_posts(*nums))
    dupes = sorted({n for n in parsed if parsed.count(n) > 1})
    problems = findings(parsed, set(parsed))
    joined = " ".join(problems)
    assert dupes
    for n in dupes:
        assert f"O{n}" in joined


def test_mention_without_post_is_derived() -> None:
    nums = (1, 2, 3)
    text = _posts(*nums) + "siehe O99 und O100\n"
    parsed = post_numbers(text)
    mentioned = mentioned_numbers(text)
    extra = sorted(mentioned - set(parsed))
    problems = findings(parsed, mentioned)
    joined = " ".join(problems)
    assert extra
    for n in extra:
        assert f"O{n}" in joined


def test_post_without_mention_is_not_a_finding() -> None:
    nums = (1, 2, 3)
    parsed = post_numbers(_posts(*nums))
    mentioned = {parsed[0]}
    assert set(parsed) - mentioned
    assert findings(parsed, mentioned) == []


def test_start_at_one_is_derived() -> None:
    nums = (2, 3)
    parsed = post_numbers(_posts(*nums))
    missing = sorted(set(range(1, max(parsed) + 1)) - set(parsed))
    problems = findings(parsed, set(parsed))
    joined = " ".join(problems)
    assert 1 in missing
    assert "O1" in joined
