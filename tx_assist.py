import os
from time import sleep, strftime, localtime
from random import choice
from re import match
try:
    from colorama import Fore as f, Style as s
except ImportError:
    print("\nThis script requires colorama module. Install it using the command \"pip install colorama\" and try again.\n\nExiting...\n")
    exit(1)


## ===========================================================================
### Variables

start_time = localtime()
start_hour = int(strftime("%H", start_time))
start_min = int(strftime("%M", start_time))
start_sec = int(strftime("%S", start_time))

torch_state = False
NOTIFICATION_LIST = ['Say \'SubhanAllah\' X 3',
                    'Say \'Allhamdulillah\' X 3',
                    'Say \'AllahuAkbar\' X 4',
                    'Say \'Laa Ilaaha Illah....\'',
                    'Say \'Subhanallahi Wabihamdihi....\'',
                    'Recite \'3rd Kalima\' (Subhanallahi Walhamdulillahi....)',
                    'Recite \'4th Kalima\' (Laa Ilaaha Illalahu Wahdahu.....)',
                    'Recite \'Surah Ikhlaas\' X 3',
                    'Recite \'Duruud-e-Shareef\'',
                    'Say \'Astagfirullah\' X 3',
                    '\'Allahu Akbar\' while Climbing \'UP\'',
                    '\'SubhanAllah\' while Climbing \'DOWN\'']
ALLOWED_PHONE_CHARS = r'^[0-9*+#]+$'

CYAN = f.CYAN
LIGHT_CYAN = f.LIGHTCYAN_EX
YELLOW = f.YELLOW
RED = f.RED
BOLD = s.BRIGHT
DIM, RESET = s.DIM, s.RESET_ALL


## ===========================================================================
### Functions

# Function to toggle torch
def termx_torch():
    global torch_state

    print(f"{YELLOW}{BOLD}\n------ TORCH ------\n{RESET}")

    if torch_state :
        os.system("termux-torch off")
        print(f"{BOLD}Torch is set \'OFF\'\n{RESET}")
        torch_state = False

    else:
        os.system("termux-torch on")
        print(f"{BOLD}Torch is set \'ON\'\n{RESET}")
        torch_state = True

## --------------------------------------------------------------------------
# Function to a call
def termux_telephony_call():
    while True:
        print(f"{YELLOW}{BOLD}\n------ CALL ------\n{RESET}")

        phoneNumber = input("Enter Phone Number : ")

        if phoneNumber.count('+') == 1 :
            phoneNumberLength = 13
        else:
            phoneNumberLength = 10

        if phoneNumber in ['0','',' ']:
            print("Call Cancelled.\n")
            break

        if not (len(phoneNumber) in [4,5,phoneNumberLength] and phoneNumber.count('+') in [0,1] and match(ALLOWED_PHONE_CHARS, phoneNumber)):
            print(f"{RED}\nInvalid Phone Number. Call not sent.\n{DIM}"
                    f"Enter number as '0' if you want to Cancel{RESET}")
            continue

        os.system(f"termux-telephony-call {phoneNumber}")

        print(f"\nCalling \'{phoneNumber}\'",end='',flush = True)

        for i in range(7):
            print(".",end = "", flush = True)
            sleep(0.25)
        print("\n")
        exit()

## --------------------------------------------------------------------------
# Function to send sms
def termux_sms_send():
    while True:
        try:
            print(f"{YELLOW}{BOLD}\n------ Send SMS ------\n{RESET}")

            phoneNumber = int(input("Enter Phone Number : "))

            if phoneNumber in [0]:
                print("SMS Cancelled.\n")
                break

            if not (len(str(phoneNumber)) in [10]):
                print(f"{RED}\nInvalid Phone Number. SMS not sent.\n{DIM}"
                    f"Enter number as '0' if you want to Cancel{RESET}")
                continue

            text = input("\nEnter message : ")

            if text.count(" ") == len(text) or len(text) == 0:
                print(f"{RED}\nEmpty message can't be sent\n{RESET}")
                break

            os.system(f"termux-sms-send -n {phoneNumber} {text}")

            print("\nSending",end = "", flush =True)

            for i in range(7):
                print(".",end = "", flush = True)
                sleep(0.25)

            print(f"\n\nMessage \"{text[:32]}\".... is sent to \'{phoneNumber}\'\n")
            break

        except ValueError:
            print(f"{RED}\nInvalid Phone Number. SMS not sent.\n{DIM}"
                f"Enter phno. as '0' if you want to Cancel{RESET}")

## --------------------------------------------------------------------------
# Function to toggle wifi
def termux_wifi_enable():
    print(f"{YELLOW}{BOLD}\n------ WIFI ------{RESET}\n")

    wifi_state = input("Enter ON (o) or OFF (f) : ").upper()

    if wifi_state in ['O','0'] :
        os.system("termux-wifi-enable true")
        print("WIFI is set \'ON\'\n")

    elif wifi_state == 'F' :
        os.system("termux-wifi-enable false")
        print("WIFI is set\'OFF\'\n")

    else :
        print(f"{RED}{DIM}Please enter between \'o\' or \'f\'\n{RESET}")

## --------------------------------------------------------------------------
# Function to get notifications
def termux_notification():
    global NOTIFICATION_LIST, start_hour, start_min

    notificationSound = input("\nPlay Notification sound.... "
                                f"Phone will be removed from Silent Mode [\'y\' or \'n\'] : ").upper()

    if notificationSound in ['Y', 'YES'] :
        os.system("termux-volume ring 100")
        os.system("termux-volume notification 100")
        print()
    else:
        print("Notification Volume is Unaltered....\n")

    flash = input("Flash on Notification...[\'y\' or \'n\'] : ").upper()
    vibration = input("\nVibrate on Notification.....[\'y\' or \'n\'] : ").upper()

    try:
        notificationDelay = int(input("\nEnter Time Delay for next Notification (in Minutes <= 60) : "))
        if notificationDelay > 60 :
            print(f"{RED}{DIM}Enter Delay less than hour (60 min)\n{RESET}")
            return
        elif notificationDelay <= 0:
            print(f"{RED}{DIM}\nMinutes should be a Positive Integer Value < \'60\'\n{RESET}")
            return

    except ValueError :
        print(f"{RED}{DIM}\nMinutes should be a Positive Integer Value < \'60\'\n{RESET}")
        return

    currentLocalTime = localtime()
    current_hour = int(strftime("%H", currentLocalTime))
    current_min = int(strftime("%M", currentLocalTime))

    if start_min != current_min:
        start_min = current_min

    print(f"{YELLOW}{BOLD}\n------ Getting Random Notification ------{RESET}")

    if start_min + notificationDelay > 59:
        current_hour = current_hour + 1
        display_min = start_min + notificationDelay - 60
    else:
        display_min = start_min + notificationDelay

    if display_min < 10:
        print(f"{DIM}Next Notification at : --- {current_hour}:0{display_min} ---{RESET}")
    else:
        print(f"{DIM}Next Notification at : --- {current_hour}:{display_min} ---{RESET}")

    print(f"{DIM}Press \' ctrl + c \' to Cancel...{RESET}\n")

    while True:
        try:
            next_notification_min = start_min + notificationDelay
            randamNotification = choice(NOTIFICATION_LIST)

            currentLocalTime = localtime()
            current_hour = int(strftime("%H", currentLocalTime))
            current_min = int(strftime("%M", currentLocalTime))
            current_sec = int(strftime("%S", currentLocalTime))

            if next_notification_min > 59 :
                next_notification_min = next_notification_min - 60
                current_hour = current_hour + 1

            if current_min == next_notification_min and current_sec == 0 :
                os.system(f"termux-notification --content \"Zikar Time\" --title \"{randamNotification}\" --image-path $(find ~ -type f -name Zikr_Image.jpeg)")

                print(f"\n{randamNotification}\n")

                if vibration in ['Y', 'YES'] :
                    os.system("termux-vibrate -f -d 1500")
                    pass
                if flash in ['Y', 'YES'] :
                    os.system("termux-torch on")
                    sleep(0.25)
                    os.system("termux-torch off")

                start_min = next_notification_min

                print(f"{YELLOW}{BOLD}\n------ Getting Random Notification ------{RESET}")

                if start_min == 0:
                    print(f"{DIM}Next Notification at : --- {current_hour - 1}:0{start_min + notificationDelay} ---{RESET}")

                elif start_min + notificationDelay < 10:
                    print(f"{DIM}Next Notification at : --- {current_hour}:0{start_min + notificationDelay} ---{RESET}")

                elif start_min + notificationDelay == 60:
                    print(f"{DIM}Next Notification at : --- {current_hour + 1}:00 ---{RESET}")

                else:
                    print(f"{DIM}Next Notification at : --- {current_hour}:{start_min + notificationDelay} ---{RESET}")

                print(f"{DIM}Press \' ctrl + c \' to Cancel...{RESET}\n")
                sleep(notificationDelay * 60 - 3)

        except KeyboardInterrupt:
            print(f"\nNotifications cancelled.\nExiting",end='',flush = True)
            for i in range(5):
                print(".",end = "", flush = True)
                sleep(0.2)
            print("\n")
            exit()

## --------------------------------------------------------------------------
# Function to adjust volumw od audio streams
def volume_change(vol_name):
    while True:
        print(f"{YELLOW}{BOLD}\n------ {vol_name} ------\n{RESET}")
        try:
            volume = input(f"Enter {vol_name} Volume [0 - 100] : ")

            if volume in ['',' ']:
                print(f"\n{vol_name} Volume is Unaltered\n")
                break

            elif 0 <= int(volume) and int(volume) <= 100:
                os.system(f'termux-volume {vol_name.lower()} {volume}')
                print(f"\n{vol_name} Volume is set to {volume}\n")
                break

            else:
                print(f"{RED}\nInvalid Volume input. Please enter Integer value between "
                        f"[0 - 100]\n{DIM}Just press \'Enter\' to Exit.{RESET}")

        except:
            print(f"{RED}\nInvalid Volume input. Please enter Integer value between [0 - 100]\n"
                    f"{DIM}Just press \'Enter\' to Exit.{RESET}")

###
# volume control
def termux_volume():

    while True :
        print(f"{YELLOW}{BOLD}\n------ Volume Adjust ------\n{RESET}")

        volume_input = input(f"{CYAN}0. Exit       1. System        2. Call        3. Ring\n"
                                f"4. Music      5. Notification       6. Alarm{RESET}\n\n---> ")

        if volume_input in ['',' ','0'] :
            print()
            break
        elif volume_input == '1' :
            volume_change("System")
        elif volume_input == '2' :
            volume_change("Call")
        elif volume_input == '3' :
            volume_change("Ring")
        elif volume_input == '4' :
            volume_change("Music")
        elif volume_input == '5' :
            volume_change("Notification")
        elif volume_input == '6' :
            volume_change("Alarm")
        else :
            print(f"{RED}{BOLD}\nUnrecognised Input{RESET}\n{RED}{DIM}Select any from [1 - 6]{RESET}\n")

## --------------------------------------------------------------------------
# Function to set all audio streams volume to 0
def silent_phone():
    os.system(f'termux-volume system 0')
    os.system(f'termux-volume call 0')
    os.system(f'termux-volume ring 0')
    os.system(f'termux-volume music 0')
    os.system(f'termux-volume notification 0')
    os.system(f'termux-volume alarm 0')

    print(f"{CYAN}\nAll Audio Streams are set to \'0\'{RESET}\n\n")

## --------------------------------------------------------------------------
# Function to set all audio streams volume to 100
def volume_up():
    os.system(f'termux-volume system 100')
    os.system(f'termux-volume call 100')
    os.system(f'termux-volume ring 100')
    os.system(f'termux-volume music 100')
    os.system(f'termux-volume notification 100')
    os.system(f'termux-volume alarm 100')

    print(f"{CYAN}\nAll Audio Streams are set to \'100\'{RESET}\n\n")


### ===========================================================================
## Main function to execute all the steps
#

def mySettings():
    print(f"{YELLOW}{BOLD}Choose the following function to perform on your phone :-\n{RESET}")

    setting = input(f"{LIGHT_CYAN}0. Exit         1. Torch on/off         "
                    f"2. Call \n3. Send SMS     4. WIFI on/off     5. Get Random Notifications\n"
                    f"6. Volume adjust     7. Silent Phone     8. Volume Up\n\n---> {RESET}")

    if setting in ['','0','exit'] :
        os.system("clear")
        exit()

    elif setting == '1' :
        termx_torch()

    elif setting == '2' :
        termux_telephony_call()

    elif setting == '3' :
        termux_sms_send()

    elif setting == '4' :
        termux_wifi_enable()

    elif setting == '5' :
        termux_notification()

    elif setting == '6' :
        termux_volume()

    elif setting == '7' :
        silent_phone()

    elif setting == '8' :
        volume_up()

    else:
        print(f"{RED}{BOLD}\nUnrecognised Input{RESET}\n{RED}{DIM}Select any from [0 - 5]{RESET}\n")


### MAIN

if __name__ == '__main__':
    while True:
        os.system("clear")
        mySettings()
        input(f"{DIM}Press \'Enter\' to continue.... {RESET} ")
