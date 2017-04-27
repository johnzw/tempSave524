import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from wave_designer import Wave, Monster, Game
import random

def read_from_file(xml_file_path):
	with open(xml_file_path, "r") as f:
		xml_string = f.read()
	g = Game.from_xml_string(xml_string, "level1", None, None)
	return g

def game_random_generation(original_game_file, number = 20):
	for i in range(number):
		game = read_from_file(original_game_file)
		game = game_mutate(game)
		xml_string= game.to_xml_string()
		with open("sample_wave/wave_"+str(i),"w") as f:
			print "DONE ",i
			f.write(xml_string)

def game_mutate(game):
	for r in range(100):
		game.mutate()
	money_options = range(400,2000,100)
	game.initial_money = random.choice(money_options)
	return game

def game_specific_generation(original_game_file, mounter_num, wave_index):
	game = read_from_file(original_game_file)
	for wave in game.waves:
		for monster in wave.monsters:
			monster.amount = mounter_num
	xml_string= game.to_xml_string()
	with open("sample_wave/wave_"+str(wave_index),"w") as f:
		print "DONE ",wave_index
		f.write(xml_string)

def test1():
	xml_file_path = "wave_0"
	game_random_generation(xml_file_path)

def test2():
	xml_file_path = "wave_0"
	game_specific_generation(xml_file_path, 8, 1)

if __name__ == '__main__':
	test2()