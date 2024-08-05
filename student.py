import json



# Object representation of the student.

class Student:
    def __init__(self, name, pwd, id, personal, mentor_assigned=None):
        self.name = name
        self._pwd = pwd
        self.id = id
        self.personal = personal
        self.mentor_assigned = mentor_assigned
        self.role = 'student'
    
    @staticmethod
    def observer_notifications():
        with open('notifications.json', 'r') as file:
            data = json.load(file)
        for i in data:
            # State Pattern and changing Pattern!
            if(i[2] == False):
                print("Notification Received :", i[1])
                i[2] = True
        with open('notifications.json', 'w') as file:
            json.dump(data, file)

    def __str__(self):
        return self.name