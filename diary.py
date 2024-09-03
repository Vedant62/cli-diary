#!/usr/bin/env python3

from pathlib import Path
import json
import argparse
from datetime import datetime
# config_location = <YOUR-PREFERRED-STORAGE-LOCATION> 
months = {
    '1': 'jan',
    '2': 'feb',
    '3': 'march',
    '4': 'april',
    '5': 'may',
    '6': 'jun',
    '7': 'july',
    '8': 'aug',
    '9': 'sept',
    '10': 'oct',
    '11': 'nov',
    '12': 'dec',
}
current_datetime = datetime.now()

def setup(location, name):
    path  = Path(location)
    created_path = path / name
    created_path.mkdir(parents= True, exist_ok=True) # creates a folder (name) at location

    with open(config_location, 'r+') as fp:
        json.dump({"diary_loc": str(created_path)}, fp, indent=2)

    #now creating month folders from current -> december
    
    for i in range(current_datetime.month, 13):
        new_path = created_path/ months[str(i)]
        new_path.mkdir(parents=True, exist_ok=True) # creates month foldes in diary

def move_diary(source, destination):
    src = Path(source)
    des = Path(destination)
    des = des / src.name

    with open(config_location, 'w') as fp:
        json.dump({"diary_loc": str(des)}, fp, indent=2)
    src.rename(des)

def new_entry(text):
    with open(config_location, 'r+') as fp:
        data = json.load(fp)
    diary_location = data['diary_loc']
    current_month = months[str(current_datetime.month)]
    path = Path(diary_location)
    path_to_add = path / current_month

    formatted_dt = current_datetime.strftime("%d_%H%M")
    filename = path_to_add / formatted_dt
    filename.touch(exist_ok=True, )

    with open(str(filename), 'a+') as fp:
        fp.write(f"{current_datetime.strftime('%d/%m')}  @{current_datetime.strftime('%H:%M')}\n\n")
        fp.write(text)
        fp.write("\n\n\n")

def view_entries(month):
    if month != 'all':
        with open(config_location, 'r') as fp:
            data = json.load(fp)
        diary_location = data['diary_loc']
        path = Path(diary_location)
        folder_name = path / month


        file_names = [file.name for file in folder_name.iterdir() if file.is_file()]

        for i in range(len(file_names)):
            if (file_names[i]!='.DS_Store'):
                required_path = folder_name/file_names[i]
                with open(str(required_path), 'r') as f:
                    content = f.read()
                    print(content)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--setup", help='specify the source location and the name of your diary', metavar=('LOC', 'NAME'),nargs=2, )
group.add_argument("--move-diary", help='specify the source and destination location for your diary. note: source must include the diary name',metavar=('SRC', 'DES'),nargs=2)
group.add_argument("-n","--new", help='enter your diary entry', metavar=('ENTRY'), type=str)
group.add_argument("--view", choices=['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec', 'all'], help="enter either the specific month or 'all'", metavar='MONTH')
group.add_argument("--delete-entry", nargs=2, metavar=('MONTH', 'DATE=D_HHMM'))

args = parser.parse_args()
if args.setup:
    setup(args.setup[0], args.setup[1])
elif args.move_diary:
    move_diary(args.move_diary[0], args.move_diary[1])
elif args.new:
    new_entry(args.new)
elif args.view:
    view_entries(args.view)
