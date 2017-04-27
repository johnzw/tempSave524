# -*- coding: utf-8 -*-
#Authors : Wen, Nandan, Venky 
#Date : Mar 1,2017

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import random
import pandas as pd
import numpy as np

class Wave:
	"""
	simple class for Wave
	"""
	def __init__(self):
		self.monsters = list()

	def add_monster(self, monster):
		self.monsters.append(monster)

	def clear(self):
		self.monsters = list()

	def generate_EA_string(self):
		"""
		based on monsters of the attacking wave,
		return corrosponding string for Evolutionary Algorithm
		"""
		#TODO
		pass

class Monster:
	"""
	simple class for Monster
	"""
	def __init__(self, ID, amount, seconds):
		"""
		id: monster ID, type: str
		amount: monster Amount, type:int
		seconds: monser Seconds, type:int
		"""
		self.id = ID
		self.amount = amount
		self.seconds = seconds
		

class Game:
	def __init__(self, waves, level, initial_money, difficulty, fun, xml_root): 

		'''
		waves: [], list of wave object
		level: str, the name of level of the game
		initial_money: int
		difficulty: int, need to hear back from evalution
		fun: int, need to hear back from evalution
		xml_root: obj, xml_root of the game

		'''
		self.waves = waves
		self.level = level
		self.initial_money = initial_money 
		self.difficulty = difficulty
		self.fun = fun
		self.xml_root = xml_root
	

	@staticmethod
	def simple_cross_over(game1, game2):
		'''
		static method:
		given game1 and game2, 
		do crossover,
		return a 3rd game
		'''
		if game1.level != game2.level:
			raise Exception("game level not compatible")
		#pivot point between 1 to len(self.waves)-1
		pivot = random.randint(1, len(game1.waves)-1)
		#combine two wave
		new_wave = game1.waves[:pivot] + game2.waves[pivot:]
		new_money = (game1.initial_money + game2.initial_money) / 2

		return Game(new_wave,game1.level,new_money, None, None, game1.xml_root)

	@staticmethod
	def advanced_cross_over(game1, game2):
		'''
		static method:
		given game1 and game2, 
		do crossover,
		return a 3rd game
		'''
		if game1.level != game2.level:
			raise Exception("game level not compatible")
		game1_monsters = [monster for wave in game1.waves for monster in wave.monsters]
		game2_monsters = [monster for wave in game2.waves for monster in wave.monsters]
		#set the pivot point
		pivot = random.randint(1, len(game1_monsters)-1)
		print pivot
		new_game_monsters = game1_monsters[:pivot] + game2_monsters[pivot:]
		num_waves = len(game1.waves)
		monster_for_each_wave = len(new_game_monsters) / num_waves

		new_wave = list()
		for i in range(num_waves):
			w = Wave()
			for j in range(monster_for_each_wave):
				w.monsters.append(new_game_monsters[i*monster_for_each_wave+j])
			new_wave.append(w)

		new_money = (game1.initial_money + game2.initial_money) / 2
		return Game(new_wave,game1.level,new_money, None, None, game1.xml_root)

	@staticmethod
	def monster_mutation(monster):
		'''
		sepecific mutation rule for one monster
		'''
		monster.id = str(random.randint(1,4))
		monster.amount = random.randint(1,10)
		monster.seconds = random.randint(1,10)

	def mutate(self, money_flag = False):
		'''
		random monster at random wave mutate
		'''
		#random wave
		random_wave = random.choice(self.waves)
		#random monster
		random_monster = random.choice(random_wave.monsters)
		#mutation on monster
		Game.monster_mutation(random_monster)
		#money mutation
		if money_flag:
			mutation_range = int(self.initial_money * 0.1)
			self.initial_money = self.initial_money + random.randint(-1*mutation_range, mutation_range)
		
	@classmethod
	def from_xml_string(cls, xml_string, level, difficulty=None, fun=None):
		'''
		factory method: 
		given xml string and other information, 
		return game object
		'''
		#read from xml
		root = ET.fromstring(xml_string)

		#What we only care is the wave
		waves = list()
		#from the wave in xml to wave in self-defined class
		for wave in root.iter('Wave'):
			wave_new = Wave()
			for monster in wave:
				ID = monster.find("ID").text
				amount = int(monster.find("Amount").text)
				seconds = int(monster.find("Seconds").text)
				wave_new.add_monster(Monster(ID, amount, seconds))
			waves.append(wave_new)

		#remove the original waves
		# xml_waves = root.find('Waves')
		# for wave in list(xml_waves):
		# 	xml_waves.remove(wave)

		initial_money = int(root.find("Money").text)
		return cls(waves, level, initial_money, difficulty, fun, root)
	
	def to_xml_string(self):
		"""
		return xml string
		"""
		#remove the original waves
		xml_waves = self.xml_root.find('Waves')
		for wave in list(xml_waves):
			xml_waves.remove(wave)

		#build new wave
		#right now it only has one wave
		waves = self.xml_root.find('Waves')
		for wave in self.waves:	
			wave_xml = ET.SubElement(waves, 'Wave')
			for monster in wave.monsters:
				#build monster element
				monster_element = ET.SubElement(wave_xml, 'Monster')
				seconds = ET.SubElement(monster_element, 'Seconds')
				seconds.text = str(monster.seconds)
				amount = ET.SubElement(monster_element, 'Amount')
				amount.text = str(monster.amount)
				ID = ET.SubElement(monster_element, 'ID')
				ID.text = str(monster.id)
		#set the money
		money = self.xml_root.find("Money")
		money.text = str(self.initial_money)
		# xmlstr = ET.tostring(self.xml_root)
		# #to nicer xml format
		xmlstr = parseString(ET.tostring(self.xml_root)).toprettyxml(indent="\t").encode('utf-8')
		return xmlstr


#csv file : xml, level, difficult, fun 	
class GameTable:
	'''
	default dataframe is the empty dataframe with specified columns
	'''
	def __init__(self,dataframe=pd.DataFrame(columns=["game","level","difficulty","fun"])):
	 	self.df = dataframe

	@classmethod
	def read_csv(cls, csv_file_path):
		'''
		factory method:
		given the csv_file_path,
		return gameTable object
		'''
		return cls(pd.read_csv(csv_file_path))

	def add_entry(self, game):
		data_entry = pd.Series([game.to_xml_string(),game.level,game.difficulty,game.fun],index=["game","level","difficulty","fun"])
		self.df = self.df.append(data_entry, ignore_index=True)

	def write_to_csv(self, csv_file_path):
		self.df.to_csv(csv_file_path,index=False)


class RuleEngine:
# we have two factors : difficulty and fun
# Fun takes priority since user engagement takes top priority. 
# Scale of Fun : 0-9 
# Sclae of Difficulty : 0-9 
# if fun > FunThreshold 
# 		select all games which is of difficulty + 1 and same fun level  
#			if found select the indexes and send back. 
#			else 
#				select games with any fun level and send the indexes. 
#	else
#		select all games which is of fun + 1 and same diffuculty level  
# 			if found select the indexes and send back. 
#			else 
#				select games with any difficulty level and send the indexes. 
	@staticmethod
	def select(game_table, level, desired_difficulty, desired_fun):
		'''
		given game table, level tag, desired difficulty, desired fun
		return (flag, Game object1, Game object2)
		more explanation on flag:
		flag:None --> there is no game that match desired difficulty and desired fun
			 1 or 2 --> the index of game object that gives desired difficulty and desired fun

		Warning:
			right now it only deal with difficulty, that is, only evolve to the desired difficulty
			But since Evaluator team treats difficulty and fun as the same thing, this does not matter at the moment
		'''
		#sort the table according to the desired_difficulty
		diff = game_table.df.difficulty.apply(lambda z:abs(z-desired_difficulty))
		diff.sort()
		game_table.df = game_table.df.set_index(diff.index).sort()[:300]

		# game_index1, game_index2 = np.random.choice(5, 2, replace=False, p=[0.45,0.4,0.05,0.05,0.05])
		game_index1, game_index2 = 0,1
		flag = None
		game1 = game_table.df.iloc[game_index1]
		game2 = game_table.df.iloc[game_index2]
		if game1.difficulty == desired_difficulty:
			flag = 1
		elif game2.difficulty == desired_difficulty:
			flag = 2
		return flag, Game.from_xml_string(game1.game,level), Game.from_xml_string(game2.game,level)



	def Interesting_Games(fun,diff):
		'''
		this method not used yet
		'''
		if fun > Fun_thresh:
			CollectIndexesFromTables(fun,diff+1)
		else :
			CollectIndexesFromTables(fun+1,diff)
	
	def getMoney(fun,diff,initial_money,compatable_game_initial_money):
		'''
		this method not used yet
		'''
		return_val=20		
		if fun > Fun_thresh:
			if diff >= Diff_second_thresh:
				return 0
			if diff >= Diff_thresh and diff < Diff_second_thresh:
				return -return_val 			
			return return_val

def test():
	#test xml parsing
	xml_string = open("Level1.xml").read()
	game = Game.from_xml_string(xml_string, "level1", None, None)
	game.initial_money = 90
	xml_string =  game.to_xml_string()
	# print xml_string
	game = Game.from_xml_string(xml_string, "level1", None, None)
	game.initial_money = 80
	xml_string =  game.to_xml_string()
	# print xml_string

	#test crossover
	game1 = Game.from_xml_string(open("Level1.xml").read(),"level1", None, None)
	game2 = Game.from_xml_string(open("Level1_new.xml").read(),"level1", None, None)
	game3 = Game.simple_cross_over(game1, game2)
	game4 = Game.simple_cross_over(game2, game1)
	# print game3.to_xml_string()
	with open("old.xml","w") as f:
		f.write(game3.to_xml_string())
	# print game4.to_xml_string()
	game3.mutate()
	# print game3.to_xml_string()
	with open("new.xml","w") as f:
		f.write(game3.to_xml_string())


	#1 initalize the game table
	#2 initalize the first population
	#3 let the evaluation assess the game and get scores
	#4 insert full game entry to game table
	#5 based on the rule engine, select games from the game table. if it fits, teerminate, print the xml file
	#6 generate new game and go to step #3
if __name__ == '__main__':
	test()

