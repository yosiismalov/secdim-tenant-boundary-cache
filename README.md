# Tenant Boundary Cache — SecDim proposal proof of concept

This is a **local-only preliminary reproduction**, not an approved or final SecDim Play SDK challenge.

## Threat model
A report API verifies tenant ownership only on cache misses. An authorized tenant warms a process-wide cache keyed solely by report ID. A user from another tenant then receives the cached body without an authorization check. The patch requires per-request authorization and uses a tenant-scoped cache key.

## Run
Requires Python 3.9+ only (no dependencies):

```bash
python3 poc.py
python3 -m unittest -v test_poc.py
```

## Proposed advanced extension, conditional on approval
Build an asynchronous export pipeline with signed job references, worker-side identity propagation, two independent cache layers, tenant reassignment/revocation handling, and adversarial concurrency tests. The advanced learning objective will require finding and fixing **all** trust-boundary violations without disabling legitimate cache functionality.

The attached PoC **by itself is not an Advanced-level challenge**. It supplies the mandatory reproducible starting point so the SecDim team can assess whether the proposed extension is worth building. No reward or acceptance is guaranteed.
