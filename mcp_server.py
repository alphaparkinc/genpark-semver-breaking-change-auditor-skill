import sys, json
from client import SemverBreakingChangeAuditor

def main():
    auditor = SemverBreakingChangeAuditor()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(auditor.run_benchmark_semver_audit(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "extract_public_api_surface", "description": "Extract function signatures from code."},
                        {"name": "diff_api_surfaces", "description": "Detect breaking changes between two code versions."},
                        {"name": "run_benchmark_semver_audit", "description": "Run SemVer audit benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "extract_public_api_surface":
                    out = auditor.extract_public_api_surface(args.get("python_code", ""))
                elif tname == "diff_api_surfaces":
                    out = auditor.diff_api_surfaces(args.get("old_code", ""), args.get("new_code", ""))
                elif tname == "run_benchmark_semver_audit":
                    out = auditor.run_benchmark_semver_audit()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
