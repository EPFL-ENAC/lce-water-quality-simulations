# File organisation

The files looks like this


```
├── Concentration_noro820.nc // raw data netCDF for the 20th of august
├── Concentration_noro825.nc // raw data netCDF for the 25th of august
├── Notes.txt // explanation of the fields of the netCDF
├── Shoreline.txt  // data used by the researcher to intersect the heat map (shoreline of the lake)
├── aug20.json // json version of the netCDF files
├── aug25.json // json version of the netCDF files
├── concentrations_20_08.geojson // geojson transformed needed to create the tiles
├── concentrations_25_08.geojson // geojson transformed need to create the tiles
├── tiles
│   ├── concentrations_20_08_tiles
│   ├── concentrations_25_08_tiles
│   └── wind_tiles // test, not ready yet
├── wind_20_08.geojson // geojson to use to create wind tiles
└── wind_25_08.geojson // geojson to use to create wind tiles

```
