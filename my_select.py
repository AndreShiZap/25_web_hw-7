from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


def select_01():
    """
     SELECT
            s.id,
            s.fullname,
            ROUND(AVG(g.grade), 2) AS average_grade
       FROM students s
            JOIN grades g ON s.id = g.student_id
      GROUP BY s.id
      ORDER BY average_grade DESC
      LIMIT 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    for el in result:
        print(el)
    return result


def select_02(x_subject):
    """
     SELECT
            s.id,
            s.fullname,
            round(AVG(g.grade), 2) AS average_grade,
            s1.name as subject_name
       FROM grades g
            JOIN subjects s1 on g.subject_id = s1.id
            JOIN students s ON g.student_id = s.id
      WHERE g.subject_id = 3  -- id предмета
      GROUP BY s.id, s1.name
      ORDER BY average_grade DESC
      LIMIT 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')
                           , Subject.name) \
        .select_from(Grade).join(Subject).join(Student).filter(Grade.subjects_id == x_subject) \
        .group_by(Student.id, Subject.name) \
        .order_by(desc('average_grade')).limit(1).all()
    return result


def select_03(x_subject):
    """
    SELECT
            g.name AS group_name,
            round(AVG(gr.grade), 2)AS average_grade,
            s1.name as subject_name
       FROM grades gr
            JOIN subjects s1 on gr.subject_id = s1.id
            JOIN students s ON gr.student_id = s.id
            JOIN groups g ON s.group_id = g.id
      WHERE gr.subject_id = 4  -- id предмета
      GROUP BY g.id, g.name, s1.name
      ORDER BY average_grade DESC;
    """
    result = session.query(Group.name.label('group_name'), func.round(func.avg(Grade.grade), 2).label('average_grade')
                           , Subject.name.label('subject_name')) \
        .select_from(Grade).join(Subject).join(Student).join(Group) \
        .filter(Grade.subjects_id == x_subject) \
        .group_by(Group.id, Group.name, Subject.name) \
        .order_by(desc('average_grade')).all()
    for el in result:
        print(el)
    return result


def select_04():
    """
    SELECT
            round(AVG(grade), 2) AS overall_average_grade
       FROM grades;
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('overall_average_grade')) \
        .select_from(Grade).all()
    return result


def select_05(x_teacher):
    """
    SELECT
            t.fullname as teacher_name,
            s.name as subject_name
       FROM subjects s
            JOIN teachers t on s.teacher_id = t.id
      WHERE s.teacher_id = 3; -- id викладачa
    """
    result = session.query(Teacher.fullname, Subject.name).select_from(Subject) \
        .join(Teacher).filter(Subject.teacher_id == x_teacher).all()
    for el in result:
        print(el)
    return result


def select_06(x_group):
    """
    SELECT
            g.name as group_name,
            s.fullname as student
       FROM students s
            JOIN "groups" g on s.group_id = g.id
      WHERE s.group_id = 1; -- id групи
    """
    result = session.query(Group.name, Student.fullname).select_from(Student) \
        .join(Group).filter(Student.group_id == x_group).all()
    for el in result:
        print(el)
    return result


def select_07(x_group, x_subject):
    """
    SELECT
            g.name AS group_name,
            s.fullname as student_name,
            gr.grade,
            s1.name as subject_name
       FROM grades gr
            JOIN subjects s1 on gr.subject_id = s1.id
            JOIN students s ON gr.student_id = s.id
            JOIN groups g ON s.group_id = g.id
      WHERE gr.subject_id = 4 -- id предмета
        AND g.id = 1 -- id групи
      GROUP BY g.id, g.name, s.fullname, gr.grade, s1.name;
    """
    result = session.query(Group.name, Student.fullname, Grade.grade, Subject.name).select_from(Grade) \
        .join(Subject).join(Student).join(Group) \
        .filter(and_(Grade.subjects_id == x_subject, Group.id == x_group)) \
        .group_by(Group.id, Group.name, Student.fullname, Grade.grade, Subject.name).all()
    for el in result:
        print(el)
    return result


def select_08(x_teacher):
    """
    SELECT
            t.fullname  as teacher_name,
            sub.name AS subject_name,
            round(AVG(gr.grade), 2) AS average_grade
       FROM grades gr
            JOIN subjects sub ON gr.subject_id = sub.id
            JOIN teachers t ON sub.teacher_id = t.id
      WHERE sub.teacher_id = 1  -- id викладачa
      GROUP BY t.fullname, sub.id, sub.name
      ORDER BY sub.name;
    """
    result = session.query(Teacher.fullname, Subject.name, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Subject).join(Teacher) \
        .filter(Subject.teacher_id == x_teacher) \
        .group_by(Teacher.fullname, Subject.id, Subject.name) \
        .order_by(Subject.name).all()
    for el in result:
        print(el)
    return result


def select_09(x_student):
    """
    SELECT
            s.fullname as student,
            s2.name as subject_name
       FROM grades g
            join students s on g.student_id = s.id
            join subjects s2 on g.subject_id = s2.id
      WHERE g.student_id = 5 -- id студенту
      GROUP BY s.fullname, s2.name;
    """
    result = session.query(Student.fullname, Subject.name).select_from(Grade) \
        .join(Student).join(Subject).filter(Grade.student_id == x_student) \
        .group_by(Student.fullname, Subject.name).all()
    for el in result:
        print(el)
    return result


def select_10(x_student, x_teacher):
    """
    SELECT
            s.fullname as student,
            s2.name as subject_name,
            t.fullname as teacher_name
       FROM grades g
            join students s on g.student_id = s.id
            join subjects s2 on g.subject_id = s2.id
            join teachers t on s2.teacher_id = t.id
      WHERE g.student_id = 1 -- id студента
        AND t.id = 3  -- id викладача
      GROUP BY s.fullname, s2.name, t.fullname;
    """
    result = session.query(Student.fullname, Subject.name, Teacher.fullname).select_from(Grade) \
        .join(Student).join(Subject).join(Teacher) \
        .filter(and_(Grade.student_id == x_student, Teacher.id == x_teacher)) \
        .group_by(Student.fullname, Subject.name, Teacher.fullname).all()
    for el in result:
        print(el)
    return result


def select_11(x_student, x_teacher):
    """
    SELECT
            s.fullname as student,
            t.fullname as teacher_name,
            round(AVG(g.grade), 2) AS average_grade
       FROM grades g
            JOIN students s on g.student_id = s.id
            JOIN subjects s2 on g.subject_id = s2.id
            JOIN teachers t on s2.teacher_id = t.id
      WHERE g.student_id = 1 -- id студента
        AND t.id = 1  -- id викладача
      GROUP BY s.fullname, t.fullname;
    """
    result = session.query(Student.fullname, Teacher.fullname,
                           func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).join(Subject).join(Teacher) \
        .filter(and_(Grade.student_id == x_student, Teacher.id == x_teacher)) \
        .group_by(Student.fullname, Teacher.fullname).all()
    for el in result:
        print(el)
    return result


def select_12(x_group, x_subject):
    """
    SELECT
            g2.name as group_name,
            s.fullname as student,
            s2.name as subject_name,
            g.grade,
            g.grade_date as last_date
       FROM grades g
            JOIN students s on g.student_id = s.id
            JOIN subjects s2 on g.subject_id = s2.id
            JOIN groups g2 on s.group_id = g2.id
      WHERE s.group_id = 1 -- id групи
        AND g.subject_id = 1  -- id предмета
        AND g.grade_date = (
            SELECT MAX(gr2.grade_date)
            FROM grades gr2
            WHERE gr2.subject_id = s2.id
            );
    """
    subquery = (select(func.max(Grade.grade_date)).filter(Grade.subjects_id == x_subject)).scalar_subquery()
    result = session.query(Group.name, Student.fullname, Subject.name, Grade.grade, Grade.grade_date) \
        .select_from(Grade) \
        .join(Student).join(Subject).join(Group) \
        .filter(and_(Student.group_id == x_group, Grade.subjects_id == x_subject, Grade.grade_date == subquery)).all()
    for el in result:
        print(el)
    return result


if __name__ == '__main__':
    print('_______________ 5 студентів із найбільшим середнім балом з усіх предметів')
    select_01()
    print('_______________ студент із найвищим середнім балом з певного предмета')
    print(select_02(3))  # param - id предмета
    print('_______________ середній бал у групах з певного предмета')
    select_03(4)  # param - id предмета
    print('_______________ середній бал на потоці (по всій таблиці оцінок)')
    print(select_04())
    print('_______________ курси, які читає певний викладач')
    select_05(3)  # param - id викладачa
    print('_______________ список студентів у певній групі')
    select_06(1)  # param - id групи
    print('_______________ оцінки студентів у окремій групі з певного предмета')
    select_07(1, 4)  # param - id групи, id предмета
    print('_______________ середній бал, який ставить певний викладач зі своїх предметів')
    select_08(1)  # param - id викладачa
    print('_______________ список курсів, які відвідує студент')
    select_09(5)  # param - id студентa
    print('_______________ Список курсів, які певному студенту читає певний викладач')
    select_10(1, 3)  # param - id студента, id викладача
    print('_______________ Середній бал, який певний викладач ставить певному студентові')
    select_11(1, 1)  # param - id студента, id викладача
    print('_______________ Оцінки студентів у певній групі з певного предмета на останньому занятті')
    select_12(1, 1)  # param - id групи, id предмета
