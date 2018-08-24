from student import Student

class HighSchoolStudent(Student):
    school_name = "Johns Creek High School"
    def get_school_name(self):
        print(super().get_school_name())
        return "This is a High School"


mark = Student("Vikrant")
print(mark)
print(Student.school_name)

james = HighSchoolStudent("james")
print(james.get_school_name())