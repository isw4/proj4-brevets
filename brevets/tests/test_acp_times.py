"""
Test suite for the acp_times 
"""

import acp_times, arrow
from acp_times import check_control_distance, convert_hrs_mins, find_time_using, open_time, close_time

### Testing convert_hrs_mins
	# Boundary case
def test_convert_00_00():
	time = 0
	hrs, mins = convert_hrs_mins(time)
	assert int(hrs) == 0
	assert int(mins) == 0

	# Normal case
def test_convert_05_20():
	time = 5.45
	hrs, mins = convert_hrs_mins(time)
	assert int(hrs) == 5
	assert int(mins) == 27


### Testing controle distance check
	# Negative value
def test_control_check_too_low():
	try: 
		check_control_distance(-1, 600)
		assert False
	except ValueError:
		pass

	# Value > 1.1*brevet_dist
def test_control_check_too_high():
	try: 
		check_control_distance(661, 600)
		assert False
	except ValueError:
		pass

### Testing find_time_using(MAXSPD, controle_dist, brevet_dist), normal and boundary cases
def test_find_time_max_1():
	time = find_time_using(acp_times.MAXSPD, 1, 1000)
	assert time - 0.03 < 0.02	#margin: +-1.2 minutes for rounding errors

def test_find_time_max_200():
	time = find_time_using(acp_times.MAXSPD, 200, 1000)
	assert time - 5.88 < 0.02

def test_find_time_max_250():
	time = find_time_using(acp_times.MAXSPD, 250, 1000)
	assert time - 7.45 < 0.02

def test_find_time_max_400():
	time = find_time_using(acp_times.MAXSPD, 400 ,1000)
	assert time - 12.13 < 0.02

def test_find_time_max_450():
	time = find_time_using(acp_times.MAXSPD, 450, 1000)
	assert time - 13.80 < 0.02

def test_find_time_max_600():
	time = find_time_using(acp_times.MAXSPD, 600, 1000)
	assert time - 18.80 < 0.02

def test_find_time_max_650():
	time = find_time_using(acp_times.MAXSPD, 650, 1000)
	assert time - 20.58 < 0.02

def test_find_time_max_1000():
	time = find_time_using(acp_times.MAXSPD, 1000, 1000)
	assert time - 33.08 < 0.02

	# Special case: controle beyond the brevet time
def test_find_time_max_1050():
	time = find_time_using(acp_times.MAXSPD, 1050, 1000)
	assert time - 33.08 < 0.02


### Testing find_time_using(MINSPD, controle_dist, brevet_dist), normal and boundary cases
def test_find_time_min_1():
	time = find_time_using(acp_times.MINSPD, 1, 1000)
	assert time - 0.07 < 0.02	#margin: +-1.2 minutes

def test_find_time_min_200():
	time = find_time_using(acp_times.MINSPD, 200, 1000)
	assert time - 13.33 < 0.02

def test_find_time_min_250():
	time = find_time_using(acp_times.MINSPD, 250, 1000)
	assert time - 16.67 < 0.02

def test_find_time_min_400():
	time = find_time_using(acp_times.MINSPD, 400 ,1000)
	assert time - 26.67 < 0.02

def test_find_time_min_450():
	time = find_time_using(acp_times.MINSPD, 450, 1000)
	assert time - 30.00 < 0.02

def test_find_time_min_600():
	time = find_time_using(acp_times.MINSPD, 600, 1000)
	assert time - 40.00 < 0.02

def test_find_time_min_650():
	time = find_time_using(acp_times.MINSPD, 650, 1000)
	assert time - 44.38 < 0.02

def test_find_time_min_1000():
	time = find_time_using(acp_times.MINSPD, 1000, 1000)
	assert time - 75.00 < 0.02

	# Special case: controle beyond the brevet time
def test_find_time_min_1050():
	time = find_time_using(acp_times.MINSPD, 1050, 1000)
	assert time - 75.00 < 0.02


### Testing shifting start time
def shift_by_0():
	here = arrow.utcnow()
	assert here.isoformat() == shift_start_by(here.isoformat(), 0)

def shift_by_some():
	here = arrow.utcnow()
	there = here.shift(hours=+1)
	there = there.shift(minutes=+27)
	assert there.isoformat() == shift_start_by(here.isoformat(), 1.45)


### Testing open_time for special case of controle_dist = 0
def test_open_0(): 
	here = arrow.utcnow().isoformat()
	assert here == open_time(0, 600, here)


# Testing close_time for special case of controle_dist = 0 and
# brevet ending times
def test_close_0():
	here = arrow.utcnow()
	there = here.shift(hours=+1)
	print(here.isoformat())
	print(close_time(0, 600, here))
	assert there.isoformat() == close_time(0, 600, here)

def test_close_200():
	here = arrow.utcnow()
	there = here.shift(hours=+13)
	there = there.shift(minutes=+30)
	assert there.isoformat() == close_time(200, 200, here)

def test_close_210():
	here = arrow.utcnow()
	there = here.shift(hours=+13)
	there = there.shift(minutes=+30)
	assert there.isoformat() == close_time(210, 200, here)

def test_close_1000():
	here = arrow.utcnow()
	there = here.shift(hours=+75)
	assert there.isoformat() == close_time(1000, 1000, here)

def test_close_1050():
	here = arrow.utcnow()
	there = here.shift(hours=+75)
	assert there.isoformat() == close_time(1050, 1000, here)