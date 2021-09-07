import os
import sys
from sgfmill import sgf
import json

SGF_FILE_TYPE = ".sgf"
JSON_FILE_TYPE = ".json"

# search the data folder for .sgf file, exit if none
#TODO: python process runs from the base Processing folder: need to get to the
# folder that the processing sketch is located in
DATA_PATH = 'C:\\Users\\Parma_Shon\\Documents\\Processing\\sketches\\go_background\\data'
print("Searching directory '{data}' for files of type '{sgf}'".format(data=DATA_PATH,sgf=SGF_FILE_TYPE))
sgf_files = [file for file in os.listdir(DATA_PATH) if \
             file.endswith(SGF_FILE_TYPE)]

# if query empty, report and exit
if not sgf_files:
    print("No files in directory '{downloads}' with extension '{sgf}'.".format(downloads=DATA_PATH,sgf=SGF_FILE_TYPE))
    print("Exiting program")
    sys.exit(1)

print("Found {num_entries} files. Taking first one".format(num_entries=len(sgf_files)))

# we're just going to take the first entry found assuming it exists
absolute_ifile_path = DATA_PATH+'\\'+sgf_files[0]

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
    # data_folder = os.getcwd() + '\{}'.format('data')
    # if data_folder:
    out_file = DATA_PATH + '\\' + sgf_files[0].replace(SGF_FILE_TYPE, JSON_FILE_TYPE)

    # TODO: encapsulate in try except block
    with open(out_file, "w") as ofile:
        json.dump(fields, ofile, indent=4)
    
    print("finished dumping contents into json file.")
    print("\nProgram Complete. Exiting...")

    
