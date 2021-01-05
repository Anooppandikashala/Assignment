import csv
import matplotlib.pyplot as plt

student_db_csv = "student_db_2.csv"


def get_all_grades():
    csv_file_content_l = read_from_file()
    grades = []
    for student_detail in csv_file_content_l:
        if len(student_detail) > 1:
            grade = int(student_detail[3])
            grades.append(grade)

    return grades


def show_histogram():
    grades = get_all_grades()
    plt.hist(grades, density=False, bins=100)
    plt.ylabel("Grades")
    plt.xlabel("Students")
    plt.show()


def get_list(line):
    list_ = [int(line[0]), line[1], line[2], int(line[3])]
    return list_


def write_to_file(fields):
    with open(student_db_csv, mode='a') as file_:
        writer = csv.writer(file_)
        writer.writerow(fields)


def read_from_file():
    csv_file = []
    with open(student_db_csv, mode='rU') as file_:
        file_content = csv.reader(file_)
        index = 0
        for line in file_content:
            if index == 0:
                index = 1
                continue
            if len(line) > 0:
                csv_file.append(get_list(line))
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
    print("6. Show Histogram ")
    print("7. Exit ")
    print_line()


def add_student():
    student_number = int(raw_input("Enter a student Number :"))
    student_name = raw_input('Enter a Student Name :')
    course_code = raw_input("Enter the Course Code :")
    student_grade = int(raw_input('Enter the Grade :'))
    writing_fields = [student_number, student_name, course_code, student_grade]
    write_to_file(writing_fields)


def print_as_table(csv_file_content_l):
    print("{:<8} {:<15} {:<12} {:<10}".format('NUMBER', 'NAME', 'COURSE CODE', 'GRADE'))
    print_line()

    for student_detail in csv_file_content_l:
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
    for student_detail in csv_file_content_l:
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
    for student_detail in csv_file_content_l:
        if len(student_detail) > 1:
            grade = int(student_detail[3])
            total_grade = total_grade + grade
            total_len = total_len + 1

    if total_len > 0:
        average_grade = float(total_grade) / float(total_len)
        print("average grade point = " + str(average_grade))


def add_student_details():
    key = raw_input('Do you want to add student? (Y/N) ')
    if key == 'N' or key == 'n':
        return
    while True:
        add_student()
        key = raw_input('Do you want to add more students? (Y/N) ')
        if key == 'N' or key == 'n':
            break


def sort_student_db(sort_option):
    # with open(student_db_csv, mode='r') as file:
    #     reader = csv.reader(file)
    #     print(reader)
    #     next(reader)
    reader = read_from_file()
    if sort_option == 'student_name':
        reader.sort(key=lambda x: x[1])
    elif sort_option == 'course_code':
        reader.sort(key=lambda x: x[2])
    elif sort_option == 'student_grade':
        reader.sort(key=lambda x: x[3])
    else:
        reader.sort(key=lambda x: x[0])
    print_as_table(reader)


def do_sorting(sorting_key):
    if sorting_key == 1:
        sort_student_db("")
    elif sorting_key == 2:
        sort_student_db("student_name")
    elif sorting_key == 3:
        sort_student_db("student_grade")
    elif sorting_key == 4:
        sort_student_db("course_code")


if __name__ == '__main__':

    while True:
        print_menu()
        choice = int(raw_input("Select an option : "))
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
            sort_key = int(raw_input("Select a Sorting option :"))
            do_sorting(sort_key)
            continue
        elif choice == 6:
            show_histogram()
            continue
        else:
            break
