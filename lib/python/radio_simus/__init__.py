# -*- coding: utf-8 -*-
"""
Add a brief description

Copyright (C) 2018 The GRAND collaboration

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

# This is generated by the GRAND framework in order to track the package
# version. DO NOT DELETE.
try:
    from .version import __version__, __githash__
except ImportError:
    __version__ = None
    __githash__ = None

# Initialise the package below


### NOTE: I am not sure that I have to import all of those... _function should be private, but still ongoing work

# Export the package public functions --- NOTE not sure that this works
#from .computevoltage import compute, compute_antennaresponse, get_voltage
#from .in_out import inputfromtxt, inputfromtxt_coreas, _get_positions_coreas, load_trace, _table_efield, _table_voltage, load_trace_to_table, _load_to_array
#from .modules import  _getXmax, _dist_decay_Xmax
#from .signal_processing import add_noise, digitization, _butter_bandpass_filter, filters, run
#from .signal_treatment import p2p
#from .shower import shower, sim_shower, reco_shower, loadInfo_toShower

# Register all modules
__all__ = ["computevoltage", "in_out", "modules", "signal_treatment", "utils", "shower", "detector", "frame", "signal_processing"]


print("..... Loading CONFIG FILE .....: "+"./test.config") 
global site
global location, longitude, latitude, obs_height
global arrayfile
global thetageo, phigeo, Bcoreas, Bzhaires
global Vrms, Vrms2, tsampling
global antx, anty, antz

### set global parameters
configfile = open("/mnt/c/Users/Anne/work/radio-simus/examples/test.config", 'r') 
for line in configfile:
    line = line.rstrip() 
    if 'SITE' in line:
        site=str(line.split('  ',-1)[1])
    if 'LONG' in line:
        longitude=float(line.split('  ',-1)[1]) # deg ->astropy.units
    if 'LAT' in line:
        latitude=float(line.split('  ',-1)[1]) # deg ->astropy.units
    if 'OBSHEIGHT' in line:
        obs_height=float(line.split('  ',-1)[1]) # m ->astropy.units        
              
    if 'ARRAY' in line:
        arrayfile=str(line.split('  ',-1)[1])
        
    if 'THETAGEO' in line:
        thetageo=float(line.split('  ',-1)[1]) # deg, GRAND ->astropy.units
    if 'PHIGEO' in line:
        phigeo=float(line.split('  ',-1)[1]) # deg, GRAND ->astropy.units
    if 'B_COREAS' in line: # B_COREAS  19.71  -14.18
        Bcoreas=list(line.split('  ',-1)) # deg, deg  ->astropy.units 
    if 'B_ZHAIRES' in line: # B_COREAS  19.71  -14.18
        Bzhaires=list(line.split('  ',-1)) # deg, deg  ->astropy.units      
    
        
    if 'VRMS' in line:
        Vrms=float(line.split('  ',-1)[1]) # muV  ->astropy.units  
    if 'VRMS2' in line:
        Vrms2=float(line.split('  ',-1)[1]) # muV  ->astropy.units        
    if 'TSAMPLING' in line:
        tsampling=float(line.split('  ',-1)[1]) # ns  ->astropy.units 
        
    if 'ANTX' in line:
        antx=str(line.split('  ',-1)[1])
    if 'ANTY' in line:
        anty=str(line.split('  ',-1)[1])
    if 'ANTZ' in line:
        antz=str(line.split('  ',-1)[1])        
        
try:
    site
except NameError:
    print("Warning: site not defined")
try:
    longitude
except NameError:
    print("Warning: longitude not defined")
try:
    latitude
except NameError:
    print("Warning: latitude not defined")
try:
    obs_height
except NameError:
    print("Warning: obs_height not defined")    
    
try:
    arrayfile
except NameError:
    print("Warning: no arrayfile defined")


try:
    thetageo
except NameError:
    print("Warning: thetageo not defined")
try:
    phigeo
except NameError:
    print("Warning: phigeo not defined")
try:
    Bcoreas
except NameError:
    print("Warning: Bcoreas not defined")
try:
    Bzhaires
except NameError:
    print("Warning: Bzhaires not defined")   
    

try:
    Vrms
except NameError:
    print("Warning: Vrms not defined")   
try:
    Vrms2
except NameError:
    print("Warning: Vrms2 not defined") 
try:
    tsampling
except NameError:
    print("Warning: tsampling not defined") 
    
try:
    antx, anty, antz
except NameError:
    print("Warning: antenna response path not defined")
 

 
