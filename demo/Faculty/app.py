# app.py
from flask import Flask, render_template, request, redirect
import pandas as pd
import mysql.connector
from mysql.connector import Error
import plotly.graph_objs as go

app = Flask(__name__, static_url_path='/static')


def connect_database():
    connection = mysql.connector.connect(
        host='localhost',
        database='STUDENT_MARKS_MANAGEMENT',
        user='root',
        password=''
    )
    return connection


def get_student_marks(user_id):
    try:
        connection = connect_database()
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
        print("couuected in student_statistics")
        # Fetch internal and external marks for a particular student
        query = f"SELECT ST.SUBJECT_CODE, ST.SUBJECT_NAME, SM.INTERNAL_MARKS, SM.EXTERNAL_MARKS FROM USER_DETAILS UD " \
                f"JOIN STUDENT_MARKS SM ON UD.USER_ID = SM.USER_ID JOIN SUBJECT_TABLE ST ON SM.SUBJECT_NO = " \
                f"ST.SUBJECT_NO WHERE UD.USER_ID = '{user_id}'; "

        cursor.execute(query)

        # Fetch all the results
        marks_data = cursor.fetchall()
        print("marks_data in student_statistics", marks_data)

        # Calculate the sum of internal and external marks for each subject
        subjects = []
        marks_sum = []

        for row in marks_data:
            subject_code = row['SUBJECT_CODE']
            marks_internal = int(float(row['INTERNAL_MARKS'])) if row['INTERNAL_MARKS'] is not None else 0
            marks_external = int(row['EXTERNAL_MARKS']) if row['EXTERNAL_MARKS'] is not None else 0
            if subject_code not in subjects:
                subjects.append(subject_code)
                marks_sum.append(marks_internal + marks_external)
            else:
                index = subjects.index(subject_code)
                marks_sum[index] += (marks_internal + marks_external)

        # Create a dictionary in the required format
        data = {
            'subject': subjects,
            'marks': marks_sum
        }
        print("data in statistics", data)
        return data
    except Error as e:
        print(f"Error fetching student marks: {e}")



# # Function to get branch_id based on the third letter from the backside of user_id

def get_branch_id(user_id):
    third_letter_from_end = user_id[-3]
    try:
        connection = connect_database()
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
        query = "SELECT BRANCH_ID, BRANCH_NAME FROM BRANCH_ID_DETAILS"
        cursor.execute(query)

        # Fetch all rows from the result set
        branch_data = cursor.fetchall()

        # Create the branch_id_mapping dictionary
        branch_id_mapping = {str(row[0]): row[0] for row in branch_data}

        return branch_id_mapping.get(third_letter_from_end, None)
    except Error as e:
        print(f"Error fetching student Branch Details: {e}")


# Function to get year based on the first two letter from the starting of user_id
def get_year(user_id):
    try:
        # Extract the first two digits from the user_id
        year_prefix = int(user_id[:2])
        # Add 20 to the extracted digits to get the year, and convert it to string
        year = str(2000 + year_prefix)
        return year
    except ValueError:
        print(f"Error: Unable to extract year from user_id {user_id}")
        return None



def fetch_user_data(user_id):
    user_data = None
    try:
        connection = connect_database()
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            print("Connected")

            # Query to fetch user data based on user_id
            query = f"""
                SELECT
                    SM.USER_ID,
                    SM.SUBJECT_NO,
                    CASE WHEN SM.INTERNAL_MARKS < 0 THEN '-' ELSE SM.INTERNAL_MARKS END AS INTERNAL_MARKS,
                    CASE WHEN SM.EXTERNAL_MARKS < 0 THEN '-' ELSE SM.EXTERNAL_MARKS END AS EXTERNAL_MARKS,
                    UD.BRANCH_ID
                FROM
                    STUDENT_MARKS SM
                JOIN
                    USER_DETAILS UD ON SM.USER_ID = UD.USER_ID
                WHERE
                    SM.USER_ID = '{user_id}'
            """
            cursor.execute(query)

            # Fetch all the results after executing the query
            user_data = cursor.fetchall()

    except Error as e:
        print(f"Error fetching user data: {e}")
    finally:
        # Close the connection and cursor after fetching the result
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")

    return user_data


def get_unique_years_and_branches_from_database():
    try:
        # Connect to the database
        connection = connect_database()
        cursor = connection.cursor()

        # Fetch unique years
        cursor.execute("SELECT DISTINCT USER_BATCH FROM USER_DETAILS")
        unique_years = [row[0] for row in cursor.fetchall()]
        # Fetch branch names
        cursor.execute("SELECT BRANCH_NAME FROM BRANCH_ID_DETAILS")
        branches = [row[0] for row in cursor.fetchall()]

        return unique_years, branches

    except mysql.connector.Error as e:
        print("Error fetching data from database:", e)
        return None, None

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def get_unique_semesters_from_database(year, branch):
    try:
        # Connect to the database
        connection = connect_database()
        cursor = connection.cursor()

        # Fetch unique semesters based on year and branch from Marks table
        cursor.execute("""
            SELECT DISTINCT SM.SEM_ID
            FROM STUDENT_MARKS SM
            JOIN USER_DETAILS UD ON SM.USER_ID = UD.USER_ID
            WHERE UD.USER_BATCH = %s AND UD.BRANCH_ID = %s;
        """, (year, branch))
        semesters = [row[0] for row in cursor.fetchall()]

        return semesters

    except mysql.connector.Error as e:
        print("Error fetching data from database:", e)
        return None

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def fetch_student_results(year, branch, semester):
    try:
        # Connect to the database
        connection = connect_database()
        cursor = connection.cursor()

        # Execute the query to fetch student results
        print(year,branch,semester)

        query = f"SELECT UD.USER_ID, UD.USER_NAME, SUB.SUBJECT_CODE, SUB.SUBJECT_NAME, " \
                f"SUB.SUBJECT_CREDITS, SM.INTERNAL_MARKS, SM.EXTERNAL_MARKS, SM.SEM_ID FROM USER_DETAILS UD " \
                f"JOIN STUDENT_MARKS SM ON UD.USER_ID = SM.USER_ID JOIN SUBJECT_TABLE SUB ON SM.SUBJECT_NO = " \
                f"SUB.SUBJECT_NO JOIN BRANCH_ID_DETAILS BD ON UD.BRANCH_ID = BD.BRANCH_ID WHERE UD.USER_BATCH = %s " \
                f"AND BD.BRANCH_NAME = %s AND SM.SEM_ID = %s;"

        cursor.execute(query, (year, branch, semester))
        results = cursor.fetchall()

        # Prepare the student results data
        student_results = {}
        print('results = ',results)
        for row in results:
            user_id = row[0]
            # total_marks = float(row[4]) + float(row[5])
            total_marks = None
            if row[5] is not None and row[6] is not None and row[5] != '-' and  row[6] != '-' and row[5] != 'AB' and row[5] != 'MP' and \
                    row[6] != 'AB' and row[6] != 'MP':
                total_marks = float(row[5]) + float(row[6])
            if row[5] == '-' and row[6] != 'AB' and row[6] != 'MP':
                total_marks = float(row[6])
            if row[5] == 'AB' and row[6] != 'AB' and row[6] != 'AB':
                total_marks = float(row[6])
            if row[6] == 'AB':
                total_marks = 0
            if row[6] == 'MP':
                total_marks = 0
            # findResult(total_marks)
            # if total_marks > 40 and row[5] >= 21:
            #     result = 'P'
            # else:
                result = 'F'

            student_result = {
                "user_id": row[0],
                "username": row[1],
                "subject_id": row[2],
                "subject_name": row[3],
                "marks_IM": row[5],
                "marks_EM": row[6],
                "total_marks": total_marks,  # Calculate total marks
                # "result": result,
                "credits": row[4]
            }
            if user_id not in student_results:
                student_results[user_id] = []
            student_results[user_id].append(student_result)
        print(student_results)

        return student_results

    except mysql.connector.Error as e:
        print("Error fetching student results:", e)
        return {}

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def calculate_sgpa(student_results):
    print("student results:",student_results)
    for student_id, subjects in student_results.items():
        total_credits = 0
        total_grade_points = 0
        total_IM = 0
        total_EM = 0
        total_marks_sum = 0
        total_result = 'P'
        for subject in subjects:
            marks = subject['total_marks']

            grade_points = 0
            # if (subject['']):
            if marks is not None:
                if 90 <= marks <= 100:
                    grade_points = 10
                    grade = 'S'
                elif 80 <= marks < 90:
                    grade_points = 9
                    grade = 'A'
                elif 70 <= marks < 80:
                    grade_points = 8
                    grade = 'B'
                elif 60 <= marks < 70:
                    grade_points = 7
                    grade = 'C'
                elif 50 <= marks < 60:
                    grade_points = 6
                    grade = 'D'
                elif 40 <= marks < 50:
                    grade_points = 5
                    grade = 'E'
                else:
                    grade_points = 0
                    grade = 'F'
            else:
                # Handle the case when marks is None (optional)
                grade_points = 0
                grade = 'F'
            subject['grade'] = grade
            if subject['marks_EM'] != 'AB' and subject['marks_EM'] != 'MP' and subject['marks_EM'] != '-':
                if subject['total_marks'] >= 40 and int(subject['marks_EM']) >= 21:
                    result = 'P'
                else:
                    result = 'F'
            else:
                result = 'F'
            subject['result'] = result
            print("subject :",subject)
            if subject['result'] == 'F':
                total_result = 'F'
            credits = float(subject['credits'])
            print("type of",type(grade_points),type(credits))
            total_grade_points += grade_points * credits
            total_credits += credits
            if subject['marks_IM'] != 'AB' and subject['marks_IM'] != 'MP' and subject['marks_IM'] != '-':
                total_IM += float(subject['marks_IM'])
            if subject['marks_EM'] != 'AB' and subject['marks_EM'] != 'MP' and subject['marks_EM'] != '-':
                total_EM += float(subject['marks_EM'])
        student_results[student_id][0]['total_result'] = total_result
        if total_credits != 0:
            sgpa = total_grade_points / total_credits
            # Update the SGPA for the student in student_results
            student_results[student_id][0]['sgpa'] = round(sgpa, 2)
        else:
            # If total credits are 0, set SGPA to 0
            student_results[student_id][0]['sgpa'] = 0.0


def fetch_student_marks(subject_id, year):
    # Connect to the database
    connection = connect_database()
    try:
        cursor = connection.cursor()
        # with connection.cursor() as cursor:
        print("working")
        sql = f"SELECT SM.INTERNAL_MARKS, SM.EXTERNAL_MARKS FROM USER_DETAILS UD JOIN STUDENT_MARKS SM ON UD.USER_ID = SM.USER_ID JOIN SUBJECT_TABLE ST ON SM.SUBJECT_NO = ST.SUBJECT_NO WHERE ST.SUBJECT_CODE = '{subject_id}' AND UD.USER_BATCH = '{year}';"
        # Construct the SQL query
        # Execute the SQL query
        cursor.execute(sql)

        # Fetch all the rows
        result = cursor.fetchall()
        print(result)
        # Convert string marks to floats
        student_marks = [(float(row[0]), float(row[1])) for row in result]

        return student_marks

    finally:
        # Close the connection
        connection.close()

def top_10(sorted_students):
    rank = 1

    # Get top 10 students with rank
    top_10_students = []
    for student_id, data in sorted_students[:10]:
        student_info = {
            'rank': rank,
            'user_id': student_id,
            'username': data[0]['username'],
            'sgpa': data[0]['sgpa']
        }
        top_10_students.append(student_info)
        rank += 1

    return top_10_students


@app.route('/display_user_data', methods=['GET', 'POST'])
def display_user_data():
    if request.method == 'POST':
        user_id = request.form.get('user_id')

        # Fetch user data from the database based on user_id
        user_data = fetch_user_data(user_id)
        print("user data is: ", user_data)

        return render_template('display_user_data.html', user_data=user_data)

    return render_template('user_data_form.html')


# #
@app.route('/')
def faculty_login():
    return render_template('faculty_login.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        selected_year = request.form['year']
        selected_branch = request.form['branch']
        selected_semester = request.form['semester']

        # Fetch student results based on selected year, branch, and semester
        student_results = fetch_student_results(selected_year, selected_branch, selected_semester)

        calculate_sgpa(student_results)

        # Render the results template with student results
        return render_template('results.html', student_results=student_results)

    else:
        # Render the form template for selecting year, branch, and semester
        unique_years, branches = get_unique_years_and_branches_from_database()
        return render_template('results.html', unique_years=unique_years, branches=branches)


@app.route('/meritlist', methods=['GET', 'POST'])
def meritlist():
    if request.method == 'POST':
        selected_year = request.form['year']
        selected_branch = request.form['branch']
        selected_semester = request.form['semester']

        # Fetch student results based on selected year, branch, and semester
        student_results = fetch_student_results(selected_year, selected_branch, selected_semester)

        # Calculate SGPA for each student
        calculate_sgpa(student_results)

        print('student_results in grade sgpa', student_results)
        # Sort students based on SGPA
        sorted_students = sorted(student_results.items(), key=lambda x: x[1][0]['sgpa'], reverse=True)

        top_10_students = top_10(sorted_students)
        print(top_10)

        # Render the meritlist template with top 10 students
        return render_template('meritlist.html', top_10_students=top_10_students)

    else:
        # Render the form template for selecting year, branch, and semester
        unique_years, branches = get_unique_years_and_branches_from_database()
        return render_template('meritlist.html', unique_years=unique_years, branches=branches)


@app.route('/student_statistics', methods=['GET', 'POST'])
def student_statistics():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        print("Received student_id:", student_id)

        # Replace the following line with your actual logic to get student marks
        df = get_student_marks(student_id)
        print("DataFrame:", df)

        if df:
            # Define colors based on marks
            colors = []
            for mark in df['marks']:
                if mark > 90:
                    colors.append('green')
                elif mark < 50:
                    colors.append('red')
                else:
                    colors.append('blue')

            # Create a Plotly bar chart with conditional colors
            fig = go.Figure()
            fig.add_trace(go.Bar(x=df['subject'], y=df['marks'], marker_color=colors))
            fig.update_layout(title=f'Student {student_id} Performance',
                              xaxis_title='Subjects',
                              yaxis_title='Marks')

            # Convert the Plotly figure to JSON
            graph_json = fig.to_json()

            print("Generated graph_json:", graph_json)
            return render_template('student_statistics.html', graph_json=graph_json)
        else:
            error_message = 'Student not found or no data available'
            print("Error message:", error_message)
            return render_template('student_statistics.html', student_error_message=error_message)

    return render_template('student_statistics.html')




@app.route('/subject_statistics', methods=['GET', 'POST'])
def subject_statistics():
    if request.method == 'POST':
        # Handle form submission
        subject_id = request.form.get('subject_id')
        year = request.form.get('year')

        # Fetch student marks for the selected subject and year
        marks = fetch_student_marks(subject_id, year)

        if not marks:
            # If there are no students, render subject_statistics.html with a message
            error_message = "No students found for the selected subject and year. Please enter valid details."
            unique_years, _ = get_unique_years_and_branches_from_database()
            return render_template('subject_statistics.html', error_message=error_message, unique_years=unique_years)

        # Initialize pass and fail counts
        pass_count = 0
        fail_count = 0
        total_students = len(marks)

        # Calculate pass and fail counts and handle cases where marks_IM or marks_EM are not available
        for mark in marks:
            if mark[0] is not None and mark[1] is not None:
                if (mark[0] + mark[1]) >= 36 and mark[1] >= 21:
                    pass_count += 1
                else:
                    fail_count += 1

        # Calculate pass and failure percentages
        pass_percentage = round((pass_count / total_students) * 100, 2)
        fail_percentage = round((fail_count / total_students) * 100, 2)

        # Create bar chart
        data = [
            go.Bar(
                x=['Pass', 'Fail'],
                y=[pass_percentage, fail_percentage],
                text=[f'{pass_count} students passed', f'{fail_count} students failed'],
                marker=dict(color=['blue', 'red'])
            )
        ]
        layout = go.Layout(
            title='Pass and Failure Percentage',
            xaxis=dict(title='Result'),
            yaxis=dict(title='Percentage'),
            barmode='group'
        )
        graph = go.Figure(data=data, layout=layout)
        graph_json = graph.to_json()

        # Fetch unique years for dropdown
        unique_years, _ = get_unique_years_and_branches_from_database()

        # Render subject_statistics.html with pass and failure percentages, pass and fail counts, and dropdown options
        return render_template('subject_statistics.html', pass_percentage=pass_percentage,
                               fail_percentage=fail_percentage, graph_json=graph_json,
                               pass_count=pass_count, fail_count=fail_count,
                               total_students=total_students, unique_years=unique_years)

    # If it's a GET request, render the initial form for subject statistics
    unique_years, _ = get_unique_years_and_branches_from_database()
    return render_template('subject_statistics.html', unique_years=unique_years)


if __name__ == "__main__":
    app.run(debug=True)

