import pandas as pd
from Class import Class

prereq_df = pd.read_csv('./WebScraper/output2.csv', header=None)
prereq_df.index = prereq_df.loc[:,0].to_numpy() # Set Row Labels
prereq_df.drop(0, inplace=True, axis=1) # Drop First Column


coreq_df = pd.read_csv('./WebScraper/output3.csv', header=None)
coreq_df.index = coreq_df.loc[:,0].to_numpy() # Set Row Labels
coreq_df.drop(0, inplace=True, axis=1) # Drop First Column

class Schedule:

    def __init__(self, completed_classes, sem_rem: int, major: str, major_reqs, gen_eds: int, lang: int):
        self.completed_classes = completed_classes # Array of Completed Classes
        self.sem_rem = sem_rem # Semesters Remaining
        self.semesters = [[]] # Semesters to be created
        self.major = major # Name of Major
        self.major_reqs = self.updateMajorReqs(major_reqs) # Array of Classes
        self.gen_eds = gen_eds # Gen Eds Remaining
        self.lang = lang # Number of language requirements
        self.first_year = self.checkFirstYear()
        self.fy_gen_eds = [] # Array with form [ENGL, FYS, Data Lit, College Thriving]

    def updateMajorReqs(self, major_reqs):
        """Construct all classes to have all prereqs and coreqs."""
        for req in self.completed_classes: # Remove all completed classes from Major Requirements Left
            if(req in major_reqs):
                major_reqs.remove(req)
        
        new_m_reqs = []
        for req in major_reqs:
            coreq = self.hasCoreq(req)
            prereqs = self.getPrereqs(req)
            new_m_reqs.append(Class(req, 3, coreq, prereqs))
        
        return new_m_reqs

    def hasCoreq(self, class_name):
        """Determine if a class has a corequisite based on class id."""
        try:
            coreq = coreq_df.loc[class_name].to_numpy()
        except:
            coreq = []
        return len(coreq) > 0

    def getPrereqs(self, class_name):
        """Get a list of prerequisites for a class."""
        prereqs
        try: 
            prereqs = prereq_df.loc[class_name].to_numpy()
        except: # If class has no prereqs
            return []
        c = 0
        for x in prereqs:
            if(type(x) != str):
                break
            else:
                c+=1
        prereqs = prereqs[0:c]
        return prereqs

    def getCoreq(self, class_name):
        """Get a list of coreqs for a"""
        coreqs
        try:
            coreqs = coreq_df.loc[class_name.ID].to_numpy() # Get the corequisites
        except:
            return ""
        
        
    def checkFirstYear(self):
        return self.sem_rem >= 7
    
    def constructSchedule(self):
        for x in range(self.sem_rem):
            self.semesters.append(self.nextSemester())

    def isACoreq(self, cla: Class, co: str) -> bool:
        """Checks if co is a coreq of cla."""
        coreqs = []
        if not cla.corequisite: # Check if cla even has any coreqs
            return False
        
        coreqs = coreq_df.loc[cla.ID].to_numpy() # Get Corequisites

        for coreq in coreqs:
            if co in coreq: # If the co passed in is in one of the coreq strings then it is a coreq
                return True
        
        return False

    def allPrereqsMet(self, cla: Class) -> tuple:
        required_coreq = False
        coreq = None
        for x in range(len(cla.prerequisites)):
            pre = cla.prerequisites[x]
            if('or' in pre): # If there are multiple equivalent classes
                start = 0
                e_classes = [] # Array of equivalent classes
                while(pre.find('or', start) >= 0):
                    temp = pre.find('or', start)
                    e_classes.append(pre[start:temp].strip())
                    start = temp+2
                e_classes.append(pre[start:].strip()) # classes is now an array of strings of the ids of equivalent classes
                has_one_equi_class = False

                for e_cla in e_classes: # Go through all equivalent prerequisites and check if one of them is satisfied
                    if e_cla in self.completed_classes:
                        has_one_equi_class = True
                    if self.isACoreq(cla, e_cla): # check if any of the equivalent classes are corequisites
                        required_coreq = True
                        coreq = e_cla

                if not has_one_equi_class: # If prereq that isn't satisfied is also a coreq then it doesn't matter
                    if not required_coreq: # If it's not a required coreq
                        return (False, False)
                    
            else: # If a specific class is needed
                if not (pre in self.completed_classes): # If the specific class has not been completed or taken then can't take this class
                    if not self.isACoreq(cla, pre):
                        return (False, False)
                    else:
                        required_coreq = True
                        coreq = pre
        return (True, coreq)

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

        for req in self.major_reqs: # Each Class left in Major Requirements
            if total_credit_hours >= 15:
                break
            can_take_req = True
            # TODO Handle array of potential options like "pick two sciences" etc. in this case req will be an array
            if type(req) == type([]): # Not a Class type aka is an array/list type
                pass
            else: # Is a Class type
                
                can_take_req, required_coreq = self.allPrereqsMet(req) # Determine if all prereqs are met and what a required coreq is if there is one

                if can_take_req:
                    if required_coreq != None:
                        classes.append(Class(required_coreq, 3, self.hasCoreq(required_coreq)))
                        if "/" in required_coreq:
                            self.completed_classes.append(required_coreq[:required_coreq.find('/')])
                            self.completed_classes.append(required_coreq[required_coreq.find('/')+1:])
                        else:
                            self.completed_classes.append(required_coreq)
                        total_credit_hours+=3
                    classes.append(req)
                    self.completed_classes.append(req.ID)
                    total_credit_hours+=req.credit_hours

                for x in range(len(self.major_reqs)): # Go through all classes for this semester
                    if self.major_reqs[x].ID in self.completed_classes: # If class ID is found in completed classes then consider it complete and remove from major_reqs
                        self.major_reqs.pop(x)
                        x-=1

        self.sem_rem -= 1 # Reduce Semester count
        return classes # Return this semesters classes
          


    def __str__(self) -> str:
        return "hi"

    