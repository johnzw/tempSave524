import os
#import datetime
import random


PRJ_ROOT = "/Users/Franz/Documents/524LoopControl/LoopControl/"


LOG_FILE_PATH = "/Users/Franz/Library/Logs/Unity/Editor.log"
WAVE_FILE_PATH = "/Users/Franz/Downloads/new_wave"





def get_info_path(target_folder_path):
    return target_folder_path + "info"

def get_target_file_path(target_folder_path, filename, index):
    return target_folder_path + filename + "_" + str(index)


def cp_op(source_file_path, target_file_path):
    return "cp " + source_file_path + " " + target_file_path

def clear_source():
    return 'echo "" > ' + source_file_path


def move_to_pool(source_file_path, target_folder_path, filename):
    index = 0
    with open(get_info_path(), "r") as fp:
        index = int(fp.readline().strip())
    with open(get_info_path(), "w") as fp:
        fp.write(str(index + 1))
    os.popen(cp_op(source_file_path, get_target_file_path(target_folder_path, filename, index)))
    os.popen(clear_source(source_file_path))


def next_step_1():
    with open(get_info_path(), "w") as fp:
        fp.write(str(random.random()))
   


def _main():
    
    move_to_pool(LOG_FILE_PATH, PRJ_ROOT + "log_pool/", "log")
    
    
    # run filter
    next_step_1()
    #next_step_2()
    #next_step_3()
    # ....
    # next_step_n()

    move_to_pool(WAVE_FILE_PATH, PRJ_ROOT + "wave_pool/", "wave")

_main()