from flask import Flask, render_template, request,redirect
import sqlite3

app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ? ",(username,password,))

        user = cursor.fetchone()

        conn.close()


        if user:
                return render_template("dashboard.html")
        else:
            return "no user found"
        
    
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    total_students = cursor.fetchone()[0]

    conn.close()
    return render_template("dashboard.html", total = total_students)

@app.route("/add_student", methods=["GET","POST"])
def add_student():

    if request.method == "POST":
        name = request.form["studentName"]
        course = request.form["studentCourse"]
        enrollment = request.form["enrollment"]
        phone = request.form["studentPhone"]

        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name,course,enrollmentNumber,phone) VALUES (?,?,?,?)",
            (name,course,enrollment,phone)
        )

        conn.commit()
        conn.close()

        return render_template("dashboard.html")

    return render_template("add_student.html")

@app.route("/search_student", methods = ["GET", "POST"])
def search_student():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    if request.method == "POST":
        enrollment = request.form["enrollment-number"]
        
        cursor.execute(
            "SELECT * FROM students WHERE enrollmentNumber=?",(enrollment,))
        
        data = cursor.fetchall()

        conn.close()

        return render_template("search_student.html", students = data)
    conn.close()

    print("no data found")
    return render_template("search_student.html", students = [])

        
@app.route("/admin_register", methods = ["POST", "GET"])
def admin_register():
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]

        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO admin (username, password, email, phone) VALUES (?, ?, ?, ?)",(name, password, email, phone))

        conn.commit()
        conn.close()

        return render_template("login.html")

    return render_template("admin_register.html")
    

@app.route("/update_student/<int:id>", methods = ["GET","POST"])
def update_student(id):
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["studentName"]
        course = request.form["studentCourse"]
        marks = request.form["studentMarks"]
        phone = request.form["studentPhone"]

        cursor.execute(
            "UPDATE students SET name=?, course=?, enrollmentNumber=?, phone=? WHERE id=?",
            (name, course, marks, phone, id)
        )

        conn.commit()
        conn.close()

        return render_template("view_student.html")
    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()

    conn.close()

    return render_template("update_student.html",student = student)

@app.route("/view_student")
def view_student():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()
    conn.close()

    return render_template("view_student.html", students=data)

@app.route("/delete_student/<int:id>")
def delete_student(id):
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/view_student")
if __name__ == "__main__":
    app.run(debug=True)
