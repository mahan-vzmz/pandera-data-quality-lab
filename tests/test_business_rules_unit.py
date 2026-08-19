"""Focused unit tests for pure business-rule helpers."""

from __future__ import annotations

import pandas as pd

from pandera_lab.business_rules import (
    TOTAL_ABSOLUTE_TOLERANCE,
    discount_amount_matches_formula,
    expected_discount_amount,
    expected_gross_amount,
    expected_order_total,
    gross_amount_matches_formula,
    is_discounted_matches_discount,
    net_amount_matches_total,
    non_blank_text,
    order_month_matches_date,
    total_matches_formula,
)


def test_non_blank_text_rejects_empty_whitespace_and_null() -> None:
    values = pd.Series(["A", "  B  ", "", "   ", None], dtype="string")
    assert non_blank_text(values).tolist() == [True, True, False, False, False]


def test_expected_amount_helpers_use_single_domain_formula(
    valid_typed_orders: pd.DataFrame,
) -> None:
    assert expected_gross_amount(valid_typed_orders).tolist() == [200.0, 60.0, 80.0]
    assert expected_discount_amount(valid_typed_orders).tolist() == [20.0, 0.0, 20.0]
    assert expected_order_total(valid_typed_orders).tolist() == [180.0, 60.0, 60.0]


def test_total_tolerance_accepts_sub_half_cent_noise(
    valid_typed_orders: pd.DataFrame,
) -> None:
    df = valid_typed_orders.copy()
    df.loc[0, "total"] += TOTAL_ABSOLUTE_TOLERANCE - 0.0001
    assert total_matches_formula(df).all()


def test_total_tolerance_rejects_one_cent_error(valid_typed_orders: pd.DataFrame) -> None:
    df = valid_typed_orders.copy()
    df.loc[0, "total"] += 0.01
    assert not total_matches_formula(df).iloc[0]


def test_formula_checks_skip_unparseable_prerequisite_to_avoid_cascade(
    valid_typed_orders: pd.DataFrame,
) -> None:
    df = valid_typed_orders.astype(object)
    df.loc[0, "quantity"] = "not-a-number"
    assert total_matches_formula(df).iloc[0]


def test_enriched_business_rule_helpers(valid_enriched_orders: pd.DataFrame) -> None:
    assert gross_amount_matches_formula(valid_enriched_orders).all()
    assert discount_amount_matches_formula(valid_enriched_orders).all()
    assert net_amount_matches_total(valid_enriched_orders).all()
    assert order_month_matches_date(valid_enriched_orders).all()
    assert is_discounted_matches_discount(valid_enriched_orders).all()


def test_enriched_helpers_detect_independent_semantic_corruption(
    valid_enriched_orders: pd.DataFrame,
) -> None:
    gross = valid_enriched_orders.copy()
    gross.loc[0, "gross_amount"] = 999.0
    assert not gross_amount_matches_formula(gross).iloc[0]

    discount = valid_enriched_orders.copy()
    discount.loc[0, "discount_amount"] = 999.0
    assert not discount_amount_matches_formula(discount).iloc[0]

    net = valid_enriched_orders.copy()
    net.loc[0, "net_amount"] = 999.0
    assert not net_amount_matches_total(net).iloc[0]

    month = valid_enriched_orders.copy()
    month.loc[0, "order_month"] = "1999-01"
    assert not order_month_matches_date(month).iloc[0]

    flag = valid_enriched_orders.copy()
    flag.loc[0, "is_discounted"] = False
    assert not is_discounted_matches_discount(flag).iloc[0]
