import os
import sys
import glob
import logging
import numpy as np
import AiresInfoFunctions as AiresInfo
root_dir = os.path.realpath(os.path.join(os.path.split(__file__)[0], "../")) # = $PROJECT
sys.path.append(os.path.join(root_dir, "lib", "python"))
from radio_simus.in_out import load_trace_to_table
import radio_simus.hdf5fileinout as hdf5io

#understand why it is loading the compute voltage module when you call it

logging.basicConfig(level=logging.DEBUG)

#if no outfilename is given, it will use the taskname on the sry file
#this function assumes that a .sry, antpos.dat file and all the .trace files are located in the showerdirectory.
#if you dont like this, you can specify the sry and antpos files manually, and point the script to where the trace files are.
#core and slopes are not really a problem of ZHAireS, but you can specify them in the input if you want (although this should be done in a separate function)

def ZHAireSHDF5FileWriter(showerdirectory,outfilename="N/A",showerID="N/A",core=[0,0,0],slopes=0,sryfile="N/A",antposfile="N/A"):

  if os.path.isdir(showerdirectory):

   ################################################################################################################################################
   if(sryfile=="N/A"):
     sryfile=glob.glob(showerdirectory+"/*.sry")

   if(len(sryfile)==1):

     zen,azim,energy,primary,xmax,distance,taskname=AiresInfo.ReadAiresSry(str(sryfile[0]),"GRAND")

     #now i will create the meta information for the shower. This should be a function call provided by the library, a part of the "shower" class
     #i would also store xmax, and its position if available. Other simulation details that might be of interest:
     #directory where the simus were (for future reference)
     #zhaires and aires versions
     #thining level
     #low energy cut
     #some tables? longitudinal e+/e-, ground e+/e-, groun u+/u-?
     #refractive index model
     #atmospheric model name
     #time bin size, tmin, tmax

     showerheader = hdf5io.CreateShowerHeader(primary, energy, zen, azim, taskname, sim="ZHAireS", inj=100000, showerID="N/A", core=(0,0,0))

   elif(len(sryfile)>1):
    logging.critical("multiple sry files " + str(len(sryfile)) + " found in " +showerdirectory + ". ZHAireSHDF5FileWriter cannot continue")
    return -1
   else:
    logging.critical("sry file not found in " +showerdirectory + ". ZHAireSHDF5FileWriter cannot continue")
    return -1
   ################################################################################################################################################

   if(antposfile=="N/A"):
     antposfile=glob.glob(showerdirectory+"/antpos.dat")

   if(len(antposfile)==1 and os.path.isfile(antposfile[0])):
     positions = np.genfromtxt(showerdirectory+"/antpos.dat") #this is not opening correctly the antena ID
     #workarround
     token = open(antposfile[0],'r')
     linestoken=token.readlines()
     tokens_column_number = 1
     IDs=[]
     for x in linestoken:
       IDs.append(x.split()[tokens_column_number])
     token.close()

   elif(len(antposfile)>1):
    logging.critical("multiple antpos.dat files " + str(len(antoposfile)) + " found in " +showerdirectory + ". ZHAireSHDF5FileWriter cannot continue")
    return -1
   else:
    logging.critical("antpos.dat file not found in " +showerdirectory + ". ZHAireSHDF5FileWriter cannot continue")
    return -1

   #now i will get radio information for the shower. This should be a function call provided by the framework, a part of the "shower" class

   if(outfilename=="N/A"):
     outfilename=showerdirectory+"/"+taskname+'.hdf5'

   #check if file exists
   if(os.path.isfile(outfilename)):
    logging.critical(outfilename+"already exists. ZHAireSHDF5FileWriter cannot continue")
    return -1

   ending_e = "/a*.trace"

   tracefiles=glob.glob(showerdirectory+ending_e)

   if(len(tracefiles)==0):
    logging.critical("no trace files found in "+showerdirectory+" ZHAireSHDF5FileWriter cannot continue")
    return -1

   if(slopes==0):
     slopes = np.zeros((len(positions),2)) #(thisis external to ZHAireS)

   EventInfo=hdf5io.GenerateEventInfo(IDs, positions.T[2], positions.T[3], positions.T[4], slopes.T[0], slopes.T[1], showerheader) #showerheder should be eventheader

   hdf5io.SaveEventInfo(outfilename,EventInfo)

   for ant in tracefiles:
     #print("\n Read in data from ", ant)

     ant_number = int(ant.split('/')[-1].split('.trace')[0].split('a')[-1]) # index in selected antenna list. this only works if all antenna files are consecutive

     ID = IDs[ant_number]
     ant_positions=(positions[ant_number,2],positions[ant_number,3],positions[ant_number,4])
     ant_slopes=(slopes[ant_number,0],slopes[ant_number,1])

     #print("antenna number:"+ str(ant_number))
     #print("ID:"+str(ID))
     #print(positions[ant_number])
     #print(ant_positions[0],ant_positions[1],ant_positions[2])
     #print(ant_slopes[0],ant_slopes[1])

     #now, this is in the library! However it mixes CoREAS and ZHAireS methods, that should be separated
     a= load_trace_to_table(path=ant, pos=ant_positions, slopes=ant_slopes,  info={}, content="e", simus="zhaires", save=outfilename, ant="/"+str(ID)+"/")

   logging.info("ZHAireSHDF5FileWriter successfully created "+ outfilename)

  else:
   logging.critical("input directory " + showerdirectory + " does not exist or is not a directory. ZHAireSHDF5FileWriter cannot continue")








if __name__ == '__main__':

  if ( len(sys.argv)<2 ):
    print("usage")

  else:
   showerdirectory=sys.argv[1]
   ZHAireSHDF5FileWriter(showerdirectory)

