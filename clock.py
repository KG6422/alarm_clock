#! /usr/bin/python3

'''
things to add:

-alarm that requires puzzle to solve
    -> math_puzzle.py
    -> remove all other ways to close the app when timer is going off
    -> make puzzle harder than retyping a sentence, but not hard enough where I will ctrl-c it
-be able to customize alarm sounds
    -> fix alarm sound being in-line, need to be executed asynchronously so it doesn't pause execution/input
-give nice morning message when unlocked
    -> weather info
    -> schedule of classes
-BUG: unable to 'exit' after solving puzzle
'''


from datetime import datetime
import PySimpleGUI as sg
import beepy
import math_puzzle as mp


alarm_hr = 6
alarm_min = 15
SOUND = "error" # error noise

# ~~~~~~~~~~~~~~~~~~~~~~~~~~

playing_sound = False

#pass in formatted time if later time is needed
def get_time(time=True):
    if time: # by default, used to get current time
        tm = datetime.now()
        return(str(tm.strftime("%X")))
    else:  
        return #not implemented

def alarm_screen():
    ans="I solemly swear to not get back in bed!"
    lay2 = [
        [sg.Text("Retype the following sentence to silence the alarm (1/2):", font="Any 40 bold")],
        [sg.Text(ans, font="Any 30 italic")],
        [sg.Text("Response", font="Any 20"), sg.InputText()],
        [sg.Button("Submit", key='-subm-')]
    ]
    win2 = sg.Window('Time to wake up!', lay2, resizable=True, modal=True)
    while True:
        beepy.beep(sound=SOUND)
        ev2, vals2 = win2.read(timeout= 1500)
        if ev2 == '-subm-' and vals2[0] == ans:
            #escape!
            break
    win2.close()
    

def math_puzzle():
    puzzle = mp.puzzle() # returns (ans, string)
    lay_math = [
        [sg.Text("Answer the following math question to silence the alarm (2/2):", font="Any 40 bold")],
        [sg.Text(puzzle[1] + " = ?", font="Any 30 italic")],
        [sg.Text("Response", font="Any 20"), sg.InputText()],
        [sg.Button("Submit", key='-subm-')]
    ]
    win_math = sg.Window('Time to wake up!', lay_math, resizable=True, modal=True)
    while True:
        beepy.beep(sound=SOUND)
        ev_math, vals_math = win_math.read(timeout= 3000)
        if ev_math == '-subm-' and vals_math[0] == puzzle[0]:
            #escape!
            break
    win_math.close()
    

def set_alarm_screen():
    lay_sas = [
        [sg.Text("When should the alarm be set for? Use 24 hour time.", font="Any 40 bold")],
        [sg.Text("Hour", font="Any 20"), sg.InputText()],
        [sg.Text("Minute", font="Any 20"), sg.InputText()],
        [sg.Button("Submit", key='-subm_sas-')]
    ]
    win_sas = sg.Window('Set Alarm Time', lay_sas, resizable=True, modal=True)
    while True:
        ev_sas, vals_sas = win_sas.read(timeout= 5000)
        # TODO: No error handling!
        if ev_sas == '-subm_sas-' and isinstance(int(vals_sas[0]),int) and isinstance(int(vals_sas[1]),int):
            global alarm_hr, alarm_min
            alarm_hr = int(vals_sas[0]) % 24
            alarm_min = int(vals_sas[1]) % 60
            break
    win_sas.close()

def is_alarm_conditions():
    delta_min = (datetime.now().minute - alarm_min) % 60 # gives num minutes past alarm
    return(alarm_hr == datetime.now().hour and delta_min >= 0 and delta_min < 8)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sg.set_options(border_width=2, text_color="white", background_color="black",
            text_element_background_color="black")

layout = [
    [sg.Text(" ", size=(1,15))],
    [sg.Text("Alarm Clock", key="-c-", font="Any 120 bold", justification="center")], 
    [sg.Button("Set Alarm", key="-alarm-")],
    [sg.Button("Exit")],
    [sg.Text("No Alarm Set", key="-info-", font="Any 30 italic")]
]

window = sg.Window("Alarm Clock", layout, resizable=True, element_justification="c")
window.finalize()

alarm_set = False

while True:
    window['-c-'].Update(get_time())
    event, values = window.read(timeout=999)
    if event == sg.WIN_CLOSED or event == "Exit":
        if alarm_set == False and not is_alarm_conditions():
            break
    elif event == "-alarm-":
        if not alarm_set:
            set_alarm_screen()
            sg.Popup("Setting alarm for "+str("{:02d}".format(alarm_hr)) +":"+str("{:02d}".format(alarm_min))+ ":00", keep_on_top=True)
            window["-alarm-"].Update("Remove Alarm")
            window["-info-"].Update("Alarm Set for "+str("{:02d}".format(alarm_hr)) +":"+str("{:02d}".format(alarm_min))+ ":00")
            alarm_set = True
        elif alarm_set:
            if is_alarm_conditions():
                win2 = alarm_screen()
                win_math = math_puzzle()
            else:
                sg.Popup("Cancelling Alarm!", keep_on_top=True)
            window["-alarm-"].Update("Set Alarm")
            alarm_set = False
            window["-info-"].Update("No Alarm Set")
    if is_alarm_conditions() and alarm_set == True:
        beepy.beep(sound=SOUND)
        
    


window.close()

print("exiting at " + get_time())