class Class:

    def __init__(self, ID: str, credit_hours: int, corequisite: bool, prerequisites=[], name=""):
        self.ID = ID
        self.credit_hours = credit_hours
        self.corequisite = corequisite
        self.prerequisites = prerequisites
        self.course_name = name
    
    