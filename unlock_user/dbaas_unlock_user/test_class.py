#/usr/bin/python
############################################
#        $Author: pmistry $                     $RCSfile: oraUserAction.py,v $
#        $Date: 2020/08/30 07:37:16 $           $Revision: 1.12 $
#        Python 3.7
############################################
# usage :  ./oraUserAction.py --help
# usage :  ./oraUserAction.py -a [unlock|lock|reset|check] -s rmb -t sc1 -c oraUserAction.json -d [yes|no]
# ./oraUserAction.py -a check -s dst  -d yes -t ot1 -c oraUserAction.json

''' Demonstrate how classes can work with instance data and aggreegate it. '''
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade      # 0-100

    def get_grade(self):
        return self.grade

class Course:
    def __init__(self,name, max_students):
        self.name = name
        self.max_students = max_students
        self.students = []

    def add_student(self,student):
        if len(self.students) < self.max_students:
            self.students.append(student)
            return True
        return False

    def get_average_grade(self):
        value = 0
        for student in self.students:
            value += student.get_grade()
        return value / len(self.students)

# Initialise the instance for class with name age and grade
s1 = Student("Tim",19,95)
s2 = Student("Bill",18,75)
s3 = Student("Jill",17,65)

# Initialise Course class with a course
c1 = Course("Science",2)
c1.add_student(s1)
c1.add_student(s2)
print(s1.name,s1.age,s1.grade)
print(s2.name,s2.age,s2.grade)
print(c1.get_average_grade())

