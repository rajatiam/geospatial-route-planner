import argparse, json
from pathlib import Path
from .core import route, validate


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compute constrained shortest paths over supplied directed networks"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("route")
    run.add_argument("network")
    run.add_argument("start")
    run.add_argument("end")
    run.add_argument("--blocked", action="append", default=[])
    check = commands.add_parser("validate")
    check.add_argument("network")
    args = parser.parse_args(argv)
    spec = json.loads(Path(args.network).read_text(encoding="utf-8"))
    result = (
        {"valid": True, "nodes": len(validate(spec))}
        if args.command == "validate"
        else route(spec, args.start, args.end, args.blocked)
    )
    print(json.dumps(result, indent=2))
    if args.command == "route" and not result["reachable"]:
        raise SystemExit(1)
