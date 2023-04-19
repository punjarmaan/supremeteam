from array import *
import pandas as pd
from Class import Class

df = pd.read_csv('output2.csv')

class Schedule:

    def __init__(self, completed_classes, sem_rem: int, major: str, gen_eds: int, lang: int):
        self.completed_classes = completed_classes # Array of Completed Classes
        self.sem_rem = sem_rem # Semesters Remaining
        self.semesters = [[]] # Semesters to be created
        self.major = major # Name of Major
        self.major_reqs = self.getMajorReqs()
        self.gen_eds = gen_eds # Gen Eds Remaining
        self.lang = lang # Number of language requirements
        self.first_year = self.checkFirstYear()
        self.fy_gen_eds = [] # Array with form [ENGL, FYS, Data Lit, College Thriving]

    def getMajorReqs(self):
        """Use dataframe to build array of all major requirements. Construct all classes to have all prereqs and coreqs."""
        df = pd.read_csv('./WebScraper/major.csv', header=None)
        print(df.head())
        df.index = df.loc[:,0].to_numpy()
        df.drop(0, inplace=True, axis=1)
        print(df.head())
        test = df.iloc[0].to_numpy()
        c = 0
        for x in test:
            print(type(x))
            if(type(x) != str):
                break
            else:
                c+=1
        print(test[0:c])

    def checkFirstYear(self):
        return self.sem_rem >= 7
    
    def constructSchedule(self):
        for x in range(self.sem_rem):
            self.semesters.append(self.nextSemester())

    def nextSemester(self):
        """
        Build next semester.
        Returns array of classes.
        Creates this array by popping top of each track in the major reqs plus two gen eds if gen eds are still needed.
        """
        classes = []
        total_credit_hours = 0
        if(self.sem_rem >= 7):# Handle First Year Requirements
            c = 0
            if(self.fy_gen_eds[0] > 0):
                classes.append(Class("ENGL 105", 3, False))
                c+=1
                self.fy_gen_eds[0] = 0
            if(self.fy_gen_eds[2] > 0):
                classes.append(Class("Data Literacy Lab", 1, False))
                c+=1
                self.fy_gen_eds[2] = 0
            if(self.fy_gen_eds[1] > 0 and c < 2):
                classes.append(Class("FYS + Gen Ed", 3, False))
                self.gen_eds -= 1
                c+=1
                self.fy_gen_eds[1] = 0
            if(self.fy_gen_eds[3] > 0 and c < 2):
                classes.append(Class("College Thriving", 1, False))
                self.fy_gen_eds[3] = 0

        if(self.lang > 0):
            classes.append(Class("Next Level Language", 3, False))
            self.lang -= 1

        for x in classes:
            total_credit_hours+=x.credit_hours
        
          


    def __str__(self) -> str:
        return "hi"

    