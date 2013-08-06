import pytz, datetime, time
from pytz import timezone
from decimal import Decimal

# SPSS uses a timestamp based on the year 1582. Makes sense, right?
# We can convert this into a POSIX timestamp by applying a delta defined here...
utc = pytz.utc
central_tz = timezone('US/Central')
gregorian_diff = (datetime.datetime(1970,1,1) - datetime.datetime(1582,10,14)).total_seconds()
year_2100 = time.mktime(datetime.datetime(2100,1,1).timetuple())
def spss_to_posix(spss_timestamp):
	if (spss_timestamp > year_2100):
		return datetime.datetime.fromtimestamp(Decimal(spss_timestamp)-Decimal(gregorian_diff)).replace(tzinfo=utc).astimezone(central_tz) 
	else:
		return spss_timestamp

# Converts a string in the form '08' and returns a 4-digit integer year e.g. 2008
this_year = datetime.datetime.now().year
def yy_to_yyyy(yy):
	yy_num = int(yy)
	if (this_year-2000 >= yy_num):
		return 2000 + yy_num
	else:
		return 1900 + yy_num 
