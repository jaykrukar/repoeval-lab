"""Behavioral verifier independent of the submitted implementation."""
from copy import deepcopy
import pytest
from order import reserve_order


def test_basic_reservation():
    inv = {"apple": 5, "pear": 3}
    prices = {"apple": 125, "pear": 80}
    new, total = reserve_order(inv, prices, {"apple": 2, "pear": 1})
    assert new == {"apple": 3, "pear": 2}
    assert total == 330
    assert inv == {"apple": 5, "pear": 3}


def test_alternative_price_zero_and_all_inventory():
    result, total = reserve_order({"a": 1, "b": 9}, {"a": 0, "b": 7}, {"a": 1})
    assert result == {"a": 0, "b": 9} and total == 0


def test_input_objects_unchanged():
    inv = {"a": 1}
    p = {"a": 5}
    cart = {"a": 1}
    before = deepcopy((inv, p, cart))
    updated, _ = reserve_order(inv, p, cart)
    assert (inv, p, cart) == before
    assert updated is not inv


@pytest.mark.parametrize("cart", [
    {}, {"a": 0}, {"a": -1}, {"a": 1.5}, {"a": True}, {"missing": 1},
    {"a": 1, "b": 1},
])
def test_reject_invalid_cart_atomically(cart):
    inv = {"a": 1, "b": 0}
    prices = {"a": 100, "b": 200}
    before = deepcopy((inv, prices, cart))
    with pytest.raises(ValueError):
        reserve_order(inv, prices, cart)
    assert (inv, prices, cart) == before


@pytest.mark.parametrize("stock", [-1, 1.0, True])
def test_invalid_stock(stock):
    with pytest.raises(ValueError):
        reserve_order({"a": stock}, {"a": 1}, {"a": 1})


@pytest.mark.parametrize("price", [-1, 1.5, True])
def test_invalid_price(price):
    with pytest.raises(ValueError):
        reserve_order({"a": 1}, {"a": price}, {"a": 1})


def test_insufficient_stock_no_partial_mutation():
    inv = {"a": 5, "b": 1}
    with pytest.raises(ValueError):
        reserve_order(inv, {"a": 100, "b": 200}, {"a": 1, "b": 2})
    assert inv == {"a": 5, "b": 1}


def test_arbitrary_precision_money():
    result, total = reserve_order({"a": 10**9}, {"a": 10**9}, {"a": 10**9})
    assert result["a"] == 0 and total == 10**18
