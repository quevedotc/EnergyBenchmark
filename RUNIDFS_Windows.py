"""multiprocessing runs

using generators instead of a list
when you are running a 100 files you have to use generators"""

import os
from eppy.modeleditor import IDF
from eppy.runner.run_functions import runIDFs

benchmark = "C:/sim/dissertacao metamodelo/"
climas = "C:/sim/dissertacao metamodelo/"

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

for file in os.listdir(benchmark):
    if file.endswith('.epw'):
        epwfile.append(file)

for file in os.listdir(benchmark):
    if file.endswith('.idf'):
        fnames.append(file)



def main():
    iddfile = "C:/EnergyPlusV9-2-0/Energy+.idd"
    IDF.setiddname(iddfile)       
          
    for epw in epwfile:
        idfs = (IDF(fname, epw) for fname in fnames)
        runs = ((idf, make_eplaunch_options(idf) ) for idf in idfs)
        print(epw)
            
        num_CPUs = 4
        runIDFs(runs, num_CPUs)

        for file in os.listdir(benchmark):
            if file.endswith('.eso') or (file.endswith('.eio') or (file.endswith('z.csv') or (file.endswith('.mdd') or (file.endswith('.rdd') or (file.endswith('.rdd')
            or (file.endswith('.rvaudit') or (file.endswith('.dxf') or (file.endswith('.shd') or (file.endswith('Sqlite.err') or (file.endswith('.audit') or (file.endswith('.bnd')))))))))))):
                os.remove(file)

if __name__ == '__main__':
    main()
