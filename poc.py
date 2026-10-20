"""Local-only proof: multi-tenant report authorization and cross-tenant cache reuse.
No network, third-party services, or real data.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Principal:
    user: str
    tenant: str

REPORTS = {"report-7": {"tenant": "alpha", "body": "ALPHA-INTERNAL-REPORT"}}
MEMBERSHIP = {("alice", "alpha"), ("bob", "beta")}

class VulnerableReportService:
    def __init__(self):
        self.cache = {}

    def get_report(self, principal: Principal, report_id: str):
        # BUG: Cached report is returned before tenant-scoped authorization.
        if report_id in self.cache:
            return self.cache[report_id]
        record = REPORTS[report_id]
        if (principal.user, principal.tenant) not in MEMBERSHIP:
            raise PermissionError("invalid tenant membership")
        if record["tenant"] != principal.tenant:
            raise PermissionError("report outside tenant")
        self.cache[report_id] = record["body"]
        return record["body"]

class PatchedReportService:
    def __init__(self):
        self.cache = {}

    def get_report(self, principal: Principal, report_id: str):
        record = REPORTS[report_id]
        if (principal.user, principal.tenant) not in MEMBERSHIP:
            raise PermissionError("invalid tenant membership")
        if record["tenant"] != principal.tenant:
            raise PermissionError("report outside tenant")
        # Authorize every access; cache scoped to the tenant + report.
        key = (principal.tenant, report_id)
        if key not in self.cache:
            self.cache[key] = record["body"]
        return self.cache[key]

if __name__ == "__main__":
    alice = Principal("alice", "alpha")
    bob = Principal("bob", "beta")
    vulnerable = VulnerableReportService()
    print("Owner request:", vulnerable.get_report(alice, "report-7"))
    leaked = vulnerable.get_report(bob, "report-7")
    print("Cross-tenant request (vulnerable):", leaked)
    assert leaked == "ALPHA-INTERNAL-REPORT"
    patched = PatchedReportService()
    assert patched.get_report(alice, "report-7") == "ALPHA-INTERNAL-REPORT"
    try:
        patched.get_report(bob, "report-7")
    except PermissionError:
        print("Cross-tenant request (patched): BLOCKED")
    else:
        raise AssertionError("patched service failed to block cross-tenant request")
