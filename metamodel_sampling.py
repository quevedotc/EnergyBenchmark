#create the sample with Sobol and all the IDFs files to simulation
import sys
import os
from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
from eppy import modeleditor
from eppy.modeleditor import IDF
import sqlite3

#folder with all database. This direcotry will have all IDF to run simulations
benchmark = "C:/sim/dissertacao metamodelo/"

#folder with idf parts
parts = 'C:/Users/LabEEE_3-7/Desktop/Tiago/Dissertação/idfs/Parts'
#folder where will be created the data base
amostras = 'C:/Users/LabEEE_3-7/Desktop/Tiago/Dissertação/idfs/amostras'
#folder to word with idfs
work = 'C:/Users/LabEEE_3-7/Desktop/Tiago/Dissertação/idfs'
#idd to select the E+ version
iddfile = 'C:/EnergyPlusV9-2-0/Energy+.idd'
#base idf file that will be changed to create the database
base_file = 'C:/Users/LabEEE_3-7/Desktop/Tiago/Dissertação/idfs/base.idf'
#epw file to work with eppy will not be used in the simulations
epwfile = 'C:/Users/Tiago/Desktop/Work/BRA_SC_Florianopolis-Luz.AP.838990_TRY.1963.epw'
IDF.setiddname(iddfile)


# list of idfs with differents constructions and other variables

list_turno = ['TURN01', 'TURN02', 'TURN03']
list_ocupacao = [1.2, 3.0]
list_tipo_cob = ['COB1', 'COB3.7']
list_tipo_par = ['PAR07', 'PAR2.5','PAR4.4']
list_absortancia_cob = [0.2, 0.5, 0.8] 
list_absortancia_par = [0.2, 0.5, 0.8]
list_FS = [0.45, 0.87]
list_transmitancia_vidro = [2.6, 5.7] 
list_DPI = [9.9, 16] #W/m2
list_somb = ['somb','semsomb']

# Getting the sample of the list of idfs        
problem = {
    'num_vars': 10,
    'names':['TipoCobertura', 'TipoParede', 'AbsortanciaCobertura', 
    'AbsortanciaParede', 'FatorSolar', 
    'TransmitanciaVidro', 'Turno', 'Ocupacao', 'DPI','Sombreamento'],
    'bounds': [[0, len(list_tipo_cob)], 
    [0, len(list_tipo_par)], 
    [0, len(list_absortancia_cob)],
    [0, len(list_absortancia_par)],
    [0, len(list_FS)],
    [0, len(list_transmitancia_vidro)],
    [0,len(list_DPI)], 
    [0,len(list_turno)],
    [0,len(list_ocupacao)],
    [0,len(list_somb)]],
    }
#problem from saltelli
param_values = saltelli.sample(problem,50)
print(param_values)

idf_amostra = []
#convert the param_Values to int since we only have int variables
for i in range(len(param_values)):
    amostra = [int(valor) for valor in param_values[i]]
    idf_amostra.append(amostra)

#print "amostra" to verify the database
print("IDF Amostra:", idf_amostra)
print (len(idf_amostra))


# Starts SQLite database

conn = sqlite3.connect('benchmark_db.sqlite')
cur = conn.cursor()

cur.executescript(''' 

DROP TABLE IF EXISTS Inputs; 
DROP TABLE IF EXISTS Outputs;

CREATE TABLE Inputs (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    TipoCobertura TEXT,
    TipoParede TEXT,
    AbsortanciaCobertura REAL,
    AbsortanciaParede REAL,
    FatorSolar REAL,
    TransmitanciaVidro REAL,
    turno REAL,
    Ocupacao REAL,
    DPI REAL,     
    sombreamento REAL);
    

CREATE TABLE Outputs (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    Filename TEXT,
    Output REAL);
    ''')



for i in range(len(idf_amostra)):
    parametros_indices = idf_amostra[i]
    tipo_cob = list_tipo_cob[parametros_indices[0]]
    tipo_par = list_tipo_par[parametros_indices[1]]
    absortancia_cob = list_absortancia_cob[parametros_indices[2]]
    absortancia_par = list_absortancia_par[parametros_indices[3]]
    FS = list_FS[parametros_indices[4]]
    transmitancia_vidro = list_transmitancia_vidro[parametros_indices[5]]
    DPI = list_DPI[parametros_indices[6]]
    turno = list_turno[parametros_indices[7]]
    ocupacao = list_ocupacao[parametros_indices[8]]
    somb = list_somb[parametros_indices[9]]
    #IDRS = list_IDRS[parametros_indices[10]]

   #change directory to get idf parts for each variable   
    os.chdir(parts)
    cob_file = (tipo_cob + ".idf")
    par_file = (tipo_par + ".idf")
    turno_file = (turno + ".idf")
    somb_file = (somb + ".idf")
    base_idf = IDF(base_file)
    cob_idf = IDF(cob_file)
    par_idf = IDF(par_file)
    turno_idf = IDF(turno_file)
    somb_idf = IDF(somb_file)
    os.chdir(work)


    #Inserts cob (roof) and par (walls) constructions into base IDF
    base_constructions = base_idf.idfobjects["CONSTRUCTION"]

    cob_construction = cob_idf.idfobjects["CONSTRUCTION"]
    for construction in cob_construction:
        base_constructions.append(construction)

    par_construction = par_idf.idfobjects["CONSTRUCTION"]
    for construction in par_construction:
        base_constructions.append(construction)

    #Inserts Turno into base iDF
    base_schedule = base_idf.idfobjects["SCHEDULE:COMPACT"]
    turno_schedule = turno_idf.idfobjects["SCHEDULE:COMPACT"]
    for schedule in turno_schedule:
        base_schedule.append(schedule)

    #Inserts Somb (shading) into base iDF
    base_somb = base_idf.idfobjects["SCHEDULE:COMPACT"]
    somb_schedule = somb_idf.idfobjects["SCHEDULE:COMPACT"]
    for schedule in somb_schedule:
        base_somb.append(schedule)

    #Updates materials absorptances of cob and par and inserts into base IDF
    base_materials = base_idf.idfobjects["MATERIAL"]

    cob_materials = cob_idf.idfobjects["MATERIAL"]
    for material in cob_materials:
        material.Solar_Absorptance = absortancia_cob
        material.Visible_Absorptance = absortancia_cob
#        print(material)
        base_materials.append(material)

    par_materials = par_idf.idfobjects["MATERIAL"]
    for material in par_materials:
        material.Solar_Absorptance = absortancia_par
        material.Visible_Absorptance = absortancia_par
#        print(material)
        base_materials.append(material)


    #Updates FS (SHGC) and glass transmittance
    base_vidro = base_idf.idfobjects["WindowMaterial:SimpleGlazingSystem"]
    for vidro in base_vidro:
        vidro.Solar_Heat_Gain_Coefficient = FS
        vidro.UFactor = transmitancia_vidro
    
    #update north axis
    #base_orientacao = base_idf.idfobjects["BUILDING"]
    #for building in base_orientacao:
     #   building.North_Axis = ORIENTACAO

    #Updates DPI
    base_DPI = base_idf.idfobjects["LIGHTS"]
    for light in base_DPI:
        light.Watts_per_Zone_Floor_Area = DPI

    #Updates IDRS
    #base_IDRS = base_idf.idfobjects["HVACTEMPLATE:ZONE:PTHP"]
    #for HVAC in base_IDRS:
     #   Cooling_Coil_Gross_Rated_COP = IDRS

    #UPDATES OCCUPANCY
    base_people = base_idf.idfobjects["PEOPLE"]
    base_people[5].Zone_Floor_Area_per_Person = ocupacao


    name_idf = (tipo_cob + '_' + tipo_par + '_' + str(absortancia_cob) + '_' + str(absortancia_par) + '_' + str(FS) + '_' + str(transmitancia_vidro) + '_' + str(DPI) + '_' + str(turno) + '_' + str(ocupacao) + '_'+ str(somb) +  '_' + '.idf')
    print(name_idf)
    os.chdir(amostras)
    base_idf.saveas(name_idf)
    os.chdir(work)
    

  #inserts values into database
    cur.execute('''INSERT INTO Inputs (TipoCobertura, TipoParede, AbsortanciaCobertura, AbsortanciaParede, FatorSolar, TransmitanciaVidro, DPI, Turno, Ocupacao,  sombreamento) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?,?)''', (tipo_cob, tipo_par, absortancia_cob, absortancia_par, FS, transmitancia_vidro, DPI, turno, ocupacao, somb))
    cur.execute('''INSERT INTO Outputs (Filename) VALUES (?)''', (name_idf,))
    conn.commit()

# Closes connectcion to database
conn.close()

# add PTHP and VRF systens to idfs in database


#directory to save VRF files
inverter = 'C:/Users/LabEEE_3-7/Desktop/Tiago/Dissertação/idfs/amostras/inverter'
#directory to save PTHP files
split = 'C:/Users/LabEEE_3-7/Desktop/Tiago/Dissertação/idfs/amostras/split'

#base file for VRF
base_VRF = 'C:/Users/LabEEE_3-7/Desktop/Tiago/Dissertação/idfs/vrf.idf'
#base file for PTHP
base_SPLIT = 'C:/Users/LabEEE_3-7/Desktop/Tiago/Dissertação/idfs/split.idf'


idf_vrf = IDF(base_VRF)
VRF_zone = idf_vrf.idfobjects["HVACTEMPLATE:ZONE:VRF"]
VRF_System = idf_vrf.idfobjects["HVACTEMPLATE:SYSTEM:VRF"]
idf_split = IDF(base_SPLIT)
SPLIT_zone = idf_split.idfobjects["HVACTEMPLATE:ZONE:PTHP"]
COP = [2.7, 3.2]
IDRS = [5, 7]

list_amostra = []

for file in os.listdir(amostras):
    if file.endswith(".idf"):
        list_amostra.append(file)
print(list_amostra)
print(len(idf_amostra))

#works in VRF files
os.chdir(amostras)
for file in list_amostra:
    base_idf = IDF(file)
    base_VRF_zone = base_idf.idfobjects["HVACTEMPLATE:ZONE:VRF"]
    base_VRF_system = base_idf.idfobjects["HVACTEMPLATE:SYSTEM:VRF"]   

    for vrfzone in VRF_zone:
        base_VRF_zone.append(vrfzone)

    for vrfs in VRF_System:
        base_VRF_system.append(vrfs)

    for idrs in IDRS:
        caso = file[:-4]
        name_idf = (caso + '_' + 'VRF' + '_' + str(idrs) +'.idf')
        for vrfs in VRF_System:
            vrfs.Gross_Rated_Cooling_COP = idrs
            vrfs.Gross_Rated_Heating_COP = idrs
            os.chdir(inverter)
            base_idf.saveas(name_idf)
            os.chdir(amostras)

outputs_vrf = idf_vrf.idfobjects["OUTPUT:VARIABLE"]
idf_vrf = []
idf_split = []

os.chdir(benchmark)
for file in os.listdir(benchmark):
    if file.endswith('.idf'):
        if 'VRF' in file:
            idf_vrf.append(file)
            idf1 = IDF(file)
            for i in range(len(outputs_vrf)):
                variavel = outputs_vrf[i]
                idf1.copyidfobject(variavel)
                idf1.save()


#Works in PTHP files

os.chdir(amostras)
for file in list_amostra:
    base_idf = IDF(file)
    base_SPLIT = base_idf.idfobjects["HVACTEMPLATE:ZONE:PTHP"]

    for splits in SPLIT_zone:
        base_SPLIT.append(splits)

    for cop in COP:
        caso = file[:-4]
        name_idf = (caso + '_' + 'SPLIT' + '_' + str(cop) + '.idf')
        for splits in SPLIT_zone:
            splits.Cooling_Coil_Gross_Rated_COP = cop
            splits.Heat_Pump_Heating_Coil_Gross_Rated_COP = cop
            os.chdir(split)
            base_idf.saveas(name_idf)
            os.chdir(amostras)


#change the output for hourly 
'''
for root, dirs, files in os.walk(path):
    for name in files:         
        if name.endswith(('.idf')):
            os.chdir(root)
            idf1 = IDF(name)
            variavel = idf1.idfobjects["OUTPUT:VARIABLE"]

            for i in range(len(variavel)):
                variavel[i].Reporting_Frequency = "Hourly"

        idf1.save()
'''


print('terminou')