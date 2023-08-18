# IMPORTS
from math import pi, tan, asin, cos, sin
# for the materials I don't use a dictionary of list because the values are constants, so is better to use a tuple
materials = \
{
    'ore': (22.7456, 0.4, 35, 0.4),
    'coal': (8.743, 0.35, None, 0.35),
    'pellet': (13.1194, 0.3, (30, 44), 0.35),
    'coke': (17.4959, 0.25, None, 0.25),
    'limestone': (17.4959, 0.5, (30, 44), 0.5)
}

data = \
{
    # INPUT
    "Material": [None, '-', None],
    "Bulk density": [None, 'r [t/m3]', None],
    "Repose angle": [None, 'f [°]', None],
    "Nominal Required Capacity": [[None, 0.494], ['Q [t/h]', "M' [m3/s]"], [None, None]], # chiedere se il secondo valore è sempre 0.494 dato che non è azzurro e non ha formule
    "Diameter (on cutting edge)": [None, 'D [m]', None],
    "Bucket wheel rotational speed": [None, 'wBW [rpm]', None],
    "Number of buckets": [None, 'z', None],
    "Bucket volume": [None, 'Vb [m3] ', None],
    "Bucket height": [None, 'tE [m]', None],
    "Bucket width": [None, 'bE [m]', None],
    "Angle in which bucket discharge starts, measured from vert": [None, 'θ [°]', None],
    "Efficiency of Drive (Coupling+Motor+Gearbox)": [None, 'm ', None],
    "Bucket Efficiency (filling factor)": [None, 'f', None],
    "Boom Lenght": [None, 'Lb [m]', None],
    "Height of boom hinge from bottom of yard": [None, 'HL [m]', None],
    "Distance of boom hinge from slewing axle": [None, 'l [m]', None],
    "Height of BW axle from boom hinge (with boom horizontal)": [None, 'h  [m]', None],
    "Distance between pile CL and slewing axle": [None, 'd [m]', None],
    "Maximum selected boom slewing speed ": [None, 'vSmax  [m/min]', None],
    "Stockpile height": [None, 'Hp [m]', None],
    "Bottom stockpile width": [None, 'Bp [m]', None],
    "Stockpile lenght (of the full stockpile section)": [None, 'Lp [m]', None],
    "Selected minimum angle of Reclaiming (in plant view)": [None, 'ymax [°]', None],
    "Selected Maximum angle of Reclaiming (in plant view)": [None, 'ymax [°]', None],
    "Slewing acceleration": [[None, None], ['a1 [°/s2]', 'a1 [rad/s2]'], [None, 'data["Slewing acceleration"][0][0] * pi / 180']],
    "Slewing deceleration": [[None, None], ['a2 [°/s2]', 'a2 [rad/s2]'], [None, 'data["Slewing deceleration"][0][0] * pi / 180']],
    "Number of selected benches": [None, '-', None],
    "Selected Step of Reclaiming": [[None, None], ['p [m]', 'θ [rad]'], [None, 'data["Angle in which bucket discharge starts, measured from vert"][0]']],

    # OUTPUT (they have not any units of measure due to the fact we don't need it)
    "Friction Coefficient (material/steel)": [None, 'materials[data["Material"][0]'],  # da ricontrollare in base a come si chiede il materiale
    "Volume calculated considering selected tE and bE": [None, '1.24 * pi / 4 * data["Bucket height"][0] ** 2 * data["Bucket width"][0]'],
    "Maximum potential capacity": [[None, None], ['data["Bucket Efficiency (filling factor)"][0] * data["Bulk density"][0] * data["Bucket volume"][0] * data["Buckets discharge"][0][1] * 3600', 'data["Maximum potential capacity"][0][0] / data["Bulk density"][0] / 3600']],
    "Top stockpile width": [None, 'data["Bottom stockpile width"][0] - 2 * data["Stockpile height"][0] / tan(data["Friction factor"][0][1])'],
    "Calculated minimum slewing angle": [[None, None], ['asin((data["Distance between pile CL and slewing axle"][0] - data["Bottom stockpile width"][0] / 2) / data["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0])', 'data["Calculated minimum slewing angle"][0][0] * 180 / pi']],
    "Calculated Maximum slewing angle": [[None, None], ['pi / 2 if (data["Distance between pile CL and slewing axle"][0] + data["Bottom stockpile width"][0] / 2) / data["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0] < 1 else asin((data["Distance between pile CL and slewing axle"][0] + data["Bottom stockpile width"][0] / 2) / data["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0])', 'data["Calculated Maximum slewing angle"][0][0] * 180 / pi']],
    "": [None, 'data["Stockpile height"] / data["Diameter (on cutting edge)"][0] * 2'],  # Questo valore non aveva alcun nome, quindi sarà da chiedere se è un errore
    "Maximum allowable step": [None, 'data["Bucket height"] / cos(data["Max Horizontal distance cutting edge/boom slew. CL"][0][6])'],

    #Data Depending on material (automatically selected)
    "Friction factor": [[None, None], ['materials[data["Material"][0]][1]', 'data["Repose angle"][0] * pi / 180']],
    "Digging Coeficient": [None, 'materials[data["Material"][0]][0]'],

    #Data used by the program (automatically calculated)
    "Minimum luffing angle": [[None, None], ['data["Minimum luffing angle"][0][1] * 180 / pi', 'asin((0.98 * data["Height of BW axle from boom hinge (with boom horizontal)"][0] + data["Height of boom hinge from bottom of yard"][0] - data["Diameter (on cutting edge)"][0] / 2) / data["Boom Lenght"][0] ']],
    "Maximum luffing angle": [[None, None], ['data["Maximum luffing angle"][0] * 180 / pi', 'asin((data["Stockpile height"][0] \' data["Height of boom hinge from bottom of yard"][0] - 0.985 *  data["Height of BW axle from boom hinge (with boom horizontal)"][0] + data["Diameter (on cutting edge)"][0] / 2) / data["Boom Lenght"][0]) ']],
    "Horizontal distance cutting edge/boom slew. CL with δmin": [None, 'data["Distance of boom hinge from slewing axle"][0] + data["Boom Lenght"][0] * cos(data["Minimum luffing angle"][0][1]) + data["Height of BW axle from boom hinge (with boom horizontal)"][0] * sin(data["Minimum luffing angle"][0][1]) + data["Diameter (on cutting edge) / 2 * sin("][0]Friction factordata["[1])"][0]'],
    "Volumetric Capacity": [None, 'data["Nominal Required Capacity"][0][0] / data["Bulk density"][0] / data["Bucket Efficiency (filling factor)"][0]'],
    "Rotational Speed": [None, 'data["Bucket wheel rotational speed"][0] * 2 * pi / 60'],
    "Tangential Speed ": [[None, None], ['data["Rotational speed"][0] * data["Diameter (on cutting edge)"][0] / 2', 'data["Tangential Speed"][0] * 60']],




}

print('MATERIALI')
materiali = materials.keys()
for i, key in enumerate(materiali):
    print(f'{i + 1} - {key}')
data["Material"][0] = materiali[int(input('Inserisci il numero del materiale che vuoi utilizzare: ')) - 1]
