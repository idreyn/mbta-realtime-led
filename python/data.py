class MapColors:
	RED = 0xFF0000
	GREEN = 0x00FF00
	BLUE = 0x0000FF
	ORANGE = 0xFFA500

BRIGHTNESS = 0.6
FADE_SIZE = 1

SLEEP_TIME = 0.03
PORTS = ['/dev/ttyACM0','/dev/ttyACM1']

API_ROUTE_NAMES = {
	'red_a': 'Red',
	'red_b': 'Red',
	'blue': 'Blue',
	'orange': 'Orange',
	'green_b': 'Green-B',
	'green_c': 'Green-C',
	'green_d': 'Green-D',
	'green_e': 'Green-E'
}

API_ROUTE_FILTERS = {
	'red_a': lambda t: 'ashmont' in t.name.lower(),
	'red_b': lambda t: 'braintree' in t.name.lower()
}

ROUTES = {
	'red_a': [
	'Alewife',
	'Davis',
	'Porter',
	'Harvard',
	'Central',
	'Kendall/MIT',
	'Charles/MGH',
	'Park Street',
	'Downtown Crossing',
	'South Station',
	'Broadway',
	'Andrew',
	'JFK/Umass',
	'Savin Hill',
	'Fields Corner',
	'Shawmut',
	'Ashmont'],

	'red_b': [
	'Alewife',
	'Davis',
	'Porter',
	'Harvard',
	'Central',
	'Kendall/MIT',
	'Charles/MGH',
	'Park Street',
	'Downtown Crossing',
	'South Station',
	'Broadway',
	'Andrew',
	'JFK/Umass',
	'North Quincy',
	'Wollaston',
	'Quincy Center',
	'Quincy Adams',
	'Braintree'],

	'orange': [
	'Oak Grove',
	'Malden Center',
	'Wellington',
	'Assembly',
	'Sullivan Square',
	'Community College',
	'North Station',
	'Haymarket',
	'State Street',
	'Downtown Crossing',
	'Chinatown',
	'Tufts Medical Center',
	'Back Bay',
	'Massachusetts Ave.',
	'Ruggles',
	'Roxbury Crossing',
	'Jackson Square',
	'Stony Brook',
	'Green Street',
	'Forest Hills'],

	'blue': [
	'Wonderland',
	'Revere Beach',
	'Beachmont',
	'Suffolk Downs',
	'Orient Heights',
	'Wood Island',
	'Airport',
	'Maverick',
	'Aquarium',
	'State Street',
	'Government Center',
	'Bowdoin'],

	'green_b': [
	'Lechmere',
	'Science Park',
	'North Station',
	'Haymarket',
	'Government Center',
	'Park Street',
	'Boylston',
	'Arlington',
	'Copley',
	'Hynes Convention Center',
	'Kenmore',
	'Blandford Street',
	'Boston Univ. East',
	'Boston Univ. Central',
	'Boston Univ. West',
	'Saint Paul Street',
	'Pleasant Street',
	'Babcock Street',
	'Packards Corner',
	'Harvard Ave.',
	'Griggs Street',
	'Allston Street',
	'Warren Street',
	'Washington Street',
	'Sutherland Road',
	'Chiswick Road',
	'Chestnut Hill Ave.',
	'South Street',
	'Boston College'],

	'green_c': [
	'Lechmere',
	'Science Park',
	'North Station',
	'Haymarket',
	'Government Center',
	'Park Street',
	'Boylston',
	'Arlington',
	'Copley',
	'Hynes Convention Center',
	'Kenmore',
	'Saint Mary Street',
	'Hawes Street',
	'Kent Street',
	'Saint Paul Street',
	'Coolidge Corner',
	'Summit Ave.',
	'Brandon Hall',
	'Fairbanks Street',
	'Washington Square',
	'Tappan Street',
	'Dean Road',
	'Englewood Ave.',
	'Cleveland Circle'],

	'green_d': [
	'Lechmere',
	'Science Park',
	'North Station',
	'Haymarket',
	'Government Center',
	'Park Street',
	'Boylston',
	'Arlington',
	'Copley',
	'Hynes Convention Center',
	'Kenmore',
	'Fenway',
	'Longwood',
	'Brookline Village',
	'Brookline Hills',
	'Beaconsfield',
	'Reservoir',
	'Chestnut Hill',
	'Newton Centre',
	'Newton Highlands',
	'Eliot',
	'Waban',
	'Woodland',
	'Riverside'],

	'green_e': [
	'Lechmere',
	'Science Park',
	'North Station',
	'Haymarket',
	'Government Center',
	'Park Street',
	'Boylston',
	'Arlington',
	'Copley',
	'Prudential',
	'Symphony',
	'Northeastern University',
	'Museum of Fine Arts',
	'Longwood Medical Area',
	'Brigham Circle',
	'Fenwood Road',
	'Mission Park',
	'Riverway',
	'Back of the Hill',
	'Heath Street']
}

STATION_LOCATIONS = {
	'red_a': [
		('Alewife',0),
		('Park Street',49),
		('Downtown Crossing',54),
		('JFK/Umass',81),
		('Ashmont',104)
	],
	'red_b': [
		('Alewife',0),
		('Park Street',49),
		('Downtown Crossing',54),
		('JFK/Umass',81),
		('Braintree',124)
	],
	'orange': [
		('Oak Grove',0),
		('North Station',31),
		('Haymarket',33),
		('State Street',37),
		('Downtown Crossing',44),
		('Forest Hills',85)
	],
	'blue': [
		('Wonderland',0),
		('State Street',41),
		('Government Center',42),
		('Bowdoin',48)
	],
	'green_b': [
		('Lechmere',0),
		('North Station',8),
		('Haymarket',10),
		('Government Center',13),
		('Park Street',18),
		('Copley',29),
		('Kenmore',37),
		('Boston College',78)
	],
	'green_c': [
		('Lechmere',0),
		('North Station',8),
		('Haymarket',10),
		('Government Center',13),
		('Park Street',18),
		('Copley',29),
		('Kenmore',37),
		('Saint Mary Street',45),
		('Cleveland Circle',75)
	],
	'green_d': [
		('Lechmere',0),
		('North Station',8),
		('Haymarket',10),
		('Government Center',13),
		('Park Street',18),
		('Copley',29),
		('Kenmore',37),
		('Fenway',45),
		('Riverside',113)
	],
	'green_e': [
		('Lechmere',0),
		('North Station',8),
		('Haymarket',10),
		('Government Center',13),
		('Park Street',18),
		('Copley',29),
		('Heath Street',56)
	]
}

STRIPS = {
	'greenLineD': (0,76),
	'greenLineB': (1,78),
	'greenLineCE_blueLine': (2,107),
	'orangeLine': (3,85),
	'redLine': (4,146)
}

ROUTE_COLORS = {
	'red_a': MapColors.RED,
	'red_b': MapColors.RED,
	'orange': MapColors.ORANGE,
	'blue': MapColors.BLUE,
	'green_b': MapColors.GREEN,
	'green_c': MapColors.GREEN,
	'green_d': MapColors.GREEN,
	'green_e': MapColors.GREEN
}

ROUTE_SEGMENTS = {
	'red_a': [
		('redLine',97,145,True),
		('greenLineB',60,60,False),
		('redLine',93,96,True),
		('orangeLine',41,41,False),
		('redLine',66,92,True),
		('redLine',0,22,True)
	],
	'red_b': [
		('redLine',97,145,True),
		('greenLineB',60,60,False),
		('redLine',93,96,True),
		('orangeLine',41,41,False),
		('redLine',66,92,True),
		('redLine',23,65,False)
	],
	'orange': [
		('orangeLine',48,84,True),
		('greenLineCE_blueLine',65,65,False),
		('orangeLine',0,47,True)
	],
	'blue': [
		('greenLineCE_blueLine',58,106,True)
	],
	'green_b': [
		('greenLineB',65,77,True),
		('greenLineCE_blueLine',64,64,False),
		('greenLineB',0,64,True)
	],
	'green_c': [
		('greenLineB',65,77,True),
		('greenLineCE_blueLine',64,64,False),
		('greenLineB',41,64,True),
		('greenLineD',69,75,True),
		('greenLineCE_blueLine',0,30,True)
	],
	'green_d': [
		('greenLineB',65,77,True),
		('greenLineCE_blueLine',64,64,False),
		('greenLineB',41,64,True),
		('greenLineD',0,75,True)
	],
	'green_e': [
		('greenLineB',65,77,True),
		('greenLineCE_blueLine',64,64,False),
		('greenLineB',49,64,True),
		('greenLineCE_blueLine',31,57,True)
	]
}
