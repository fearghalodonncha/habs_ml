import subprocess
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import tempfile
import math
import json
from netCDF4 import Dataset


def chla_time_to_utc(time, origin_date_seconds, multiplier_to_seconds):
    time = time*multiplier_to_seconds + float(origin_date_seconds)
    time = [datetime.utcfromtimestamp(t) for t in time]
    return time

def getcoordinates(ncdataset, lon, lat, time):
    """
    The ADCP data report coordinates in terms 
    of 'latitude', 'longitude', 'time', & 'depth'
    """
    x = ncdataset.variables[lon][:]
    y = ncdataset.variables[lat][:]
    time = ncdataset.variables[time][:]
    return x, y, time

                
                
def download_variable_from_motu(model_id, product_id, motu_url,
                                user_parameters, variable_str, out_dir, out_file, cmems_auth):
    MOTUCLIENT = 'python3 -m motuclient --motu  ' + motu_url
    OUTDIR = "/tmp/"
    call_txt = (MOTUCLIENT + ' --service-id ' + model_id + ' --product-id ' + product_id +
                                  ' --longitude-min '+ str(user_parameters['lon_min']) + 
                                  ' --longitude-max ' +  str(user_parameters['lon_max']) +
                                  ' --latitude-min ' + str(user_parameters['lat_min']) +
                                  ' --latitude-max ' + str(user_parameters['lat_max']) + 
                                  ' -t ' + user_parameters['from_date'] + ' -T ' + user_parameters['to_date'] + 
                                  ' --depth-min ' + user_parameters['depth_min'] + ' --depth-max ' + 
                                    user_parameters['depth_max'] + variable_str +
                                  ' --out-dir ' + out_dir + ' --out-name ' +  out_file +
                                  ' --user '  + cmems_auth[0] +  ' --pwd '  + cmems_auth[1])
    call = subprocess.getoutput(call_txt) 
    if 'error' in call.lower():
        print(call)
    return call, call_txt


