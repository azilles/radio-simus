from astropy.table import Table as apTable
from astropy.table import Column as apColumn
from astropy import units as apUnits
import astropy as ap
import numpy as np


################################################################################################################################
#### by M. Tueros. Shared with the Wineware licence. Support and feature requests accepted only accompanied by bottles of wine.
################################################################################################################################
#this library provides a user interface and defines HDF5 file format for the GRAND experiment
#
# file format
# ===========
# sim shower
# ==========
# showerheader: containing general shower information (zenith, azimuth, energy, xmax, xmax position and the like) (for now the meta of EventInfo for compatibility with anne)
# showersimulation: simulation details: thinning paramethers, energy cut, ground altitude, injection height, atmospheric model, hadronic model. number of observing levels, number of lateral bins
# showertables: containing longitudinal and lateral distribution tables: lateral density at ground and longitudinal:muon electron gamma hadrons
# maybe this elements could be put toghether, with one header as the meta of the longitudinal tables (say the shower header) and the other as the header of the lateral tables (simheader)

# antennalist: With antenna Ids, and antenna positions (currently "events")
# fieldsimulation: containing details on the electric field computation: index of refraction model, tmin, tmax, tbin (this would be the meta of the antenalist)

# voltagesimulation: details on the model used
# electronicsimulation: details on the models used
# external noise simulation: details on the models used
# internal noise simulation: details on the models used
# each antenna
# =============
# antennaheader: With antenna details:antennamodel, antenna position, antenna slope
# efield:trace, units are already on info
# voltage:trace
# externalnoise: trace
# internalnoise: trace
# * and maybe filtered and sample versions of all
# event
#======
# this should be things like event id, core position, info on the neutrino decay, etc (things external to the shower sim)
#========
# reco shower (to be implemented with a similar structure in the future.
#=========
# here would go reconstructed things, and should mirror the simulated structure

##showerheader
#============
#returns a "labeled list" , that will be used later as the meta of one table in the file
#for now, compatible with Anne to show functionality, contents need to be agreed upon
def CreateShowerHeader(primary, energy, zen, azim, taskname, sim="N/A", inj=100000, showerID="N/A", core=(0,0,0)):

  showerheader = {
    "ID" : showerID,              # shower ID, number of simulation (this is external to ZHAireS, its a thing of how you are identifying your sims)
    "primary" : primary,          # primary (electron, pion): This also needs standarizing. Do we use zhaires coding?
    "energy" : energy*1E18,       # eV  (GRAND units?). Should we use the astropy units framework?
    "zenith" : zen,               # deg (GRAND frame)
    "azimuth" : azim,             # deg (GRAND frame)
    "injection_height" : inj,  # m (injection height in the local coordinate system) (this is more a simulation detail, although very relevant for neutrinos)
    "task" : taskname,            # Identification to the simulation program (that dictates your file names)
    "core" : core,                # m, numpy array, core position (thisis external to the shower simulation, more related to the "event")
    "simulation" : sim      # coreas or zhaires (i could put version info)
  }

  return showerheader

# i will later make methods to GetFromHDF5. Then they might get hidden.
# This is the only section where you would need to actualize the code if you ever change the internal labels of the header
# i dont check for existance. this is left for the routine that gets the header from the file, and that might deal with units
def GetIDFromShowerHeader(showerheader):
    return showerheader["ID"]
def GetPrimaryFromShowerHeader(showerheader):
    return showerheader["primary"]
def GetEnergyFromShowerHeader(showerheader):
    return showerheader["energy"]
def GetZenithFromShowerHeader(showerheader):
    return showerheader["zenith"]
def GetAzimuthFromShowerHeader(showerheader):
    return showerheader["azimuth"]
def GetInjHeightFromShowerHeader(showerheader):
    return showerheader["injection_height"]
def GetTaskFromShowerHeader(showerheader):
    return showerheader["task"]
def GetCoreFromShowerHeader(showerheader):
    return showerheader["core"]
def GetSimulatorFromShowerHeader(showerheader):
    return showerheader["simulation"]

#this is to generate the current "event" structure as coded by Anne, for compatibility. The actual contents will change when we agree on a file structure
def GenerateEventInfo(IDs, xpositions, ypositions, zpositions,alphas,betas, showerheader): #showerheder should be eventheader
   # IDs,xpositions, ypositions and z positions are lists
   a1 = apColumn(data=IDs, name='ant_ID')
   b1 = apColumn(data=xpositions, unit=apUnits.m, name='pos_x')
   c1 = apColumn(data=ypositions, unit=apUnits.m, name='pos_y')
   d1 = apColumn(data=zpositions, unit=apUnits.m, name='pos_z')  #u.eV, u.deg
   e1 = apColumn(data=alphas, unit=apUnits.deg, name='alpha')
   f1 = apColumn(data=betas, unit=apUnits.deg, name='beta')  #u.eV, u.deg
   event_info = apTable(data=(a1,b1,c1,d1,e1,f1,), meta=showerheader)
   return event_info

def SaveEventInfo(outfilename,EventInfo): #i think the other formats should not change, but can be added in the future
   #ToDO: Handle error when "event" exists
   EventInfo.write(outfilename, path='event', format="hdf5", append=True,  compression=True, serialize_meta=True)

def GetEventInfo(inputfilename):
   #ToDo: HAndle error when "event" does not exists
   #ToDo: HAndle error when "inputfilename" is not a file, or a valid file.
   EventInfo=apTable.read(inputfilename, path="/event") #i am opening the file twice, but i dont know better
   return EventInfo

def UpdateEventInfo(outfilename,EventInfo): #this should be the method that overwrites the existing information
   print("To Do: this needs to be implemented")

def GetShowerHeaderFromEventInfo(EventInfo):
   return EventInfo.meta

def GetAntennaInfoFromEventInfo(EventInfo,nant):
   return EventInfo[nant]

def GetAntIDFromAntennaInfo(AntennaInfo):
   return AntennaInfo["ant_ID"]

def GetXFromAntennaInfo(AntennaInfo):
   return AntennaInfo["pos_x"]

def GetYFromAntennaInfo(AntennaInfo):
   return AntennaInfo["pos_y"]

def GetZFromAntennaInfo(AntennaInfo):
   return AntennaInfo["pos_z"]

#saves the "efield" astropy table to the "outputfilename" hdf5 file for the given antennaID
def SaveElectricFieldTrace(outputfilename,antennaID,efield):
   #ToDo: HAndle error when "efield" already exists
   #ToDo: HAndle error when "outputfilename" is not a file, or a valid file.
   #ToDo: Adjust format so that we have the relevant number of significant figures. Maybe float64 is not necesary?. What about using float32 or even float 16?
   efield.write(outputfilename, path=antennaID+"/efield", format="hdf5", append=True, compression=True,serialize_meta=True)

def GetElectricFieldTrace(inputfilename,antennaID):
   #ToDo: HAndle error when "efield" does not exists
   #ToDo: HAndle error when "inputfilename" is not a file, or a valid file.
   Trace=apTable.read(inputfilename, path=antennaID+"/efield")
   return Trace

def ElectricFieldTraceToNumpy(trace):
   return np.array([trace['Time'], trace['Ex'],trace['Ey'], trace['Ez']]).T


def SaveVoltageTrace(outputfilename,antennaID,voltage):
   #ToDo: HAndle error when "voltage" already exists
   #ToDo: HAndle error when "outputfilename" is not a file, or a valid file.
   #ToDo: Adjust format so that we have the relevant number of significant figures. Maybe float64 is not necesary?. What about using float32 or even float 16?
   voltage.write(outputfilename, path=antennaID+"/voltage", format="hdf5", append=True, compression=True,serialize_meta=True)

def GetVoltageTrace(inputfilename,antennaID):
   #ToDo: HAndle error when "efield" does not exists
   #ToDo: HAndle error when "inputfilename" is not a file, or a valid file.
   Trace=apTable.read(inputfilename, path=antennaID+"/voltage")
   return Trace

def GetSlopesFromTrace(Trace):
   return Trace.meta['slopes']


##WriteAzimuth
##WriteZenith
##...
#GetHeder
##GetAzimuth
##GetZenith
##...



##antennaheader
#==============
#WriteHeader
#UpdateHeder
#GetHeader
#GetNAntennas

#for each antenna:
#=================
#GetAntennaInfo()
#GetAntennaEfield() -> to np array and to ap array
#GetAntennaVoltage()
#GetAntennaNois()
#WriteAntennaInfo()
#WriteAntennaEfield()
#WriteAntennaVoltage()
#WritentennaNois()
##...



