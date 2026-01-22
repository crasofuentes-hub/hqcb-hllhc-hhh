from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
import sys


def run(cmd: list[str]) -> None:
    p = subprocess.run(cmd)
    if p.returncode != 0:
        raise SystemExit(p.returncode)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    docs_fig = repo / "docs" / "figures"
    paper_fig = repo / "paper" / "figures"
    docs_fig.mkdir(parents=True, exist_ok=True)
    paper_fig.mkdir(parents=True, exist_ok=True)

    # 1) HQCB-B demo (figuras)
    run([sys.executable, "-m", "hqcb_hhh", "demo-b", "--config", "data/cosmology/hqcb_b_toy.yaml"])

    # 2) Inference toy (si existe el script/config en tu repo)
    infer_toy_cfg = repo / "data" / "cosmology" / "hqcb_infer_toy.yaml"
    if infer_toy_cfg.exists():
        run([sys.executable, "-m", "hqcb_hhh", "infer-toy", "--config", str(infer_toy_cfg)])
    else:
        print("note: infer-toy config not found; skipping")

    # 3) Inference data (BAO mock cov)
    infer_data_cfg = repo / "data" / "cosmology" / "hqcb_infer_data_mock.yaml"
    if infer_data_cfg.exists():
        run([sys.executable, "-m", "hqcb_hhh", "infer-data", "--config", str(infer_data_cfg)])
    else:
        print("note: infer-data config not found; skipping")

    # Copia un conjunto mínimo al paper/figures
    want = [
        "hqcb_b_v_ratio.png",
        "hqcb_b_H0_ratio.png",
        "hqcb_infer_joint_gamma.png",
    ]
    for name in want:
        src = docs_fig / name
        if src.exists():
            shutil.copy2(src, paper_fig / name)

    print("OK: figures generated in docs/figures and copied to paper/figures (subset).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())