from flask import Flask, render_template
import sqlite3
from flask import request
from flask import Flask, render_template, request, redirect, session
import os
from flask import flash
app = Flask(__name__)
app.secret_key = "employee_management_system"

@app.route('/', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":

            session['user'] = username

            return redirect('/dashboard')

        else:
            return "Invalid Credentials"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/')

    conn = sqlite3.connect('employees.db')

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(DISTINCT department)
    FROM employees
    """)
    department_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT name, salary
    FROM employees
    ORDER BY salary DESC
    LIMIT 1
    """)
    highest_salary_employee = cursor.fetchone()
    cursor.execute("""
    SELECT *
    FROM employees
    ORDER BY emp_id DESC
    LIMIT 5
    """)

    recent_employees = cursor.fetchall()
    conn.close()

    return render_template(
        'dashboard.html',
        total_employees=total_employees,
        department_count=department_count,
        highest_salary_employee=highest_salary_employee
    )

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')

@app.route('/add_employee', methods=['GET','POST'])
def add_employee():

    if request.method == 'POST':

        emp_id = request.form['emp_id']
        name = request.form['name']
        department = request.form['department']
        salary = request.form['salary']
        email = request.form['email']
        photo = request.files['photo']

        photo_name = photo.filename

        photo.save(
        os.path.join(
        'static/uploads',
        photo_name
            )
        )
        conn = sqlite3.connect('employees.db')

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO employees
        VALUES(?,?,?,?,?,?)
        """,
        (emp_id,name,department,salary,email,photo_name))

        conn.commit()
        conn.close()

        flash("Employee Added Successfully")
        return redirect('/add_employee')

    return render_template("add_employee.html")

@app.route('/employees')
def employees():

    conn = sqlite3.connect('employees.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    conn.close()

    return render_template(
        "employees.html",
        employees=employees
    )

@app.route('/update_employee', methods=['GET','POST'])
def update_employee():

    if request.method == 'POST':

        emp_id = request.form['emp_id']
        salary = request.form['salary']

        conn = sqlite3.connect('employees.db')

        cursor = conn.cursor()

        cursor.execute("""
        UPDATE employees
        SET salary=?
        WHERE emp_id=?
        """,(salary,emp_id))

        conn.commit()
        conn.close()

        flash("Employee Updated Successfully")
        return redirect('/update_employee')

    return render_template("update_employee.html")

@app.route('/delete_employee', methods=['GET','POST'])
def delete_employee():

    if request.method == 'POST':

        emp_id = request.form['emp_id']

        conn = sqlite3.connect('employees.db')

        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM employees
        WHERE emp_id=?
        """,(emp_id,))

        conn.commit()
        conn.close()

        flash("Employee Deleted Successfully")
        return redirect('/delete_employee')

    return render_template("delete_employee.html")

@app.route('/search_employee', methods=['GET','POST'])
def search_employee():

    employee = None

    if request.method == 'POST':

        emp_id = request.form['emp_id']

        conn = sqlite3.connect('employees.db')

        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM employees
        WHERE emp_id=?
        """,(emp_id,))

        employee = cursor.fetchone()

        conn.close()

    return render_template(
        'search_employee.html',
        employee=employee
    )

@app.route('/department_search', methods=['GET','POST'])
def department_search():

    employees = []

    if request.method == 'POST':

        department = request.form['department']

        conn = sqlite3.connect('employees.db')

        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM employees
        WHERE department=?
        """,(department,))

        employees = cursor.fetchall()

        conn.close()

    return render_template(
        'department_search.html',
        employees=employees
    )
@app.route('/salary_report')
def salary_report():

    conn = sqlite3.connect('employees.db')

    cursor = conn.cursor()

    cursor.execute("SELECT SUM(salary) FROM employees")
    total_salary = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(salary) FROM employees")
    average_salary = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(salary) FROM employees")
    max_salary = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(salary) FROM employees")
    min_salary = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'salary_report.html',
        total_salary=total_salary,
        average_salary=round(average_salary,2),
        max_salary=max_salary,
        min_salary=min_salary
    )
if __name__ == "__main__":
    app.run(debug=True)