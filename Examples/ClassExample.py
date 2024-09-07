#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      ptcha
#
# Created:     02/09/2024
# Copyright:   (c) ptcha 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from datetime import date

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def calculate_age(cls, name, birth_year):
        # calculate age an set it as a age
        # return new object
        return cls(name, date.today().year - birth_year)

    def show(self):
        print(self.name + "'s age is: " + str(self.age))



def main():
    jessa = Student('Jessa', 20)
    jessa.show()

    # create new object using the factory method
    joy = Student.calculate_age("Joy", 1995)
    joy.show()


if __name__ == '__main__':
    main()
