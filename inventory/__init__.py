"""Offline inventory allocation."""


def _is_quantity(value):
    """Return whether *value* is a non-negative integer other than bool."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def allocate(stock, requests):
    """Allocate stock to requests in order and return allocations and remainder.

    All input is validated before allocation begins. Inputs are never mutated.
    Invalid stock or request data raises ``ValueError``.
    """
    if not isinstance(stock, dict):
        raise ValueError("stock must be a dict")

    validated_stock = {}
    for sku, quantity in stock.items():
        if not isinstance(sku, str) or not sku:
            raise ValueError("stock SKU keys must be nonempty strings")
        if not _is_quantity(quantity):
            raise ValueError("stock quantities must be non-negative integers")
        validated_stock[sku] = quantity

    if not isinstance(requests, list):
        raise ValueError("requests must be a list")

    validated_requests = []
    required_fields = {"sku", "quantity"}
    for request in requests:
        if not isinstance(request, dict) or set(request) != required_fields:
            raise ValueError("each request must contain exactly sku and quantity")
        sku = request["sku"]
        quantity = request["quantity"]
        if not isinstance(sku, str) or not sku:
            raise ValueError("request SKU must be a nonempty string")
        if not _is_quantity(quantity):
            raise ValueError("request quantity must be a non-negative integer")
        if sku not in validated_stock:
            raise ValueError("request SKU is not present in stock")
        validated_requests.append((sku, quantity))

    remaining = validated_stock.copy()
    allocations = []
    for sku, requested in validated_requests:
        fulfilled = min(requested, remaining[sku])
        remaining[sku] -= fulfilled
        allocations.append(
            {"sku": sku, "requested": requested, "fulfilled": fulfilled}
        )

    return {"allocations": allocations, "remaining": remaining}


__all__ = ["allocate"]
