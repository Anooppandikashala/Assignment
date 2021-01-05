student_db = {}


def print_line():
    print("----------------------")


def add_student():
    student_name = input('Enter a Student Name')
    student_grade = int(input('Enter the Grade'))
    student_db[student_name] = student_grade


def print_as_table():
    print("{:<10} {:<10}".format('NAME', 'GRADE'))
    print_line()
    for name in student_db:
        print("{:<10} {:<10}".format(name, student_db[name]))


def find_highest_grade():
    highest_grade = 0
    topper_name = ""
    for name in student_db:
        if student_db[name] > highest_grade:
            highest_grade = student_db[name]
            topper_name = name
    print("Topper of a class : " + topper_name)
    print("Highest Grade : " + str(highest_grade))


def calculate_average_grade():
    total_grade = 0
    for name in student_db:
        total_grade = total_grade + int(student_db[name])
    if len(student_db) > 0:
        average_grade = float(total_grade) / float(len(student_db))
        print("average grade point = " + str(average_grade))


if __name__ == '__main__':
    print("hello")
    Number_of_students = int(input('Enter the number of students:'))
    for i in range(Number_of_students):
        add_student()
    print_line()
    print_as_table()
    print_line()
    find_highest_grade()
    calculate_average_grade()
