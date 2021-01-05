import csv

student_db_csv = "student_db_2.csv"


def getList(line):
    # print(line)
    list_ = [int(line[0]), line[1], line[2], int(line[3])]
    return list_


def write_to_file(fields):
    with open(student_db_csv, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow(fields)


def read_from_file():
    csv_file = []
    with open(student_db_csv, mode='r') as file:
        file_content = csv.reader(file)
        index = 0
        for line in file_content:
            if index == 0:
                index = 1
                continue
            if len(line) > 0:
                csv_file.append(getList(line))
    return csv_file


def print_line():
    print("---------------------------------------------")


def print_sort_menu():
    print_line()
    print("\t1. Student Number ")
    print("\t2. Student Name ")
    print("\t3. Student Grade ")
    print("\t4. Student Course Code ")


def print_menu():
    print_line()
    print("1. Add Student ")
    print("2. Print Average Grade ")
    print("3. Print Topper of a class ")
    print("4. All Student Details ")
    print("5. Sort Student Details ")
    print("6. Exit ")
    print_line()


def add_student():
    student_number = int(input("Enter a student Number :"))
    student_name = input('Enter a Student Name :')
    course_code = input("Enter the Course Code :")
    student_grade = int(input('Enter the Grade :'))
    writing_fields = [student_number, student_name, course_code, student_grade]
    write_to_file(writing_fields)


def print_as_table(csv_file_content):
    print("{:<8} {:<15} {:<12} {:<10}".format('NUMBER', 'NAME', 'COURSE CODE', 'GRADE'))
    print_line()

    for student_detail in csv_file_content:
        if len(student_detail) > 1:
            student_number = student_detail[0]
            name = student_detail[1]
            course_code = student_detail[2]
            grade = student_detail[3]
            print("{:<8} {:<15} {:<12} {:<10}".format(student_number, name, course_code, grade))


def find_highest_grade():
    highest_grade = 0
    topper_name = ""
    csv_file_content_l = read_from_file()
    for student_detail in csv_file_content_l[1:]:
        if len(student_detail) > 1:
            grade = int(student_detail[3])
            name = student_detail[1]
            if grade > highest_grade:
                highest_grade = grade
                topper_name = name
    print("Topper of a class : " + topper_name)
    print("Highest Grade : " + str(highest_grade))


def calculate_average_grade():
    total_grade = 0
    csv_file_content_l = read_from_file()
    total_len = 0
    for student_detail in csv_file_content_l[1:]:
        if len(student_detail) > 1:
            grade = int(student_detail[3])
            total_grade = total_grade + grade
            total_len = total_len + 1

    if total_len > 0:
        average_grade = float(total_grade) / float(total_len)
        print("average grade point = " + str(average_grade))


def add_student_details():
    key = input('Do you want to add student? (Y/N) ')
    if key == 'N' or key == 'n':
        return
    while True:
        add_student()
        key = input('Do you want to add more students? (Y/N) ')
        if key == 'N' or key == 'n':
            break


def sortStudentDb(sort_option):
    # with open(student_db_csv, mode='r') as file:
    #     reader = csv.reader(file)
    #     print(reader)
    #     next(reader)
    reader = read_from_file()[1:]
    if sort_option == 'student_name':
        reader.sort(key=lambda x: x[1])
    elif sort_option == 'course_code':
        reader.sort(key=lambda x: x[2])
    elif sort_option == 'student_grade':
        reader.sort(key=lambda x: x[3])
    else:
        reader.sort(key=lambda x: x[0])
    print_as_table(reader)


def doSorting(sorting_key):
    if sorting_key == 1:
        sortStudentDb("")
    elif sorting_key == 2:
        sortStudentDb("student_name")
    elif sorting_key == 3:
        sortStudentDb("student_grade")
    elif sorting_key == 4:
        sortStudentDb("course_code")


if __name__ == '__main__':

    while True:
        print_menu()
        choice = int(input("Select an option : "))
        if choice == 1:
            add_student_details()
            continue
        elif choice == 2:
            calculate_average_grade()
            continue
        elif choice == 3:
            find_highest_grade()
            continue
        elif choice == 4:
            csv_file_content = read_from_file()
            print_as_table(csv_file_content)

            continue
        elif choice == 5:
            print_sort_menu()
            sort_key = int(input("Select a Sorting option :"))
            doSorting(sort_key)
            continue
        else:
            break
