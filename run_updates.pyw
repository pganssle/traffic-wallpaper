from subprocess import call
from time import sleep
import os
import json

with open("settings.json", "r") as sf:
    set_dict = json.load(sf)

    time_interval = set_dict["time_interval"]
    runner_file = set_dict["runner_file"]

time_interval = 30      # Seconds
runner_file = 'runner.txt'

scriptloc, __ = os.path.split(os.path.realpath(__file__))
make_map_loc = os.path.join(scriptloc, "make_traffic_map.pyw")
merge_set_loc = os.path.join(scriptloc, "merge_and_save_wallpaper.pyw")
save_wallpaper_loc = os.path.join(scriptloc, "set_wallpaper.pyw")

open(runner_file, 'w+').close() # Create this file. Delete it to stop the script.

while os.path.exists(runner_file):
    call(["python.exe", make_map_loc])
    call(["python.exe", merge_set_loc])
    call(["python.exe", save_wallpaper_loc])
    sleep(time_interval)

