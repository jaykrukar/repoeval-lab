"""One reference solution; all valid alternative implementations should pass."""

def reserve_order(inventory, prices_cents, cart):
    if not isinstance(inventory, dict) or not isinstance(prices_cents, dict) or not isinstance(cart, dict):
        raise ValueError("inventory, prices, and cart must be dictionaries")
    if not cart:
        raise ValueError("cart must not be empty")
    for product, stock in inventory.items():
        if type(stock) is not int or stock < 0:
            raise ValueError("stock must be a nonnegative integer")
    for product, price in prices_cents.items():
        if type(price) is not int or price < 0:
            raise ValueError("price must be a nonnegative integer")
    total = 0
    for product, count in cart.items():
        if type(count) is not int or count <= 0:
            raise ValueError("quantity must be a positive integer")
        if product not in inventory or product not in prices_cents:
            raise ValueError("unknown product or missing price")
        if count > inventory[product]:
            raise ValueError("insufficient stock")
        total += prices_cents[product] * count
    updated = inventory.copy()
    for product, count in cart.items():
        updated[product] -= count
    return updated, total
