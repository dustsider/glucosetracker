import numpy as np
from collections import defaultdict, Counter
import threading
import time
import pygame

#global variables and initialization
low_blood_sugar_event = 0
high_blood_sugar_event = 0
week = [defaultdict(int) for _ in range(7)]

def main():
    print("Blood Glucose/Sugar Recorder")
    #main menu loop 
    done=False
    while not done:
        options = input("What would you like to do: \n1 -> record blood glucose \n2 -> print current readings \n3 -> look at statistics \nq -> quit ")
        if options == "1":
            record_blood_glucose()
        elif options == "2":
            show_available_readings()
        elif options == "3":
            statistics()
        elif options == "q":
            done=True
        else:
            print("Invalid response")

def record_blood_glucose():
    global week

    while True:
        #try/except to handle errors in inputs
        try:
            day_choice = int(input("Which Day do you want to record? (1-7): "))
            #keeps day choice between 1-7
            if 1 <= day_choice <= 7:
                break #return to main loop
            else:
                print("Invalid day choice. Please enter a number between 1 and 7")

        except ValueError:
            print("Please enter a valid number.") #

        
    event = input("Enter the event (e.g., wakeup, breakfast, lunch, dinner, evening, etc.): ")
    try:
        reading = int(input("Enter the blood glucose reading (mg/dL): "))
    except ValueError:
        print("Please enter a valid number for blood glucose reading.")
        return

    week[day_choice - 1][event] = reading 
    # adding reading to the specific day's dictionary entry
    print(f"Recorded {reading} for {event} on day {day_choice}.")
    
    if reading < 70:
        global low_blood_sugar_event
        low_blood_sugar_event += 1
        print("Alert: Hypoglycemic event detected!")
    elif reading > 180:
        global high_blood_sugar_event
        high_blood_sugar_event += 1
        print("Alert: Hyperglycemic event detected")
    
    alarm=input("Do you want to set up a future alarm? (y/n): ").upper()
    if alarm=="Y":
    
        #initialize alarm for future recordings    
        try:
            alarm_time = int(input("Set an alarm for how many minutes do you want to input your next recording? (1 hour = 60 minutes) "))
            #start alarm thread
            alarm_thread = threading.Thread(target=start_alarm, args=(alarm_time,))
            alarm_thread.start()
        except ValueError:
            print("Please enter a valid number for alarm time.")
    else:
        print("No alarm set up.")

def start_alarm(delay):
    time.sleep(delay * 60)
    play_alarm()

def play_alarm():
    pygame.mixer.init()3
    pygame.mixer.music.load("alarm.mp3")
    pygame.mixer.music.play()
    while True:
        response = input("Alarm! Press 's' to snooze for 5 minutes, or 'q' to quit.")
        if response == "s":
            time.sleep(5 * 60) #snooze for 5 minutes
            playsound("alarm.mp3")
        elif response == "q":
            pygame.mixer.music.stop()
            break
        else:
            print("Invalid response.")

def show_available_readings():
    global week
    which_readings=input("Which do you want? week/day: ")
    if which_readings=="week":
        for i, day in enumerate(week, start=1):
            print(f"Day {i}")
            for event, value in day.items():
                print(f" {event}: {value}")
    elif which_readings=="day":
        try:
            day_choice = int(input("Which day do you want? (1-7): "))
            if 1 <= day_choice <= 7:
                day = week[day_choice - 1]
                for event, value in day.items():
                    print(f"  {event}: {value}")
            else:
                print("Invalid day choice.")
        except ValueError:
            print("Please enter a valid number for day choice.")

def statistics():
    global week, low_blood_sugar_event, high_blood_sugar_event
    #list comprehension of all available values in week variable
    all_readings = [value for day in week for value in day.values()]

    if not all_readings:
        print("No readings available for statistics")
        return

    mean_value = np.mean(all_readings)
    median_value = np.median(all_readings)
    mode_value = Counter(all_readings).most_common(1)[0][0]

    print("Statistics")
    print(f"Mean: {mean_value:.2f}")
    print(f"Median: {median_value:.2f}")
    print(f"Mode: {mode_value:.2f}")
    print(f"Total Hypoglycemic Events: {low_blood_sugar_event}")
    print(f"Total Hyperglycemic Events: {high_blood_sugar_event}")

if __name__ == "__main__":
    main()
