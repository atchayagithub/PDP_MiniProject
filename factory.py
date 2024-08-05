from student import Student
from mentor import Mentor

def Factory(obj_type :('student', 'mentor'), name, pwd, id_info, details):
    if(obj_type == "student"):
        student_obj = Student(name, pwd, id_info, details)
        return student_obj
    elif(obj_type == "mentor"):
        mentor_obj = Mentor(name, pwd, id_info, details)
        return mentor_obj