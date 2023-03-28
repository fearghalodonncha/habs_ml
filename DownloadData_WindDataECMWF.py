import cdsapi
import argparse
import sys
import plotly.graph_objects as go

'''
Purpose of this script is to download pertinent 
weather data for the Sagres HAB study. Essentially
need wind data (don't think anything further influence
algal bloom development)
Based on the above, can do an area encompassing
'''

c = cdsapi.Client()
#Based on the above, can do an area encompassing

lat_beg = 36.5
lon_beg = -11
lat_end = 38.5
lon_end = -8.3


## Let's have a look at what we're plotting
plot = False
if plot:
    fig = go.Figure(go.Scattergeo(lat=[lat_beg,lat_end,lat_end,lat_beg, lat_beg ],
                                                                          lon=[lon_beg,lon_beg, lon_end, lon_end, lon_beg ], fill="toself"))
    fig.update_layout(
            title = 'Domain extent',
            geo = dict(
                scope='europe',
                projection_type="natural earth",
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                countrywidth = 0.5,
                subunitwidth = 0.5
            ),
        )
    fig.show()

years = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']
fname = './weather_data/ECMWF_WEATHER_windspeed.nc'


def download_ecmwf_data():
    r = c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind',
        ],
            'product_type': 'reanalysis',
            'year': years,
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12'
            ],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31'
            ],
            'area': [lat_end, lon_beg, lat_beg, lon_end],  # North, West, South, East. Default: global
            'time': [
                '00:00', '03:00', '06:00',
                '09:00', '12:00', '15:00',
                '18:00', '21:00'
                ],
            'format': 'netcdf'  # Supported format: grib and netcdf. Default: grib
        }, fname)

if __name__ == "__main__":
    #download_ecmwf_data(year_begin, year_end, lat_beg, lon_beg, lat_end, lon_end )
    download_ecmwf_data()