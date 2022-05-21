import threading
from json import load
from time import sleep
import os
import argparse as ag
import sys

from utils.GameStateEnum import GameState
from utils.Console import Console
from utils.InstructionHandler import InstructionHandler
from utils.Statemachine import Statemachine

global OS_PATH
global DELIMETER
OS_PATH = os.path.dirname(os.path.realpath(__file__))
if os.name in ['nt']:
    DELIMETER = '\\'
else:
    DELIMETER = '/'

# Fetch command line arguments for map
parser = ag.ArgumentParser()
parser.add_argument("-map", "--map")
parser.add_argument("-gm", "--gamemode")
args = parser.parse_args(sys.argv[1:])

# Create Console
console = Console()

# Load settings file
with open(os.path.join(OS_PATH, "config/settings.json"), 'r') as json_settings:
    settings = load(json_settings)

    info = {
        "stop": False,
        "paused": False,
        "victory": False,
        "defeat": False,
        "insta": False,
        "levelup": False,
        "mapsettings": None,
        "isFreeplay": False,
        "currentRound": 0
    }


def instructions():
    info['instructionHandler'].start()

    while not info["stop"]:
        if not info["paused"] and not info["victory"] and not info["defeat"] and not info["insta"] and not info["levelup"]:
            info['instructionHandler'].check_for_instruction(info)
        if info["victory"] and not info["isFreeplay"]:
            console.wins += 1
            info['instructionHandler'].restart_game()
            info['instructionHandler'].start()
        if info["victory"] and info["isFreeplay"]:
            info['instructionHandler'].start_freeplay()
        if info["levelup"]:
            info['instructionHandler'].leveled_up()
        if info["defeat"]:
            console.loss += 1

        sleep(0.2)


def state_machine():
    while True:
        info["currentRound"] = info["statemachine"].currend_round(info["isFreeplay"])

        state = info["statemachine"].check_current_state()
        if state == GameState.PAUSED:
            print(f"Paused script...")
            info["paused"] = True
        else:
            info["paused"] = False

        if state == GameState.VICTORY:
            print(f"Victory")
            info["victory"] = True
        else:
            info["victory"] = False

        if state == GameState.DEFEAT:
            print(f"Defeat")
            info["defeat"] = True
        else:
            info["defeat"] = False

        if state == GameState.INSTA:
            print(f"Got insta monkey!")
            info["insta"] = True
        else:
            info["insta"] = False

        if state == GameState.LEVELUP:
            print(f"Congratulations! You have leveled up:)")
            info["levelup"] = True
        else:
            info["levelup"] = False

        sleep(0.2)


try:
    console.welcome_screen()

    if not args.map:
        mapName = input("Please choose the map you want to load the configs for >>> ")
    else:
        mapName = args.map

    if not args.gamemode:
        gamemode = input("Please choose the gamemode (no .json extension) >>> ")
    else:
        gamemode = args.gamemode

    mapName = mapName.lower()
    gamemode = gamemode.lower()
    print(f"Loading Config: {os.path.join(OS_PATH, f'config{DELIMETER}maps{DELIMETER}{mapName}{DELIMETER}{gamemode}.json')}")

    with open(os.path.join(OS_PATH, f"config{DELIMETER}maps{DELIMETER}{mapName}{DELIMETER}{gamemode}.json"), 'r') as map_json:
        map_settings = load(map_json)
    sleep(2)

    info["mapsettings"] = map_settings

    console.welcome_screen()
    console.show_stats()
    console.print_new_lines(2)

    statemachine = Statemachine(console)
    instructionHandler = InstructionHandler(settings, map_settings, console)

    info['statemachine'] = statemachine
    info['instructionHandler'] = instructionHandler

    state_machine_thread = threading.Thread(target=state_machine, args=())
    instruction_thread = threading.Thread(target=instructions, args=())

    state_machine_thread.start()
    instruction_thread.start()


except KeyboardInterrupt:
    exit()

except Exception as e:
    print(f"An error has occured:")
    raise e
