import geopandas as gpd

def classify_earthquake(df):
    if df['magnitude'] <= 2.5:
        return 'minor'
    elif 2.5 < df['magnitude'] <= 5.4:
        return 'minimal risk'
    else:
        return 'alert'


"""
2.5 or less	Usually not felt, but can be recorded by seismograph.	Millions
2.5 to 5.4	Often felt, but only causes minor damage.	500,000
5.5 to 6.0	Slight damage to buildings and other structures.	350
6.1 to 6.9	May cause a lot of damage in very populated areas.	100
7.0 to 7.9	Major earthquake. Serious damage.	10-15
8.0 or greater	Great earthquake. Can totally destroy communities near the epicenter.	One every year or two
"""