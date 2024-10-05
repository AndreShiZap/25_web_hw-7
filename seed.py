import random
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from faker import Faker

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session

fake = Faker('uk-UA')

disciplines = [
    "Вища математика",
    "Хімія",
    "Економіка підприємства",
    "Обчислювальна математика",
    "Історія України",
    "Теоретична механіка",
    "Менеджмент організацій",
    "Системне програмування",
]

groups = ["A-101", "D-235", "АА-12"]

def insert_group():
    for group in groups:
        session.add(Group(name=group))
        session.commit()


def insert_students():
    group_ids = session.scalars(select(Group.id)).all()
    for _ in range(50):
        student = Student(
            fullname=fake.name(),
            group_id=random.choice(group_ids))
        session.add(student)
        session.commit()


def insert_teachers():
    for _ in range(5):
        teacher = Teacher(
            fullname=fake.full_name(),
        )
        session.add(teacher)
        session.commit()


def insert_subject():
    teacher_ids = session.scalars(select(Teacher.id)).all()
    for el in disciplines:
        session.add(Subject(name=el, teacher_id=random.choice(teacher_ids)))
    session.commit()


def insert_grades():
    discipline_ids = session.scalars(select(Subject.id)).all()
    #student_ids = session.scalars(select(Student.id)).all()
    students = session.query(Student).all()
    #subjects = session.query(Subject).all()
    for student in students:
        for _ in range(20):
            grades = Grade(
                student_id=student.id,
                subjects_id=random.choice(discipline_ids),
                grade=random.randint(1, 12),
                grade_date=fake.date_this_year()
            )
            session.add(grades)
            session.commit()


if __name__ == '__main__':
    try:
        insert_group()
        insert_students()
        insert_teachers()
        insert_subject()
        insert_grades()

    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
