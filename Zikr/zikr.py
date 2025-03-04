import os
import sys
try:
    from colorama import Fore as f, Style as s
except ImportError:
    print("\nThis script requires colorama module. Install it using the command \"pip install colorama\" and try again.\n\nExiting...\n")
    exit(1)

CYAN = f.CYAN
LIGHT_CYAN = f.LIGHTCYAN_EX
YELLOW = f.YELLOW
RED = f.RED
BOLD = s.BRIGHT
DIM, RESET = s.DIM, s.RESET_ALL

class CustomError(Exception):
    """Custom exception with message"""
    def __init__(self):
        super().__init__()

def zikr(tasbeeh, count):
    print("-->",tasbeeh)
    print(f"  Count: 0", end='\r')
    print("\n" + f"\033[F",end='')

    for i in range(1,count+1):
        try:
            user_input = input()
        except (KeyboardInterrupt,EOFError):
            print("\nKeyboard Interrupt!\n\nExiting...\n")
            exit(1)
        if user_input.lower() in ['x','q']:
            exit(1)
        elif user_input.lower() == 's':
            break
        # Print the counter with carriage return
        print(f"\033[F  Count: {i}", end='\r')
    print('\n')
    os.system("termux-vibrate -f -d 100")

def single_zikr():
    print("\n ----- Zikr -----\n")
    all_zikr = ["Subhanallah", "Alhamdulillah", "Allahu Akbar", "Astagfirullah", "Duruud-e-Ibraheem", "Duruud-e-Shareef Short", "Subhanallahi Wabihamdihi Subhanallahil Azeem", "1st Kalima", "3rd Kalima", "4th Kalima", "Surah Ikhlaas"]

    for index, tasbeeh in enumerate(all_zikr,start=1):
        print(f"{index}.".center(4) + f"{tasbeeh}")
    try:
        choice = int(input("\nSelect Zikr:\n --> "))
        if choice < 1 or choice > 11:
            raise ValueError
        count = int(input("\nEnter Count:\n --> "))
        if count < 1:
            raise CustomError
    except (KeyboardInterrupt,EOFError):
        print("\nKeyboard Interrupt!\n\nExiting...\n")
        exit(1)
    except ValueError:
        print("\nInvalid input!\nPlease enter integer value from 1 - 11\n\nExiting...\n")
        exit(1)
    except CustomError:
        print("\nInvalid input!\nPlease enter positive integer value\n\nExiting...\n")
        exit(1)
    print()

    zikr(all_zikr[choice-1],count)
    print("\nAllhamdulillah DONE!\n")


def main():
    os.system("termux-vibrate -f -d 100")
    long_counts = [7,1,33,33,34,70,3,10,10,10,10,10,3,3,3,10]
    short_counts = [7,1,10,10,10,10,1,3,3,3,3,3,1,1,1,3]
    count = long_counts
    
    if len(sys.argv) > 1 and sys.argv[1] == "l":
        pass
    elif len(sys.argv) > 1 and sys.argv[1] == "s": 
        count = short_counts
    elif len(sys.argv) > 1 and sys.argv[1] == "i":
        single_zikr()
        exit(0)

    print("\n " + f" Zikr {"Long" if count[2]==33 else "Short"} ".center(21, '-') + "\n")
    zikr(f"Allahumna Ajirni minan naar [ x {count[0]} ]",count[0])
    zikr(f"Surah baqarah Last 2 ayats [ x {count[1]} ]",count[1])
    zikr(f"Subhanallah [ x {count[2]} ]",count[2])
    zikr(f"Alhamdulillah [ x {count[3]} ]",count[3])
    zikr(f"Allahu Akbar [ x {count[4]} ]",count[4])
    zikr(f"Astagfirullah [ x {count[5]} ]",count[5])
    zikr(f"Duruud-e-Ibraheem [ x {count[6]} ]",count[6])
    zikr(f"Duruud-e-Shareef Short [ x {count[7]} ]",count[7])
    zikr(f"Subhanallahi Wabihamdihi Subhanallahil Azeem [ x {count[8]} ]",count[8])
    zikr(f"3rd Kalima [ x {count[9]} ]",count[9])
    zikr(f"4th Kalima [ x {count[10]} ]",count[10])
    zikr(f"Surah Ikhlaas [ x {count[11]} ]",count[11])
    zikr(f"Surah Falaq [ x {count[12]} ]",count[12])
    zikr(f"Surah Naas [ x {count[13]} ]",count[13])
    zikr(f"Surah Kaafiruun [ x {count[14]} ]",count[14])
    zikr(f"1st Kalima [ x {count[15]} ]",count[15])

    print("\nAllhamdulillah DONE!\n")

if __name__ == "__main__":
    print(f"{BOLD}",end='')
    main()

