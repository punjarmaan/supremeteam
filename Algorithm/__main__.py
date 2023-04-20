#from Schedule import Schedule
import pandas as pd
import numpy as np
from Schedule import Schedule

major_df = pd.read_csv('./WebScraper/major_updated.csv', header=None)
major_df.index = major_df.loc[:,0].to_numpy() # Set Row Labels
major_df.drop(0, inplace=True, axis=1) # Drop First Column

def getMajorClasses(major: str):
    major_classes = major_df.loc[major].to_numpy()
    c = 0
    for x in major_classes:
        if(type(x) != str):
            break
        else:
            c+=1
    major_classes = major_classes[0:c]
    return major_classes

def valid(major: str) -> bool:
    try:
        major_classes = major_df.loc[major].to_numpy()
        return True
    except:
        return False
def main():
    # Initialize variables for creating Schedule object
    semesters_remaining = int(input("How many semesters do you have remaining?\n"))
    major = input("What is your major? Type it exactly how it is on the UNC Course Catalog including B.S. or B.A.. Located here: https://catalog.unc.edu/undergraduate/programs-study/\n")
    while(valid(major) != True):
          print("Invalid Major")
          major = input("What is your major? Type it exactly how it is on the UNC Course Catalog including B.S. or B.A.. Located here: https://catalog.unc.edu/undergraduate/programs-study/\n")
    
    gen_eds = int(input("How many focus capacities (Gen Eds) do you have left?\n"))
    completed_classes = []

    # Get all completed classes from user
    major_classes = getMajorClasses(major)
    print("Out of the following classes which have you taken or have credit for? Enter the course ID's as you see them one at a time. Enter 'Done' when you have listed all completed courses.")
    for x in major_classes:
        print(x)
    user_input = input()

    while user_input != 'Done':
        completed_classes.append(user_input)
        user_input = input()
    lang = int(input("How many more semesters of language do you need to take to satisfy the gen ed requirement (3 semesters max)?"))
    
    # Create Scheduler
    schedule = Schedule(completed_classes, semesters_remaining, major, major_classes, gen_eds, lang)
    print("You are" + (" a " if schedule.first_year else " not a ") + "first year.")
    if(schedule.first_year):
        fy_gen_eds = []
        fy_gen_eds.append(int(input("Do you still need to take ENGL 105? 1 - Yes or 0 - No")))
        fy_gen_eds.append(int(input("Do you still need to take a First Year Seminar? 1 - Yes or 0 - No")))
        fy_gen_eds.append(int(input("Do you still need to take Data Literacy Lab? 1 - Yes or 0 - No")))
        fy_gen_eds.append(int(input("Do you still need to take College Thriving? 1 - Yes or 0 - No")))
        schedule.fy_gen_eds = fy_gen_eds
    # schedule.constructSchedule()

    print("Here is your schedule: ")
    # print(schedule)
    




if __name__ == "__main__":
    main()
    