students = []

def add_student():
    name = input("أدخل اسم الطالب: ")

    try:
        grade = float(input("أدخل العلامة: "))
    except ValueError:
        print("يجب إدخال علامة رقمية.")
        return

    student = {
        "name": name,
        "grade": grade
    }

    students.append(student)
    print("تمت إضافة الطالب بنجاح.")

def show_students():
    if not students:
        print("لا يوجد طلاب.")
        return

    for student in students:
        print(
            student["name"],
            "- العلامة:",
            student["grade"]
        )

def show_average():
    if not students:
        print("لا توجد علامات لحساب المتوسط.")
        return

    total = sum(student["grade"] for student in students)
    average = total / len(students)

    print("متوسط العلامات:", round(average, 2))

while True:
    print("\n--- إدارة الطلاب ---")
    print("1. إضافة طالب")
    print("2. عرض الطلاب")
    print("3. حساب متوسط العلامات")
    print("4. خروج")

    choice = input("اختر عملية: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        show_students()

    elif choice == "3":
        show_average()

    elif choice == "4":
        print("إلى اللقاء!")
        break

    else:
        print("اختيار غير صحيح.")