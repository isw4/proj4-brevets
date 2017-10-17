"""
Test suite for the acp_times 
"""

import acp_times, arrow
from acp_times import convert_hrs_mins, find_time_using, open_time, close_time

# Testing convert_hrs_mins
def test_convert_00_00():
	time = 0
	hrs, mins = convert_hrs_mins(time)
	assert int(hrs) == 0
	assert int(mins) == 0

def test_convert_05_20():
	time = 5.45
	hrs, mins = convert_hrs_mins(time)
	assert int(hrs) == 5
	assert int(mins) == 27


# Testing find_time_using(MAXSPD, distance)
def test_find_time_max_100():
	time = find_time_using(acp_times.MAXSPD, 100)
	assert time - 2.93 < 0.02	#margin: +-1.2 minutes

def test_find_time_max_300():
	time = find_time_using(acp_times.MAXSPD, 300)
	assert time - 9.00 < 0.02

def test_find_time_max_500():
	time = find_time_using(acp_times.MAXSPD, 500)
	assert time - 15.47 < 0.02

def test_find_time_max_900():
	time = find_time_using(acp_times.MAXSPD, 900)
	assert time - 29.52 < 0.02


# Testing find_time_using(MINSPD, distance)
def test_find_time_min_100():
	time = find_time_using(acp_times.MINSPD, 100)
	assert time - 6.67 < 0.02	#margin: +-1.2 minutes

def test_find_time_min_300():
	time = find_time_using(acp_times.MINSPD, 300)
	assert time - 20.00 < 0.02

def test_find_time_min_500():
	time = find_time_using(acp_times.MINSPD, 500)
	assert time - 33.33 < 0.02

def test_find_time_min_900():
	time = find_time_using(acp_times.MINSPD, 900)
	assert time - 66.25 < 0.02


# Testing open_time
def test_open_neg():
	try:
		open_time(-1, 600, arrow.utcnow().isoformat())
		assert False
	except ValueError:
		pass

def test_open_1001():
	try:
		open_time(1001, 600, arrow.utcnow().isoformat())
		assert False
	except ValueError:
		pass

def test_open_0():
	here = arrow.utcnow().isoformat()
	assert here == open_time(0, 600, here)

def test_open_1000():
	here = arrow.utcnow()
	there = here.shift(hours=+33)
	there = there.shift(minutes=+5)
	assert there.isoformat() == open_time(1000, 1000, here)


# Testing close_time
def test_close_neg():
	try:
		close_time(-1, 600, arrow.utcnow().isoformat())
		assert False
	except ValueError:
		pass

def test_close_1001():
	try:
		close_time(1001, 600, arrow.utcnow().isoformat())
		assert False
	except ValueError:
		pass

def test_close_0():
	here = arrow.utcnow()
	there = here.shift(hours=+1)
	assert there.isoformat() == close_time(0, 600, here)

def test_close_1000():
	here = arrow.utcnow()
	there = here.shift(hours=+75)
	there = there.shift(minutes=+0)
	assert there.isoformat() == close_time(1000, 1000, here)
