from flask import Flask, render_template, request, url_for
from facade_design import *
import json
import pickle
from student import *
from mentor import *
from flask import jsonify
from factory import Factory


app = Flask(__name__)



def get_notifications():
    try:
        data = read_from_json('notifications.json')
        return data
    except:
        print("Error")

def get_details(name):
    mentee_data = load_from_pickle('student_data.pickle')

    for mentee_obj in mentee_data:
        if(mentee_obj.id == name or mentee_obj.name == name):
            name = mentee_obj.name
            id = mentee_obj.id
            details = mentee_obj.personal
            mentor_assigned = mentee_obj.mentor_assigned
    
    return name, id, details, mentor_assigned

    

def save_to_json(path, data):
    with open(path, 'w') as file:
        json.dump(data, file)

def read_from_json(path):
    with open(path, 'r') as file:
       data = json.load(file)
    
    return data

# Middle Ware Function 1 for chain of responsibility pattern!
def check_credentials(name, pwd, role):
    if role == "mentor":
        data = load_from_pickle('mentor_data.pickle')
        for mentor in data:
            if mentor.name == name and mentor._pwd == pwd:
                return True
    elif(role == "student"):
        data = load_from_pickle('student_data.pickle')
        for student in data:
            if student.name == name and student._pwd == pwd:
                return True
    return False


@app.route("/")
def index():
    return render_template("Welcome.html")

@app.route("/go_home")
def go_home():
    return render_template("Welcome.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    name = request.form["username"]
    pwd = request.form["password"]
    role = request.form["role"]
    try:
        if(check_credentials(name, pwd, role)):
            if(role == "mentor"):
                with open('mentor_mentee.pickle', 'rb') as infile:
                    data = pickle.load(infile)
                    printable_data = {}
                    for mentor in data:
                        students_data = []
                        for student_obj in data[mentor]:
                            students_data.append(str(student_obj))
                        printable_data[str(mentor)] = students_data
                
                #print("Data :", printable_data) 
            
                for mentor_obj, lst_student_obj in data.items():
                    if(mentor_obj.name == name):
                        mtr_obj = mentor_obj
                        student_id = [student.id for student in lst_student_obj]
                        student_name = [student.name for student in lst_student_obj]
                        student_details = [student.personal for student in lst_student_obj]
                        #print("Details :", student_id, student_name, student_details)

                return render_template("main_mentor.html", ids=student_id, 
                                       names=student_name, mentor_id=mtr_obj.id)
            elif(role == "student"):
                flag = 0
                with open('students_data_form.json', 'r') as file:
                    data_set = json.load(file)
                student_obj_set = load_from_pickle("student_data.pickle")

                for stud_dict in data_set:
                    for obj in student_obj_set:
                        if(obj.name == name and obj.id == stud_dict['id_no']):
                            wanted = stud_dict
                            flag = 1
                
                if flag:
                    return render_template("student_main_page_condition.html", data=wanted)
            
                return render_template("student_main_page.html")
            return "Going to your main page ...."
        else:
            return render_template('error_template.html', error_message="Invalid Credentials")
    except KeyError:
        return render_template('error_template.html', error_message="Unable to Find Name")
    except Exception as e:
        return render_template('error_template.html', error_message=e)

@app.route("/schedule_meeting", methods=['POST', "GET"])
def schedule_meeting():

    notifications = get_notifications()

    data = request.get_json()
    mentee_name = data.get('menteeName')

    notification = f'Meeting scheduled for mentee: {mentee_name}'
    value = False
    notifications.append([mentee_name, notification, value])

    save_to_json('notifications.json', notifications)

    #Calling Observer for Student!
    Student.observer_notifications()

    return render_template("go_home_page.html", message="Meeting Scheduled Sucessfully!")

@app.route("/end_page_schedule_meeting")
def end_page_schedule_meeting():
    return render_template("go_home_page.html", message="Meeting has been Scheduled!")

@app.route("/view_details", methods=["POST"])
def view_details():
    data = request.get_json()
    mentee_name = data.get("menteeName")

    name, id, details, mentor_assigned = get_details(mentee_name)

    return jsonify(name=name, id=id, details=details, mentor_assigned=mentor_assigned)

@app.route("/assign_mentee_details", methods=["POST", "GET"])
def assign_mentee_details():
    id_no = request.form["id_no"]
    mentee_details = request.form["mentor_assigned"]

    mentee_data = load_from_pickle('student_data.pickle')

    for mentee_obj in mentee_data:
        if(mentee_obj.id == id_no or mentee_obj.name == id_no):
            mentee_obj.mentor_assigned = mentee_details 
    
    with open('student_data.pickle', 'wb') as file:
        pickle.dump(mentee_data, file)

    name, id, details, mentor_assigned = get_details(id_no)

    return render_template('student_details_template.html', 
                           name=name, id=id, details=details, mentor_assigned=mentor_assigned)


@app.route('/details_page')
def details_page():

    name = request.args.get('name')

    # Fetch details using the get_details function
    name, id, details, mentor_assigned = get_details(name)

    # Pass the details to the template
    if(mentor_assigned is None):
        mentor_assigned = "Default Not Assigned"
    
    return render_template(
        'student_details_template.html',
        name=name,
        id=id,
        details=details,
        mentor_assigned=mentor_assigned
    )
    
   # return jsonify(name, id, details, mentor_assigned)


@app.route("/signup_page")
def signup_page():
    return render_template('Signup.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    name = request.form["username"]
    pwd = request.form["password"]
    role = request.form["role"]
    details = request.form["details"]
    id_info = request.form['id']

    if(role == "mentor"):
        mentor_obj = Factory('mentor', name, pwd, id_info, details)
        write_to_pickle(mentor_obj, 'mentor_data.pickle')
    elif(role == "student"):
        student_obj = Factory('student', name, pwd, id_info, details)
        write_to_pickle(student_obj, 'student_data.pickle')
    calculate_mentees()
    return render_template('go_home_page.html',message='SignUp SuccessFul')


@app.route("/handle_forms_data", methods=["POST", "GET"])
def handle_forms_data():
    with open('students_data_form.json', 'r') as file:
        data = json.load(file)
    
    name = request.form.get('name')
    registerNo = request.form.get('registerNo')
    dob = request.form.get('dob')
    email_id = request.form.get('emailid')
    mobile_no = request.form.get('mobile_no')
    department = request.form.get('department')
    year_of_studying = request.form.get('year_of_studying')
    admission_category = request.form.get('admission_category')

    new_data = {}
    new_data['name'] = name
    new_data['id_no'] = registerNo
    new_data['dob'] = dob
    new_data['email_id'] = email_id
    new_data["ph_no"] = mobile_no
    new_data["department"] = department
    new_data["year"] = year_of_studying
    new_data['category'] = admission_category

    data.append(new_data)

    with open('students_data_form.json', 'w') as file:
        json.dump(data, file)

    return "Submitted"


@app.route("/go_to_meeting_forms", methods=["POST", "GET"])
def go_to_meeting_forms():
    id_no = request.args.get('name')

    mentor_mentee_data = load_from_pickle('mentor_mentee.pickle')
    for mentor_obj, lst_mentee_obj in mentor_mentee_data.items():
        for student_obj in lst_mentee_obj:
            if(student_obj.id == id_no or student_obj.name == id_no):
                our_mentor = mentor_obj
    
    mentor_name = our_mentor.name

    return render_template('student_page_2.html', student_id=id_no, mentor_name=mentor_name)

@app.route('/handle_mentor_meeting_request', methods=["POST", "GET"])
def handle_mentor_meeting_request():
    name = request.form.get("name")
    id_no = request.form.get("id_no")
    topic = request.form.get("topic")
    message = request.form.get("msg")

    notification = [f"{id_no} has requested a meeting with mentor {name} for {topic}.\nAdditional Message :{message}", False]

    notifications = read_from_json('mentor_notifications.json')
    notifications.append(notification)

    save_to_json('mentor_notifications.json', notifications)

    # Observer Pattern Call!
    Mentor.notification_send()

    return render_template('go_home_page.html', message="Meeting Scheduled SuccessFully!")

@app.route("/home_after_mentee_schedule")
def home_after_mentee_schedule():
    return render_template('go_home_page.html', message="Meeting Scheduled SuccessFully!")

if __name__ == "__main__":
    # Facade Patterns uaage!
    calculate_mentees()
    app.run(debug = True)