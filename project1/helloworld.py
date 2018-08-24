print("Hello World")

python_cousce = True

aliens_found = None

names = [1,2,3,4,5]
print(names[-2:])

students = []

def add_student(name, id):
    student =  {"name": name, "id": id}
    students.append(student)

def get_student_titlecase():
    students_titlecase = []
    for student in students:
        students_titlecase.append(student["name"].title())
    return students_titlecase

def print_students_titlecase():
    students_titlecase = get_student_titlecase()
    for student in students_titlecase:
        print(student)

def save_file(student):
    try:
        f = open("students.txt", "a")
        f.write(student + "\n")
        f.close()
    except Exception:
        print("Could not save file")

def read_file():
    try:
        f = open("students.txt", "r")
        for student in f.readlines():
            print(student)
        f.close()
    except Exception:
        print("Cound not read file")

add_student("Sanjiv", "1")
add_student("mark", "2")

read_file()
student_name = input("Enter Student Name:")
student_id = input("Enter Student Id:")
add_student(student_name, student_id)
save_file(student_name)


