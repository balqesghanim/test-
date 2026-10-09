
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "students.db"


# الاتصال بقاعدة البيانات وإنشاء الجدول عند الحاجة
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                grade REAL NOT NULL
            )
        """)


# عرض واجهة الموقع
@app.route("/")
def home():
    return render_template("index.html")


# جلب جميع الطلاب
@app.route("/api/students", methods=["GET"])
def get_students():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, name, grade FROM students ORDER BY id DESC"
        ).fetchall()

    return jsonify([dict(row) for row in rows])


# إضافة طالب جديد
@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    grade = data.get("grade")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "أدخل اسم الطالب."}), 400

    try:
        grade = float(grade)
    except (ValueError, TypeError):
        return jsonify({"error": "أدخل علامة رقمية صحيحة."}), 400

    if not 0 <= grade <= 100:
        return jsonify({"error": "يجب أن تكون العلامة بين 0 و100."}), 400

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO students (name, grade) VALUES (?, ?)",
            (name.strip(), grade)
        )

    return jsonify({"message": "تمت إضافة الطالب بنجاح."}), 201


# حساب متوسط العلامات
@app.route("/api/average", methods=["GET"])
def get_average():
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute(
            "SELECT COUNT(*), AVG(grade) FROM students"
        ).fetchone()

    count, average = result

    return jsonify({
        "count": count,
        "average": round(average, 2) if average is not None else None
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)