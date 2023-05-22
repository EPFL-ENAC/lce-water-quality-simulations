install:
	pip install colour

all: concentrations wind

concentrations:
	python concentrations.py aug20.json > concentrations_20_08.geojson
	python concentrations.py aug25.json > concentrations_25_08.geojson

wind:
	python wind.py aug20.json > wind_20_08.geojson
	python wind.py aug25.json > wind_25_08.geojson