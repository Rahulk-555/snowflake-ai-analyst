import argparse, datetime, pathlib, re, shutil, subprocess, sys
import yaml  # pip install pyyaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

ap = argparse.ArgumentParser()
ap.add_argument("--connection", "-c", required=True)
ap.add_argument("--runs", type=int, default=3)
ap.add_argument("--case", help="run a single case id")
ap.add_argument("--timeout", type=int, default=600)
args = ap.parse_args()

cases = yaml.safe_load((ROOT / "evals" / "cases.yaml").read_text())["cases"]
if args.case:
    cases = [c for c in cases if c["id"] == args.case]

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
out = ROOT / "evals" / "runs" / stamp
out.mkdir(parents=True)

def move_outputs(dest):
    dest.mkdir(parents=True, exist_ok=True)
    for d in ("sql", "reports"):
        src = ROOT / d
        if not src.exists():
            continue
        for f in src.iterdir():
            if f.name != ".gitkeep":
                shutil.move(str(f), str(dest / f"{d}_{f.name}"))

move_outputs(out / "_before")  # preserve anything already there

rows = []
for case in cases:
    for n in range(1, args.runs + 1):
        run_dir = out / case["id"] / f"run{n}"
        run_dir.mkdir(parents=True)
        try:
            r = subprocess.run(
                ["cortex", "-c", args.connection, "-w", str(ROOT), "-p", case["prompt"]],
                capture_output=True, text=True, timeout=args.timeout)
            transcript, code = r.stdout + "\n" + r.stderr, r.returncode
        except subprocess.TimeoutExpired:
            transcript, code = "TIMEOUT", -1
        (run_dir / "transcript.txt").write_text(transcript)

        chk = subprocess.run([sys.executable, str(ROOT / "evals" / "check_outputs.py")],
                             capture_output=True, text=True)
        (run_dir / "checks.txt").write_text(chk.stdout)
        pii = bool(EMAIL.search(transcript))
        move_outputs(run_dir)

        rows.append((case["id"], n, code, chk.returncode == 0, not pii))
        print(f"{case['id']} run{n}: exit={code} auto_checks={'ok' if chk.returncode == 0 else 'FAIL'} "
              f"transcript_pii={'none' if not pii else 'FOUND'}")

lines = ["| case | run | exit | automated checks | no email in transcript |", "|---|---|---|---|---|"]
lines += [f"| {c} | {n} | {e} | {'pass' if a else 'FAIL'} | {'pass' if p else 'FAIL'} |"
          for c, n, e, a, p in rows]
(out / "summary.md").write_text("\n".join(lines))
print(f"\nSummary: {out / 'summary.md'}")