
import random
middle = ["A","S","D","F","G","H","J","K","L"]
outliers = ["Q","W","E","R","T","Y","U","I","O","P","Z","X","C","V","B","N","M"]





while True:
	String = ""
	NUM = 2000
	for x in range(NUM):
		if random.choice(range(6)) == 1:
			String+=random.choice(outliers)
		else:
			String+=random.choice(middle)

	input(String)