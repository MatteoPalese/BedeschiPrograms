# BOOM SLEWING

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


current_line = 0
data = \
{
    #chiedono 2 input, e il terzo è un output
    'SLING': [[None, None, None], u1, [None, None, 'data["SLING"][0][0] * (data["SLING"][0][1]**2)']],
    'MFX mast front column': [[None, None, None], u1, [None, None, 'data["MFX mast front column"][0][0] * (data["MFX mast front column"][0][1]**2)']],
    'TOTAL BOOM': [[None, None, None], u1, [None, None, 'data["TOTAL BOOM"][0][0] * (data["TOTAL BOOM"][0][1]**2)']],
    'TOTAL BOOM TIE RODS': [[None, None, None], u1, [None, None, 'data["TOTAL BOOM TIE RODS"][0][0] * (data["TOTAL BOOM TIE RODS"][0][1]**2)']],
    'TOTAL RTR': [[None, None, None], u1, [None, None, 'data["TOTAL RTR"][0][0] * (data["TOTAL RTR"][0][1]**2)']],
    'TOTAL CWTB': [[None, None, None], u1, [None, None, 'data["TOTAL CWTB"][0][0] * (data["TOTAL CWTB"][0][1]**2)']],
    'TOTAL CYL': [[None, None, None], u1, [None, None, 'data["TOTAL CYL"][0][0] * (data["TOTAL CYL"][0][1]**2)']],
    'TOTAL MAST': [[None, None, None], u1, [None, None, 'data["TOTAL MAST"][0][0] * (data["TOTAL MAST"][0][1]**2)']],
    '- MATERIAL ON BOOM AND BUCKET WHEEL': [[None, None, None], u1, [None, None, 'data["- MATERIAL ON BOOM AND BUCKET WHEEL"][0][0] * (data["- MATERIAL ON BOOM AND BUCKET WHEEL"][0][1]**2)']],

    #chiedono solo 1 input e a volte danno output
    'BOOM LENGTH': [None, 'm', None],
    'MAX BOOM SLEWING SPEED': [[None, None], ['rpm', 'm/min'], [None, 'data["MAX BOOM SLEWING SPEED"][0][0] * 6.28 / 60 * data["BOOM LENGTH"][0]']],
    'ACCELERATION TIME': [None, 's', None],
    'FRICTION FACTOR': [None, 'N/t', None],
    'SLEW BEARING PRIMITIVE DIAMETER': [None, 'm', None],
    'MECHANICAL EFFICIENCY': [None, '-', None],
    'RATING WIND PRESSURE': [[None, None, None], ['N/m²', 'm/s', 'km/h'], [None, '(data["RATING WIND PRESSURE"][0][0] / 0.613) ** 0.5', 'data["RATING WIND PRESSURE"][0][1] * 3.6']],
    'MAXIMUM WIND PRESSURE (TRAVELLING)': [[None, None, None], ['N/m²', 'm/s', 'km/h'], [None, '(data["MAXIMUM WIND PRESSURE (TRAVELLING)"][0][0] / 0.613) ** 0.5', 'data["MAXIMUM WIND PRESSURE (TRAVELLING)"][0][1] * 3.6']],
    'TOTAL WIND EXPOSED AREA': [None, 'm²', None],
    'DISTANCE FROM THE POINT OF WIND FORCE AND THE ROTATION AXLE': [None, 'm', None],
    'MOTORS NUMBER': [None, '-', None],
    'NOMINAL MOTOR SPEED': [[None, None], [' rpm', 'rad/s'], [None, 'data["NOMINAL MOTOR SPEED"][0][0] * 6.28 / 60']],
    'MOTOR INERTIA ( of 1 drive )': [None, 'Kgm2', None], # chiedere unità di misura
    'GEARS AND BRAKE INERTIA ( of 1 drive )': [None, 'Kgm2', None],
    'Lateral digging force': [[None, None], ['t', 'N'], [None, 'data["Lateral digging force"][0][0] * 1000 * 9.81']],
    'bucket distance from and slewing axe': [None, 'm', None], # chiedere unità di misura
    'Digging force': [[None, None], ['t', 'N'], [None, 'data["Digging force"][0][0] * 1000 * 9.81']], # chiedere unità di misura
    'MODULE': [None, 'mm', None],
    'PINION TEET NUMBER': [None, '-', None],
    'SLEW BEARING TEETH NUMBER': [None, 'mm', None],
    'power of each motor': [None, '-', None],
    'coefficent on brake regulation on max absorbed torque': [None, '-', None],
    'yeld stress [N/mm2]': [[None, None], ['pinion teeth stress', 'slew bearing teeth stress'], [None, None]],
    'teeth tickness b': [[None, None], ['pinion teeth stress', 'slew bearing teeth stress'], [None, None]],
    'Y': [[None, None], ['pinion teeth stress', 'slew bearing teeth stress'], [None, None]],
    # output
    'TOT.WEIGHT OF SLEWING PART  =': [[None, None, None], u1, ['sum([data[keys[i]][0][0] for i in range(9)])', 'sum([data[keys[i]][0][1] for i in range(9)])', 'sum([data[keys[i]][0][2] for i in range(9)])']],

    #'POWER CALCULATION ( for 1 motor ) RIGA 84
    'MOMENT OF INERTIA AT MOTOR SHAFT': [None, 'Kgm2', '(data["TOT.WEIGHT OF SLEWING PART  ="][0][2] * 1000 * (data["MAX BOOM SLEWING SPEED"][0][0] ** 2) / (data["NOMINAL MOTOR SPEED"][0][0] ** 2)) + data["MOTORS NUMBER"][0] * (data["MOTOR INERTIA ( of 1 drive )"][0] + data["GEARS AND BRAKE INERTIA ( of 1 drive )"][0])'],
    'FRICTION TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["TOT.WEIGHT OF SLEWING PART  ="][0][2] * data["FRICTION FACTOR"][0] * data["MAX BOOM SLEWING SPEED"][0][0] * data["SLEW BEARING PRIMITIVE DIAMETER"][0] / 2 / data["NOMINAL MOTOR SPEED"][0][0] / data["MECHANICAL EFFICIENCY"][0] / data["MOTORS NUMBER"][0]', 'data["FRICTION TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]']],
    'RATING WIND TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["TOTAL WIND EXPOSED AREA"][0] * data["RATING WIND PRESSURE"][0][0] * data["MAX BOOM SLEWING SPEED"][0][0] * data["DISTANCE FROM THE POINT OF WIND FORCE AND THE ROTATION AXLE"][0] / data["NOMINAL MOTOR SPEED"][0][0] / data["MECHANICAL EFFICIENCY"][0] / data["MOTORS NUMBER"][0]', 'data["RATING WIND TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]']],
    ' MAX. TRAVELLING WIND  TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["TOTAL WIND EXPOSED AREA"][0] * data["MAXIMUM WIND PRESSURE (TRAVELLING)"][0][0] * data["MAX BOOM SLEWING SPEED"][0][0] * data["DISTANCE FROM THE POINT OF WIND FORCE AND THE ROTATION AXLE"][0] / data["NOMINAL MOTOR SPEED"][0][0] / data["MECHANICAL EFFICIENCY"][0] / data["MOTORS NUMBER"][0]', 'data[" MAX. TRAVELLING WIND  TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]']],
    'ACCELERATION TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["MOMENT OF INERTIA AT MOTOR SHAFT"][0] * data["NOMINAL MOTOR SPEED"][0][1] / data["ACCELERATION TIME"][0] / data["MOTORS NUMBER"][0] / data["MECHANICAL EFFICIENCY"][0]', 'data["ACCELERATION TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]']],
    'DIGGING TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["TOTAL WIND EXPOSED AREA"][0] * data["MAXIMUM WIND PRESSURE (TRAVELLING)"][0][0] * data["MAX BOOM SLEWING SPEED"][0][0] * data["DISTANCE FROM THE POINT OF WIND FORCE AND THE ROTATION AXLE"][0] / data["NOMINAL MOTOR SPEED"][0][0] / data["MECHANICAL EFFICIENCY"][0] / data["MOTORS NUMBER"][0]', 'data[" MAX. TRAVELLING WIND  TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]']],
    'ABNORMAL DIGGING TORQUE AT MOTOR SHAFT': [[None, None], ['Nm', 'kW'], ['data["Digging force"][0][1] * data["bucket distance from and slewing axe"][0] * data["MAX BOOM SLEWING SPEED"][0][0] / data["MOTORS NUMBER"][0] / data["NOMINAL MOTOR SPEED"][0][0] / data["MECHANICAL EFFICIENCY"][0]', 'data["ABNORMAL DIGGING TORQUE AT MOTOR SHAFT"][0][0] / 1000 * data["NOMINAL MOTOR SPEED"][0][1]']],

    # REDUCTION GEAR TORQUES
    'TOTAL REDUCTION RATIO': [None, '-', 'data["NOMINAL MOTOR SPEED"][0][0] / data["MAX BOOM SLEWING SPEED"][0][0]'],
    'PINION DIAMETER':  [None, 'mm', 'data["MODULE"][0] * data["PINION TEET NUMBER"][0]'],
    'slewing bearing diameter':  [[None, None], ['mm', 'boolean'], ['data["slewing bearing diameter"][0] * 1000', '(data["SLEW BEARING TEETH NUMBER"][0] * data["MODULE"][0]) == data["slewing bearing diameter"][0]']],
    'slew bearing / pinion ratio':  [None, '-', 'data["SLEW BEARING PRIMITIVE DIAMETER"][0] / data["PINION DIAMETER"][0]'],
    'gear box ratio':  [None, '-', 'data["TOTAL REDUCTION RATIO"][0] / data["slew bearing / pinion ratio"][0]'],

    #SUMMARY OF THE LOADS
    'FRICTION':  [[None, None, None, None, None], u2, ['data["FRICTION TORQUE AT MOTOR SHAFT"][0][0]', 'data["FRICTION"][0][0] * data["gear box ratio"][0]', 'data["FRICTION"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["FRICTION"][0][3] / 9.81']],
    'RATING WIND':  [[None, None, None, None, None], u2, ['data["RATING WIND TORQUE AT MOTOR SHAFT"][0][0]', 'data["RATING WIND"][0][0] * data["gear box ratio"][0]', 'data["RATING WIND"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["RATING WIND"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["RATING WIND"][0][3] / 9.81']],
    'MAX TRAVELLING WIND':  [[None, None, None, None, None], u2, ['data[" MAX. TRAVELLING WIND  TORQUE AT MOTOR SHAFT"][0][0]', 'data["MAX TRAVELLING WIND"][0][0] * data["gear box ratio"][0]', 'data["MAX TRAVELLING WIND"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["MAX TRAVELLING WIND"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["MAX TRAVELLING WIND"][0][3] / 9.81']],
    'ACCELERATION':  [[None, None, None, None, None], u2, ['data["ACCELERATION TORQUE AT MOTOR SHAFT"][0][0]', 'data["ACCELERATION"][0][0] * data["gear box ratio"][0]', 'data["ACCELERATION"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["ACCELERATION"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["ACCELERATION"][0][3] / 9.81']],
    'NORMAL DIGGING': [[None, None, None, None, None], u2, ['data["DIGGING TORQUE AT MOTOR SHAFT"][0][0]', 'data["NORMAL DIGGING"][0][0] * data["gear box ratio"][0]', 'data["NORMAL DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["NORMAL DIGGING"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["NORMAL DIGGING"][0][3] / 9.81']],
    'ABNORMAL DIGGING':  [[None, None, None, None, None], u2, ['data["ABNORMAL DIGGING TORQUE AT MOTOR SHAFT"][0][0]', 'data["ABNORMAL DIGGING"][0][0] * data["gear box ratio"][0]', 'data["ABNORMAL DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["ABNORMAL DIGGING"][0][1] / (data["PINION DIAMETER"][0] / 2)', 'data["ABNORMAL DIGGING"][0][3] / 9.81']],

    #LOAD CONDITION
    'FRICTION AND NORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["NORMAL DIGGING"][0][0] + data["FRICTION"][0][0]', 'data["FRICTION AND NORMAL DIGGING"][0][0] * data["gear box ratio"][0]', 'data["FRICTION AND NORMAL DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION AND NORMAL DIGGING"][0][1] / 9.81', 'data["FRICTION AND NORMAL DIGGING"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1480', 'data["FRICTION AND NORMAL DIGGING"][0][6] / data["gear box ratio"][0]', 'data["FRICTION AND NORMAL DIGGING"][0][7] / data["gear box ratio"][0]', 'data["FRICTION AND NORMAL DIGGING"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND NORMAL DIGGING"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND NORMAL DIGGING"][0][0] * data["FRICTION AND NORMAL DIGGING"][0][14] / 1000', 'data["FRICTION AND NORMAL DIGGING"][0][0] * data["FRICTION AND NORMAL DIGGING"][0][15] / 1000', 'data["FRICTION AND NORMAL DIGGING"][0][6] * 6.28 / 60', 'data["FRICTION AND NORMAL DIGGING"][0][7] * 6.28 / 60']],
    'FRICTION, RAT. WIND, NORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["FRICTION AND NORMAL DIGGING"][0][0] + data["RATING WIND"][0][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] * data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][1] / 9.81', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1480', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][6] / data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][7] / data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] * data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][14] / 1000', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] * data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][15] / 1000', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][6] * 6.28 / 60', 'data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][7] * 6.28 / 60']],
    'FRICTION, RAT. WIND, ACC, NOR. DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] + data["ACCELERATION"][0][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] * data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][1] / 9.81', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1480', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][6] / data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][7] / data["gear box ratio"][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] * data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][14] / 1000', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] * data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][15] / 1000', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][6] * 6.28 / 60', 'data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][7] * 6.28 / 60']],
    'MAX TRAVELLING WIND (STATIC)': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["MAX TRAVELLING WIND"][0][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][0] * data["gear box ratio"][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["MAX TRAVELLING WIND (STATIC)"][0][1] / 9.81', 'data["MAX TRAVELLING WIND (STATIC)"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1480', 'data["MAX TRAVELLING WIND (STATIC)"][0][6] / data["gear box ratio"][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][7] / data["gear box ratio"][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["MAX TRAVELLING WIND (STATIC)"][0][0] * data["MAX TRAVELLING WIND (STATIC)"][0][14] / 1000', 'data["MAX TRAVELLING WIND (STATIC)"][0][0] * data["MAX TRAVELLING WIND (STATIC)"][0][15] / 1000', 'data["MAX TRAVELLING WIND (STATIC)"][0][6] * 6.28 / 60', 'data["MAX TRAVELLING WIND (STATIC)"][0][7] * 6.28 / 60']],
    'FRICTION AND ABNORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["FRICTION"][0][0] + data["ABNORMAL DIGGING"][0][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][0] * data["gear box ratio"][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION AND ABNORMAL DIGGING"][0][1] / 9.81', 'data["FRICTION AND ABNORMAL DIGGING"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1480', 'data["FRICTION AND ABNORMAL DIGGING"][0][6] / data["gear box ratio"][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][7] / data["gear box ratio"][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND ABNORMAL DIGGING"][0][0] * data["FRICTION AND ABNORMAL DIGGING"][0][14] / 1000', 'data["FRICTION AND ABNORMAL DIGGING"][0][0] * data["FRICTION AND ABNORMAL DIGGING"][0][15] / 1000', 'data["FRICTION AND ABNORMAL DIGGING"][0][6] * 6.28 / 60', 'data["FRICTION AND ABNORMAL DIGGING"][0][7] * 6.28 / 60']],
    'FRICTION AND RAT. WIND (STACKING)': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u3, ['data["FRICTION"][0][0] + data["RATING WIND"][0][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][0] * data["gear box ratio"][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][0] * data["NOMINAL MOTOR SPEED"][0][1] / 1000', 'data["FRICTION AND RAT. WIND (STACKING)"][0][1] / 9.81', 'data["FRICTION AND RAT. WIND (STACKING)"][0][0] * data["gear box ratio"][0] / (data["PINION DIAMETER"][0] / 2)', None, '615', '1480', 'data["FRICTION AND RAT. WIND (STACKING)"][0][6] / data["gear box ratio"][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][7] / data["gear box ratio"][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][8] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][9] / data["slew bearing / pinion ratio"][0] * 6.28 * data["BOOM LENGTH"][0]', 'data["FRICTION AND RAT. WIND (STACKING)"][0][0] * data["FRICTION AND RAT. WIND (STACKING)"][0][14] / 1000', 'data["FRICTION AND RAT. WIND (STACKING)"][0][0] * data["FRICTION AND RAT. WIND (STACKING)"][0][15] / 1000', 'data["FRICTION AND RAT. WIND (STACKING)"][0][6] * 6.28 / 60', 'data["FRICTION AND RAT. WIND (STACKING)"][0][7] * 6.28 / 60']],

    #BRAKES
    'equivalent mass of drives': [None, 't', 'data["MOTORS NUMBER"][0] * (data["MOTOR INERTIA ( of 1 drive )"][0] + data["GEARS AND BRAKE INERTIA ( of 1 drive )"][0]) * data["TOTAL REDUCTION RATIO"][0] ** 2 / data["BOOM LENGTH"][0] ** 2 / 1000'],
    'total inertia on each drive': [None, '-', 'data["MOMENT OF INERTIA AT MOTOR SHAFT"][0] / data["MOTORS NUMBER"][0]'],
    'Rated brake torque setting': [None, '-', 'data["coefficent on brake regulation on max absorbed torque"][0] * max([data["FRICTION AND NORMAL DIGGING"][0][0], data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0], data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0], data["MAX TRAVELLING WIND (STATIC)"][0][0], data["FRICTION AND ABNORMAL DIGGING"][0][0], data["FRICTION AND RAT. WIND (STACKING)"][0][0]])'],


    '\'FRICTION AND NORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["FRICTION AND NORMAL DIGGING"][0][0]', 'data["Rated brake torque setting"][0]', 'data["\'FRICTION AND NORMAL DIGGING"][0][0] + data["\'FRICTION AND NORMAL DIGGING"][0][1]', 'data["total inertia on each drive"][0]', 'data["\'FRICTION AND NORMAL DIGGING"][0][2] / data["\'FRICTION AND NORMAL DIGGING"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][0]', 'data["\'FRICTION AND NORMAL DIGGING"][0][4] / data["\'FRICTION AND NORMAL DIGGING"][0][5]', 'data["\'FRICTION AND NORMAL DIGGING"][0][2] * data["gear box ratio"][0] / 1000', 'data["\'FRICTION AND NORMAL DIGGING"][0][7] / (data["gear box ratio"][0] / 1000 / 2)', 'data["\'FRICTION AND NORMAL DIGGING"][0][8] / 9.81', 'data["\'FRICTION AND NORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["\'FRICTION AND NORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'\'FRICTION AND NORMAL DIGGING\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'\'FRICTION AND NORMAL DIGGING\'][0][11]:.1f}"']],
    '\'FRICTION, RAT. WIND, NORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["FRICTION, RAT. WIND, NORMAL DIGGING"][0][0]', 'data["Rated brake torque setting"][0]', 'data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][0] + data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][1]', 'data["total inertia on each drive"][0]', 'data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][2] / data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][0]', 'data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][4] / data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][5]', 'data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][2] * data["gear box ratio"][0] / 1000', 'data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][7] / (data["gear box ratio"][0] / 1000 / 2)', 'data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][8] / 9.81', 'data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["\'FRICTION, RAT. WIND, NORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'\'FRICTION, RAT. WIND, NORMAL DIGGING\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'\'FRICTION, RAT. WIND, NORMAL DIGGING\'][0][11]:.1f}"']],
    '\'FRICTION, RAT. WIND, ACC, NOR. DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0]', 'data["Rated brake torque setting"][0]', 'data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][0] + data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][1]', 'data["total inertia on each drive"][0]', 'data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][2] / data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][0]', 'data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][4] / data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][5]', 'data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][2] * data["gear box ratio"][0] / 1000', 'data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][7] / (data["gear box ratio"][0] / 1000 / 2)', 'data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][8] / 9.81', 'data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["\'FRICTION, RAT. WIND, ACC, NOR. DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'\'FRICTION, RAT. WIND, ACC, NOR. DIGGING\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'\'FRICTION, RAT. WIND, ACC, NOR. DIGGING\'][0][11]:.1f}"']],
    '\'MAX TRAVELLING WIND (STATIC)': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["MAX TRAVELLING WIND (STATIC)"][0][0]', 'data["Rated brake torque setting"][0]', 'data["\'MAX TRAVELLING WIND (STATIC)"][0][0] + data["\'MAX TRAVELLING WIND (STATIC)"][0][1]', 'data["total inertia on each drive"][0]', 'data["\'MAX TRAVELLING WIND (STATIC)"][0][2] / data["\'MAX TRAVELLING WIND (STATIC)"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][0]', 'data["\'MAX TRAVELLING WIND (STATIC)"][0][4] / data["\'MAX TRAVELLING WIND (STATIC)"][0][5]', 'data["\'MAX TRAVELLING WIND (STATIC)"][0][2] * data["gear box ratio"][0] / 1000', 'data["\'MAX TRAVELLING WIND (STATIC)"][0][7] / (data["gear box ratio"][0] / 1000 / 2)', 'data["\'MAX TRAVELLING WIND (STATIC)"][0][8] / 9.81', 'data["\'MAX TRAVELLING WIND (STATIC)"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["\'MAX TRAVELLING WIND (STATIC)"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'\'MAX TRAVELLING WIND (STATIC)\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'\'MAX TRAVELLING WIND (STATIC)\'][0][11]:.1f}"']],
    '\'FRICTION AND ABNORMAL DIGGING': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["FRICTION AND ABNORMAL DIGGING"][0][0]', 'data["Rated brake torque setting"][0]', 'data["\'FRICTION AND ABNORMAL DIGGING"][0][0] + data["\'FRICTION AND ABNORMAL DIGGING"][0][1]', 'data["total inertia on each drive"][0]', 'data["\'FRICTION AND ABNORMAL DIGGING"][0][2] / data["\'FRICTION AND ABNORMAL DIGGING"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][0]', 'data["\'FRICTION AND ABNORMAL DIGGING"][0][4] / data["\'FRICTION AND ABNORMAL DIGGING"][0][5]', 'data["\'FRICTION AND ABNORMAL DIGGING"][0][2] * data["gear box ratio"][0] / 1000', 'data["\'FRICTION AND ABNORMAL DIGGING"][0][7] / (data["gear box ratio"][0] / 1000 / 2)', 'data["\'FRICTION AND ABNORMAL DIGGING"][0][8] / 9.81', 'data["\'FRICTION AND ABNORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["\'FRICTION AND ABNORMAL DIGGING"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'\'FRICTION AND ABNORMAL DIGGING\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'\'FRICTION AND ABNORMAL DIGGING\'][0][11]:.1f}"']],
    '\'FRICTION AND RAT. WIND (STACKING)': [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], u4, ['data["FRICTION AND RAT. WIND (STACKING)"][0][0]', 'data["Rated brake torque setting"][0]', 'data["\'FRICTION AND RAT. WIND (STACKING)"][0][0] + data["\'FRICTION AND RAT. WIND (STACKING)"][0][1]', 'data["total inertia on each drive"][0]', 'data["\'FRICTION AND RAT. WIND (STACKING)"][0][2] / data["\'FRICTION AND RAT. WIND (STACKING)"][0][3]', 'data["NOMINAL MOTOR SPEED"][0][0]', 'data["\'FRICTION AND RAT. WIND (STACKING)"][0][4] / data["\'FRICTION AND RAT. WIND (STACKING)"][0][5]', 'data["\'FRICTION AND RAT. WIND (STACKING)"][0][2] * data["gear box ratio"][0] / 1000', 'data["\'FRICTION AND RAT. WIND (STACKING)"][0][7] / (data["gear box ratio"][0] / 1000 / 2)', 'data["\'FRICTION AND RAT. WIND (STACKING)"][0][8] / 9.81', 'data["\'FRICTION AND RAT. WIND (STACKING)"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][0] / data["teeth tickness b"][0][0]', 'data["\'FRICTION AND RAT. WIND (STACKING)"][0][8] * 1000 / data["MODULE"][0] / data["Y"][0][1] / data["teeth tickness b"][0][1]', 'f"{data[\'yeld stress [N/mm2]\'][0][0] / data[\'\'FRICTION AND RAT. WIND (STACKING)\'][0][10]:.1f} ; {data[\'yeld stress [N/mm2]\'][0][1] / data[\'\'FRICTION AND RAT. WIND (STACKING)\'][0][11]:.1f}']],





}

keys = list(data.keys())
formule_errate = []

# richiesta modalità di input dati
print('Choose the data input mode:\n\t1. manual input: each value is entered by the user, one by one.\n\t2. file input: a text file is read to retrieve each value, one per line.\n')
scelta = int(input('Your choice: '))

# richiesta dati di input manuale
if scelta == 1:
    # richiesta dati di input
    print('Insert every values as requested.\n')
    for key in data.keys(): # cerca i dati di input controllando il terzo valore
        if type(data[key][2]) is list: # controllo se ha più di un dato
            for i in range(len(data[key][2])): # cerco None nella lista
                if not data[key][2][i]: # se lo trovo
                    try: # prendo l'input
                        data[key][0][i] = float(input(key + '(' + data[key][1][i] + '): '))
                    except ValueError: # se non viene inserito il valore corretto
                        print('\nLast input data is not valid.')
                        exit(-1) # fermo il programma
        else: # se è un singolo valore
            if not data[key][2]:  # controllo se è dato di input
                try: # se lo è
                    data[key][0] = float(input(key + '(' + data[key][1] + '): '))
                except ValueError:
                    print('\nLast input data is not valid.')
                    exit(-1)
# lettura dati input da file
elif scelta == 2:
    print('\nReading file...')
    with open('data_sample.txt', 'r') as f: # apre il file di testo e leggi le righe
        lines = f.readlines() # crea una lista, ogni riga è un elemento
    for key in data.keys():
        if type(data[key][2]) is list:
            for i in range(len(data[key][2])):
                if not data[key][2][i]:
                    try:
                        data[key][0][i] = float(lines[current_line].strip()) # legge la riga corrente e incrementa l'indice della riga corrente
                        current_line += 1
                    except ValueError:
                        print('\nFile input data is not valid at line ' + str(current_line) + '.')
                        exit(-1)
        else:
            if not data[key][2]:
                try:
                    data[key][0] = float(lines[current_line].strip()) # legge la riga corrente e incrementa l'indice della riga corrente
                    current_line += 1
                except ValueError:
                    print('\nFile input data is not valid at line ' + str(current_line) + '.')
                    exit(-1)


# calcolo dei valori di output
print('\n\nCalculating output values...\n')
for key in data.keys(): # cerca i dati di output
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
        print(str(data[formula[1]][2][formula[2]]) + " - " + formula[1] + ' - ' + str(formula[2]))
        print(data["\'FRICTION AND NORMAL DIGGING"][0][5])
        data[formula[1]][0][formula[2]] = eval(data[formula[1]][2][formula[2]])
    else:
        print(f'{data[formula[1]][2]} - {formula[1]}')
        data[formula[1]][0] = eval(data[formula[1]][2]) # calcolo

for key, value in data.items():
    print(f"{key}: {value}")
