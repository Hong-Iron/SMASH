# Prints the SQL that registers every school in schools.json with the leaderboard (safe to re-run).
# usage: python3 tools/schools_sql.py > supabase/schools.sql, then run it in the Supabase SQL Editor
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
schools = json.loads((root / "schools.json").read_text(encoding="utf-8"))
q = lambda s: "'" + s.replace("'", "''") + "'"
rows = ",\n".join(f"  ({q(s['code'])}, {q(s['campus'])}, {max(1, int(s['buildings']))})" for s in schools)
print("-- SMASH 학교 목록: 새 학교를 추가한 뒤 다시 실행한다\n"
      "insert into public.smash_school (code, name, buildings) values\n"
      f"{rows}\n"
      "on conflict (code) do update set name = excluded.name, buildings = excluded.buildings;")
