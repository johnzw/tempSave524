import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from wave_designer import Wave, Monster, Game


def evaluate(log_file):
	with open(log_file,"r") as f:
		data = f.read().strip().split(" ")
		feature = [float(entry) for entry in data]
	coeff = [1, 2, 3]
	score = 0
	for c, f in zip(coeff, feature):
		score += c * f
	difficulty = score
	fun = score

	return difficulty, fun

def test():
	xml_file_path = "log"
	difficulty, fun = evaluate(xml_file_path)
	print difficulty, fun

if __name__ == '__main__':
	test()