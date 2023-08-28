# IMPORTS
from math import pi, tan, asin, cos, sin, acos, ceil

data = \
{
    # INPUT
    "Input Data": {
        "Material": [None, '-', None, 'C2'],
        "Bulk density": [None, 'r [t/m3]', None, 'C3'],
        "Repose angle": [None, 'f [°]', None, 'C4'],
        "Nominal Required Capacity": [[None, None], ['Q [t/h]', "M' [m3/s]"], [None, 'data["Input Data"]["Nominal Required Capacity"][0][0] / data["Input Data"]["Bulk density"][0] / 3600'], ['C6', 'C7']],
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
        "Slewing acceleration": [[None, None], ['a1 [°/s2]', 'a1 [rad/s2]'], [None, 'data["Input Data"]["Slewing acceleration"][0][0] * pi / 180'], ['C36', 'C37']],
        "Slewing deceleration": [[None, None], ['a2 [°/s2]', 'a2 [rad/s2]'], [None, 'data["Input Data"]["Slewing deceleration"][0][0] * pi / 180'], ['C38', 'C39']],
        "Number of selected benches": [None, '-', None, 'C41'],
        "Selected Step of Reclaiming": [[None, None], ['p [m]', 'θ [rad]'], [None, 'data["Input Data"]["Angle in which bucket discharge starts, measured from vert"][0]'], ['C43', 'C44']],

        # OUTPUT (they have not any units of measure due to the fact we don't need it)
        "Friction Coefficient (material/steel)": [None, 'materials[data["Input Data"]["Material"][0]', 'C5'],  # da ricontrollare in base a come si chiede il materiale
        "Volume calculated considering selected tE and bE": [None, '1.24 * pi / 4 * data["Input Data"]["Bucket height"][0] ** 2 * data["Input Data"]["Bucket width"][0]', 'C14'],
        "Maximum potential capacity": [[None, None], ['data["Input Data"]["Bucket Efficiency (filling factor)"][0] * data["Input Data"]["Bulk density"][0] * data["Input Data"]["Bucket volume"][0] * data["Input Data"]["Buckets discharge"][0][1] * 3600', 'data["Input Data"]["Maximum potential capacity"][0][0] / data["Input Data"]["Bulk density"][0] / 3600'], ['C18', 'C19']],
        "Top stockpile width": [None, 'data["Input Data"]["Bottom stockpile width"][0] - 2 * data["Input Data"]["Stockpile height"][0] / tan(data["Input Data"]["Friction factor"][0][1])', 'C29'],
        "Calculated minimum slewing angle": [[None, None], ['asin((data["Input Data"]["Distance between pile CL and slewing axle"][0] - data["Input Data"]["Bottom stockpile width"][0] / 2) / data["Input Data"]["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0])', 'data["Input Data"]["Calculated minimum slewing angle"][0][0] * 180 / pi'], ['C30', 'C31']],
        "Calculated Maximum slewing angle": [[None, None], ['pi / 2 if (data["Input Data"]["Distance between pile CL and slewing axle"][0] + data["Input Data"]["Bottom stockpile width"][0] / 2) / data["Input Data"]["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0] < 1 else asin((data["Input Data"]["Distance between pile CL and slewing axle"][0] + data["Input Data"]["Bottom stockpile width"][0] / 2) / data["Input Data"]["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0])', 'data["Input Data"]["Calculated Maximum slewing angle"][0][0] * 180 / pi'], ['C33', 'C34']],
        "": [None, 'data["Input Data"]["Stockpile height"] / data["Input Data"]["Diameter (on cutting edge)"][0] * 2', 'C40'],  # Questo valore non aveva alcun nome, quindi sarà da chiedere se è un errore
        "Maximum allowable step": [None, 'data["Input Data"]["Bucket height"] / cos(data["Input Data"]["Max Horizontal distance cutting edge/boom slew. CL"][0][6])', 'C42'],

        #Data["Input Data"] Depending on material (automatically selected)
        "Friction factor": [[None, None], ['materials[data["Input Data"]["Material"][0]][1]', 'data["Input Data"]["Repose angle"][0] * pi / 180'], ['C46', 'C47']],
        "Digging Coeficient": [None, 'materials[data["Input Data"]["Material"][0]][0]', 'C48'],

        #Data["Input Data"] used by the program (automatically calculated)
        "Minimum luffing angle": [[None, None], ['data["Input Data"]["Minimum luffing angle"][0][1] * 180 / pi', 'asin((0.98 * data["Input Data"]["Height of BW axle from boom hinge (with boom horizontal)"][0] + data["Input Data"]["Height of boom hinge from bottom of yard"][0] - data["Input Data"]["Diameter (on cutting edge)"][0] / 2) / data["Input Data"]["Boom Lenght"][0] '], ['C51', 'C52']],
        "Maximum luffing angle": [[None, None], ['data["Input Data"]["Maximum luffing angle"][0] * 180 / pi', 'asin((data["Input Data"]''["Stockpile height"][0] \' data["Input Data"]["Height of boom hinge from bottom of yard"][0] - 0.985 *  data["Input Data"]["Height of BW axle from boom hinge (with boom horizontal)"][0] + data["Input Data"]["Diameter (on cutting edge)"][0] / 2) / data["Input Data"]["Boom Lenght"][0]) '], ['C53', 'C54']],
        "Horizontal distance cutting edge/boom slew. CL with δmin": [None, 'data["Input Data"]["Distance of boom hinge from slewing axle"][0] + data["Input Data"]["Boom Lenght"][0] * cos(data["Input Data"]["Minimum luffing angle"][0][1]) + data["Input Data"]["Height of BW axle from boom hinge (with boom horizontal)"][0] * sin(data["Input Data"]["Minimum luffing angle"][0][1]) + data["Input Data"]["Diameter (on cutting edge) / 2 * sin("][0]Friction factordata["Input Data"]["[1])"][0]', 'C55'],
        "Volumetric Capacity": [None, 'data["Input Data"]["Nominal Required Capacity"][0][0] / data["Input Data"]["Bulk density"][0] / data["Input Data"]["Bucket Efficiency (filling factor)"][0]', 'C57'],
        "Rotational Speed": [None, 'data["Input Data"]["Bucket wheel rotational speed"][0] * 2 * pi / 60', 'C58'],
        "Tangential Speed ": [[None, None], ['data["Input Data"]["Rotational speed"][0] * data["Input Data"]["Diameter (on cutting edge)"][0] / 2', 'data["Input Data"]["Tangential Speed"][0] * 60'], ['C59', 'C60']],
        "Angle between buckets": [[None, None], ['2 * pi  / data["Input Data"]["Number of buckets"][0]', '360 / data["Input Data"]["Number of buckets"][0]'], ['C61', 'C62']],
        "Time in which bucket wheel rotates of a": [None, '60 / data["Input Data"]["Bucket wheel rotational speed"][0] / data["Input Data"]["Number of buckets"][0]', 'C63'],
        "Buckets discharge": [[None, None], ['data["Input Data"]["Bucket wheel rotational speed"][0] * data["Input Data"]["Number of buckets"][0]', 'data["Input Data"]["Buckets discharge"][0][0] / 60'], ['C64', 'C65']],
        "Pitch between buckets": [[None, None, None], ['3.14 * data["Input Data"]["Diameter (on cutting edge)"][0] / data["Input Data"]["Number of buckets"][0]', 'data["Input Data"]["Maximum selected boom slewing speed"][0] / 60', 'data["Input Data"]["Max Horizontal distance cutting edge/boom slew. CL"][0][1] * data["Input Data"]["Max Horizontal distance cutting edge/boom slew. CL"][0][0]'], ['C66', 'C67', 'C68']],
        "Max Horizontal distance cutting edge/boom slew. CL": [[None, None, None, None, None, None, None], ['data["Input Data"]["Boom Lenght"][0] + data["Input Data"]["Diameter (on cutting edge)"][0] / 2 * sin(data["Input Data"]["Friction Coefficient (material/steel)"][0]) + data["Input Data"]["Distance of boom hinge from slewing axle"][0]', 'data["Input Data"]["Bucket volume"][0] * data["Input Data"]["Bucket Efficiency (filling factor)"][0] * data["Input Data"]["Buckets discharge"][0][1] / data["Input Data"]["Selected Step of Reclaiming"][0][0] / (data["Input Data"]["Stockpile height"][0] / data["Input Data"]["Number of selected benches"][0]) / data["Input Data"]["Horizontal distance cutting edge/boom slew. CL with δmin"][0][0]', 'data["Input Data"]["Max Horizontal distance cutting edge/boom slew. CL"][0] / 60 / 6.28', 'data["Input Data"]["Pitch between buckets"][0][1] / data["Input Data"]["Max Horizontal distance cutting edge/boom slew. CL"][0][0]', 'data["Input Data"]["Max Horizontal distance cutting edge/boom slew. CL"][0][3] * 60 / 6.28', 'data["Input Data"]["Selected minimum angle of Reclaiming (in plant view)"][0] * pi / 180', ' data["Input Data"]["Selected Maximum angle of Reclaiming (in plant view)"][0] * pi / 180'], ['C69', 'C70', 'C71', 'C72', 'C73', 'C74', 'C75', 'C76', 'C77']],
        "Reclaiming Angle at which max slewing speed is reached": [[None, None], ['data["Input Data"]["Reclaiming Angle at which max slewing speed is reached"][0][1] * 180 / pi', 'acos(data["Input Data"]["Max Horizontal distance cutting edge/boom slew. CL"][0][1] / data["Input Data"]["Max Horizontal distance cutting edge/boom slew. CL"][0][3])'], ['C78', 'C79']],
        "Bench height": [None, 'data["Input Data"]["Stockpile height"][0] / data["Input Data"]["Number of selected benches"][0]', 'C80'],
        "Number of buckets in the material": [None, 'data["Input Data"]["Scarp angle"][0] / data["Input Data"]["Angle between buckets"][0][0]', 'C81'],
        "Numb. of buckets in the material considered for calc.": [None, 'ceil(data["Input Data"]["Number of buckets in the material"][0])', 'C82'],
        "Angle of 1° Bucket": [None, '0', 'C84'],
        "Angle of 2° Bucket": [None, 'data["Input Data"]["Angle between buckets"][0] if data["Input Data"]["Numb. of buckets in the material considered for calc."][0] >=2 else "n.a."', 'C85'],
        "Angle of 3° Bucket": [None, 'data["Input Data"]["Angle between buckets"][0] * 2 if data["Input Data"]["Numb. of buckets in the material considered for calc."][0] >=3 else "n.a."', 'C86'],
        "Angle of 4° Bucket": [None, 'data["Input Data"]["Angle between buckets"][0] * 3 if data["Input Data"]["Numb. of buckets in the material considered for calc."][0] >=4 else "n.a."', 'C87'],
        # Check Data["Input Data"]
        "Scarp angle": [[None, None, None], ['acos(data["Input Data"]["Diameter (on cutting edge)"][0] / 2 - data["Input Data"]["Bench height"][0]) / (data["Input Data"]["Diameter (on cutting edge)"][0] / 2) if data["Input Data"]["Diameter (on cutting edge)"][0] >= data["Input Data"]["Bench height"][0] else pi / 2 + asin((data["Input Data"]["Bench height"][0] - data["Input Data"]["Diameter (on cutting edge)"][0] / 2) / (data["Input Data"]["Diameter (on cutting edge)"][0] / 2)) ', 'data["Input Data"]["Scarp angle"][0][0] * 180 / pi', '"ok" if data["Input Data"]["Scarp angle"][0][1] <110 and if data["Input Data"]["Scarp angle"][0][1] < 720 / data["Input Data"]["Number of buckets"][0] else "verify"'], ['J4', 'J5', 'K5']],
        "Froud factor": [[None, None], ['data["Input Data"]["Tangential Speed"][0][0] / (data["Input Data"]["Diameter (on cutting edge)"][0] / 2 * 9.81) ** (1 / 2)', '"ok" if 0.2<data["Input Data"]["Froud factor"][0][0]<0.7 else "verify"'], ['J6', 'K6']],
        "Bucket Wheel Tangential Limit Speed": [None, '(9.81 * data["Input Data"]["Diameter (on cutting edge)"][0] / 2) ** 0.5', 'J7'],
        "k factor": [[None, None], ['data["Input Data"]["Tangential Speed"][0][0] / data["Input Data"]["Bucket Wheel Tangential Limit Speed"][0]', '"BW speed increasable" if data["Input Data"]["k factor"][0][0] < 0.5 else "it is necessary to decrease BW speed" if data["Input Data"]["k factor"][0][0] > 0.6 else "ok, value between 0,5-0,6"'], ['J8', 'K8']],
        "Required Bucket Capacity": [[None, None], ['data["Input Data"]["Volumetric Capacity"][0] / 3600 / data["Input Data"]["Buckets discharge"][0][1]', '"ok" if data["Input Data"]["Bucket volume"][0] > data["Input Data"]["Required Bucket Capacity"][0][0] / data["Input Data"]["Bucket Efficiency (filling factor)"][0] else "verify"'], ['J9', 'K9']],
        "Reclaimed Capacity per each revolution": [None, 'data["Input Data"]["Bucket Efficiency (filling factor)"][0] * data["Input Data"]["Number of buckets"][0] * data["Input Data"]["Bucket volume"][0]', 'J10'],
        "Shape factor": [[None, None], ['data["Input Data"]["Bucket volume"][0] ** (1/3) / data["Input Data"]["Pitch between buckets"][0][0]', '"ok" if 0.24 < data["Input Data"]["Shape factor"][0][0] < 0.4 else "verify" '], ['J11', 'K11']],
        "Ratio of pile height to wheel radious": [None, 'data["Input Data"]["Stockpile height"][0] / data["Input Data"]["Diameter (on cutting edge)"][0] * 2', 'J12'],
        "Ratio of cutting height to wheel radious": [[None, None], ['data["Input Data"]["Bench height"][0] / data["Input Data"]["Diameter (on cutting edge)"][0] * 2', '"ok" if 1 < data["Input Data"]["Ratio of cutting height to wheel radious"][0][0] < 1.44 else "verify"'], ['J13', 'K13']],
        "Maximum bucket frontal sinking": [[None, None], ['data["Input Data"]["Selected Step of Reclaiming"][0][0] * cos(data["Input Data"]["Max Horizontal distance cutting edge/boom slew. CL"][0][6]) * sin(data["Input Data"]["Friction factor"][0][0])', '"ok" if data["Input Data"]["Bucket height"][0] > data["Input Data"]["Maximum bucket frontal sinking"][0][0] else "verify"'], ['J14', 'K14']],
        "Maximum bucket lateral sinking": [[None, None], ['data["Input Data"]["Pitch between buckets"][0][1] / data["Input Data"]["Buckets discharge"][0][1]', '"ok" if data["Input Data"]["Bucket width"][0] >= data["Input Data"]["Maximum bucket lateral sinking"][0][0] else "verify"'], ['J15', 'K15']],
    },
    "PRINT": {
        # First page
        "_": [[None, None, None], ['data["Input Data"]["Nominal Required Capacity"][0][0]', 'data["Input Data"]["Material"][0]', 'data["Input Data"]["Bulk density"][0]'], ['K48', 'J52', 'M52']],

        # DATA USED FOR CALCULATION
        "Nominal Required Capacity": [None, 'data["Input Data"]["Nominal Required Capacity"][0][0]', 'O98'],

        # MATERIAL DATA
        "Type": [None, 'data["Input Data"]["Material"][0]', 'L101'],
        "Bulk density": [None, 'data["Input Data"]["Bulk density"][0]', 'O102'],
        "Repose angle": [None, 'data["Input Data"]["Repose angle"][0]', 'O103'],
        "Friction Coefficient (material/steel)": [None, 'data["Input Data"]["Friction Coefficient (material/steel)"][0]', 'O104'],

        #STOCKPILE DATA
        "Bottom stockpile width": [None, 'data["Input Data"]["Bottom stockpile width"][0]', 'O108'],
        "Stockpile height": [None, 'data["Input Data"]["Stockpile height"][0]', 'O109'],
        "Top stockpile width": [None, 'data["Input Data"]["Top stockpile width"][0]', 'O110'],
        "Stockpile lenght (of the full stockpile section)": [None, 'data["Input Data"]["Stockpile lenght (of the full stockpile section)"][0]', 'O111'],

        #BUCKET WHEEL DATA
        "Diameter (on cutting edge)": [None, 'data["Input Data"]["Diameter (on cutting edge)"][0]', 'O115'],
        "Number of buckets": [None, 'data["Input Data"]["Number of buckets"][0]', 'O116'],
        "Bucket height": [None, 'data["Input Data"]["Bucket height"][0]', 'O118'],
        "Bucket volume": [None, 'data["Input Data"]["Bucket volume"][0]', 'O117'],
        "Bucket width": [None, 'data["Input Data"]["Bucket width"][0]', 'O119'],
        "Bucket wheel rotational speed": [None, 'data["Input Data"]["Bucket wheel rotational speed"][0]', 'O120'],
        "Efficiency of Drive (Coupling+Motor+Gearbox)": [None, 'data["Input Data"]["Efficiency of Drive (Coupling+Motor+Gearbox)"][0]', 'O121'],
        "Bucket Efficiency (filling factor)": [None, 'data["Input Data"]["Bucket Efficiency (filling factor)"][0]', 'O122'],
        "Maximum potential capacity": [None, 'data["Input Data"]["Maximum potential capacity"][0]', 'O123'],
        "Froud factor": [None, 'data["Input Data"]["Froud factor"][0]', 'O124'],
        "Buckets discharge": [None, 'data["Input Data"]["Buckets discharge"][0]', 'O125'],

        # RECLAIMER DATA

    }

}

# for the materials I don't use a dictionary of list because the values are constants, so is better to use a tuple
materials = \
{
    'ore': (22.7456, 0.4, 35, 0.4),
    'coal': (8.743, 0.35, None, 0.35),
    'pellet': (13.1194, 0.3, (30, 44), 0.35),
    'coke': (17.4959, 0.25, None, 0.25),
    'limestone': (17.4959, 0.5, (30, 44), 0.5)
}

print('MATERIALI')
materiali = materials.keys()
for i, key in enumerate(materiali):
    print(f'{i + 1} - {key}')
data["Input Data"]["Material"][0] = materiali[int(input('Inserisci il numero del materiale che vuoi utilizzare: ')) - 1]
