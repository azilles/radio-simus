import os
import sys
import logging

root_dir = os.path.realpath(os.path.join(os.path.split(__file__)[0], "../")) # = $PROJECT
sys.path.append(os.path.join(root_dir, "lib", "python"))
from radio_simus.in_out import _table_voltage
from radio_simus.computevoltage import compute_antennaresponse
import radio_simus.hdf5fileinout as hdf5io

logging.basicConfig(level=logging.DEBUG)

#if no outfilename is given, it will store the table in the same HDF5 dile, in a separate table (handle what happens if it already exists)

#this computes the voltage on all the antennas, but if this gets too CPU intense in some application we might want to apply some filter,
#that could go in the funnction call like...such as only compute if the peak to peak amplitude is higher than something, or the distance to the core is less than something.

def ComputeVoltageOnHDF5(inputfilename,outfilename="N/A"):

  if os.path.isfile(inputfilename):
    if(outfilename=="N/A"):
      outfilename=inputfilename

      #In the current implementation, EventInfo is an astropy table with the positions of the antennas, and the meta of EventInfo is the ShowerHeader
      EventInfo=hdf5io.GetEventInfo(inputfilename)
      ShowerHeader=hdf5io.GetShowerHeaderFromEventInfo(EventInfo)
      ID=hdf5io.GetIDFromShowerHeader(ShowerHeader)
      Primary=hdf5io.GetPrimaryFromShowerHeader(ShowerHeader)

      nantennas=len(EventInfo) #get the number of antennas. Here, a check to see that this is not 0 would be in order.

      #about this loop: note that astropy table could use their oun iterator, like: "for row in table:" andthen access row['columnname'].
      #The porblem with this, is that it hardwires the file structure into the code, and i dont want that. All those details must remain hidden in hdf5io, so that we dont have
      #all the scripts if we decide to change something on the file format/structure.

      for i in range(0,nantennas):
        AntennaInfo=hdf5io.GetAntennaInfoFromEventInfo(EventInfo,i)
        antennaID=hdf5io.GetAntIDFromAntennaInfo(AntennaInfo)
        logging.info("computing voltage for antenna "+antennaID+" ("+str(i+1)+"/"+str(nantennas)+")")
        position=(hdf5io.GetXFromAntennaInfo(AntennaInfo),hdf5io.GetYFromAntennaInfo(AntennaInfo),hdf5io.GetZFromAntennaInfo(AntennaInfo))
        logging.debug("at position"+str(position))

        #in the current implementation, the electric field trace is stored in an astropy table
        trace=hdf5io.GetElectricFieldTrace(inputfilename,antennaID)
        slopes=hdf5io.GetSlopesFromTrace(trace)

        #A NICE call to the radio-simus library. Configuration and details of the voltage computation unavailable for now!.
        #Configuration should be a little more "present" in the function call,
        #also maybe the library to handle .ini files would be more profesional and robust than current implementation

        #other detail, we are storing things in astropy arrays, but then switching to numpy, that needs Transposition. This is not very efficient.
        #I hide this detail to hf5io, so that the names of the field dont remain hardcoded in the script
        efield=hdf5io.ElectricFieldTraceToNumpy(trace)
        voltage = compute_antennaresponse(efield, hdf5io.GetZenithFromShowerHeader(ShowerHeader), hdf5io.GetAzimuthFromShowerHeader(ShowerHeader), alpha=slopes[0], beta=slopes[1] )

        #now i need to put a numpy array into an astropy table, this is done, thanks to Anne with:
        voltage = _table_voltage(voltage, pos=position, slopes=slopes, info={})

        #and this is saved  to the data file
        hdf5io.SaveVoltageTrace(outfilename,antennaID,voltage)
        #end for

  else:
   logging.critical("input file " + inputfilename + " does not exist or is not a directory. ComputeVoltageOnSHDF5 cannot continue")


if __name__ == '__main__':

  if ( len(sys.argv)<2 ):
    print("usage")

  else:
   inputfile=sys.argv[1]
   ComputeVoltageOnHDF5(inputfile)

