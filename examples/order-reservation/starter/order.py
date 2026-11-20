"""Buggy starter. Implement reserve_order according to CHALLENGE.md."""
def reserve_order(inventory, prices_cents, cart):
    total = 0
    for product, count in cart.items():
        inventory[product] -= count  # BUG: partial mutations on failure
        total += prices_cents[product] * count
    return inventory, total
