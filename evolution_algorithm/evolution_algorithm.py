from wave_designer import *
# import dummy_score
import argparse
import time


def evolve_process_for_demo(path_file, level, desired_difficulty = None, desired_fun = None):
	'''
	This is just for demo
	'''
	#1 initalize the game table
	gt = GameTable()
	#2 initalize the first population
	#3 let the evaluation assess the game and get scores
	#4 insert full game entry to game table
	initial_game = Game.from_xml_string(open(path_file).read(),level, None, None)
	for num_games in range(10):
		for i in range(20):
			initial_game.mutate()
		d,f = dummy_score.evaluate(initial_game)
		initial_game.difficulty = d
		initial_game.fun = f
		gt.add_entry(initial_game)
		#for the sake of my drive, I don't do this for now
		# gt.write_to_csv("game_log.csv")
	
	#5 based on the rule engine, select games from the game table. if it fits, terminate, print the xml file
	while True:
		result = RuleEngine.select(gt, level, desired_difficulty, desired_fun)
		flag = result[0]
		if flag:
			final_game = result[1]
			"Finally generate right game"
			with open("result/final_game.xml","w") as f:
				f.write(final_game.to_xml_string())
			break
		else:
			#6 generate new game and go to step #3
			new_game = Game.simple_cross_over(result[1], result[2])
			new_game.mutate()
			#3 let the evaluation assess the game and get scores
			#4 insert full game entry to game table
			print "Generate a new game xml"
			print "Simulated AI plays the new game"
			print "Simulated Evaluator gives feedback"
			d,f = dummy_score.evaluate(new_game)
			new_game.difficulty = d
			new_game.fun = f
			print "difficulty",d,"fun",f,"\n"
			if d == desired_difficulty and f == desired_fun:
				with open("result/final_game.xml","w") as f:
					print "Finally generate a right game:"
					f.write(new_game.to_xml_string())
				break
			gt.add_entry(new_game)

def generate_wave(game_design_file, level, difficulty, fun, desired_difficulty, desired_fun, gametable_csv_file, target_wave_path):
	'''
	given game_design_file and its feedback which is difficulty and fun,
	according to EA, genearate new game, and write to File System
	'''
	if difficulty == desired_difficulty and fun == desired_fun:
		return True
	else:
		#read gametable from csv file
		flag = True
		try:
			gt = GameTable.read_csv(gametable_csv_file)
		except:
			gt = GameTable()
			flag = False
		with open(game_design_file,'r') as f:
			xml_string = f.read()
		#restore game from xml file
		new_game = Game.from_xml_string(xml_string, level, difficulty, fun)
		#add game to game table
		if flag:
			gt.add_entry(new_game)
		else:
			gt.add_entry(new_game)
			gt.add_entry(new_game)
		#get new result 
		result = RuleEngine.select(gt, level, desired_difficulty, desired_fun)
		new_game = Game.simple_cross_over(result[1], result[2])
		new_game.mutate()
		#write gametable into the csv file
		gt.write_to_csv(gametable_csv_file)
		#write the new_game to xml format
		game_xml = new_game.to_xml_string()
		with open(target_wave_path, "w") as f:
			f.write(game_xml)
		return False

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("path_file",type=str,help="file path for Path xml")
	parser.add_argument("difficulty", type=int, help="desired difficulty")
	parser.add_argument("fun", type=int, help="desired fun")
	args = parser.parse_args()

	difficulty = args.difficulty
	fun = args.fun
	path_file = args.path_file

	# evolve_process(path_file,"level1",difficulty,fun)