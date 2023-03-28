import requests
import json
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime as dt, timedelta
import argparse
from pathlib import Path

'''

DESCRIPTION

    This file downloads historical weather data from TWC API.

AUTHOR

    Fearghal O'Donncha <feardonn@ie.ibm.com>, IBM Research, Dublin, Ireland

COPYRIGHT

    International Business Machines Corporation (IBM).  All rights reserved.


Run this code as:
    python3 DownloadDataFromWeatherCompany.py start_date end_date longitude latitude

    e.g. to download data from January 1st to May 1st 2017:
    python3 DownloadDataFromWeatherCompany.py -s 20170101 -e 20170501 -lon  36.905531 -lat  -0.899210

Function:
    This code is used download historical weather data

Things to note:
    1) Details on the different data packages available here:
        https://www.datamensional.com/wp-content/uploads/2019/04/TWC-Data-Package-Summary-Feb-2019.pdf
    1) Details on the history on demand package provided here:
        https://docs.google.com/document/d/12V8zpVRh15cgP0IiuQ6n875-I04_rl2J28uE0jQcblI/edit
    3) Details on the TWC core package provided here:
        https://docs.google.com/document/d/1TPj7h6z4Gjaqjlup4rJ8B43Ge7n6iXfCF8GLw74lOeA/edit
    2) Downloaded data are placed in the './WeatherData/'folder.
    None
'''

def main_different_observables(start_date, end_date, longitude, latitude):
    date_begin = start_date # since this change inside loop
    year_string = date_begin.strftime("%Y")
    # Create WeatherData folder if doesn't exist
    Path("./WeatherData").mkdir(parents=True, exist_ok=True)
    fname_out = 'WeatherData/TWC_historical_pandas_Full_lat' + str(latitude) \
              + '_lon' + str(longitude)+ "_year" + year_string + '.csv'
    init = True # create or append to pandas data frame
    # We simply iterate over the given date period in 30 day intervals and request data
    # from API. We append to dataframe and end we write to file
    while date_begin < end_date:
        date_end = date_begin + timedelta(days=30)
        if date_end > end_date:   # check that we don't beyond user specified
            date_end = end_date
        # request data from API for given lat, lon, and particular date period
        df_return = getTWCfct_new(latitude, longitude, date_begin, date_end)
        if init:
            df_weather = df_return
            init = False
        else:
            df_weather = df_weather.append(df_return, ignore_index=False)
        date_begin = date_begin + timedelta(days=30)  # TWC allows to download historical
    df_weather.to_csv(fname_out)

'''

pointType  - Which type of point query is desired (radius, nearest, weighted)    e.g. pointType=weighted
geocode  -  Point around which the query is based. Any <lat,lng> must be -90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0
                    e.g. geocode=47.694,-117.465
distance    -  Relevant to pointType=radius query. Specifies proximity to the geocode within which data should be
                included in the result. Specified as numeric, integral value, interpreted as a kilometer (km) value.
                e.g. distance=23  [note only if radius specified
All date and time expressions in the format YYYYMMDDHHmm
'''
def getTWCfct_new(latitudes, longitudes, date_begin, date_end):
    print(date_begin, date_end)
    # Number of forecast hours to download for each point
    twc_date_begin = date_begin.strftime("%Y%m%d%H%M")
    twc_date_end = date_end.strftime("%Y%m%d%H%M")
    api_key = 'be01c34853ca4cae81c34853cabcaef1'
    # we need to convert the date_begin/end to correct string
    pointType = 'weighted'
    geocode = '{},{}'.format(latitudes, longitudes)

    url_hod = 'https://api.weather.com/v3/wx/hod/reanalysis/historical/point?pointType={}&geocode={}' \
              '&distance=50&startDateTime={}&endDateTime={}&units=m&format=json&apiKey={}'.format(
        pointType, geocode, twc_date_begin, twc_date_end, api_key)
    print(url_hod)
    r = requests.get(url_hod)
    try:
        weather = json.loads(r.text)
        json.dumps(weather, indent=1)
        df = pd.DataFrame.from_dict(weather)
        df.set_index('observationTimeUtcIso', inplace=True)
        df = df.drop_duplicates()  # some dates are duplicated
        return df
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Json decoding has failed for', twc_date_begin, twc_date_end)
        return -999, -999

def runmain():
    print(sys.path)
    #change current time to PT time
    parser = argparse.ArgumentParser(description="script to download TWC atmosphereic data.")
    parser.add_argument("-s", "--start_date", type=str, nargs="+",
                        help="specify start date, i.e: YYYY MM DD")
    parser.add_argument("-e", "--end_date", type=str, nargs="+",
                        help="specify start date, i.e: YYYY MM DD")
    parser.add_argument("-lon", "--longitude", type=float, nargs="+",
                        help="specify desired LONGITUDE location in decimal degree")
    parser.add_argument("-lat", "--latitude", type=float, nargs="+",
                        help="specify desired LATITUDE location in decimal degree")
    args = parser.parse_args()
    start_date = dt.strptime(args.start_date[0],'%Y%m%d')
    end_date = dt.strptime(args.end_date[0],'%Y%m%d')
    longitude = float(args.longitude[0])
    latitude = float(args.latitude[0])

    main_different_observables(start_date, end_date, longitude, latitude)

if __name__ == '__main__':
    runmain()
