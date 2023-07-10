'''
TRAVELLING - a data printable file creator based on input values

I valori delle chiavi hanno un significato basato sulla posizione:
    - 0 = valore
    - 1 = unità di misura
    - 2 = formula di ricavo del valore (se è None, è un dato di input)
    - 3 = caratteristica valore (valore input) o info aggiuntiva (controllo per verificare qualcosa)
'''
import math

E15 = 'Machine dead load'
E16 = 'Tripper / trailer dead load'
E17 = 'Live loads on machine'
E18 = 'Live loads on tripper / trailer'
E20 = 'Dead load and live load'
E21 = 'Dead load'
E22 = '\'Operating wind speed'
E23 = '\'Max wind speed for travelling to parking position'
E24 = 'Out of service wind'
E25 = '\'Equivalent pressure to v1'
E26 = '\'Equivalent pressure to v2'
E27 = '\'Equivalent pressure to v3'
E28 = '\'Max operating speed'
E29 = '\'Max travel speed'
E30 = '\'Max travel, with max travel wind'
E31 = '\'Shape coefficient (according to ISO 5049)'
E32 = '\'Rolling friction factor'
E33 = '\'Static friction factor'
E34 = '\'Fictitious friction factor'
E35 = 'Friction factor to grip limit'
E36 = '\'Rail slope'
E37 = '\'Belt\'s lenght on tripper'
E38 = '\'Lifting height on tripper'
E39 = '\'Max wind area during normal operation'
E40 = '\'Min wind area during traveling to parking'
E41 = '\'Tripper carrying rollers weight (single roller)'
E42 = '\'Tripper carrying rollers pitch'
E43 = '\'Tripper carrying rollers quantity for each station'
E44 = '\'Tripper return rollers weight (single roller)'
E45 = '\'Tripper return rollers pitch'
E46 = '\'Tripper return rollers quantity for each station'
E47 = 'iIdlers weight'
E48 = '\'Belt weight'
E49 = '\'Tripper capacity'
E50 = '\'Tripper conveyor speed'
E51 = '\'Material density'
E52 = '\'Material weight'
E53 = '\'Mechanical efficency '
E54 = 'Acceleration time to max speed'
E55 = 'Acceleration to max speed'
E56 = 'High speed rotating parts inertia'
E58 = 'Wheel and shaft inertia'
E59 = 'Motor, clutch and gear box inertia'
E62F62 = '\'Friction force on rail during normal operation, travelling at c1'
E63F63 = '\'Friction force on rail during travelling at c2'
E66F66 = '\'Max wind force during normal operation (v1), travelling at c1'
E67F67 = '\'Wind force during travelling to parking position (v2), travelling at c2*'
E68 = '\'Storm wind, out of service (v3), static condition'
E71F71 = '\'Force due to yard slope during normal operation, travelling at c1'
E72F72 = '\'Force due to yard slope during travelling at c2'
E75F75 = '\'Force for lifting material on tripper, travelling at c1'
E78F78 = '\'Friction force due to material on tripper'
E81F81 = '\'Friction force due to tripper idlers and belt'
E84F84 = 'Force due to material digging, normal lateral digging force'
E85F85 = 'Force due to material digging, abnormal lateral digging force'
E88F88 = 'Acceleration force'
E92F92G92H92 = 'Normal operation - stacking'
E93F93G93H93 = 'Normal operation acceleration - stacking'
E94F94G94H94 = 'Normal operation - reclaiming'
E95F95G95H95 = 'Normal operation accelaration- reclaiming'
E96F96G96H96 = 'Abnormal operation - reclaiming'
E97F97G97H97 = 'Travelling to parking position with max wind'
H98 = 'Total percentage'
D99 = 'RMS power'
D100 = 'Min power'
D101 = 'Max power'
D105 = '\'Number of drive units'
D106 = '\'Power of each unit'
D107 = 'Motor torque'
D109 = '\'Total installed power'
D110 = 'Total motor torque'
D111 = 'Ratio of installed power vs max absorbed power'
D112 = 'Ratio of installed power vs RMS absorbed power'
D115 = 'Service factor'
D116 = 'Wheel diameter'
D117 = '\'Max travel speed'
D118 = 'Motor speed'
D119 = '\'Wheel speed'
D120 = 'Prereduction gear'
D121 = 'Nominal power'
D122 = 'Reduction ratio'
D123 = 'Nominal torque'
D127 = 'Wheel diameter'
D128 = 'Min load on each wheel (Min operating load in FEM II condition)'
D129 = 'NO_NAME' # non c'è il nome?
D130 = 'Starting factor'
D131 = 'Nom motor torque'
D132 = 'Reduction ratio'
D133 = '\'Min traction force'
D134 = 'Max allowed torque'
D135 = 'Number of motorized wheel for each motor'
D136 = 'Max wheel torque'
D137 = 'Total number of driven wheel'
D138 = 'Total number of wheel (for machine)'
E143 = 'Equivalent mass of motor'
E144 = 'Equivalent mass of wheels'
E145 = 'Equivalent mass of drives'
D147 = 'Rated brake torque setting'
D149 = 'Total brake force against witch the brake shall act during operation'
D150 = 'Total brake force against witch the brake shall act during relocation'

t_D152 = 'Braking forces with all drives installed' # possono servire i titoli per la stampa?

D155 = 'Rolling friction assuming straight travelling, considering dead loading and encrustation'
D156 = 'Braking torque per drive unit'
D157 = 'Braking force per drive unit'
D158 = 'Total braking force per machine'
D159 = 'Max traction under DL + LL'
D160 = 'Total braking and friction force'
D162 = 'Brake quotlent'

D167 = 'Net deceleration force'
D168 = 'Deleleration:'
D169 = 'NO_NAME' # non c'è il nome?
D170 = 'Stopping time at c2 speed'
D171 = 'Stopping distance'

D175 = 'Net deceleration force'
D176 = 'Deleleration:'
D177 = 'NO_NAME' # non c'è il nome?
D178 = 'Stopping time at c2 speed'
D179 = 'Stopping distance'

D182 = 'Design deceleration time'
D183 = 'Design acceleration at c2 speed'
D184 = 'Net force'
D185 = 'Total braking force considering the slope'
D186 = 'Stopping distance, total braking force considering the slope'
D187 = 'Minimum required torque per brake'

D192 = 'Storm wind and slope force'
D193 = 'Total braking force per machine with 2/3 of brakes in function'
D194 = 'Max force for each rail clamp with 2/3 of brakes in function'
D195 = 'Number of rail clamps'
D196 = 'Load of each rail clamp'

current_line = 0 # inizializza l'indice della riga corrente a 0

scelta = 0 # la scelta per il menù che si presenterà all'avvio del programma

data = \
{
    E15: [None, 't', None],
    E16: [None, 't', None],
    E17: [None, 't', None],
    E18: [None, 't', None],
    E20: [None, 't',
          'data[E15][0] + data[E16][0] + '
          'data[E17][0] + data[E18][0]'],
    E21: [None, 't',
          'data[E15][0] + '
          'data[E16][0]'],
    E22: [None, 'km/h', None],
    E23: [None, 'km/h', None],
    E24: [None, 'km/h', None],
    E25: [None, 'N/m²',
          '(data[E22][0]/3.6)**2/16*9.81'],
    E26: [None, 'N/m²',
          '(data[E23][0]/3.6)**2/16*9.81'],
    E27: [None, 'N/m²',
          '(data[E24][0]/3.6)**2/16*9.81'],

    E28: [None, 'm/min', None],
    E29: [None, 'm/min', None],
    E30: [None, 'm/min', None],
    E31: [None, '', None], # no unità
    E32: [None, '', None], # no unità
    E33: [None, '', None], # no unità
    E34: [None, '', None], # no unità
    E35: [None, '', None], # no unità
    E36: [None, '%', None],
    E37: [None, 'm', None],
    E38: [None, 'm', None],
    E39: [None, 'm²', None],
    E40: [None, 'm²', None],
    E41: [None, 'kg', None, None], # quarto valore in input, da chiarire
    E42: [None, 'm', None],
    E43: [None, '', None], # no unità
    E44: [None, '', None, None], # quarto valore in input, da chiarire
    E45: [None, 'm', None],
    E46: [None, '', None], # no unità
    E47: [None, 'kg/m',
           'data[E41][0] * '
           'data[E43][0] / '
           'data[E42][0] + '
           'data[E44][0] * '
           'data[E46][0] / '
           'data[E45][0]'],
    E48: [None, 'kg/m', None],
    E49: [None, 't/h', None],
    E50: [None, 'm/s', None],
    E51: [None, 't/m³', None],
    E52: [None, 'kg/m',
           'data[E49][0] / 3.6 / data[E51][0] / data[E50][0]'],
    E53: [None, '', None], # no unità
    E54: [None, 's', None],
    E55: [None, 'm/s²',
           'data[E29][0] / 60 / data[E54][0]'],
    E56: [None, 'kg m²', None],
    E58: [None, 'kg m²', None],
    E59: [None, 'kg m²', None],

    E62F62: [[None, None], ['kN', 'kW'],
             ['9.81 * data[E20][0] * data[E32][0]',
              'data[E62F62][0][0] * data[E28][0] / 60 / data[E53][0]']],
    E63F63: [[None, None], ['kN', 'kW'],
             ['9.81 * data[E21][0] * data[E32][0]',
              'data[E63F63][0][0] * data[E29][0] / 60 / data[E53][0]']],

    E66F66: [[None, None], ['kN', 'kW'],
             ['data[E31][0] * data[E25][0] * data[E39][0] / 1000',
              'data[E66F66][0][0] * data[E28][0] / 60 / data[E53][0]']],
    E67F67: [[None, None], ['kN', 'kW'],
             ['data[E31][0] * data[E26][0] * data[E40][0] / 1000',
              'data[E67F67][0][0] * data[E30][0] / 60 / data[E53][0]']],
    E68: [None, 'kN',
          'data[E31][0] * data[E27][0] * data[E40][0] / 1000'],

    E71F71: [[None, None], ['kN', 'kW'],
             ['9.81 * data[E20][0] * data[E36][0]',
              'data[E71F71][0][0] * data[E28][0] / 60 / data[E53][0]']],
    E72F72: [[None, None], ['kN', 'kW'],
             ['data[E21][0] * data[E36][0] * 9.81',
              'data[E72F72][0][0] * data[E29][0] / 60 / data[E53][0]']],

    E75F75: [[None, None], ['kN', 'kW'],
         ['9.81 * data[E38][0] * data[E52][0] / 1000',
          'data[E75F75][0][0] * data[E28][0] / 60 / data[E53][0]']],

    E78F78: [[None, None], ['kN', 'kW'],
         ['9.81 * data[E52][0] * data[E37][0] * data[E34][0] / 1000',
          'data[E78F78][0][0] * data[E28][0] / 60 / data[E53][0]']],

    E81F81: [[None, None], ['kN', 'kW'],
         ['9.81 * data[E37][0] * (data[E48][0] + data[E47][0]) * data[E34][0] / 1000',
          'data[E81F81][0][0] * data[E28][0] / 60 / data[E53][0]']],

    E84F84: [[None, None], ['kN', 'kW'],
             [None, 'data[E84F84][0][0] * data[E28][0] / 60 / data[E53][0]']],
    E85F85: [[None, None], ['kN', 'kW'],
             [None, 'data[E85F85][0][0] * data[E28][0] / 60 / data[E53][0]']],

    E88F88: [[None, None], ['kN', 'kW'],
             ['data[E20][0] * data[E55][0]',
              '(data[E88F88][0][0] * data[E28][0] / 60) / data[E53][0]']],

    E92F92G92H92: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   ['data[E62F62][0][0] + data[E66F66][0][0] + data[E71F71][0][0] + data[E75F75][0][0] + data[E78F78][0][0] + data[E81F81][0][0]',
                    'data[E62F62][0][1] + data[E66F66][0][1] + data[E71F71][0][1] + data[E75F75][0][1] + data[E78F78][0][1] + data[E81F81][0][1]',
                    'data[E92F92G92H92][0][1] / data[D105][0]',
                    None]],
    E93F93G93H93: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   [
                   'data[E62F62][0][0] + data[E66F66][0][0] + data[E71F71][0][0] + data[E75F75][0][0] + data[E78F78][0][0] + data[E81F81][0][0] + data[E88F88][0][0]',
                   'data[E62F62][0][1] + data[E66F66][0][1] + data[E71F71][0][1] + data[E75F75][0][1] + data[E78F78][0][1] + data[E81F81][0][1] + data[E88F88][0][1]',
                   'data[E93F93G93H93][0][1] / data[D105][0]',
                   None]],
    E94F94G94H94: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   [
                   'data[E62F62][0][0] + data[E66F66][0][0] + data[E71F71][0][0] + data[E84F84][0][0]',
                   'data[E62F62][0][1] + data[E66F66][0][1] + data[E71F71][0][1] + data[E84F84][0][1]',
                   'data[E94F94G94H94][0][1] / data[D105][0]',
                   None]],
    E95F95G95H95: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   [
                   'data[E62F62][0][0] + data[E66F66][0][0] + data[E71F71][0][0] + data[E84F84][0][0] + data[E88F88][0][0]',
                   'data[E62F62][0][1] + data[E66F66][0][1] + data[E71F71][0][1] + data[E84F84][0][1] + data[E88F88][0][1]',
                   'data[E95F95G95H95][0][1] / data[D105][0]',
                   None]],
    E96F96G96H96: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   [
                   'data[E62F62][0][0] + data[E66F66][0][0] + data[E71F71][0][0] + data[E85F85][0][0]',
                   'data[E62F62][0][1] + data[E66F66][0][1] + data[E71F71][0][1] + data[E85F85][0][1]',
                   'data[E96F96G96H96][0][1] / data[D105][0]',
                       None]],
    E97F97G97H97: [[None, None, None, None], ['kN', 'kW', 'kW', '%'],
                   [
                    'data[E63F63][0][0] + data[E67F67][0][0] + data[E72F72][0][0] + data[E88F88][0][0]',
                    'data[E63F63][0][1] + data[E67F67][0][1] + data[E72F72][0][1] + data[E88F88][0][1]',
                    'data[E97F97G97H97][0][1] / data[D105][0]',
                       None]],
    H98: [None, '%',
           'sum([data[E92F92G92H92][0][3], data[E93F93G93H93][0][3],'
           'data[E94F94G94H94][0][3]), data[E95F95G95H95][0][3],'
           'data[E96F96G96H96][0][3], data[E97F97G97H97][0][3]])'],

    D99: [None, 'kW',
          'math.sqrt(('
          'data[E92F92G92H92][0][1] ** 2 * data[E92F92G92H92][0][3] +'
          'data[E93F93G93H93][0][1] ** 2 * data[E93F93G93H93][0][3] +'
          'data[E94F94G94H94][0][1] ** 2 * data[E94F94G94H94][0][3] +'
          'data[E95F95G95H95][0][1] ** 2 * data[E95F95G95H95][0][3] +'
          'data[E96F96G96H96][0][1] ** 2 * data[E96F96G96H96][0][3] +'
          'data[E97F97G97H97][0][1] ** 2 * data[E97F97G97H97][0][3] +) /'
          'data[H98][0])'],
    D100: [None, 'kW',
           'min([data[E92F92G92H92][0][1], data[E93F93G93H93][0][1],'
           'data[E94F94G94H94][0][1]), data[E95F95G95H95][0][1],'
           'data[E96F96G96H96][0][1], data[E97F97G97H97][0][1]])'],
    D101: [None, 'kW',
           'max([data[E92F92G92H92][0][1], data[E93F93G93H93][0][1],'
           'data[E94F94G94H94][0][1]), data[E95F95G95H95][0][1],'
           'data[E96F96G96H96][0][1], data[E97F97G97H97][0][1]])'],

    D105: [None, '', None],
    D106: [None, 'kW', None],
    D107: [None, 'N m',
           'data[106][0] * 1000 / (data[D118][0] / (60 / 6.28))'],

    D109: [None, 'kW',
           'data[D105][0] * data[D106][0]',
           '"verified" if data[D109][0] > data[D101][0] else "not verified"'],
    D110: [None, 'N m',
           'data[D109][0] * 1000 / (data[D118][0] * 6.28 / 60)'],
    D111: [None, '',
           'data[D109][0] / data[D101][0]'],
    D112: [None, '',
           'data[D109][0] / data[D99][0]',
           '"OK" if data[D112][0] > 1 else "NOT OK"'],

    D115: [None, '', None],
    D116: [None, 'm', None],
    D117: [None, 'm/min', # COPIA DI E29, VALUTARE SE ELIMINARE
           'data[E29][0]'],
    D118: [None, 'rpm', None],
    D119: [None, 'rpm',
           'data[D117][0] * 2 / (data[D116][0] * 2 * 3.14)'],
    D120: [None, '', None],
    D121: [None, 'kW',
           'data[D106][0] * data[D115][0]'],
    D122: [None, '',
           'data[D118][0] / (data[D119][0] * data[D120][0])'],
    D123: [None, 'Nm',
           'data[D107][0] * data[D122][0] * data[D115][0]'],

    D127: [None, 'm',
           'data[D116][0]'], # COPIA DI D116, VALUTARE SE ELIMINARE
    D128: [None, 't', None],
    D129: [None, 'kN',
           'data[D128][0] * 9.8121'],
    D130: [None, '', None],

    D131: [None, 'Nm',
           'data[D130][0] * 60 * 1000 * data[D106][0] / (data[D118][0] * 2 * 3.14)'],
    D132: [None, '',
           'data[D122][0] * data[D120][0]'],
    D133: [None, 'kN',
           'data[E35][0] * data[D129][0]'],
    D134: [None, 'Nm',
           'data[D133][0] * data[D127][0] * 1000 / 2'],
    D135: [None, '', None],
    D136: [None, 'Nm',
           '(data[D131][0] * data[D132][0] / data[D135][0]) * data[E53][0]',
           '"WHEEL/RAIL GRIP VERIFIED" if data[D134][0] > data[D136][0] else "SKIDDING SLIP"'],
    D137: [None, '',
           'data[D135][0] * data[D105][0]'],
    D138: [None, '', None],

    E143: [None, 't',
           'data[D105][0] * data[E59][0] * data[D122][0] ** 2 * 4 / data[D116][0] ** 2 / 1000'],
    E144: [None, 't',
           'data[D138][0] * data[E58][0] * 4 / data[D116][0] ** 2 / 1000'],
    E145: [None, 't',
           'data[E143][0] + data[E144][0]'],

    D147: [None, 'Nm', None],

    D149: [None, 'kN',
           'data[E66][0] + data[E71][0]'],
    D150: [None, 'kN',
           'data[E67][0] + data[E72][0]'],

    D155: [None, 'kN',
           'data[E21][0] * data[E32][0] * 9.81'],
    D156: [None, 'kNm',
           'data[D147][0] * data[D122][0] / 1000'],
    D157: [None, 'kN',
           'data[D156][0] * 2 / data[D116][0]'],
    D158: [None, 'kN',
           'data[D157][0] * data[D105][0]'],
    D159: [None, 'kN',
           'data[E35][0] * data[E15][0] * 9.81 * data[D137][0] / data[D138][0]'],
    D160: [None, 'kN',
           'min([data[D158][0], data[D159][0]]) + data[D155][0]'],

    D162: [None, '',
           'data[D150][0] / data[D160][0],',
           '"OK" if data[D162][0] < 1 else "NOT OK"'],

    # mancano i dati da D167 fino alla fine, D196

}

# richiesta modalità di input dati
print('Choose the data input mode:\n '
      '\t1. manual input: each value is entered by the user, one by one.\n'
      '\t2. file input: a text file is read to retrieve each value, one per line.\n')
scelta = int(input('Your choice: '))

# richiesta dati di input manuale
if scelta == 1:
    print('Insert every values one by one requested.\n')
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
    f.close() # chiudi il file di testo

# calcolo dei valori di output
print('\nCalculating ouput values...\n')
for key in data.keys(): # cerca i dati di output
    if type(data[key][2]) is list: # controllo se ha più di un dato
        for i in range(len(data[key][2])): # cerco formule nella lista
            if data[key][2][i]: # se trovo la lista
                data[key][0][i] = eval(data[key][2][i]) # calcolo con eval il dato di output
    elif data[key][2]: # se è un valore singolo, controllo che sia una formula
         data[key][0] = eval(data[key][2]) # calcolo

# stampa dei valori incolonnati
print("{:<80} {:<10} {:<10}".format("Key", "Value", "Unit")) # header con titoli delle colonne
print('------------------------------------------------------------------------------------------------------')
for key, value in data.items():
    if type(value[0]) is list:
        for i in range(len(data[key][0])):
            if type(value[0][i]) is float:
                formatted_value = '{:.3f}'.format(value[0][i])
                print("{:<80} {:<10} {:<10}".format(key, formatted_value, value[1][i]))
    elif type(value[0]) is float:
        formatted_value = '{:.3f}'.format(value[0])
        print("{:<80} {:<10} {:<10}".format(key, formatted_value, value[1]))
    else:
        print("{:<80} {:<10} {:<10}".format(key, value[0], value[1]))

