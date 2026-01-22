from __future__ import annotations

import argparse
import subprocess
import sys


def _run(cmd: list[str]) -> int:
    p = subprocess.run(cmd)
    return int(p.returncode)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="hqcb_hhh", description="HQCB repo CLI (demos + inference)")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("demo-b", help="Run HQCB-B demo (figures)")
    b.add_argument("--config", default="data/cosmology/hqcb_b_toy.yaml")

    t = sub.add_parser("infer-toy", help="Run HQCB inference toy (posterior gamma) + figures")
    t.add_argument("--config", default="data/cosmology/hqcb_infer_toy.yaml")

    d = sub.add_parser("infer-data", help="Run HQCB inference with BAO mock(cov) + H0 toy")
    d.add_argument("--config", default="data/cosmology/hqcb_infer_data_mock.yaml")

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.cmd == "demo-b":
        return _run([sys.executable, "scripts/hqcb_b_demo.py", "--config", args.config])

    if args.cmd == "infer-toy":
        return _run([sys.executable, "scripts/hqcb_infer.py", "--config", args.config])

    if args.cmd == "infer-data":
        return _run([sys.executable, "scripts/hqcb_infer_data.py", "--config", args.config])

    raise SystemExit("Unknown command")


if __name__ == "__main__":
    raise SystemExit(main())