# Proposal: Tenant Boundary Cache — cross-tenant report disclosure via shared cache

**Target tier:** Advanced (proposed, not guaranteed)
**Domain:** API authorization, multi-tenant isolation, caching, asynchronous export jobs
**Proof-of-concept status:** Working local Python reproduction of the cache authorization flaw. The asynchronous worker extension is NOT implemented yet.

## Existing working reproduction
A report service checks whether a requester's tenant owns a report only on cache miss. After an authorized requester retrieves the report, a second requester in a different tenant can retrieve the cached report using the same identifier. The reference fix checks authorization on every request and scopes cache entries by tenant. All four Python unit tests pass locally.

To reproduce: `python3 poc.py` and `python3 -m unittest -v test_poc.py` (Python 3.9+, no dependencies).

## Proposed scope *after* approval
Extend the small reproduction into an asynchronous report-export pipeline involving worker-side authorization context, tenant-scoped cache keys, stale entitlements after membership revocation, and request-order / concurrency regression tests. Learners should fix authorization and isolation without turning off caching or breaking legitimate export functionality.

## Why this is distinct
Unlike generic principal-cache context collapse proposals, this scenario focuses specifically on tenant-owned report artifacts, asynchronous job completion, cache warm-up order, and revocation-aware delivery. These features are proposed, not yet delivered.

## Learning objectives
1. Distinguish authentication, membership, and ownership checks.
2. Trace authorization decisions across cache hits and misses.
3. Design tenant-safe caching and verify remediation with adversarial regression tests.
4. Evaluate the additional authorization boundary introduced by background workers.

## Request to SecDim
Please confirm whether this concept is sufficiently distinct and suitable for Advanced-level development before I build the SecDim Play SDK version. Please also clarify contributor eligibility and payouts for a creator based in Israel and whether AI-assisted implementation is permitted with appropriate disclosure.

**Code link:** https://github.com/yosiismalov/secdim-tenant-boundary-cache
