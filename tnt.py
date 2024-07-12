import json
import os
import sys
import pystyle

from pynput import keyboard
global preset

def on_release(key):
    global preset
    try:
        if key == keyboard.Key.f1:
            Aimbot.update_status_aimbot()
        if key == keyboard.Key.f2:
            Aimbot.clean_up()
        
    except NameError:
        pass

def main():
    global preset
    global lunar
    lunar = Aimbot(collect_data = "collect_data" in sys.argv)
    lunar.start()

def setup():
    path = "lib/config"
    if not os.path.exists(path):
        os.makedirs(path)

    print("[INFO] In-game X and Y axis sensitivity should be the same")
    def prompt(str):
        valid_input = False
        while not valid_input:
            try:
                number = float(input(str))
                valid_input = True
            except ValueError:
                print("[!] Invalid Input. Make sure to enter only the number (e.g. 6.9)")
        return number

    xy_sens = prompt("X-Axis and Y-Axis Sensitivity (from in-game settings): ")
    targeting_sens = prompt("Targeting Sensitivity (from in-game settings): ")

    print("[INFO] Your in-game targeting sensitivity must be the same as your scoping sensitivity")
    sensitivity_settings = {"xy_sens": xy_sens, "targeting_sens": targeting_sens, "xy_scale": 10/xy_sens, "targeting_scale": 330/(targeting_sens * xy_sens), "targeting_scale_aiming": 920/(targeting_sens * xy_sens)}

    with open('lib/config/config.json', 'w') as outfile:
        json.dump(sensitivity_settings, outfile)
    print("[INFO] Sensitivity configuration complete")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

    banner = """
██████████████████████████████████████████████
█─▄─▄─█▄─▀█▄─▄█─▄─▄─█▀▀▀▀▀███▀▄─██▄─▄█▄─▀█▀─▄█
███─████─█▄▀─████─███████████─▀─███─███─█▄█─██
▀▀▄▄▄▀▀▄▄▄▀▀▄▄▀▀▄▄▄▀▀▀▀▀▀▀▀▀▄▄▀▄▄▀▄▄▄▀▄▄▄▀▄▄▄▀"""

    banner = pystyle.Colorate.Horizontal(pystyle.Colors.red_to_green, pystyle.Center.XCenter(banner))
    print(banner+"\n")

    path_exists = os.path.exists("lib/config/config.json")
    if not path_exists or ("setup" in sys.argv):
        if not path_exists:
            print("[!] Sensitivity configuration is not set")
        setup()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner+"\n")
    smooth = input(f"Smoothing? (y/n) > ")
    path_exists = os.path.exists("lib/data")
    if "collect_data" in sys.argv and not path_exists:
        os.makedirs("lib/data")
    if (smooth.lower() in ["yes", "ye", "y"]):
        from lib.orig import Aimbot
        listener = keyboard.Listener(on_release=on_release)
        listener.start()
        main()
    elif (smooth.lower() in ["no", "n"]):
        from lib.smooth import Aimbot
        listener = keyboard.Listener(on_release=on_release)
        listener.start()
        main()
    else:
        print(f"Invalid Answer.")
        input()
        sys.exit()