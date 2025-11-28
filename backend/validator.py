# backend/sql_validator.py
import re

# disallowed statements
DANGEROUS = {"drop", "truncate", "delete", "update", "alter", "create", "replace", "grant", "revoke"}

def clean_sql(sql: str) -> str:
    # remove code fences / markdown
    sql = sql.replace("```sql", "").replace("```", "")
    return sql.strip()

def is_safe_sql(sql: str) -> (bool, str):
    s = sql.lower()
    for bad in DANGEROUS:
        if re.search(r'\b' + re.escape(bad) + r'\b', s):
            return False, f"Unsafe SQL contains '{bad}'"
    return True, "safe"

def ensure_groupby_safe(sql: str) -> (bool, str):
    """
    Quick heuristic: if GROUP BY present, ensure non-group columns are aggregated.
    (Not perfect but good guard.)
    """
    s = sql.strip().rstrip(';')
    if 'group by' not in s.lower():
        return True, "ok"

    # crude parse: find select and group by clauses
    sel = s.lower().split("from")[0] if "from" in s.lower() else s
    sel_cols = sel.replace("select", "").strip()
    group_part = s.lower().split("group by", 1)[1]
    group_cols = [c.strip().strip(",") for c in group_part.split(",")[0:]]
    # if any non-aggregated col (no paren functions) exist in select -> require aggregation
    tokens = [c.strip() for c in sel_cols.split(",")]
    for t in tokens:
        tt = t.strip()
        if "(" not in tt and tt not in group_cols and tt != "":
            # non-aggregated column present and not in GROUP BY
            return False, f"Non-aggregated column in SELECT with GROUP BY: '{tt}'"
    return True, "ok"
