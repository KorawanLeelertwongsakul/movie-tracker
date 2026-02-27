import sqlite3

conn = sqlite3.connect("database.db")

try:
    conn.execute("ALTER TABLE movies ADD COLUMN review TEXT")
    print("✅ เพิ่ม review column สำเร็จ")
except Exception as e:
    print("⚠️ อาจมี column นี้อยู่แล้ว:", e)

conn.commit()
conn.close()