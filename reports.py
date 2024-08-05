import pickle
import types
import json

class Report:
    def __init__(self, id_no, strategy=None):
        if(strategy is not None):
            self.id = id_no
            self.strategy = strategy
            self.strategy_method = types.MethodType(strategy, self.id)
        else:
            # Default one!
            self.id = id_no
            self.strategy = "Simplified_Details"
    
    def generate(self):
        data = self.strategy_method()
        return data
    
    def strategy_method(self):
        data = Simplfied_Details(self.id)
        return data
    
    def change_stratergy(self, strategy):
        self.strategy = strategy
        self.strategy_method = types.MethodType(strategy, self.id)


# Stratergy 1
def Simplfied_Details(id_no):
    with open('mentor_mentee.pickle', 'rb' ) as infile:
        mentor_mentee_data = pickle.load(infile)

    # Generating Report
    for mentor in mentor_mentee_data:
        for stud_obj in mentor_mentee_data[mentor]:
            if(stud_obj.id == id_no or stud_obj.name == id_no):
                mentor_name = mentor.name
                student_name = stud_obj.name
                student_details = stud_obj.personal
                reports_data = "-" * 40 + "<br>" + f"Student Name: {student_name}<br>Student Id: {stud_obj.id}<br>Mentor Name: {mentor_name}<br>Details: {student_details}<br>"

    
    return reports_data

#Stratergy 2
def Complete_Details(id_no):

    with open('students_data_form.json', 'r' ) as infile:
        student_data = json.load(infile)
    
    for data in student_data:
        if(data["id_no"] == id_no):
            reports_data = data
    
    string = ""
    for k,v in reports_data.items():
        string += f"{k} :{v}" + "<br>"
    
    return string

# Stratergy 3
def Every_Details(id_no):
    # Define a helper Method
    def get_full_detail(obj, req_data):
        data = None
        for k,v in req_data.items():
            for stud_obj in v:
                if(stud_obj.name == obj.name and stud_obj.id == obj.id and stud_obj._pwd == obj._pwd):
                    mentor = k.name
                    student_name = obj.name
                    student_details = obj.personal
                    data = "-" * 40 + "<br>" + f"Student Name :{student_name}<br>Student Id :{obj.id}<br>Mentor Name :{mentor}<br>Details :{student_details}<br>" 

        return data

    with open('student_data.pickle', 'rb' ) as infile:
        student_data = pickle.load(infile)

    with open('mentor_mentee.pickle', 'rb' ) as infile:
        mentor_mentee_data = pickle.load(infile)


    # Generating Report
    reports_data = ""
    for student_obj in student_data:
        reports_data += get_full_detail(student_obj, mentor_mentee_data)
    
    return reports_data
    
