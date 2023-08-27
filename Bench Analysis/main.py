# IMPORTS
from math import pi, tan, asin, cos, sin, acos, ceil
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
    "Material": [None, '-', None, 'C2'],
    "Bulk density": [None, 'r [t/m3]', None, 'C3'],
    "Repose angle": [None, 'f [°]', None, 'C4'],
    "Nominal Required Capacity": [[None, None], ['Q [t/h]', "M' [m3/s]"], [None, 'data["Nominal Required Capacity"][0][0] / data["Bulk density"][0] / 3600'], ['C6', 'C7']],
    "Diameter (on cutting edge)": [None, 'D [m]', None, 'C8'],
    "Bucket wheel rotational speed": [None, 'wBW [rpm]', None, 'C9'],
    "Number of buckets": [None, 'z', None, 'C10'],
    "Bucket volume": [None, 'Vb [m3] ', None, 'C11'],
    "Bucket height": [None, 'tE [m]', None, 'C12'],
    "Bucket width": [None, 'bE [m]', None, 'C13'],
    "Angle in which bucket discharge starts, measured from vert": [None, 'θ [°]', None, 'C15'],
    "Efficiency of Drive (Coupling+Motor+Gearbox)": [None, 'm ', None, 'C16'],
    "Bucket Efficiency (filling factor)": [None, 'f', None, 'C17'],
    "Boom Lenght": [None, 'Lb [m]', None, 'C20'],
    "Height of boom hinge from bottom of yard": [None, 'HL [m]', None, 'C21'],
    "Distance of boom hinge from slewing axle": [None, 'l [m]', None, 'C22'],
    "Height of BW axle from boom hinge (with boom horizontal)": [None, 'h  [m]', None, 'C23'],
    "Distance between pile CL and slewing axle": [None, 'd [m]', None, 'C24'],
    "Maximum selected boom slewing speed": [None, 'vSmax  [m/min]', None, "C25"],
    "Stockpile height": [None, 'Hp [m]', None, 'C26'],
    "Bottom stockpile width": [None, 'Bp [m]', None, 'C27'],
    "Stockpile lenght (of the full stockpile section)": [None, 'Lp [m]', None, 'C28'],
    "Selected minimum angle of Reclaiming (in plant view)": [None, 'ymax [°]', None, 'C29'],
    "Selected Maximum angle of Reclaiming (in plant view)": [None, 'ymax [°]', None, 'C32'],
    "Slewing acceleration": [[None, None], ['a1 [°/s2]', 'a1 [rad/s2]'], [None, 'data["Slewing acceleration"][0][0] * pi / 180'], ['C36', 'C37']],
    "Slewing deceleration": [[None, None], ['a2 [°/s2]', 'a2 [rad/s2]'], [None, 'data["Slewing deceleration"][0][0] * pi / 180'], ['C38', 'C39']],
    "Number of selected benches": [None, '-', None, 'C41'],
    "Selected Step of Reclaiming": [[None, None], ['p [m]', 'θ [rad]'], [None, 'data["Angle in which bucket discharge starts, measured from vert"][0]'], ['C43', 'C44']],

    # OUTPUT (they have not any units of measure due to the fact we don't need it)
    "Friction Coefficient (material/steel)": [None, 'materials[data["Material"][0]', 'C5'],  # da ricontrollare in base a come si chiede il materiale
    "Volume calculated considering selected tE and bE": [None, '1.24 * pi / 4 * data["Bucket height"][0] ** 2 * data["Bucket width"][0]', 'C14'],
    "Maximum potential capacity": [[None, None], ['data["Bucket Efficiency (filling factor)"][0] * data["Bulk density"][0] * data["Bucket volume"][0] * data["Buckets discharge"][0][1] * 3600', 'data["Maximum potential capacity"][0][0] / data["Bulk density"][0] / 3600'], ['C18', 'C19']],
    "Top stockpile width": [None, 'data["Bottom stockpile width"][0] - 2 * data["Stockpile height"][0] / tan(data["Friction factor"][0][1])', 'C29'],
    "Calculated minimum slewing angle": [[None, None], ['asin((data["Distance between pile CL and slewing axle"][0] - data["Bottom stockpile width"][0] / 2) / data["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0])', 'data["Calculated minimum slewing angle"][0][0] * 180 / pi'], ['C30', 'C31']],
    "Calculated Maximum slewing angle": [[None, None], ['pi / 2 if (data["Distance between pile CL and slewing axle"][0] + data["Bottom stockpile width"][0] / 2) / data["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0] < 1 else asin((data["Distance between pile CL and slewing axle"][0] + data["Bottom stockpile width"][0] / 2) / data["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0])', 'data["Calculated Maximum slewing angle"][0][0] * 180 / pi'], ['C33', 'C34']],
    "": [None, 'data["Stockpile height"] / data["Diameter (on cutting edge)"][0] * 2', 'C40'],  # Questo valore non aveva alcun nome, quindi sarà da chiedere se è un errore
    "Maximum allowable step": [None, 'data["Bucket height"] / cos(data["Max Horizontal distance cutting edge/boom slew. CL"][0][6])', 'C42'],

    #Data Depending on material (automatically selected)
    "Friction factor": [[None, None], ['materials[data["Material"][0]][1]', 'data["Repose angle"][0] * pi / 180'], ['C46', 'C47']],
    "Digging Coeficient": [None, 'materials[data["Material"][0]][0]', 'C48'],

    #Data used by the program (automatically calculated)
    "Minimum luffing angle": [[None, None], ['data["Minimum luffing angle"][0][1] * 180 / pi', 'asin((0.98 * data["Height of BW axle from boom hinge (with boom horizontal)"][0] + data["Height of boom hinge from bottom of yard"][0] - data["Diameter (on cutting edge)"][0] / 2) / data["Boom Lenght"][0] '], ['C51', 'C52']],
    "Maximum luffing angle": [[None, None], ['data["Maximum luffing angle"][0] * 180 / pi', 'asin((data["Stockpile height"][0] \' data["Height of boom hinge from bottom of yard"][0] - 0.985 *  data["Height of BW axle from boom hinge (with boom horizontal)"][0] + data["Diameter (on cutting edge)"][0] / 2) / data["Boom Lenght"][0]) '], ['C53', 'C54']],
    "Horizontal distance cutting edge/boom slew. CL with δmin": [None, 'data["Distance of boom hinge from slewing axle"][0] + data["Boom Lenght"][0] * cos(data["Minimum luffing angle"][0][1]) + data["Height of BW axle from boom hinge (with boom horizontal)"][0] * sin(data["Minimum luffing angle"][0][1]) + data["Diameter (on cutting edge) / 2 * sin("][0]Friction factordata["[1])"][0]', 'C55'],
    "Volumetric Capacity": [None, 'data["Nominal Required Capacity"][0][0] / data["Bulk density"][0] / data["Bucket Efficiency (filling factor)"][0]', 'C57'],
    "Rotational Speed": [None, 'data["Bucket wheel rotational speed"][0] * 2 * pi / 60', 'C58'],
    "Tangential Speed ": [[None, None], ['data["Rotational speed"][0] * data["Diameter (on cutting edge)"][0] / 2', 'data["Tangential Speed"][0] * 60'], ['C59', 'C60']],
    "Angle between buckets": [[None, None], ['2 * pi  / data["Number of buckets"][0]', '360 / data["Number of buckets"][0]'], ['C61', 'C62']],
    "Time in which bucket wheel rotates of a": [None, '60 / data["Bucket wheel rotational speed"][0] / data["Number of buckets"][0]', 'C63'],
    "Buckets discharge": [[None, None], ['data["Bucket wheel rotational speed"][0] * data["Number of buckets"][0]', 'data["Buckets discharge"][0][0] / 60'], ['C64', 'C65']],
    "Pitch between buckets": [[None, None, None], ['3.14 * data["Diameter (on cutting edge)"][0] / data["Number of buckets"][0]', 'data["Maximum selected boom slewing speed"][0] / 60', 'data["Max Horizontal distance cutting edge/boom slew. CL"][0][1] * data["Max Horizontal distance cutting edge/boom slew. CL"][0][0]'], ['C66', 'C67', 'C68']],
    "Max Horizontal distance cutting edge/boom slew. CL": [[None, None, None, None, None, None, None], ['data["Boom Lenght"][0] + data["Diameter (on cutting edge)"][0] / 2 * sin(data["Friction Coefficient (material/steel)"][0]) + data["Distance of boom hinge from slewing axle"][0]', 'data["Bucket volume"][0] * data["Bucket Efficiency (filling factor)"][0] * data["Buckets discharge"][0][1] / data["Selected Step of Reclaiming"][0][0] / (data["Stockpile height"][0] / data["Number of selected benches"][0]) / data["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0]', 'data["Max Horizontal distance cutting edge/boom slew. CL"][0] / 60 / 6.28', 'data["Pitch between buckets"][0][1] / data["Max Horizontal distance cutting edge/boom slew. CL"][0][0]', 'data["Max Horizontal distance cutting edge/boom slew. CL"][0][3] * 60 / 6.28', 'data["Selected minimum angle of Reclaiming (in plant view)"][0] * pi / 180', ' data["Selected Maximum angle of Reclaiming (in plant view)"][0] * pi / 180'], ['C69', 'C70', 'C71', 'C72', 'C73', 'C74', 'C75', 'C76', 'C77']],
    "Reclaiming Angle at which max slewing speed is reached": [[None, None], ['data["Reclaiming Angle at which max slewing speed is reached"][0][1] * 180 / pi', 'acos(data["Max Horizontal distance cutting edge/boom slew. CL"][0][1] / data["Max Horizontal distance cutting edge/boom slew. CL"][0][3])'], ['C78', 'C79']],
    "Bench height": [None, 'data["Stockpile height"][0] / data["Number of selected benches"][0]', 'C80'],
    "Number of buckets in the material": [None, 'data["Scarp angle"][0] / data["Angle between buckets"][0][0]', 'C81'],
    "Numb. of buckets in the material considered for calc.": [None, 'ceil(data["Number of buckets in the material"][0])', 'C82'],
    "Angle of 1° Bucket": [None, '0', 'C84'],
    "Angle of 2° Bucket": [None, 'data["Angle between buckets"][0] if data["Numb. of buckets in the material considered for calc."][0] >=2 else "n.a."', 'C85'],
    "Angle of 3° Bucket": [None, 'data["Angle between buckets"][0] * 2 if data["Numb. of buckets in the material considered for calc."][0] >=3 else "n.a."', 'C86'],
    "Angle of 4° Bucket": [None, 'data["Angle between buckets"][0] * 3 if data["Numb. of buckets in the material considered for calc."][0] >=4 else "n.a."', 'C87'],
    # Check Data
    "Scarp angle": [[None, None, None], ['acos(data["Diameter (on cutting edge)"][0] / 2 - data["Bench height"][0]) / (data["Diameter (on cutting edge)"][0] / 2) if data["Diameter (on cutting edge)"][0] >= data["Bench height"][0] else pi / 2 + asin((data["Bench height"][0] - data["Diameter (on cutting edge)"][0] / 2) / (data["Diameter (on cutting edge)"][0] / 2)) ', 'data["Scarp angle"][0][0] * 180 / pi', '"ok" if data["Scarp angle"][0][1] <110 and if data["Scarp angle"][0][1] < 720 / data["Number of buckets"][0] else "verify"'], ['J4', 'J5', 'K5']],
    "Froud factor": [[None, None], ['data["Tangential Speed"][0][0] / (data["Diameter (on cutting edge)"][0] / 2 * 9.81) ** (1 / 2)', '"ok" if 0.2<data["Froud factor"][0][0]<0.7 else "verify"'], ['J6', 'K6']],
    "Bucket Wheel Tangential Limit Speed": [None, '(9.81 * data["Diameter (on cutting edge)"][0] / 2) ** 0.5', 'J7'],
    "k factor": [[None, None], ['data["Tangential Speed"][0][0] / data["Bucket Wheel Tangential Limit Speed"][0]', '"BW speed increasable" if data["k factor"][0][0] < 0.5 else "it is necessary to decrease BW speed" if data["k factor"][0][0] > 0.6 else "ok, value between 0,5-0,6"'], ['J8', 'K8']],
    "Required Bucket Capacity": [[None, None], ['data["Volumetric Capacity"][0] / 3600 / data["Buckets discharge"][0][1]', '"ok" if data["Bucket volume"][0] > data["Required Bucket Capacity"][0][0] / data["Bucket Efficiency (filling factor)"][0] else "verify"'], ['J9', 'K9']],
    "Reclaimed Capacity per each revolution": [None, 'data["Bucket Efficiency (filling factor)"][0] * data["Number of buckets"][0] * data["Bucket volume"][0]', 'J10'],
    "Shape factor": [[None, None], ['data["Bucket volume"][0] ** (1/3) / data["Pitch between buckets"][0][0]', '"ok" if 0.24 < data["Shape factor"][0][0] < 0.4 else "verify" '], ['J11', 'K11']],
    "Ratio of pile height to wheel radious": [None, 'data["Stockpile height"][0] / data["Diameter (on cutting edge)"][0] * 2', 'J12'],
    "Ratio of cutting height to wheel radious": [[None, None], ['data["Bench height"][0] / data["Diameter (on cutting edge)"][0] * 2', '"ok" if 1 < data["Ratio of cutting height to wheel radious"][0][0] < 1.44 else "verify"'], ['J13', 'K13']],
    "Maximum bucket frontal sinking": [[None, None], ['data["Selected Step of Reclaiming"][0][0] * cos(data["Max Horizontal distance cutting edge/boom slew. CL"][0][6]) * sin(data["Friction factor"][0][0])', '"ok" if data["Bucket height"][0] > data["Maximum bucket frontal sinking"][0][0] else "verify"'], ['J14', 'K14']],
    "Maximum bucket lateral sinking": [[None, None], ['data["Pitch between buckets"][0][1] / data["Buckets discharge"][0][1]', '"ok" if data["Bucket width"][0] >= data["Maximum bucket lateral sinking"][0][0] else "verify"'], ['J15', 'K15']],


}
print('MATERIALI')
materiali = materials.keys()
for i, key in enumerate(materiali):
    print(f'{i + 1} - {key}')
data["Material"][0] = materiali[int(input('Inserisci il numero del materiale che vuoi utilizzare: ')) - 1]
