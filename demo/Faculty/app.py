# app.py
from flask import Flask, render_template, request, redirect, url_for

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
            marks_internal = int(float(row['INTERNAL_MARKS'])) \
                if row['INTERNAL_MARKS'] is not None and row['INTERNAL_MARKS'] != '-' and\
                   row['INTERNAL_MARKS'] != 'MP' and row['INTERNAL_MARKS'] != 'AB' else 0
            marks_external = int(row['EXTERNAL_MARKS']) if row['EXTERNAL_MARKS'] is not None and row['EXTERNAL_MARKS'] != '-' and\
                   row['EXTERNAL_MARKS'] != 'MP' and row['EXTERNAL_MARKS'] != 'AB' else 0
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
        # print('year, branch and semester : ',year,branch,semester)

        query = query = """
            SELECT UD.USER_ID, UD.USER_NAME, SUB.SUBJECT_CODE, SUB.SUBJECT_NAME,
                SUB.SUBJECT_CREDITS,
                CASE 
                    WHEN SM.INTERNAL_MARKS = -7 THEN '-'
                    WHEN SM.INTERNAL_MARKS = -1 OR SM.EXTERNAL_MARKS = -1 THEN 'AB'
                    ELSE CAST(SM.INTERNAL_MARKS AS CHAR) 
                END AS INTERNAL_MARKS,
                CASE 
                    WHEN SM.EXTERNAL_MARKS = -2 THEN 'MP'
                    ELSE CAST(SM.EXTERNAL_MARKS AS CHAR) 
                END AS EXTERNAL_MARKS,
                SM.SEM_ID
            FROM USER_DETAILS UD 
            JOIN STUDENT_MARKS SM ON UD.USER_ID = SM.USER_ID 
            JOIN SUBJECT_TABLE SUB ON SM.SUBJECT_NO = SUB.SUBJECT_NO 
            JOIN BRANCH_ID_DETAILS BD ON UD.BRANCH_ID = BD.BRANCH_ID 
            WHERE UD.USER_BATCH = %s AND BD.BRANCH_NAME = %s AND SM.SEM_ID = %s;
        """


        cursor.execute(query, (year, branch, semester))
        results = cursor.fetchall()

        # Prepare the student results data
        student_results = {}
        print('results = ',results)
        for row in results:
            user_id = row[0]
            # total_marks = float(row[4]) + float(row[5])
            total_marks = None
            if row[5] == '':
                row[5] = 0
            if row[6] == '':
                row[6] = 0
            if row[5] is not None and row[6] is not None and row[5] != '-' and row[6] != '-' and row[5] != 'AB' and row[5] != 'MP' and \
                    row[6] != 'AB' and row[6] != 'MP':
                total_marks = float(row[5]) + float(row[6])
            # if there is no internal and external
            elif row[5] == '-' and row[6] == '-':
                total_marks = 0
            # if there is no internal
            elif row[5] == '-' and row[6] != 'AB' and row[6] != 'MP' and row[6] is not None:
                total_marks = float(row[6])
            # if there is no external
            elif row[6] == '-' and row[5] != 'AB' and row[5] != 'MP' and row[5] is not None:
                total_marks = float(row[5])
            # if internal is absent
            elif row[5] == 'AB' and row[6] != 'AB' and row[6] != 'MP' and row[6] is not None:
                total_marks = float(row[6])
            # if external is absent
            elif row[6] == 'AB' and row[5] != 'MP' and row[5] != 'AB' and row[5] is not None:
                total_marks = float(row[5])
            # if external is Mall practise
            elif row[6] == 'MP' and row[5] != 'MP' and row[5] != 'AB' and row[5] is not None:
                total_marks = float(row[5])
            # if internal is Mall practise
            elif row[5] == 'MP' and row[6] != 'MP' and row[6] != 'AB' and row[6] is not None:
                total_marks = float(row[6])
            elif (row[5] is None and row[6] is None) or (row[5] == '-' and row[6] == '-') or \
                (row[5] == 'AB' and row[6] == 'AB') or \
                (row[5] == 'MB' and row[6] == 'MP'):
                total_marks = 0
            else:
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
                "credits": row[4],
                "marks_IM": row[5],
                "marks_EM": row[6],
                "total_marks": total_marks  # Calculate total marks
                # "result": result,
            }
            if user_id not in student_results:
                student_results[user_id] = []
            student_results[user_id].append(student_result)
        # print('student_results', student_results)

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
    # print("student results:",student_results)
    for student_id, subjects in student_results.items():
        total_credits = 0
        total_grade_points = 0
        total_IM = 0
        total_EM = 0
        final_marks = 0
        total_result = 'P'
        for subject in subjects:
            marks = subject['total_marks']

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
            if subject['marks_EM'] != 'AB' and subject['marks_EM'] != 'MP' and subject['marks_EM'] != '-':
                if subject['total_marks'] >= 40 and int(subject['marks_EM']) >= 21:
                    result = 'P'
                else:
                    result = 'F'
            elif subject['marks_EM'] == '-' and subject['marks_IM'] != 'AB' and subject['marks_IM'] != 'MP'\
                    and int(subject['marks_IM']) > 17:
                result = 'P'
                grade = '-'
            else:
                result = 'F'
            subject['grade'] = grade
            subject['result'] = result
            print("subject :",subject)
            if subject['result'] == 'F':
                total_result = 'F'
            if subject['result'] == 'P':
                credits = float(subject['credits'])
            else:
                credits = 0
                subject['credits'] = 0
            # print("type of",type(grade_points),type(credits))
            total_grade_points += grade_points * credits
            total_credits += credits
            if subject['marks_IM'] != 'AB' and subject['marks_IM'] != 'MP' and subject['marks_IM'] != '-':
                total_IM += float(subject['marks_IM'])
            if subject['marks_EM'] != 'AB' and subject['marks_EM'] != 'MP' and subject['marks_EM'] != '-':
                total_EM += float(subject['marks_EM'])
            if subject['total_marks'] != 'AB' and subject['total_marks'] != 'MP' and subject['total_marks'] != '-':
                final_marks += float(subject['total_marks'])
        # total marks of each student
        student_results[student_id][0]['total_result'] = total_result
        student_results[student_id][0]['total_credits'] = total_credits
        student_results[student_id][0]['total_IM'] = total_IM
        student_results[student_id][0]['total_EM'] = total_EM
        student_results[student_id][0]['final_marks'] = final_marks
        if total_credits != 0:
            sgpa = total_grade_points / total_credits
            # Update the SGPA for the student in student_results
            student_results[student_id][0]['sgpa'] = round(sgpa, 2)
        else:
            # If total credits are 0, set SGPA to 0
            student_results[student_id][0]['sgpa'] = 0.0


def fetch_pass_results(results):
    pass_results = {}
    for student_id, student_data_list in results.items():
        if student_data_list[0]['total_result'] == 'P':
            pass_results[student_id] = student_data_list
    return pass_results


def fetch_fail_results(results):
    fail_results = {}
    for student_id, student_data_list in results.items():
        if student_data_list[0]['total_result'] == 'F':
            fail_results[student_id] = student_data_list
    return fail_results


def fetch_subject_marks(subject_id, year):
    try:
        # Connect to the database
        connection = connect_database()
        cursor = connection.cursor()

        # Construct the SQL query
        query = f"SELECT UD.USER_ID, UD.USER_NAME, SUB.SUBJECT_CODE, SUB.SUBJECT_NAME, " \
                f"CASE " \
                f"  WHEN SM.INTERNAL_MARKS = -7 OR SM.EXTERNAL_MARKS = -7 THEN '-' " \
                f"  WHEN SM.INTERNAL_MARKS = -1 OR SM.EXTERNAL_MARKS = -1 THEN 'AB' " \
                f"  ELSE CAST(SM.INTERNAL_MARKS AS CHAR) " \
                f"END AS INTERNAL_MARKS, " \
                f"CASE " \
                f"  WHEN SM.EXTERNAL_MARKS = -2 THEN 'MP' " \
                f"  ELSE CAST(SM.EXTERNAL_MARKS AS CHAR) " \
                f"END AS EXTERNAL_MARKS " \
                f"FROM USER_DETAILS UD " \
                f"JOIN STUDENT_MARKS SM ON UD.USER_ID = SM.USER_ID " \
                f"JOIN SUBJECT_TABLE SUB ON SM.SUBJECT_NO = SUB.SUBJECT_NO " \
                f"JOIN BRANCH_ID_DETAILS BD ON UD.BRANCH_ID = BD.BRANCH_ID " \
                f"WHERE SUB.SUBJECT_CODE = '{subject_id}' AND UD.USER_BATCH = '{year}';"

        # Execute the SQL query
        cursor.execute(query)

        # Fetch all the rows
        result = cursor.fetchall()

        # Process fetched results
        processed_results = []
        for row in result:
            # Calculate total marks
            internal_marks = row[4] if row[4] not in ('AB', '-', 'MP') else 0
            external_marks = row[5] if row[5] not in ('AB', '-', 'MP') else 0
            total_marks = int(internal_marks) + int(external_marks)

            # Determine result
            result = 'P' if total_marks >= 40 and int(external_marks) >= 21 else 'F'

            # Append processed data to the row tuple
            row += (total_marks, result)

            # Add the modified row to the processed results
            processed_results.append(row)

        # Return the processed results
        return processed_results

    finally:
        # Close the connection
        if connection:
            connection.close()


def fetch_student_marks(subject_id, year):
    # Connect to the database
    connection = connect_database()
    try:
        cursor = connection.cursor()
        # with connection.cursor() as cursor:
        print("working")
        sql = sql = f"SELECT ST.SUBJECT_CODE, ST.SUBJECT_NAME, SM.INTERNAL_MARKS, SM.EXTERNAL_MARKS FROM" \
                    f" USER_DETAILS UD JOIN STUDENT_MARKS SM ON UD.USER_ID = SM.USER_ID " \
                    f"JOIN SUBJECT_TABLE ST ON SM.SUBJECT_NO = ST.SUBJECT_NO " \
                    f"WHERE ST.SUBJECT_CODE = '{subject_id}' AND UD.USER_BATCH = '{year}';"

        # Construct the SQL query
        # Execute the SQL query
        cursor.execute(sql)

        # Fetch all the rows
        result = cursor.fetchall()
        print(result)
        # Convert string marks to floats

        student_marks = [(float(row[2]), float(row[3])) for row in result]
        if result:
            subject_details = [result[0][0], result[0][1]]
        else:
            subject_details = []

        return student_marks, subject_details

    finally:
        # Close the connection
        connection.close()


def fetch_passed_subjects(marks):
    filtered_students = []
    for row in marks:
        if row[7] == 'P':
            filtered_students.append(row)

    return filtered_students


def fetch_failed_subjects(marks):
    filtered_students = []
    for row in marks:
        if row[7] == 'F':
            filtered_students.append(row)

    return filtered_students

def calculate_marks_distribution(marks):
    if not marks:
        return None

    # Define the ranges
    ranges = {
        '90-100': 0,
        '80-89': 0,
        '70-79': 0,
        '<70': 0
    }

    # Count the number of students falling into each range
    for mark in marks:
        total_marks = mark[6]
        if total_marks >= 90:
            ranges['90-100'] += 1
        elif total_marks >= 80:
            ranges['80-89'] += 1
        elif total_marks >= 70:
            ranges['70-79'] += 1
        else:
            ranges['<70'] += 1

    return ranges


@app.route('/display_user_data', methods=['GET', 'POST'])
def display_user_data():
    if request.method == 'POST':
        user_id = request.form.get('user_id')

        # Fetch user data from the database based on user_id
        user_data = fetch_user_data(user_id)
        print("user data is: ", user_data)

        return render_template('display_user_data.html', user_data=user_data)

    return render_template('user_data_form.html')


#
@app.route('/')
def faculty_login():
    return render_template('faculty_login.html')


# Route for displaying the form to select year, branch, and semester
@app.route('/results', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        selected_year = request.form['year']
        selected_branch = request.form['branch']
        selected_semester = request.form['semester']

        # Redirect to the statistics page with the selected parameters
        return redirect(url_for('student_results', year=selected_year, branch=selected_branch, semester=selected_semester))

    else:
        # Render the form template for selecting year, branch, and semester
        unique_years, branches = get_unique_years_and_branches_from_database()
        return render_template('results_form.html', unique_years=unique_years, branches=branches)


# Route for displaying statistics based on selected parameters
@app.route('/student_results/<year>/<branch>/<semester>', methods=['GET', 'POST'])
def student_results(year, branch, semester):
    if request.method == 'POST':
        action = request.form['action']
        if action == 'results':
            return redirect(url_for('display_results', year=year, branch=branch, semester=semester))
        elif action == 'merit_list':
            return redirect(url_for('meritlist', year=year, branch=branch, semester=semester))
        elif action == 'pass_results':
            return redirect(url_for('display_pass_results', year=year, branch=branch, semester=semester))
        elif action == 'fail_results':
            return redirect(url_for('display_fail_results', year=year, branch=branch, semester=semester))
    else:
        return render_template('student_results.html', year=year, branch=branch, semester=semester)


# Route for displaying results based on selected parameters
@app.route('/display_results/<year>/<branch>/<semester>', methods=['GET'])
def display_results(year, branch, semester):
    # print('I am here')
    # Fetch student results based on selected year, branch, and semester
    student_results = fetch_student_results(year, branch, semester)
    calculate_sgpa(student_results)
    print('sresults ',student_results)
    # Render the results template with student results
    return render_template('results.html', student_results=student_results, year=year, branch=branch, semester=semester)


@app.route('/meritlist/<year>/<branch>/<semester>', methods=['GET'])
def meritlist(year, branch, semester):
    student_results = fetch_student_results(year, branch, semester)
    calculate_sgpa(student_results)

    # Sort students based on SGPA
    sorted_students = sorted(student_results.items(), key=lambda x: x[1][0]['sgpa'], reverse=True)
    print('sorted_students = ',sorted_students)
    # Default number of top students to display
    num_top_students = 3

    # Check if the 'num_students' query parameter is provided
    if 'num_students' in request.args:
        try:
            # Get the number of top students from the query parameter
            num_top_students = int(request.args.get('num_students'))
        except ValueError:
            pass  # Handle the case where the query parameter is not an integer

    # Get the top N students based on the selected number
    top_students = sorted_students[:num_top_students]

    return render_template('meritlist.html', top_students=top_students, num_top_students=num_top_students, year=year, branch=branch, semester=semester)


# Route for displaying results based on selected parameters
@app.route('/pass_results/<year>/<branch>/<semester>', methods=['GET'])
def display_pass_results(year, branch, semester):
    # Fetch student results based on selected year, branch, and semester
    student_results = fetch_student_results(year, branch, semester)
    calculate_sgpa(student_results)

    # Fetch pass results based on the fetched student results
    pass_results = fetch_pass_results(student_results)

    # Render the pass_results template with pass_results data
    return render_template('pass_results.html', pass_results=pass_results)


# Route for displaying results based on selected parameters
@app.route('/fail_results/<year>/<branch>/<semester>', methods=['GET'])
def display_fail_results(year, branch, semester):
    # Fetch student results based on selected year, branch, and semester
    student_results = fetch_student_results(year, branch, semester)
    calculate_sgpa(student_results)

    # Fetch pass results based on the fetched student results
    fail_results = fetch_fail_results(student_results)

    # Render the pass_results template with pass_results data
    return render_template('fail_results.html', fail_results=fail_results)


# Route for displaying the form to select subject id, Year
@app.route('/subject_details', methods=['GET', 'POST'])
def subject_form():
    if request.method == 'POST':
        # Handle form submission
        subject_id = request.form.get('subject_id')
        year = request.form.get('year')
        # Redirect to the statistics page with the selected parameters
        return redirect(url_for('subject_results', subject_id=subject_id, year=year))
        # Render the template with the fetched subject marks

    # If it's a GET request, render the initial form for subject statistics
    unique_years, _ = get_unique_years_and_branches_from_database()
    return render_template('subject_form.html', unique_years=unique_years)


# Route for displaying the form to select year, branch, and semester
@app.route('/subject_results/<subject_id>/<year>', methods=['GET', 'POST'])
def subject_results(subject_id, year):
    if request.method == 'POST':
        action = request.form['action']
        if action == 'results':
            return redirect(url_for('display_subject_results', subject_id=subject_id, year=year))
        elif action == 'subject_merits':
            return redirect(url_for('display_subject_merits', subject_id=subject_id, year=year))
        elif action == 'passed_results':
            return redirect(url_for('display_passed_subject', subject_id=subject_id, year=year))
        elif action == 'failed_results':
            return redirect(url_for('display_failed_subject', subject_id=subject_id, year=year))
    else:
        return render_template('subject_results.html', subject_id=subject_id, year=year)


# Route for displaying the form to select year, branch, and semester
@app.route('/display_subject_results/<subject_id>/<year>', methods=['GET', 'POST'])
def display_subject_results(subject_id, year):
    marks = fetch_subject_marks(subject_id, year)
    print(marks)
    # Render the template with the fetched subject marks
    return render_template('display_subject_results.html', subject_marks=marks)


# Route for displaying the form to select year, branch, and semester
@app.route('/display_subject_merits/<subject_id>/<year>', methods=['GET', 'POST'])
def display_subject_merits(subject_id, year):
    marks = fetch_subject_marks(subject_id, year)
    marks.sort(key=lambda x: x[6], reverse=True)

    num_top_students = 3

    # Check if the 'num_students' query parameter is provided
    if 'num_students' in request.args:
        try:
            # Get the number of top students from the query parameter
            num_top_students = int(request.args.get('num_students'))
        except ValueError:
            pass  # Handle the case where the query parameter is not an integer
    # Get the top N students based on the selected number
    top_students = marks[:num_top_students]
    print(top_students)

    return render_template('display_subject_merits.html', top_students=top_students, num_top_students=num_top_students
                           , subject_id=subject_id, year=year)


# Route for displaying the form to select year, branch, and semester
@app.route('/display_passed_subject/<subject_id>/<year>', methods=['GET', 'POST'])
def display_passed_subject(subject_id, year):
    marks = fetch_subject_marks(subject_id, year)
    passed_marks = fetch_passed_subjects(marks)
    # Render the template with the fetched subject marks
    return render_template('display_passed_subjects.html', passed_subjects=passed_marks)


# Route for displaying the form to select year, branch, and semester
@app.route('/display_failed_subject/<subject_id>/<year>', methods=['GET', 'POST'])
def display_failed_subject(subject_id, year):
    marks = fetch_subject_marks(subject_id, year)
    failed_marks = fetch_failed_subjects(marks)
    # Render the template with the fetched subject marks
    return render_template('display_failed_subjects.html', failed_subjects=failed_marks)


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


# Route for displaying the form to select subject id, Year
@app.route('/subject_statistics_form', methods=['GET', 'POST'])
def subject_statistics_form():
    if request.method == 'POST':
        # Handle form submission
        subject_id = request.form.get('subject_id')
        year = request.form.get('year')
        # Redirect to the statistics page with the selected parameters
        return redirect(url_for('subject_statistics_results', subject_id=subject_id, year=year))
        # Render the template with the fetched subject marks

    # If it's a GET request, render the initial form for subject statistics
    unique_years, _ = get_unique_years_and_branches_from_database()
    return render_template('subject_statistics_form.html', unique_years=unique_years)


# Route for displaying the form to select year, branch, and semester
@app.route('/subject_statistics_results/<subject_id>/<year>', methods=['GET', 'POST'])
def subject_statistics_results(subject_id, year):
    if request.method == 'POST':
        action = request.form['action']
        if action == 'results_statistics':
            return redirect(url_for('pass_fail_statistics', subject_id=subject_id, year=year))
        elif action == 'marks_distribution':
            return redirect(url_for('subject_marks_distribution', subject_id=subject_id, year=year))
    else:
        return render_template('subject_statistics_results.html', subject_id=subject_id, year=year)


@app.route('/pass_fail_statistics/<subject_id>/<year>', methods=['GET', 'POST'])
def pass_fail_statistics(subject_id, year):
    print('entered')
    # Fetch student marks for the selected subject and year
    marks = fetch_subject_marks(subject_id, year)
    print('marks = ', marks)

    # Check if marks is empty
    if not marks:
        return render_template('display_pass_fail_statistics.html', marks=marks)

    # Initialize pass and fail counts
    pass_count = 0
    fail_count = 0
    total_students = len(marks)

    # Calculate pass and fail counts and handle cases where marks_IM or marks_EM are not available
    for mark in marks:
        if mark[7] == 'P':
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

    # display_pass_fail_statistics.html with pass and failure percentages, pass and fail counts, and dropdown options
    return render_template('display_pass_fail_statistics.html', pass_percentage=pass_percentage,marks=marks,
                           fail_percentage=fail_percentage, graph_json=graph_json,
                           pass_count=pass_count, fail_count=fail_count,
                           total_students=total_students, unique_years=unique_years)


@app.route('/subject_marks_distribution/<subject_id>/<year>', methods=['GET', 'POST'])
def subject_marks_distribution(subject_id, year):

    # Fetch student marks for the selected subject and year
    marks = fetch_subject_marks(subject_id, year)
    print('marks = ', marks)

    # Check if marks is empty
    if not marks:
        return render_template('display_marks_distribution.html', marks=marks)

    # Calculate marks distribution
    marks_distribution = calculate_marks_distribution(marks)
    labels = list(marks_distribution.keys())
    values = list(marks_distribution.values())

    # Create the Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title='Distribution of Total Marks')
    pie_chart_json = fig.to_json()

    # Render the template with the pie chart JSON data
    return render_template('display_marks_distribution.html', marks=marks, pie_chart_json=pie_chart_json)


if __name__ == "__main__":
    app.run(debug=True)

