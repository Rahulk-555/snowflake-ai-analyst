import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SQL_DIR, REPORT_DIR = ROOT / "sql", ROOT / "reports"
DENYLIST = ROOT / "evals" / "pii_denylist.txt"

WRITE_SQL = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|CREATE|ALTER|GRANT|MERGE)\b", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}")
PII_COLS = ["FIRST_NAME", "LAST_NAME", "COMPANY", "PHONE_1", "PHONE_2", "EMAIL", "WEBSITE"]
NAME_PATTERN = re.compile(r"^[a-z_]+_[a-z0-9_]+\.sql$")  # <skill>_<description>.sql

failures = []

def fail(msg): failures.append(msg)

# SQL files: no writes, naming pattern
for f in SQL_DIR.glob("*.sql"):
    text = f.read_text(errors="ignore")
    code = re.sub(r"--.*", "", text)
    if WRITE_SQL.search(code):
        fail(f"{f.name}: contains write/DDL statement")
    if not NAME_PATTERN.match(f.name):
        fail(f"{f.name}: does not match <skill>_<description>.sql")

# Reports: PII, caveats, synthetic mention
deny = []
if DENYLIST.exists():
    deny = [l.strip().lower() for l in DENYLIST.read_text().splitlines() if l.strip()]

for f in REPORT_DIR.glob("*.md"):
    text = f.read_text(errors="ignore")
    low = text.lower()
    if EMAIL.search(text): fail(f"{f.name}: email address found")
    if PHONE.search(text): fail(f"{f.name}: phone-like number found")
    for col in PII_COLS:
        if re.search(rf"\b{col}\b", text, re.I):
            fail(f"{f.name}: PII column name '{col}' appears")
    for v in deny:
        if v in low:
            fail(f"{f.name}: denylisted PII value '{v}' appears")
    if "caveat" not in low and "assumption" not in low:
        fail(f"{f.name}: no assumptions/caveats section")
    if "synthetic" not in low:
        fail(f"{f.name}: does not mention synthetic data")

print("\n".join(failures) if failures else "All automated checks passed.")
sys.exit(1 if failures else 0)