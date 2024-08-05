import json


#Object representation of the mentor

class Mentor:
    def __init__(self, name, pwd, id, details:list):
        self.name = name
        self._pwd = pwd
        self.id = id
        self.details = details
        self.role = "mentor"
    
    #Notification Observer for mentor!
    @staticmethod
    def notification_send():
        with open('mentor_notifications.json', 'r') as file:
            data = json.load(file)

        for i in data:
            if(i[1] == False):
                notification = i[0]
                print("Notification Receiver For mentor :", notification)
                i[1] = True
        
        with open('mentor_notifications.json', 'w') as file:
            json.dump(data, file)

    def __str__(self):
        return self.name
    
    