from configure_env import *
import os


for sub_dir in os.listdir(PRJ_ROOT):
	if sub_dir.endswith("pool"):
		dir_path = os.path.join(PRJ_ROOT, sub_dir)
		#delete all the other things
		for file_name in os.listdir(dir_path):
			if not file_name.endswith("_0"):
				os.remove(os.path.join(dir_path, file_name))
		#add info file
		info_path = os.path.join(dir_path, "info")
		with open(info_path,'w') as f:
			f.write("1")

if os.path.exists(GAMETABLE_CSV_FILE):
	os.remove(GAMETABLE_CSV_FILE)
	
if os.path.exists(RESULT_PATH):
	os.remove(RESULT_PATH)