students = []
class Student:
    school_name = "Abbotts Hill Elementary"
    def __init__(self, name, student_id=32):
        self.name = name
        self.student_id = student_id
        students.append(self)
    def __str__(self):
        return "Student " + self.name

    def get_school_name(self):
        return self.school_name