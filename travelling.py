'''
TRAVELLING - a data printable file creator based on input values

I valori delle chiavi hanno un significato basato sulla posizione:
    - 0 = valore
    - 1 = unità di misura
    - 2 = formula di ricavo del valore (se è None, è un dato di input)
'''

data = \
{
    'Machine dead load': [None, 't', None],
    'Tripper / trailer dead load': [None, 't', None],
    'Live loads on machine': [None, 't', None],
    'Live loads on tripper / trailer': [None, 't', None],
    'Dead load and live load': [None, 't',
                                'data["Machine dead load"][0] + data["Tripper / trailer dead load"][0] + '
                                'data["Live loads on machine"][0] + data["Live loads on tripper / trailer"][0]'],
    'Dead load': [None, 't',
                  'data["Machine dead load"][0] + '
                  'data["Tripper / trailer dead load"][0]'],
    '\'Operating wind speed': [None, 'km/h', None],
    '\'Max wind speed for travelling to parking position': [None, 'km/h', None],
    'Out of service wind': [None, 'km/h', None],
    '\'Equivalent pressure to v1': [None, 'N/m²',
                                    '(data["\'Operating wind speed"][0]/3.6)**2/16*9.81'],
    '\'Equivalent pressure to v2': [None, 'N/m²',
                                    '(data["\'Max wind speed for travelling to parking position"][0]/3.6)**2/16*9.81'],
    '\'Equivalent pressure to v3': [None, 'N/m²',
                                    '(data["Out of service wind"][0]/3.6)**2/16*9.81'],
    '\'Max operating speed': [None, 'm/min', None],
    '\'Max travel speed': [None, 'm/min', None],
    '\'Max travel, with max travel wind': [None, 'm/min', None],
    '\'Shape coefficient (according to ISO 5049)': [None, '', None], # no unità
    '\'Rolling friction factor': [None, '', None], # no unità
    '\'Static friction factor': [None, '', None], # no unità
    '\'Fictitious friction factor': [None, '', None], # no unità
    'Friction factor to grip limit': [None, '', None], # no unità
    '\'Rail slope': [None, '%', None],
    '\'Belt\'s lenght on tripper': [None, 'm', None],
    '\'Lifting height on tripper': [None, 'm', None],
    '\'Max wind area during normal operation': [None, 'm²', None],
    '\'Min wind area during traveling to parking': [None, 'm²', None],
    '\'Tripper carrying rollers weight (single roller)': [None, 'kg', None, None], # quarto valore in input, da chiarire
    '\'Tripper carrying rollers pitch': [None, 'm', None],
    '\'Tripper carrying rollers quantity for each station': [None, '', None], # no unità
    '\'Tripper return rollers weight (single roller)': [None, '', None, None], # quarto valore in input, da chiarire
    '\'Tripper return rollers pitch': [None, 'm', None],
    '\'Tripper return rollers quantity for each station': [None, '', None], # no unità
    'iIdlers weight': [None, 'kg/m',
                       'data["\'Tripper carrying rollers weight (single roller)"][0] * '
                       'data["\'Tripper return rollers quantity for each station"][0] / '
                       'data["\'Tripper carrying rollers pitch"][0] + '
                       'data["\'Tripper return rollers weight (single roller)"][0] * '
                       'data["\'Tripper return rollers quantity for each station"][0] / '
                       'data["\'Tripper return rollers pitch"][0]'],
    '\'Belt weight': [None, 'kg/m', None],
    '\'Tripper capacity': [None, 't/h', None],
    '\'Tripper conveyor speed': [None, 'm/s', None],
    '\'Material density': [None, 't/m³', None],
    '\'Material weight': [None, 'kg/m',
                          'data["\'Tripper capacity"][0] / 3.6 / data["\'Material density"][0] / data["\'Tripper conveyor speed"][0]'],
    '\'Mechanical efficency ': [None, '', None], # no unità
    'Acceleration time to max speed': [None, 's', None],
    'Acceleration to max speed': [None, 'm/s²',
                                  'data["\'Max travel speed"][0] / 60 / data["Acceleration time to max speed"][0]'],
    'High speed rotating parts inertia': [None, 'kg m²', None],
    'Wheel and shaft inertia': [None, 'kg m²', None],
    'Motor, clutch and gear box inertia': [None, 'kg m²', None],

    # da finire!!!!!!!!!!!
}

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
                data[key][0] = int(input(key + '(' + data[key][1] + '): '))
            except ValueError:
                print('\nLast input data is not valid.')
                exit(-1)

# calcolo dei valori di output
print('\n\nCalculating ouput values...\n')
for key in data.keys(): # cerca i dati di output
    if type(data[key][2]) is list: # controllo se ha più di un dato
        for i in range(len(data[key][2])): # cerco formule nella lista
            if data[key][2][i]: # se trovo la lista
                data[key][0][i] = eval(data[key][2][i]) # calcolo con eval il dato di output
    elif data[key][2]: # se è un valore singolo, controllo che sia una formula
         data[key][0] = eval(data[key][2]) # calcolo

for key, value in data.items():
    print(f"{key}: {value}")
