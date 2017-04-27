import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from wave_designer import Wave, Monster, Game


def read_from_file(xml_file_path):
	with open(xml_file_path, "r") as f:
		xml_string = f.read()
	g = Game.from_xml_string(xml_string, "level1", None, None)
	return g

def calculate_monster_score(monster):
	#simplest one
	return monster.amount * 1

def highest_score():
	return 8

def evaluate(game_file):
	game = read_from_file(game_file)
	score = 0
	high_score = 0
	for wave in game.waves:
		for monster in wave.monsters:
			score += calculate_monster_score(monster)
			high_score += highest_score()

	difficulty = round(score * 10.0/ high_score, 1)
	fun = difficulty
	return difficulty, fun

def test():
	xml_file_path = "Level1.xml"
	game = read_from_file(xml_file_path)
	difficulty, fun = evaluate(game)
	print difficulty, fun

if __name__ == '__main__':
	test()