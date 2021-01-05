import csv

student_db_csv ="student_db.csv"
def write_to_file(fields):
    with open(student_db_csv,mode='a') as file:
        writer=csv.writer(file)
        writer.writerow(fields)
def read_from_file():
    csv_file=[]
    with open(student_db_csv,mode='r') as file:
        file_content=csv.reader(file)
        for line in file_content:
            csv_file.append(line)
    return csv_file

def print_line():
    print("----------------------")

def print_menu():
    print_line()
    print("1. Add Student ")
    print("2. Print Average Grade ")
    print("3. Print Topper of a class ")
    print("4. All Student Details ")
    print("5. Exit ")
    print_line()





def add_student():
    student_name = input('Enter a Student Name')
    student_grade = int(input('Enter the Grade'))
    writing_fields=[student_name,student_grade]
    write_to_file(writing_fields)


def print_as_table():
    print("{:<10} {:<10}".format('NAME', 'GRADE'))
    print_line()
    csv_file_content=read_from_file()
    for student_detail in csv_file_content[1:]:
        if len(student_detail)>1:
            name=student_detail[0]
            grade=student_detail[1]
            print("{:<10} {:<10}".format(name,grade))

def find_highest_grade():
    highest_grade = 0
    topper_name = ""
    csv_file_content=read_from_file()
    for student_detail in csv_file_content[1:]:
        if len(student_detail)>1:
            grade=int(student_detail[1])
            name=student_detail[0]
            if grade>highest_grade:
                highest_grade = grade
                topper_name = name
    print("Topper of a class : " + topper_name)
    print("Highest Grade : " + str(highest_grade))


def calculate_average_grade():
    total_grade = 0
    csv_file_content=read_from_file()
    total_len=0
    for student_detail in csv_file_content[1:]:
        if len(student_detail)>1:
            grade=int(student_detail[1])
            total_grade = total_grade + grade
            total_len=total_len+1


    if total_len> 0:
        average_grade = float(total_grade) / float(total_len)
        print("average grade point = " + str(average_grade))
def add_student_details():
    key=input('Do you want to add student? (Y/N) ')
    if key=='N' or key=='n':
        return
    while True:
        add_student()
        key = input('Do you want to add more students? (Y/N) ')
        if key == 'N' or key == 'n':
            break



if __name__ == '__main__':

    while True:
        print_menu()
        choice= int(input("Select an option : "))
        if choice==1:
            add_student_details()
            continue
        elif choice==2:
            calculate_average_grade()
            continue
        elif choice==3:
            find_highest_grade()
            continue
        elif choice==4:
            print_as_table()
            continue
        else:
            break
