import sys, json
from client import SemverBreakingChangeAuditor

def main():
    print("Testing SemverBreakingChangeAuditor...")
    auditor = SemverBreakingChangeAuditor()
    res = auditor.run_benchmark_semver_audit()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["recommended_bump"] == "MAJOR"
    assert res["breaking_count"] >= 2
    print("All Semver Breaking Change Auditor tests passed successfully!")

if __name__ == "__main__":
    main()
