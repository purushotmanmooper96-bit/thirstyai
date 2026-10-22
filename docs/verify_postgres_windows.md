# PostgreSQL on Windows: run it, then compare

Prerequisites: install PostgreSQL with pgAdmin, Python 3.12 and Node 22. Keep the password chosen during installation private. Run `python scripts/reproduce.py` from the repository first. PostgreSQL 16 is the CI target; your installed version must be recorded separately.

1. Open **pgAdmin 4**. Expand **Servers → PostgreSQL**. Enter your server password if asked.
2. Right-click **Databases → Create → Database**. Database: `thirstyai_db`. Owner: your PostgreSQL role (often `postgres`). Click **Save**. Use a dedicated project database.
3. Select `thirstyai_db`, right-click **Query Tool**. Click **Open File**, select `sql/postgresql_schema.sql`, then **Execute/Refresh** (F5).
4. In the same database, open and execute these files in order: `sql/sources_seed.sql`, `sql/seed.sql`, `sql/scenario_seed.sql`, `sql/company_seed.sql`. These are inserts for a fresh database; do not repeat them on populated tables. The verifier below provides a repeatable transactional reload.
5. Execute `sql/queries.sql` if present, then run:

```sql
SELECT version();
SELECT * FROM vw_india_context ORDER BY state;
SELECT * FROM vw_scenarios ORDER BY scenario_id;
SELECT * FROM vw_company_reporting ORDER BY observation_id;
SELECT COUNT(*) FROM vw_india_context; -- 36
SELECT COUNT(*) FROM vw_company_reporting; -- 16, including two null WUE records
```

6. Open PowerShell in the repo. Replace the role/port if needed. Enter the password at the prompt; it is not saved in the script or terminal command history.

```powershell
python scripts/reproduce.py
python -m pip install "psycopg[binary]>=3.2,<4"
$env:PGHOST = "localhost"
$env:PGPORT = "5432"
$env:PGDATABASE = "thirstyai_db"
$env:PGUSER = "postgres"
$secret = Read-Host "PostgreSQL password" -AsSecureString
$env:PGPASSWORD = [System.Net.NetworkCredential]::new("", $secret).Password
python scripts/verify_postgres.py --load
Remove-Item Env:PGPASSWORD
```

`--load` replaces only the four project tables inside `thirstyai_db`, in a transaction. Omit it to compare a database you loaded manually. Expected: PASS for all three views. Scenario totals: Baseline 2,200,000 L; Alternative 1,500,000 L — **illustrative consumption, not measured savings**. Row order is ignored, null differs from zero, numeric tolerance is 1e-6 absolute / 1e-10 relative. Every column is compared; Python parity is checked by the rebuild.

Send the server version and redacted PASS/FAIL output for confirmation. Do not send passwords. `docs/limitations.md` remains the v0.1 validation record until your confirmation; the new execution record is in `docs/validation_v02.md`.
