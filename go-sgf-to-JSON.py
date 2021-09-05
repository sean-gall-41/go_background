import os
import sys
import argparse
from sgfmill import sgf
import json

SGF_FILE_TYPE = ".sgf"
JSON_FILE_TYPE = ".json"

# search downloads folder for all SGF files and inform user
DOWNLOAD_PATH = os.environ['HOMEPATH'] + '\\Downloads'
print("Searching directory '{downloads}' for files of type '{sgf}'".format(downloads=DOWNLOAD_PATH,sgf=SGF_FILE_TYPE))
sgf_files = [file for file in os.listdir(DOWNLOAD_PATH) if \
             file.endswith(SGF_FILE_TYPE)]

# if query empty, report and exit
if not sgf_files:
    print("No files in directory '{downloads}' with extension '{sgf}'.".format(downloads=DOWNLOAD_PATH,sgf=SGF_FILE_TYPE))
    print("Exiting program")
    sys.exit()

print("Found {num_entries} files. Which one do you wish to display? (enter a number)".format(num_entries=len(sgf_files)))
user_choice = 0
while True:   
    try:
        user_choice = int(input())

        if user_choice not in range(1, len(sgf_files)+1):
            print("Must enter a value between {first} and {last}. Please try again.".format(first=1, last=len(sgf_files)))
        else:
            break
    except ValueError:
        print("Must enter an integer. Please try again.")

# parser = argparse.ArgumentParser()
# parser.add_argument("file", help="The file to be converted to JSON.")
# args = parser.parse_args()

# if not args.file.endswith(".sgf"):
#     print("file must end with '.sgf'")
#     sys.exit()

absolute_ifile_path = DOWNLOAD_PATH+'\\'+sgf_files[user_choice-1]
try:
    with open(absolute_ifile_path, "rb") as ifile:
        game = sgf.Sgf_game.from_bytes(ifile.read())

except FileNotFoundError:
    print("File could not be found.\n\nMake sure you are properly "
          "referencing the file path either with a relative or "
          "absolute path.")
    sys.exit()

else:
    # define a dict for easier converstion of data into JSON
    fields = {
        'EV': '',
        'RO': '',
        'PB': '',
        'BR': '',
        'PW': '',
        'WR': '',
        'TM': '',
        'KM': '',
        'RE': '',
        'DT': '',
        'PC': ''
    }

    # the root node of the game. I guess it is the node which contains
    # all of the info about the game except the moves
    root_node = game.get_root()
    
    # loop through keys in our fields dict and set each field to its 
    # corresponding value from the sgf file
    for field in fields.keys():
        fields[field] = root_node.get_raw(field).decode()

    moveset = []
    first_player = ''
    i = 0
    for node in game.get_main_sequence():
        move = node.get_move()
        # assuming no other node has move value of None except root
        if i == 0: 
            i += 1
            continue
        if i == 1:
            first_player = move[0]
        moveset.append(move[1])
        i += 1

    moveset = tuple(moveset)

    fields['PL'] = first_player
    # add the moves entry to our dict
    fields['MVS'] = moveset

    # create outfile name as same as in file but with .json extension
    # (if we want compatibility with linux we may have to rethink this)
    # out_file = args.file[:-4] + '.json'
    data_folder = os.getcwd() + '\{}'.format('Data')
    if data_folder:
        out_file = data_folder + '\\' + sgf_files[user_choice-1].replace(SGF_FILE_TYPE, JSON_FILE_TYPE)

    # TODO: encapsulate in try except block
    with open(out_file, "w") as ofile:
        json.dump(fields, ofile, indent=4)

    
