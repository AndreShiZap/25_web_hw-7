# програмa для CRUD операцій із базою даних
import argparse

from conf.models import Teacher, Student, Group, Subject
from conf.db import session


def create_teacher(name):
    new_teacher = Teacher(fullname=name)
    session.add(new_teacher)
    session.commit()
    print(f"Teacher {name} was successfully added.")


def list_teachers():
    teachers = session.query(Teacher).order_by(Teacher.id).all()
    for teacher in teachers:
        print(f"ID: {teacher.id}, Fullname: {teacher.fullname}")


def update_teacher(id, name):
    teacher = session.query(Teacher).filter(Teacher.id == id).first()
    if teacher:
        teacher.fullname = name
        session.commit()
        print(f"Teacher with ID {id} was changed.")
    else:
        print(f"Teacher with ID {id} not found.")


def delete_teacher(id):
    teacher = session.query(Teacher).filter(Teacher.id == id).first()
    if teacher:
        session.delete(teacher)
        session.commit()
        print(f"Teacher with ID {id} was deleted.")
    else:
        print(f"Teacher with ID {id} not found.")


#  -------------------------------------------------------------------
def create_student(name, id_group):
    new_student = Student(fullname=name, group_id=id_group)
    session.add(new_student)
    session.commit()
    print(f"Student {name} was successfully added in group: {id_group}.")


def list_students():
    students = session.query(Student).order_by(Student.id).all()
    for student in students:
        print(f"ID: {student.id}, Fullname: {student.fullname}, Group: {student.group_id}")


def update_student(id, args):
    name = None
    id_group = None
    if type(args) is not int:
        name = args
    else:
        id_group = args
    student = session.query(Student).filter(Student.id == id).first()
    if student:
        if name:
            student.fullname = name
        if id_group:
            student.group_id = id_group
        session.commit()
        print(f"Student with ID {id} was changed.")
    else:
        print(f"Student with ID {id} not found.")


def delete_student(id):
    student = session.query(Student).filter(Student.id == id).first()
    if student:
        session.delete(student)
        session.commit()
        print(f"Student with ID {id} was deleted.")
    else:
        print(f"Student with ID {id} not found.")
# -------------------------------------------------------------------------


def create_group(name):
    new_group = Group(name=name)
    session.add(new_group)
    session.commit()
    print(f"Group {name} was successfully added.")


def list_group():
    groups = session.query(Group).order_by(Group.id).all()
    for group in groups:
        print(f"ID: {group.id}, Fullname: {group.name}")


def update_group(id, name):
    group = session.query(Group).filter(Group.id == id).first()
    if group:
        group.name = name
        session.commit()
        print(f"Group with ID {id} was changed.")
    else:
        print(f"Group with ID {id} not found.")


def delete_group(id):
    group = session.query(Group).filter(Group.id == id).first()
    if group:
        session.delete(group)
        session.commit()
        print(f"Group with ID {id} was deleted.")
    else:
        print(f"Group with ID {id} not found.")
# ---------------------------------------------------------------------------------


def create_subject(name, id_teacher):
    new_subject = Subject(name=name, teacher_id=id_teacher)
    session.add(new_subject)
    session.commit()
    print(f"Subject {name} was successfully added with teacher: {id_teacher}.")


def list_subject():
    subjects = session.query(Subject).order_by(Subject.id).all()
    for subject in subjects:
        print(f"ID: {subject.id}, Fullname: {subject.name}, Teacher: {subject.teacher_id}")


def update_subject(id, args):
    name = None
    id_teacher = None
    if type(args) is not int:
        name = args
    else:
        id_teacher = args
    subject = (session.query(Subject).filter(Subject.id == id).first())
    if subject:
        if name:
            subject.name = name
        if id_teacher:
            subject.teacher_id = id_teacher
        session.commit()
        print(f"Subject with ID {id} was changed.")
    else:
        print(f"Subject with ID {id} not found.")


def delete_subject(id):
    subject = session.query(Subject).filter(Subject.id == id).first()
    if subject:
        session.delete(subject)
        session.commit()
        print(f"Subject with ID {id} was deleted.")
    else:
        print(f"Subject with ID {id} not found.")


def main():
    parser = argparse.ArgumentParser(description='CRUD operations for DB')
    parser.add_argument('-a', '--action', choices=['create', 'list', 'update', 'remove'], required=True,
                        help='list of CRUD operations: create, list, update, remove')
    parser.add_argument('-m', '--model', choices=['Teacher', 'Student', 'Group', 'Subject'], required=True,
                        help='model table: Teacher, Student, Group, Subject')
    parser.add_argument('-n', '--name', type=str, help='name(fullname)')
    parser.add_argument('--id', type=int, help='id subjects')
    parser.add_argument('--id_group', type=int, help='id group for student')
    parser.add_argument('--id_teacher', type=int, help='id teachers for group')
    args = parser.parse_args()

    # Логика обработки команд для модели Teacher
    if args.model == 'Teacher':
        if args.action == 'create':
            if args.name:
                create_teacher(args.name)
            else:
                print("To create a teacher, you must specify his name via --name.")
        elif args.action == 'list':
            list_teachers()
        elif args.action == 'update':
            if args.id and args.name:
                update_teacher(args.id, args.name)
            else:
                print("To update a teacher, you must specify the ID (--id) and the new name (--name).")
        elif args.action == 'remove':
            if args.id:
                delete_teacher(args.id)
            else:
                print("To delete a teacher, you must specify his ID via --id.")

    # Логика обработки команд для модели Student
    if args.model == 'Student':
        if args.action == 'create':
            if args.name:
                create_student(args.name, args.id_group)
            else:
                print("To create a student, you must specify his name (--name) and ID group (--id_group).")
        elif args.action == 'list':
            list_students()
        elif args.action == 'update':
            if args.id and (args.name or args.id_group):
                if args.name:
                    update_student(args.id, args.name)
                if args.id_group:
                    update_student(args.id, args.id_group)
            else:
                print("To update a student, you must specify the ID (--id) and new name (--name) or new group (--id_group)")
        elif args.action == 'remove':
            if args.id:
                delete_student(args.id)
            else:
                print("To delete a student, you must specify his ID via --id.")

    # Логика обработки команд для модели Group
    if args.model == 'Group':
        if args.action == 'create':
            if args.name:
                create_group(args.name)
            else:
                print("To create a group, you must specify his name via --name.")
        elif args.action == 'list':
            list_group()
        elif args.action == 'update':
            if args.id and args.name:
                update_group(args.id, args.name)
            else:
                print("To update a group, you must specify the ID (--id) and the new name (--name).")
        elif args.action == 'remove':
            if args.id:
                delete_group(args.id)
            else:
                print("To delete a group, you must specify his ID via --id.")

    # Логика обработки команд для модели Subject
    if args.model == 'Subject':
        if args.action == 'create':
            if args.name:
                create_subject(args.name, args.id_teacher)
            else:
                print("To create a subject, you must specify his name (--name) and ID teacher (id_teacher).")
        elif args.action == 'list':
            list_subject()
        elif args.action == 'update':
            if args.id and (args.name or args.id_teacher):
                if args.name:
                    update_subject(args.id, args.name)
                if args.id_teacher:
                    update_subject(args.id, args.id_teacher)
            else:
                print("To update a subject, you must specify the ID (--id) and new name (--name) or new teacher (--id_teacher)")
        elif args.action == 'remove':
            if args.id:
                delete_subject(args.id)
            else:
                print("To delete a subject, you must specify his ID via --id.")


if __name__ == '__main__':
    main()
