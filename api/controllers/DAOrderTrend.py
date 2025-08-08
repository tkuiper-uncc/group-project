from fastapi import Query
from typing import Optional
import sqlite3
from datetime import datetime, timedelta

# Ensure created_at exists in orders table
def ensure_created_at():
    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(orders)")
    cols = [c[1] for c in cur.fetchall()]
    if "created_at" not in cols:
        cur.execute("ALTER TABLE orders ADD COLUMN created_at TEXT DEFAULT (datetime('now'))")
        conn.commit()
    conn.close()

ensure_created_at()

@app.get("/reports/order-trends")
def order_trends(
    start: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end: Optional[str] = Query(None, description="YYYY-MM-DD"),
    top_n: int = 5
):
    # Default = last 7 days
    if not start or not end:
        today = datetime.utcnow().date()
        start = (today - timedelta(days=6)).strftime("%Y-%m-%d 00:00:00")
        end = (today + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
    else:
        start += " 00:00:00"
        end += " 23:59:59"

    conn = sqlite3.connect("orders.db")
    cur = conn.cursor()

    # Total orders per day
    cur.execute("""
        SELECT date(created_at) AS day, COUNT(*) AS total
        FROM orders
        WHERE datetime(created_at) BETWEEN ? AND ?
        GROUP BY day ORDER BY day
    """, (start, end))
    totals = [{"day": r[0], "total_orders": r[1]} for r in cur.fetchall()]

    # Most ordered items
    cur.execute("""
        SELECT item, SUM(quantity) AS qty
        FROM orders
        WHERE datetime(created_at) BETWEEN ? AND ?
        GROUP BY item
        ORDER BY qty DESC
        LIMIT ?
    """, (start, end, top_n))
    top_items = [{"item": r[0], "quantity": r[1]} for r in cur.fetchall()]

    conn.close()

    return {"totals_per_day": totals, "top_items": top_items}
