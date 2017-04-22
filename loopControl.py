import os
import re
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



def write_to_pool(stream, name):
    target_folder_path = POOLS_ROOT + name + "_pool/"
    with open(get_info_path(target_folder_path), "r") as fp:
        index = int(fp.readline().strip())
    with open(get_info_path(target_folder_path), "w") as fp:
        fp.write(str(index + 1))
    with open(get_target_file_path(target_folder_path, name, index), "a") as fp:
        fp.write(stream)

def getDF(log_file_path):
    return 7, 7

def saveTmpData(data):
    with open(TMP_DF_PATH, "w") as fp:
        fp.write(data)


def get_filtered_log():
    with open(LOG_FILE_PATH, "rb") as fp:
        stream = fp.read()
    #std_stream = stream.replace('\x00', '')
    logs = re.findall('{\s+"Type": ".+".+},', stream)
    joined_logs = '\n'.join(logs)
    return '['+joined_logs[:-1]+']'


def _main(desired_difficulty, desired_fun):
    write_to_pool(get_filtered_log(), "log")
    os.popen(clear_source(LOG_FILE_PATH))
    #move_to_pool(LOG_FILE_PATH, POOLS_ROOT + "log_pool/", "log")
    log_file_path = get_cur_file_path(POOLS_ROOT + "log_pool/", "log")
    difficulty, fun = evaluator.evaluate(log_file_path) #Bhavy group
    print difficulty, fun
    saveTmpData(str(difficulty) + " " + str(fun))  
    move_to_pool(TMP_DF_PATH, POOLS_ROOT + "df_pool/", "df")
    level = "placeholder"
    game_design_file = get_cur_file_path(POOLS_ROOT + "wave_pool/", "wave")
    evolution_algorithm.generate_wave(game_design_file, level, difficulty, fun, desired_difficulty, desired_fun, GAMETABLE_CSV_FILE, WAVE_FILE_PATH)
    move_to_pool(WAVE_FILE_PATH, POOLS_ROOT + "wave_pool/", "wave")




if __name__ == '__main__':
    desired_difficulty=9
    desired_fun=9
    _main(desired_difficulty, desired_fun)

