# Challenge: Atomic order reservation

Implement `reserve_order(inventory, prices_cents, cart)` in `order.py`.

- `inventory`: dictionary mapping product ID to nonnegative integer units available.
- `prices_cents`: dictionary mapping product ID to nonnegative integer prices.
- `cart`: nonempty dictionary mapping product ID to **positive** integer quantities.
- Reject unknown products, missing prices, invalid quantities, invalid stock, and insufficient inventory with `ValueError`.
- Return `(new_inventory, total_cents)` where `new_inventory` is a **new** mapping.
- Never mutate inputs, even if validation or fulfillment fails.
- Accept an empty `inventory` only if the cart could be valid (which it cannot here).
- No floating-point money math.

The starter deliberately mutates inputs and misses checks. Tests target behavior,
not exact source code or a single intended implementation.
