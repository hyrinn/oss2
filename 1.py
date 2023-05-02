import geopandas as gpd
path_to_data = gpd.datasets.get_path("nybb")
gdf = gpd.read_file(path_to_data)

#print(gdf)
gdf.to_file("my_file.geojson", drive = "GeoJSON")
gdf = gdf.set_index("BoroName")
gdf["area"] = gdf.area
#print(gdf["area"])
gdf['boundary'] = gdf.boundary
#print(gdf['boundary'])
gdf['centroid'] = gdf.centroid
#print(gdf['centroid'])
first_point = gdf['centroid'].iloc[0]
gdf['distance'] = gdf['centroid'].distance(first_point)
#print(gdf['distance'])
#print(gdf['distance'].mean())
gdf.plot("area", legend = True)
input()