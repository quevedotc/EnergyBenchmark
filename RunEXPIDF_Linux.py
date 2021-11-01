"""multiprocessing runs

using generators instead of a list
when you are running a 100 files you have to use generators"""

import os
from eppy.modeleditor import IDF
from eppy.runner.run_functions import runIDFs

benchmark = "path to folder with idfs"
#This folder can only contain the EPW files that will be used in simulation. Every EPW in this folder will be used to run simulations
climas = "path to folder with EPW files that will be used in simulation"

os.chdir(benchmark)
def make_eplaunch_options(idf):
    
    """Make options for run, so that it runs like EPLaunch on Windows"""
    idfversion = idf.idfobjects['version'][0].Version_Identifier.split('.')
    idfversion.extend([0] * (3 - len(idfversion)))
    idfversionstr = '-'.join([str(item) for item in idfversion])
    
    fname = idf.idfname
    epwfile = idf.epw
    options = {
        'ep_version':idfversionstr, # runIDFs needs the version number
        'output_prefix': (fname.replace('.idf', '_') + epwfile[:6]) , 
        'output_suffix':'C',
        'output_directory':benchmark,
        'readvars':True
        }
    return options


fnames = []
epwfile = []

for file in os.listdir(climas):
    if file.endswith('.epw'):
        epwfile.append(file)

for file in os.listdir(benchmark):
    if file.endswith('.expidf'):
        fnames.append(file)



def main():
    iddfile = "/usr/local/EnergyPlus-9-2-0/Energy+.idd"
    IDF.setiddname(iddfile)       
                
    for epw in epwfile:
        idfs = (IDF(fname, epw) for fname in fnames)
        runs = ((idf, make_eplaunch_options(idf) ) for idf in idfs)

            
        num_CPUs = 10
        runIDFs(runs, num_CPUs)

if __name__ == '__main__':
    main()
