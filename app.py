from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from db_config import get_database_connection

# Create Flask application
app = Flask(__name__)
app.secret_key = 'student_task_manager_secret_key'

# Home page route
# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    # Check login form submission
    if request.method == 'POST':

        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Create database connection
        connection = get_database_connection()

        # Create cursor object
        cursor = connection.cursor(dictionary=True)

        # SQL query
        query = """
            SELECT *
            FROM users
            WHERE username = %s
            AND password = %s
        """

        # Execute query
        cursor.execute(
            query,
            (
                username,
                password
            )
        )

        # Fetch user
        user = cursor.fetchone()

        # Close connection
        cursor.close()
        connection.close()

        # Check login success
        if user:

            # Store session data
            session['user_id'] = user['user_id']
            session['full_name'] = user['full_name']

            # Redirect dashboard
            return redirect('/')

        # Invalid login
        return render_template(
            'login.html',
            error='Invalid Username or Password'
        )

    # Load login page
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():

    # Clear session
    session.clear()

    # Redirect login page
    return redirect('/login')

@app.route('/')
def home():

    # Check user login
    if 'user_id' not in session:

        return redirect('/login')

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor()

    # -----------------------------
    # Total Students
    # -----------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM students"
    )

    total_students = cursor.fetchone()[0]



    # -----------------------------
    # Total Tasks
    # -----------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM tasks"
    )

    total_tasks = cursor.fetchone()[0]



    # -----------------------------
    # Total Attendance Records
    # -----------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM attendance"
    )

    total_attendance = cursor.fetchone()[0]



    # -----------------------------
    # Total Task Assignments
    # -----------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM student_tasks"
    )

    total_assignments = cursor.fetchone()[0]



    # Close database connection
    cursor.close()
    connection.close()

    # Load dashboard page
    return render_template(
        'index.html',
        total_students=total_students,
        total_tasks=total_tasks,
        total_attendance=total_attendance,
        total_assignments=total_assignments
    )


# Student list page
@app.route('/students')
def students():

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # SQL query to fetch all students
    query = """
        SELECT *
        FROM students
        ORDER BY student_id DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch all students
    student_list = cursor.fetchall()

    # Close database connection
    cursor.close()
    connection.close()

    # Send data to HTML page
    return render_template(
        'students.html',
        students=student_list
    )


# Add student page
@app.route('/add_student/', methods=['GET', 'POST'])
def add_student():

    # Check form submission
    if request.method == 'POST':

        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        course_name = request.form['course_name']

        # Create database connection
        connection = get_database_connection()

        # Create cursor object
        cursor = connection.cursor()

        # SQL insert query
        query = """
            INSERT INTO students
            (
                first_name,
                last_name,
                gender,
                mobile_number,
                email,
                course_name,
                admission_date
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, CURDATE())
        """

        # Execute query
        cursor.execute(
            query,
            (
                first_name,
                last_name,
                gender,
                mobile_number,
                email,
                course_name
            )
        )

        # Save changes
        connection.commit()

        # Close database connection
        cursor.close()
        connection.close()

        # Redirect to students page
        return redirect('/students')

    # Load form page
    return render_template('add_student.html')

# Edit student page
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # Check form submission
    if request.method == 'POST':

        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        course_name = request.form['course_name']

        # SQL update query
        query = """
            UPDATE students
            SET
                first_name = %s,
                last_name = %s,
                gender = %s,
                mobile_number = %s,
                email = %s,
                course_name = %s
            WHERE student_id = %s
        """

        # Execute query
        cursor.execute(
            query,
            (
                first_name,
                last_name,
                gender,
                mobile_number,
                email,
                course_name,
                student_id
            )
        )

        # Save changes
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()

        # Redirect to student list
        return redirect('/students')

    # Fetch existing student data
    query = """
        SELECT *
        FROM students
        WHERE student_id = %s
    """

    # Execute query
    cursor.execute(query, (student_id,))

    # Fetch single student
    student = cursor.fetchone()

    # Close database connection
    cursor.close()
    connection.close()

    # Load edit page
    return render_template(
        'edit_student.html',
        student=student
    )

# Delete student
@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor()

    # SQL delete query
    query = """
        DELETE FROM students
        WHERE student_id = %s
    """

    # Execute query
    cursor.execute(query, (student_id,))

    # Save changes
    connection.commit()

    # Close database connection
    cursor.close()
    connection.close()

    # Redirect to student list page
    return redirect('/students')

# Attendance page
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # Save attendance
    if request.method == 'POST':

        # Get form data
        student_id = request.form['student_id']
        attendance_date = request.form['attendance_date']
        attendance_status = request.form['attendance_status']
        remarks = request.form['remarks']

        # SQL insert query
        query = """
            INSERT INTO attendance
            (
                student_id,
                attendance_date,
                attendance_status,
                remarks
            )
            VALUES
            (%s, %s, %s, %s)
        """

        # Execute query
        cursor.execute(
            query,
            (
                student_id,
                attendance_date,
                attendance_status,
                remarks
            )
        )

        # Save changes
        connection.commit()

        # Redirect page
        return redirect('/attendance')

    # Fetch all students
    query = """
        SELECT *
        FROM students
        ORDER BY first_name ASC
    """

    # Execute query
    cursor.execute(query)

    # Fetch students
    student_list = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load page
    return render_template(
        'attendance.html',
        students=student_list
    )

# Attendance report page
@app.route('/attendance_report')
def attendance_report():

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # SQL query with INNER JOIN
    query = """
        SELECT

            attendance.attendance_id,
            attendance.attendance_date,
            attendance.attendance_status,
            attendance.remarks,

            students.first_name,
            students.last_name,
            students.course_name

        FROM attendance

        INNER JOIN students
            ON attendance.student_id = students.student_id

        ORDER BY attendance.attendance_id DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch records
    attendance_list = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load report page
    return render_template(
        'attendance_report.html',
        attendance_records=attendance_list
    )

# Task list page
@app.route('/tasks')
def tasks():

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # SQL query
    query = """
        SELECT *
        FROM tasks
        ORDER BY task_id DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch tasks
    task_list = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load page
    return render_template(
        'tasks.html',
        tasks=task_list
    )

# Add task page
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():

    # Save task
    if request.method == 'POST':

        # Get form data
        task_title = request.form['task_title']
        task_description = request.form['task_description']
        due_date = request.form['due_date']
        maximum_marks = request.form['maximum_marks']

        # Create database connection
        connection = get_database_connection()

        # Create cursor
        cursor = connection.cursor()

        # SQL insert query
        query = """
            INSERT INTO tasks
            (
                task_title,
                task_description,
                due_date,
                maximum_marks
            )
            VALUES
            (%s, %s, %s, %s)
        """

        # Execute query
        cursor.execute(
            query,
            (
                task_title,
                task_description,
                due_date,
                maximum_marks
            )
        )

        # Save changes
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()

        # Redirect
        return redirect('/tasks')

    # Load page
    return render_template('add_task.html')

# Assign task to student
@app.route('/assign_task', methods=['GET', 'POST'])
def assign_task():

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # Save assignment
    if request.method == 'POST':

        # Get form data
        student_id = request.form['student_id']
        task_id = request.form['task_id']
        submission_status = request.form['submission_status']
        marks_obtained = request.form['marks_obtained']
        remarks = request.form['remarks']

        # SQL insert query
        query = """
            INSERT INTO student_tasks
            (
                student_id,
                task_id,
                submission_status,
                marks_obtained,
                submission_date,
                remarks
            )
            VALUES
            (%s, %s, %s, %s, CURDATE(), %s)
        """

        # Execute query
        cursor.execute(
            query,
            (
                student_id,
                task_id,
                submission_status,
                marks_obtained,
                remarks
            )
        )

        # Save changes
        connection.commit()

        # Redirect page
        return redirect('/student_tasks')

    # Fetch students
    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY first_name ASC
    """)

    student_list = cursor.fetchall()

    # Fetch tasks
    cursor.execute("""
        SELECT *
        FROM tasks
        ORDER BY task_title ASC
    """)

    task_list = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load page
    return render_template(
        'assign_task.html',
        students=student_list,
        tasks=task_list
    )

# Student task report
@app.route('/student_tasks')
def student_tasks():

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # SQL query with multiple joins
    query = """
        SELECT

            student_tasks.student_task_id,
            student_tasks.submission_status,
            student_tasks.marks_obtained,
            student_tasks.submission_date,
            student_tasks.remarks,

            students.first_name,
            students.last_name,

            tasks.task_title,
            tasks.maximum_marks

        FROM student_tasks

        INNER JOIN students
            ON student_tasks.student_id = students.student_id

        INNER JOIN tasks
            ON student_tasks.task_id = tasks.task_id

        ORDER BY student_tasks.student_task_id DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch records
    task_records = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load page
    return render_template(
        'student_tasks.html',
        task_records=task_records
    )

# Student performance report
@app.route('/performance_report')
def performance_report():

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # SQL query with GROUP BY and aggregate functions
    query = """
        SELECT

            students.student_id,
            students.first_name,
            students.last_name,
            students.course_name,

            COUNT(student_tasks.student_task_id)
                AS total_tasks,

            SUM(student_tasks.marks_obtained)
                AS total_marks,

            AVG(student_tasks.marks_obtained)
                AS average_marks,

            SUM(
                CASE
                    WHEN student_tasks.submission_status = 'Submitted'
                    THEN 1
                    ELSE 0
                END
            ) AS submitted_tasks

        FROM students

        LEFT JOIN student_tasks
            ON students.student_id = student_tasks.student_id

        GROUP BY
            students.student_id,
            students.first_name,
            students.last_name,
            students.course_name

        ORDER BY total_marks DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch report data
    performance_records = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load report page
    return render_template(
        'performance_report.html',
        performance_records=performance_records
    )

# Attendance summary report
@app.route('/attendance_summary')
def attendance_summary():

    # Create database connection
    connection = get_database_connection()

    # Create cursor object
    cursor = connection.cursor(dictionary=True)

    # SQL summary query
    query = """
        SELECT

            attendance_date,

            COUNT(attendance_id)
                AS total_records,

            SUM(
                CASE
                    WHEN attendance_status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS total_present,

            SUM(
                CASE
                    WHEN attendance_status = 'Absent'
                    THEN 1
                    ELSE 0
                END
            ) AS total_absent,

            SUM(
                CASE
                    WHEN attendance_status = 'Leave'
                    THEN 1
                    ELSE 0
                END
            ) AS total_leave

        FROM attendance

        GROUP BY attendance_date

        ORDER BY attendance_date DESC
    """

    # Execute query
    cursor.execute(query)

    # Fetch records
    attendance_summary_records = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Load page
    return render_template(
        'attendance_summary.html',
        attendance_summary_records=attendance_summary_records
    )

# Start Flask application
if __name__ == '__main__':
    app.run(debug=True)