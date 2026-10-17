# Offline inventory allocation

The `inventory.allocate(stock, requests)` function allocates available stock to
requests in input order. `stock` is a dictionary mapping nonempty SKU strings to
non-negative integer quantities. `requests` is a list of dictionaries containing
exactly `sku` and `quantity`. Each result records the requested and fulfilled
quantity, and `remaining` contains the stock left afterward.

Inputs are fully validated before allocation and are never modified. Invalid
input raises `ValueError`; booleans are not accepted as integer quantities.

```python
from inventory import allocate

result = allocate(
    {"apple": 5, "pear": 2},
    [{"sku": "apple", "quantity": 3}, {"sku": "apple", "quantity": 4}],
)
# result == {
#     "allocations": [
#         {"sku": "apple", "requested": 3, "fulfilled": 3},
#         {"sku": "apple", "requested": 4, "fulfilled": 2},
#     ],
#     "remaining": {"apple": 0, "pear": 2},
# }
```

## Command line

Pass one JSON document on standard input with exactly `stock` and `requests`:

```sh
printf '%s\n' '{"stock":{"A":3},"requests":[{"sku":"A","quantity":5}]}' \
  | python -m inventory.cli
```

Output:

```json
{"allocations":[{"sku":"A","requested":5,"fulfilled":3}],"remaining":{"A":0}}
```

Successful input exits with status 0. Malformed JSON, invalid top-level fields,
or invalid allocation input exits with status 2, writes a short diagnostic to
standard error, and writes nothing to standard output.
