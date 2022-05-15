import pandas
import geopandas

def csv_to_shp(csv_file):
    df = pandas.read_csv(csv_file, encoding='utf-8')
    gdf = geopandas.GeoDataFrame(
        df, geometry = geopandas.points_from_xy(df.poi_lon, df.poi_lat),crs= 'EPSG:4326'
    )
    
    print(gdf.head())

    # to shp
    gdf.to_file('bj_hs_pois.shp', encoding = 'utf-8')
    # to geojson
    gdf.to_file('bj_hs_pois.geojson', driver='GeoJSON')

if __name__ == "__main__":
    csv_file = './bj_hs_pois_utf8.csv'
    csv_to_shp(csv_file)