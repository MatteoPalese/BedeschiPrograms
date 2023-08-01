# BOOM SLEWING
import os
from datetime import datetime
from tkinter import *
from tkinter import filedialog

from openpyxl import load_workbook

# le unità dalle righe 8 a 20
u1 = ['t', 'm', 't x m²']
# le unità dalla riga 193 alla 203
u2 = ['Nm', 'Nm', 'kW', 'kN', 't']
# le unità dalla riga 209 alla 219
u3 = ['Nm', 'Nm', 'kW', 'kN', 't', '%', '', 'rpm', 'rpm', 'rpm', 'm/min', 'm/min', 'kW', 'kW', 'rad/s', 'rad/s']
# le unità dalla riga 235 alla 245
u4 = ['Nm', 'Nm', 'Nm', 'kgm2', 'ras/s2', 'rad/s', 's', 'kNm', 'kN', 't', 'n/mm2', 'n/mm2', 'stringa'] # ras o rad in u4[4]


# 0 = value
# 1 = unità di misura (- quando non ha alcuna unità di misura)
# 2 = formula da usare (None quando è un dato di input)
# 2 = la cella nella quale si trova il dato


current_line = 0
data = \
{
    #chiedono 2 input, e il terzo è un output
    'SLING': [[None, None, None], u1, [None, None, 'data["SLING"][0][0] * (data["SLING"][0][1]**2)'], ['E8', 'G8', 'I8']],
    'MFX mast front column': [[None, None, None], u1, [None, None, 'data["MFX mast front column"][0][0] * (data["MFX mast front column"][0][1]**2)'], ['E11', 'G11', 'I11']],
    'TOTAL BOOM': [[None, None, None], u1, [None, None, 'data["TOTAL BOOM"][0][0] * (data["TOTAL BOOM"][0][1]**2)'], ['E14', 'G14', 'I14']],
    'TOTAL BOOM TIE RODS': [[None, None, None], u1, [None, None, 'data["TOTAL BOOM TIE RODS"][0][0] * (data["TOTAL BOOM TIE RODS"][0][1]**2)'], ['E17', 'G17', 'I17']],
    'TOTAL RTR': [[None, None, None], u1, [None, None, 'data["TOTAL RTR"][0][0] * (data["TOTAL RTR"][0][1]**2)'], ['E20', 'G20', 'I20']],
    'TOTAL CWTB': [[None, None, None], u1, [None, None, 'data["TOTAL CWTB"][0][0] * (data["TOTAL CWTB"][0][1]**2)'], ['E23', 'G23', 'I23']],
    'TOTAL CYL': [[None, None, None], u1, [None, None, 'data["TOTAL CYL"][0][0] * (data["TOTAL CYL"][0][1]**2)'], ['E26', 'G26', 'I26']],
    'TOTAL MAST': [[None, None, None], u1, [None, None, 'data["TOTAL MAST"][0][0] * (data["TOTAL MAST"][0][1]**2)'], ['E29', 'G29', 'I29']],
    'MATERIAL ON BOOM AND BUCKET WHEEL': [[None, None, None], u1, [None, None, 'data["MATERIAL ON BOOM AND BUCKET WHEEL"][0][0] * (data["MATERIAL ON BOOM AND BUCKET WHEEL"][0][1]**2)'], ['E32', 'G32', 'I32']],

    #chiedono solo 1 input e a volte danno output
    'BOOM LENGTH': [None, 'm', None, 'H41'],
    'MAX BOOM SLEWING SPEED': [[None, None], ['rpm', 'm/min'], [None, 'data["MAX BOOM SLEWING SPEED"][0][0] * 6.28 / 60 * data["BOOM LENGTH"][0]'], ['H43', 'N43']],
    'ACCELERATION TIME': [None, 's', None, 'H46'],
    'FRICTION FACTOR': [None, 'N/t', None, 'H49'],
    'SLEW BEARING PRIMITIVE DIAMETER': [None, 'm', None, 'H52'],
    'MECHANICAL EFFICIENCY': [None, '-', None, 'H55'],
    'RATING WIND PRESSURE': [[None, None, None], ['N/m²', 'm/s', 'km/h'], [None, '(data["RATING WIND PRESSURE"][0][0] / 0.613) ** 0.5', 'data["RATING WIND PRESSURE"][0][1] * 3.6'], ['H58', 'L58', 'N58']],
    'MAXIMUM WIND PRESSURE (TRAVELLING)': [[None, None, None], ['N/m²', 'm/s', 'km/h'], [None, '(data["MAXIMUM WIND PRESSURE (TRAVELLING)"][0][0] / 0.613) ** 0.5', 'data["MAXIMUM WIND PRESSURE (TRAVELLING)"][0][1] * 3.6'], ['H61', 'L61', 'N61']],
    'TOTAL WIND EXPOSED AREA': [None, 'm²', None, 'H64'],
    'DISTANCE FROM THE POINT OF WIND FORCE AND THE ROTATION AXLE': [None, 'm', None, 'H67'],
    'MOTORS NUMBER': [None, '-', None, 'H71'],
    'NOMINAL MOTOR SPEED': [[None, None], [' rpm', 'rad/s'], [None, 'data["NOMINAL MOTOR SPEED"][0][0] * 6.28 / 60'], ['H74', 'L74']],
    'MOTOR INERTIA ( of 1 drive )': [None, 'Kgm2', None, 'H77'], # chiedere unità di misura
    'GEARS AND BRAKE INERTIA ( of 1 drive )': [None, 'Kgm2', None, 'H80'],
    'Lateral digging force': [[None, None], ['t', 'N'], [None, 'data["Lateral digging force"][0][0] * 1000 * 9.81'], ['F140', 'I140']],
    'bucket distance from and slewing axe': [None, 'm', None, 'F142'], # chiedere unità di misura
    'Digging force': [[None, None], ['t', 'N'], [None, 'data["Digging force"][0][0] * 1000 * 9.81'], ['F155', 'I155']], # chiedere unità di misura
    'MODULE': [None, 'mm', None, 'G175'],
    'PINION TEET NUMBER': [None, '-', None, 'G177'],
    'SLEW BEARING TEETH NUMBER': [None, 'mm', None, 'G181'],
    'power of each motor': [None, 'kW', None, 'D251'],
    'coefficent on brake regulation on max absorbed torque': [None, '-', None, 'G228'],
    'yeld stress [N/mm2]': [[None, None], ['pinion teeth stress', 'slew bearing teeth stress'], [None, None], ['P230', 'Q230']],
    'teeth tickness b': [[None, None], ['pinion teeth stress', 'slew bearing teeth stress'], [None, None], ['P231', 'Q231']],
    'Y': [[None, None], ['pinion teeth stress', 'slew bearing teeth stress'], [None, None], ['P232', 'Q232']],
    # output
    'TOT.WEIGHT OF SLEWING PART  =': [[None, None], ['t', 'tm2'], ['sum([data[KEYS[i]][0][0] for i in range(9)])', 'sum([data[KEYS[i]][0][2] for i in range(9)])'], ['E35', 'I35']],

    #'POWER CALCULATION ( for 1 motor ) RIGA 84
    'MOMENT OF INERTIA AT MOTOR SHAFT': [None, 'Kgm2', '(data["TOT.WEIGHT OF SLEWING PART  ="][0][1] * 1000 * (data["MAX BOOM SLEWING SPEED"][0][0] ** 2) / (data["NOMINAL MOTOR SPEED"][0][0] ** 2)) + data["MOTORS NUMBER"][0] * (data["MOTOR INERTIA ( of 1 drive )"][0] + data["GEARS AND BRAKE INERTIA ( of 1 drive )"][0])', 'F91'],
    'FRICTION TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["TOT.WEIGHT OF SLEWING PART  ="][0][0] * data["FRICTION FACTOR"][0] * data["MAX BOOM SLEWING SPEED"][0][0] * data["SLEW BEARING PRIMITIVE DIAMETER"][0] / 2 / data["NOMINAL MOTOR SPEED"][0][0] / data["MECHANICAL EFFICIENCY"][0] / data["MOTORS NUMBER"][0]', 'data["FRICTION TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]'], ['F99', 'F102']],
    'RATING WIND TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["TOTAL WIND EXPOSED AREA"][0] * data["RATING WIND PRESSURE"][0][0] * data["MAX BOOM SLEWING SPEED"][0][0] * data["DISTANCE FROM THE POINT OF WIND FORCE AND THE ROTATION AXLE"][0] / data["NOMINAL MOTOR SPEED"][0][0] / data["MECHANICAL EFFICIENCY"][0] / data["MOTORS NUMBER"][0]', 'data["RATING WIND TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]'], ['F109', 'F112']],
    ' MAX. TRAVELLING WIND  TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["TOTAL WIND EXPOSED AREA"][0] * data["MAXIMUM WIND PRESSURE (TRAVELLING)"][0][0] * data["MAX BOOM SLEWING SPEED"][0][0] * data["DISTANCE FROM THE POINT OF WIND FORCE AND THE ROTATION AXLE"][0] / data["NOMINAL MOTOR SPEED"][0][0] / data["MECHANICAL EFFICIENCY"][0] / data["MOTORS NUMBER"][0]', 'data[" MAX. TRAVELLING WIND  TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]'], ['F119', 'F122']],
    'ACCELERATION TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["MOMENT OF INERTIA AT MOTOR SHAFT"][0] * data["NOMINAL MOTOR SPEED"][0][1] / data["ACCELERATION TIME"][0] / data["MOTORS NUMBER"][0] / data["MECHANICAL EFFICIENCY"][0]', 'data["ACCELERATION TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]'], ['F130', 'F133']],
    'DIGGING TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["Lateral digging force"][0][1] * data["bucket distance from and slewing axe"][0] * data["MAX BOOM SLEWING SPEED"][0][0] / data["NOMINAL MOTOR SPEED"][0][0] / data["MECHANICAL EFFICIENCY"][0] / data["MOTORS NUMBER"][0]', 'data["DIGGING TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]'], ['H146', 'G150']],
    'ABNORMAL DIGGING TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["Digging force"][0][1] * data["bucket distance from and slewing axe"][0] * data["MAX BOOM SLEWING SPEED"][0][0] / data["MOTORS NUMBER"][0] / data["NOMINAL MOTOR SPEED"][0][0] / data["MECHANICAL EFFICIENCY"][0]', 'data["ABNORMAL DIGGING TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]'], ['H161', 'G165']],

    # REDUCTION GEAR TORQUES
    'TOTAL REDUCTION RATIO': [None, '-', 'data["NOMINAL MOTOR SPEED"][0][0] / data["MAX BOOM SLEWING SPEED"][0][0]', 'G173'],
    'PINION DIAMETER':  [None, 'mm', 'data["MODULE"][0] * data["PINION TEET NUMBER"][0]', 'G179'],
    'slewing bearing diameter':  [[None, None], ['mm', 'boolean'], ['data["SLEW BEARING PRIMITIVE DIAMETER"][0] * 1000', '"OK" if (data["SLEW BEARING TEETH NUMBER"][0] * data["MODULE"][0]) == data["slewing bearing diameter"][0][0] else "check teeth number"'], ['G183', 'I183']],
    'slew bearing / pinion ratio':  [None, '-', 'data["slewing bearing diameter"][0][0] / data["PINION DIAMETER"][0]', 'G185'],
    'gear box ratio':  [None, '-', 'data["TOTAL REDUCTION RATIO"][0] / data["slew bearing / pinion ratio"][0]', 'G187'],

    #SUMMARY OF THE LOADS
    'FRICTION':  [[None, None, None, None, None], u2, ['data["FRICTION TORQUE AT MOTOR SHAFT"][0][0]', 'data["FRICTION"][0][0] * data["gear box ratio"][0]', 'data["FRICTION"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["FRICTION"][0][3] / 9.81'], ['E193', 'F193', 'G193', 'H193', 'I193']],
    'RATING WIND':  [[None, None, None, None, None], u2, ['data["RATING WIND TORQUE AT MOTOR SHAFT"][0][0]', 'data["RATING WIND"][0][0] * data["gear box ratio"][0]', 'data["RATING WIND"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["RATING WIND"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["RATING WIND"][0][3] / 9.81'], ['E195', 'F195', 'G195', 'H195', 'I195']],
    'MAX TRAVELLING WIND':  [[None, None, None, None, None], u2, ['data[" MAX. TRAVELLING WIND  TORQUE AT MOTOR SHAFT"][0][0]', 'data["MAX TRAVELLING WIND"][0][0] * data["gear box ratio"][0]', 'data["MAX TRAVELLING WIND"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["MAX TRAVELLING WIND"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["MAX TRAVELLING WIND"][0][3] / 9.81'], ['E197', 'F197', 'G197', 'H197', 'I197']],
    'ACCELERATION':  [[None, None, None, None, None], u2, ['data["ACCELERATION TORQUE AT MOTOR SHAFT"][0][0]', 'data["ACCELERATION"][0][0] * data["gear box ratio"][0]', 'data["ACCELERATION"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["ACCELERATION"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["ACCELERATION"][0][3] / 9.81'], ['E199', 'F199', 'G199', 'H199', 'I199']],
    'NORMAL DIGGING': [[None, None, None, None, None], u2, ['data["DIGGING TORQUE AT MOTOR SHAFT"][0][0]', 'data["NORMAL DIGGING"][0][0] * data["gear box ratio"][0]', 'data["NORMAL DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["NORMAL DIGGING"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["NORMAL DIGGING"][0][3] / 9.81'], ['E201', 'F201', 'G201', 'H201', 'I201']],
    'ABNORMAL DIGGING':  [[None, None, None, None, None], u2, ['data["ABNORMAL DIGGING TORQUE AT MOTOR SHAFT"][0][0]', 'data["ABNORMAL DIGGING"][0][0] * data["gear box ratio"][0]', 'data["ABNORMAL DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["ABNORMAL DIGGING"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["ABNORMAL DIGGING"][0][3] / 9.81'], ['E203', 'F203', 'G203', 'H203', 'I203']],

    #LOAD CONDITION
    'FRICTION AND NORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["NORMAL DIGGING"][0][0] + data["FRICTION"][0][0]', 'data["FRICTION AND NORMAL DIGGING"][0][0] * data["gear box ratio"][0]', 'data["FRICTION AND NORMAL DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION AND NORMAL DIGGING"][0][1] / 9.81', 'data["FRICTION AND NORMAL DIGGING"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1480', 'data["FRICTION AND NORMAL DIGGING"][0][6] / data["gear box ratio"][0]', 'data["FRICTION AND NORMAL DIGGING"][0][7] / data["gear box ratio"][0]', 'data["FRICTION AND NORMAL DIGGING"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND NORMAL DIGGING"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND NORMAL DIGGING"][0][0] * data["FRICTION AND NORMAL DIGGING"][0][14] / 1000', 'data["FRICTION AND NORMAL DIGGING"][0][0] * data["FRICTION AND NORMAL DIGGING"][0][15] / 1000', 'data["FRICTION AND NORMAL DIGGING"][0][6] * 6.28 / 60', 'data["FRICTION AND NORMAL DIGGING"][0][7] * 6.28 / 60'], ['E209', 'F209', 'G209', 'H209', 'I209', 'J209', 'K209', 'L209', 'M209', 'N209', 'O209', 'P209', 'Q209', 'R209', 'S209', 'T209']],
    'FRICTION, RAT. WIND, NORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["FRICTION AND NORMAL DIGGING"][0][0] + data["RATING WIND"][0][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] * data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][1] / 9.81', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1480', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][6] / data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][7] / data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] * data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][14] / 1000', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] * data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][15] / 1000', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][6] * 6.28 / 60', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][7] * 6.28 / 60'], ['E211', 'F211', 'G211', 'H211', 'I211', 'J211', 'K211', 'L211', 'M211', 'N211', 'O211', 'P211', 'Q211', 'R211', 'S211', 'T211']],
    'FRICTION, RAT. WIND, ACC, NOR. DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] + data["ACCELERATION"][0][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] * data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][1] / 9.81', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1280', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][6] / data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][7] / data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] * data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][14] / 1000', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] * data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][15] / 1000', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][6] * 6.28 / 60', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][7] * 6.28 / 60'], ['E213', 'F213', 'G213', 'H213', 'I213', 'J213', 'K213', 'L213', 'M213', 'N213', 'O213', 'P213', 'Q213', 'R213', 'S213', 'T213']],
    'MAX TRAVELLING WIND (STATIC)': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["MAX TRAVELLING WIND"][0][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][0] * data["gear box ratio"][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["MAX TRAVELLING WIND (STATIC)"][0][1] / 9.81', 'data["MAX TRAVELLING WIND (STATIC)"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1000', 'data["MAX TRAVELLING WIND (STATIC)"][0][6] / data["gear box ratio"][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][7] / data["gear box ratio"][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][0] * data["MAX TRAVELLING WIND (STATIC)"][0][14] / 1000', 'data["MAX TRAVELLING WIND (STATIC)"][0][0] * data["MAX TRAVELLING WIND (STATIC)"][0][15] / 1000', 'data["MAX TRAVELLING WIND (STATIC)"][0][6] * 6.28 / 60', 'data["MAX TRAVELLING WIND (STATIC)"][0][7] * 6.28 / 60'], ['E215', 'F215', 'G215', 'H215', 'I215', 'J215', 'K215', 'L215', 'M215', 'N215', 'O215', 'P215', 'Q215', 'R215', 'S215', 'T215']],
    'FRICTION AND ABNORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["FRICTION"][0][0] + data["ABNORMAL DIGGING"][0][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][0] * data["gear box ratio"][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION AND ABNORMAL DIGGING"][0][1] / 9.81', 'data["FRICTION AND ABNORMAL DIGGING"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1480', 'data["FRICTION AND ABNORMAL DIGGING"][0][6] / data["gear box ratio"][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][7] / data["gear box ratio"][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][0] * data["FRICTION AND ABNORMAL DIGGING"][0][14] / 1000', 'data["FRICTION AND ABNORMAL DIGGING"][0][0] * data["FRICTION AND ABNORMAL DIGGING"][0][15] / 1000', 'data["FRICTION AND ABNORMAL DIGGING"][0][6] * 6.28 / 60', 'data["FRICTION AND ABNORMAL DIGGING"][0][7] * 6.28 / 60'], ['E217', 'F217', 'G217', 'H217', 'I217', 'J217', 'K217', 'L217', 'M217', 'N217', 'O217', 'P217', 'Q217', 'R217', 'S217', 'T217']],
    'FRICTION AND RAT. WIND (STACKING)': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["FRICTION"][0][0] + data["RATING WIND"][0][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][0] * data["gear box ratio"][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION AND RAT. WIND (STACKING)"][0][1] / 9.81', 'data["FRICTION AND RAT. WIND (STACKING)"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1480', 'data["FRICTION AND RAT. WIND (STACKING)"][0][6] / data["gear box ratio"][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][7] / data["gear box ratio"][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][0] * data["FRICTION AND RAT. WIND (STACKING)"][0][14] / 1000', 'data["FRICTION AND RAT. WIND (STACKING)"][0][0] * data["FRICTION AND RAT. WIND (STACKING)"][0][15] / 1000', 'data["FRICTION AND RAT. WIND (STACKING)"][0][6] * 6.28 / 60', 'data["FRICTION AND RAT. WIND (STACKING)"][0][7] * 6.28 / 60'], ['E219', 'F219', 'G219', 'H219', 'I219', 'J219', 'K219', 'L219', 'M219', 'N219', 'O219', 'P219', 'Q219', 'R219', 'S219', 'T219']],

    #BRAKES
    'equivalent mass of drives': [None, 't', 'data["MOTORS NUMBER"][0] * (data["MOTOR INERTIA ( of 1 drive )"][0] + data["GEARS AND BRAKE INERTIA ( of 1 drive )"][0]) * data["TOTAL REDUCTION RATIO"][0] ** 2 / data["BOOM LENGTH"][0] ** 2 / 1000', 'G226'],
    'total inertia on each drive': [None, '-', 'data["MOMENT OF INERTIA AT MOTOR SHAFT"][0] / data["MOTORS NUMBER"][0]', 'G227'],
    'Rated brake torque setting': [None, '-', 'data["coefficent on brake regulation on max absorbed torque"][0] * max([data["FRICTION AND NORMAL DIGGING"][0][0], data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0], data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0], data["MAX TRAVELLING WIND (STATIC)"][0][0], data["FRICTION AND ABNORMAL DIGGING"][0][0], data["FRICTION AND RAT. WIND (STACKING)"][0][0]])', 'G229'],


    '-FRICTION AND NORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["FRICTION AND NORMAL DIGGING"][0][0]', 'data["Rated brake torque setting"][0]', 'data["-FRICTION AND NORMAL DIGGING"][0][0] + data["-FRICTION AND NORMAL DIGGING"][0][1]', 'data["total inertia on each drive"][0]', 'data["-FRICTION AND NORMAL DIGGING"][0][2] / data["-FRICTION AND NORMAL DIGGING"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][1]', 'data["-FRICTION AND NORMAL DIGGING"][0][5] / data["-FRICTION AND NORMAL DIGGING"][0][4]', 'data["-FRICTION AND NORMAL DIGGING"][0][2] * data["gear box ratio"][0] / 1000', 'data["-FRICTION AND NORMAL DIGGING"][0][7] / (data["PINION DIAMETER"][0] / 1000 / 2)', 'data["-FRICTION AND NORMAL DIGGING"][0][8] / 9.81', 'data["-FRICTION AND NORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["-FRICTION AND NORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'-FRICTION AND NORMAL DIGGING\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'-FRICTION AND NORMAL DIGGING\'][0][11]:.1f}".replace(".", ",")'], ['E235', 'F235', 'G235', 'H235', 'I235', 'J235', 'K235', 'L235', 'N235', 'O235', 'P235', 'Q235', 'R235']],
    '-FRICTION, RAT. WIND, NORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0]', 'data["Rated brake torque setting"][0]', 'data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] + data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][1]', 'data["total inertia on each drive"][0]', 'data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][2] / data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][1]', 'data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][5] / data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][4]', 'data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][2] * data["gear box ratio"][0] / 1000', 'data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][7] / (data["PINION DIAMETER"][0] / 1000 / 2)', 'data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][8] / 9.81', 'data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["-FRICTION, RAT. WIND, NORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'-FRICTION, RAT. WIND, NORMAL DIGGING\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'-FRICTION, RAT. WIND, NORMAL DIGGING\'][0][11]:.1f}".replace(".", ",")'], ['E237', 'F237', 'G237', 'H237', 'I237', 'J237', 'K237', 'L237', 'N237', 'O237', 'P237', 'Q237', 'R237']],
    '-FRICTION, RAT. WIND, ACC, NOR. DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0]', 'data["Rated brake torque setting"][0]', 'data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] + data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][1]', 'data["total inertia on each drive"][0]', 'data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][2] / data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][1]', 'data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][5] / data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][4]', 'data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][2] * data["gear box ratio"][0] / 1000', 'data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][7] / (data["PINION DIAMETER"][0] / 1000 / 2)', 'data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][8] / 9.81', 'data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["-FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'-FRICTION, RAT. WIND, ACC, NOR. DIGGING\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'-FRICTION, RAT. WIND, ACC, NOR. DIGGING\'][0][11]:.1f}".replace(".", ",")'], ['E239', 'F239', 'G239', 'H239', 'I239', 'J239', 'K239', 'L239', 'N239', 'O239', 'P239', 'Q239', 'R239']],
    '-MAX TRAVELLING WIND (STATIC)': [[None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["MAX TRAVELLING WIND (STATIC)"][0][0]', 'data["Rated brake torque setting"][0]', 'data["-MAX TRAVELLING WIND (STATIC)"][0][0] + data["-MAX TRAVELLING WIND (STATIC)"][0][1]', 'data["total inertia on each drive"][0]', 'data["-MAX TRAVELLING WIND (STATIC)"][0][2] / data["-MAX TRAVELLING WIND (STATIC)"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][1]', 'data["-MAX TRAVELLING WIND (STATIC)"][0][5] / data["-MAX TRAVELLING WIND (STATIC)"][0][4]', 'data["-MAX TRAVELLING WIND (STATIC)"][0][2] * data["gear box ratio"][0] / 1000', 'data["-MAX TRAVELLING WIND (STATIC)"][0][7] / (data["PINION DIAMETER"][0] / 1000 / 2)', 'data["-MAX TRAVELLING WIND (STATIC)"][0][8] / 9.81', 'data["-MAX TRAVELLING WIND (STATIC)"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["-MAX TRAVELLING WIND (STATIC)"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'-MAX TRAVELLING WIND (STATIC)\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'-MAX TRAVELLING WIND (STATIC)\'][0][11]:.1f}".replace(".", ",")'], ['E241', 'F241', 'G241', 'H241', 'I241', 'J241', 'K241', 'L241', 'N241', 'O241', 'P241', 'Q241', 'R241']],
    '-FRICTION AND ABNORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["FRICTION AND ABNORMAL DIGGING"][0][0]', 'data["Rated brake torque setting"][0]', 'data["-FRICTION AND ABNORMAL DIGGING"][0][0] + data["-FRICTION AND ABNORMAL DIGGING"][0][1]', 'data["total inertia on each drive"][0]', 'data["-FRICTION AND ABNORMAL DIGGING"][0][2] / data["-FRICTION AND ABNORMAL DIGGING"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][1]', 'data["-FRICTION AND ABNORMAL DIGGING"][0][5] / data["-FRICTION AND ABNORMAL DIGGING"][0][4]', 'data["-FRICTION AND ABNORMAL DIGGING"][0][2] * data["gear box ratio"][0] / 1000', 'data["-FRICTION AND ABNORMAL DIGGING"][0][7] / (data["PINION DIAMETER"][0] / 1000 / 2)', 'data["-FRICTION AND ABNORMAL DIGGING"][0][8] / 9.81', 'data["-FRICTION AND ABNORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["-FRICTION AND ABNORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'-FRICTION AND ABNORMAL DIGGING\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'-FRICTION AND ABNORMAL DIGGING\'][0][11]:.1f}".replace(".", ",")'], ['E243', 'F243', 'G243', 'H243', 'I243', 'J243', 'K243', 'L243', 'N243', 'O243', 'P243', 'Q243', 'R243']],
    '-FRICTION AND RAT. WIND (STACKING)': [[None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["FRICTION AND RAT. WIND (STACKING)"][0][0]', 'data["Rated brake torque setting"][0]', 'data["-FRICTION AND RAT. WIND (STACKING)"][0][0] + data["-FRICTION AND RAT. WIND (STACKING)"][0][1]', 'data["total inertia on each drive"][0]', 'data["-FRICTION AND RAT. WIND (STACKING)"][0][2] / data["-FRICTION AND RAT. WIND (STACKING)"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][1]', 'data["-FRICTION AND RAT. WIND (STACKING)"][0][5] / data["-FRICTION AND RAT. WIND (STACKING)"][0][4]', 'data["-FRICTION AND RAT. WIND (STACKING)"][0][2] * data["gear box ratio"][0] / 1000', 'data["-FRICTION AND RAT. WIND (STACKING)"][0][7] / (data["PINION DIAMETER"][0] / 1000 / 2)', 'data["-FRICTION AND RAT. WIND (STACKING)"][0][8] / 9.81', 'data["-FRICTION AND RAT. WIND (STACKING)"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["-FRICTION AND RAT. WIND (STACKING)"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'-FRICTION AND RAT. WIND (STACKING)\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'-FRICTION AND RAT. WIND (STACKING)\'][0][11]:.1f}".replace(".", ",")'], ['E245', 'F245', 'G245', 'H245', 'I245', 'J245', 'K245', 'L245', 'N245', 'O245', 'P245', 'Q245', 'R245']]
}

KEYS = list(data.keys())
formule_errate = []


# inserimento dei dati su file Excel
def inserisci_dati_excel(trav_sheet, data):
    for key in ["FRICTION AND NORMAL DIGGING", 'FRICTION, RAT. WIND, NORMAL DIGGING', 'FRICTION, RAT. WIND, ACC, NOR. DIGGING', 'MAX TRAVELLING WIND (STATIC)', 'FRICTION AND ABNORMAL DIGGING', 'FRICTION AND RAT. WIND (STACKING)']:
        data[key][0][5] = data[key][0][5] / 100
    for key in data.keys():
        if type(data[key][3]) is list: # controllo se ha più di una cella
            for i in range(len(data[key][3])): # per ogni posizione
                trav_sheet[data[key][3][i]].value = data[key][0][i] # inserisco il valore
        else: # se non è una lista
            trav_sheet[data[key][3]].value = data[key][0]
    trav_sheet['H38'].value = data['TOT.WEIGHT OF SLEWING PART  ='][0][0]
    trav_sheet['F157'].value = data['bucket distance from and slewing axe'][0]
    trav_sheet['J91'].value = data['MOTORS NUMBER'][0]
    print(data['FRICTION AND NORMAL DIGGING'][0][5])
    trav_sheet['F251'].value = "NOT SATISFIED IN ALL CONDITIONS" if (data['power of each motor'][0] < max([data['FRICTION AND NORMAL DIGGING'][0][13], data['FRICTION, RAT. WIND, NORMAL DIGGING'][0][13], data['FRICTION, RAT. WIND, ACC, NOR. DIGGING'][0][13], data['MAX TRAVELLING WIND (STATIC)'][0][13], data['FRICTION AND ABNORMAL DIGGING'][0][13], data['FRICTION AND RAT. WIND (STACKING)'][0][13]])) else "SATISFIED IN ALL CONDITIONS"


# calcola i dati di output e prende i dati di input
def assegna_valori(dati, data):
    j = 0
    for key in KEYS:
        if type(data[key][2]) is list:
            for i in range(len(data[key][2])):
                if not data[key][2][i]:
                    data[key][0][i] = dati[j]
                    j += 1
        elif not data[key][2]:
            data[key][0] = dati[j]
            j += 1
    # calcolo dei valori di output
    print('\n\nCalculating output values...\n')
    for key in KEYS: # cerca i dati di output
        if type(data[key][2]) is list: # controllo se ha più di un dato
            for i in range(len(data[key][2])): # cerco formule nella lista
                if data[key][2][i]: # se trovo la formula
                    try:
                        data[key][0][i] = eval(data[key][2][i]) # calcolo con eval il dato di output
                    except:
                        formule_errate.append([True, key, i])
        elif data[key][2]: # se è un valore singolo, controllo che sia una formula
             try:
                 data[key][0] = eval(data[key][2]) # calcolo
             except:
                 formule_errate.append([False, key])

    for formula in formule_errate:
        print(formula)
        if formula[0]:
            data[formula[1]][0][formula[2]] = eval(data[formula[1]][2][formula[2]])
        else:
            data[formula[1]][0] = eval(data[formula[1]][2]) # calcolo

def crea_excel(dati):
    # inserimento dei dati su file Excel e salvataggio di un nuovo file
    trav_file = load_workbook('templateBoomSlewing.xlsx') # carico il file Excel completo
    trav_sheet = trav_file.active # carico il foglio singolo, l'unico che è presente, TRAVELLING
    assegna_valori(dati, data)
    inserisci_dati_excel(trav_sheet, data)
    data_corrente = datetime.now().strftime('%Y-%m-%d__%H-%M')
    trav_file_name = 'BoomSlewing__' + data_corrente + '.xlsx'
    root = Tk()  # creo la finestra principale di tkinter
    root.withdraw()  # la nascondo
    print('\nSelect the folder to save the Excel file.')
    new_dir_path = filedialog.askdirectory()  # chiedo dove salvare il file
    new_file_path = os.path.join(new_dir_path, trav_file_name)  # salvo il percorso del file
    trav_file.save(new_file_path)  # salvataggio del file
    print('\nThe new Travelling file was created in ' + new_dir_path)
