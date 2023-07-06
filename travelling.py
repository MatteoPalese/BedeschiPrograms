'''
TRAVELLING - a data printable file creator based on input values

I valori delle chiavi hanno un significato basato sulla posizione:
    - 0 = valore
    - 1 = unità di misura
    - 2 = formula di ricavo del valore (se è None, è un dato di input)
    - 3 = caratteristica valore (?) (vedi linea 45)
'''

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

current_line = 0 # inizializza l'indice della riga corrente a 0


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

    # da finire!!!!!!!!!!!
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
                    data[key][0] = int(input(key + '(' + data[key][1] + '): '))
                except ValueError:
                    print('\nLast input data is not valid.')
                    exit(-1)
# lettura dati input da file
elif scelta == 2:
    print('\nReading file...')
    with open('data.txt', 'r') as f: # apre il file di testo e leggi le righe
        lines = f.readlines() # crea una lista, ogni riga è un elemento
    for key in data.keys():
        if type(data[key][2]) is list:
            for i in range(len(data[key][2])):
                if not data[key][2][i]:
                    try:
                        data[key][0][i] = float(lines[current_line].strip()) # legge la riga corrente e incrementa l'indice della riga corrente
                        current_line += 1
                    except ValueError:
                        print('\nLast input data is not valid.')
                        exit(-1)
        else:
            if not data[key][2]:
                try:
                    data[key][0] = int(lines[current_line].strip()) # legge la riga corrente e incrementa l'indice della riga corrente
                    current_line += 1
                except ValueError:
                    print('\nLast input data is not valid.')
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

