import time,os
os.system("color")

# Define all the time increments
seconds = 0
minutes = 0
hours = 0
days = 0
weeks = 0
months = 0
years = 0
decades = 0
centuries = 0
milenia = 0

# The main function
def increase_num_if_big(smallerNum, biggerNum, increaseThreshold):
	if smallerNum >= increaseThreshold:
		smallerNum = 0
		biggerNum += 1

	return (smallerNum, biggerNum)

def pretty_print(num):
	if num <= 9:
		num = f"0{num}"
	return num

try:
	# The main loop
	for x in range(10000):
		seconds, minutes = increase_num_if_big(seconds, minutes, 60)
		minutes, hours = increase_num_if_big(minutes, hours, 60)
		hours, days = increase_num_if_big(hours, days, 24)
		days, weeks = increase_num_if_big(days, weeks, 7)
		weeks, months = increase_num_if_big(weeks, months, 30)
		months, years = increase_num_if_big(months, years, 12)
		years, decades = increase_num_if_big(years, decades, 10)
		decades, centuries = increase_num_if_big(decades, centuries, 10)
		centuries, milenia = increase_num_if_big(centuries, milenia, 10)

		seconds += 1
		time.sleep(1)

		print(f"\033[2J{pretty_print(centuries)}:{pretty_print(decades)}:{pretty_print(years)}:{pretty_print(months)}:{pretty_print(weeks)}:{pretty_print(days)}:{pretty_print(hours)}:{pretty_print(minutes)}:{pretty_print(seconds)}")
except KeyboardInterrupt:
	input("Cancelled")