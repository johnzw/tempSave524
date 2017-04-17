import os
#import datetime
import random
import evolution_algorithm
from configure_env import *
import evaluator

def get_info_path(target_folder_path):
    return target_folder_path + "info"

def get_target_file_path(target_folder_path, filename, index):
    return target_folder_path + filename + "_" + str(index)

def cp_op(source_file_path, target_file_path):
    return "cp " + source_file_path + " " + target_file_path

def clear_source(source_file_path):
    return 'echo "" > ' + source_file_path

def move_to_pool(source_file_path, target_folder_path, filename):
    index = 0
    with open(get_info_path(target_folder_path), "r") as fp:
        index = int(fp.readline().strip())
    with open(get_info_path(target_folder_path), "w") as fp:
        fp.write(str(index + 1))
    os.popen(cp_op(source_file_path, get_target_file_path(target_folder_path, filename, index)))
    os.popen(clear_source(source_file_path))


def get_cur_file_path(target_folder_path, filename):
    with open(get_info_path(target_folder_path), "r") as fp:
        index = int(fp.readline().strip())
    return get_target_file_path(target_folder_path, filename, index - 1)


def getDF(log_file_path):
    return 7, 7

def saveTmpData(data):
    with open(TMP_DF_PATH, "w") as fp:
        fp.write(data)

def _main(desired_difficulty, desired_fun):
    move_to_pool(LOG_FILE_PATH, PRJ_ROOT + "log_pool/", "log")
    log_file_path = get_cur_file_path(PRJ_ROOT + "log_pool/", "log")
    difficulty, fun = evaluator.getDF(log_file_path) #Bhavy group
    saveTmpData(str(difficulty) + " " + str(fun))  
    move_to_pool(TMP_DF_PATH, PRJ_ROOT + "df_pool/", "df")
    level = "placeholder"
    game_design_file = get_cur_file_path(PRJ_ROOT + "wave_pool/", "wave")
    evolution_algorithm.generate_wave(game_design_file, level, difficulty, fun, desired_difficulty, desired_fun, GAMETABLE_CSV_FILE, WAVE_FILE_PATH)
    # run filter
    # next_step_1()
    #next_step_2()
    #next_step_3()
    # ....
    # next_step_n()
    move_to_pool(WAVE_FILE_PATH, PRJ_ROOT + "wave_pool/", "wave")

if __name__ == '__main__':
    desired_difficulty=9
    desired_fun=9
    _main(desired_difficulty, desired_fun)