import argparse, json
from pathlib import Path
from .core import route_via, validate


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Route through required waypoints on constrained networks"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    sub = commands.add_parser("validate")
    sub.add_argument("network")
    sub = commands.add_parser("route")
    sub.add_argument("network")
    sub.add_argument("start")
    sub.add_argument("end")
    sub.add_argument("--blocked", action="append", default=[])
    sub.add_argument("--via", action="append", default=[])
    args = parser.parse_args(argv)
    spec = json.loads(Path(args.network).read_text(encoding="utf-8"))
    result = (
        {"valid": True, "nodes": len(validate(spec))}
        if args.command == "validate"
        else route_via(spec, args.start, args.end, args.via, args.blocked)
    )
    print(json.dumps(result, indent=2))
    if args.command == "route" and not result["reachable"]:
        raise SystemExit(1)
