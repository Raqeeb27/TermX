"""
zikr.py - A command-line tool for guided zikr (remembrance of Allah).

This script provides an interactive way to perform zikr with customizable
repetition counts. Users can choose from:
    - Long zikr sequence (predefined counts)
    - Short zikr sequence (simplified counts)
    - A single zikr from a menu of common options

Features:
    - Interactive counter with live updates
    - Exit or skip options during recitation
    - Termux vibration feedback after each zikr (if available)
    - Error handling for invalid or interrupted input

Requirements:
    - Python 3
    - colorama (`pip install colorama`)

Usage:
    python zikr.py --long
    python zikr.py --short
    python zikr.py --single
"""

import os
import sys
import time
import argparse

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
    """Custom exception raised when invalid input is provided."""
    def __init__(self):
        super().__init__()


def hold_console_for_input() -> None:
    """
    Pauses execution and waits for user input before exiting.

    This function is primarily useful in environments where the console
    might close immediately (e.g., double-clicking the script). It allows
    the user to read the output by waiting for them to press Enter. 

    Exits gracefully if interrupted with `Ctrl+C` or `Ctrl+D`.
    """
    try:
        input("\n[*] Press Enter to exit...")
    except (KeyboardInterrupt, EOFError):
        print("\n\n[!] Keyboard Interrupt\n")
        time.sleep(0.75)
        sys.exit(1)


def zikr(tasbeeh: str, count: int) -> None:
    """
    Guides the user through reciting a specific Zikr with a counter.

    Args:
        tasbeeh (str): The zikr phrase (e.g., "Subhanallah").
        count (int): The number of times to repeat the zikr.

    Behavior:
        - Displays the zikr and counts each recitation as the user presses Enter.
        - Supports early exit with 'x' or 'q'.
        - Allows skipping the zikr with 's'.
        - Vibrates the device (Termux) upon completion.
    """
    print("-->", tasbeeh)
    print(f"  Count: 0", end='\r')
    print("\n" + f"\033[F", end='')

    for i in range(1, count + 1):
        try:
            user_input = input()
        except (KeyboardInterrupt, EOFError):
            print("\nKeyboard Interrupt!\n\nExiting...\n")
            exit(1)
        if user_input.lower() in ['x', 'q']:
            print("\nExiting...")
            sys.exit(1)
        elif user_input.lower() == 's':
            break
        print(f"\033[F  Count: {i}", end='\r')
    print('\n')
    os.system("termux-vibrate -f -d 100")


def single_zikr() -> None:
    """
    Allows the user to select and perform a single zikr from a predefined list.

    Behavior:
        - Displays a menu of available zikr options.
        - Prompts the user to select one and specify the number of repetitions.
        - Validates user input for correctness.
        - Calls the `zikr()` function to perform the recitation process.
        - Exits gracefully on invalid input or interruption.
    """
    print("\n ----- Zikr -----\n")
    all_zikr = [
        "Subhanallah", "Alhamdulillah", "Allahu Akbar", "Astagfirullah",
        "Duruud-e-Ibraheem", "Duruud-e-Shareef Short",
        "Subhanallahi Wabihamdihi Subhanallahil Azeem",
        "1st Kalima", "3rd Kalima", "4th Kalima", "Surah Ikhlaas"
    ]

    for index, tasbeeh in enumerate(all_zikr, start=1):
        print(f"{index}.".center(4) + f"{tasbeeh}")
    try:
        choice = int(input("\nSelect Zikr:\n --> "))
        if choice < 1 or choice > 11:
            raise ValueError
        count = int(input("\nEnter Count:\n --> "))
        if count < 1:
            raise CustomError
    except (KeyboardInterrupt, EOFError):
        print("\nKeyboard Interrupt!\n\nExiting...\n")
        exit(1)
    except ValueError:
        print("\nInvalid input!\nPlease enter integer value from 1 - 11\n\nExiting...\n")
        exit(1)
    except CustomError:
        print("\nInvalid input!\nPlease enter positive integer value\n\nExiting...\n")
        exit(1)
    print()

    zikr(f"{all_zikr[choice-1]} [ x {count} ]", count)
    print("Allhamdulillah DONE!\n")


def main(long: bool = False, short: bool = False, single: bool = False) -> None:
    """
    Main function to execute zikr sequences based on user choice.

    Args:
        long (bool): If True, performs the "long" zikr sequence.
        short (bool): If True, performs the "short" zikr sequence.
        single (bool): If True, prompts the user to select a single zikr.

    Behavior:
        - Executes the zikr sequence according to the provided flag.
        - Uses predefined counts for long/short zikr lists.
        - Calls `single_zikr()` if the single option is chosen.
        - Provides interactive counting for each zikr.
    """
    os.system("termux-vibrate -f -d 100")
    long_counts = [7, 1, 33, 33, 34, 70, 3, 10, 10, 10, 10, 10, 3, 3, 3, 10]
    short_counts = [7, 1, 10, 10, 10, 10, 1, 3, 3, 3, 3, 3, 1, 1, 1, 3]
    count = long_counts

    if long:
        pass
    elif short:
        count = short_counts
    elif single:
        single_zikr()
        sys.exit(0)

    print("\n " + f" Zikr {"Long" if count[2]==33 else "Short"} ".center(21, '-') + "\n")
    zikr(f"Allahumna Ajirni minan naar [ x {count[0]} ]", count[0])
    zikr(f"Surah baqarah Last 2 ayats [ x {count[1]} ]", count[1])
    zikr(f"Subhanallah [ x {count[2]} ]", count[2])
    zikr(f"Alhamdulillah [ x {count[3]} ]", count[3])
    zikr(f"Allahu Akbar [ x {count[4]} ]", count[4])
    zikr(f"Astagfirullah [ x {count[5]} ]", count[5])
    zikr(f"Duruud-e-Ibraheem [ x {count[6]} ]", count[6])
    zikr(f"Duruud-e-Shareef Short [ x {count[7]} ]", count[7])
    zikr(f"Subhanallahi Wabihamdihi Subhanallahil Azeem [ x {count[8]} ]", count[8])
    zikr(f"3rd Kalima [ x {count[9]} ]", count[9])
    zikr(f"4th Kalima [ x {count[10]} ]", count[10])
    zikr(f"Surah Ikhlaas [ x {count[11]} ]", count[11])
    zikr(f"Surah Falaq [ x {count[12]} ]", count[12])
    zikr(f"Surah Naas [ x {count[13]} ]", count[13])
    zikr(f"Surah Kaafiruun [ x {count[14]} ]", count[14])
    zikr(f"1st Kalima [ x {count[15]} ]", count[15])

    print("\nAllhamdulillah DONE!\n")


if __name__ == "__main__":
    """
    Command-line interface for zikr.py.

    Parses arguments to determine which zikr mode to run:
        --long   : Performs the long zikr sequence.
        --short  : Performs the short zikr sequence.
        --single : Lets the user select and perform a single zikr.

    Rules:
        - At least one argument must be provided.
        - Only one argument can be used at a time.

    Exits with status code 1 if arguments are missing or invalid.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--long", action="store_true", help="Long Zikr")
    parser.add_argument("--short", action="store_true", help="Short Zikr")
    parser.add_argument("--single", action="store_true", help="Single Zikr")

    args = parser.parse_args()

    if not any([args.long, args.short, args.single]):
        print("\n[-] No arguments provided.")
        print(f"[*] Usage: zikr.py --long OR --short OR --single")
        sys.exit(1)

    if sum([bool(args.long), bool(args.short), bool(args.single)]) > 1:
        print("\n[-] Only one of --long, --short or --single can be used at a time.")
        sys.exit(1)

    print(f"{BOLD}", end='')
    main(args.long, args.short, args.single)

