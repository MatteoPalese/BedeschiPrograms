# se l'unità di misura è adimensionale inserire -, altrimenti con il vuoto potrebbe dare un errore
# per le formule inserire tra "" o '' il nome della variabile e data['nome'] verrà messo in automatico
# per facilitare l'inserimento delle formule scrivere il nome della variabile circondato da ^nome^, e se c'è una posizione mettere &index (index sarà un numero)

ret = dict()
nome, valore, unit, formula = '', 0, '', ''
print('AUTO INSERIMENTO DATI')
# prendo i dati
while True:
    print()
    print(f'Ultimo valore inserito = {nome}')
    if input('Vuoi ottenere il risultato (y = si): ') == 'y':
        break
    nome = input("Inserisci il nome della variabile: ")
    if input('Contiene più di un valore (y = si): ') == 'y':
        valori, units, formule = [], [], []
        for i in range(100):  # se ha più di cento valori mi dispiace
            valori.append(input(f"Inserisci il valore n. {i + 1}: "))
            # units.append(input(f"Inserisci l'unità n. {i}: "))
            formule.append(input(f"Inserisci la formula n. {i + 1}: "))
            if input("I valori sono finiti (y = si): ") == 'y':
                break
            try:  # mi assicuro che non ci siano due variabili con lo stesso nome
                tmp = ret[nome]
            except KeyError:
                ret[nome] = [valori, units, formule]
                continue
            if input(
                    'Hai scritto due variabili con lo stesso nome, vuoi cambiarlo (y = si): '
            ) == 'y':
                nome = input(f'Inserisci il nuovo nome (nomePrecedente = {nome}): ')
            ret[nome] = [valori, units, formule]
    else:
        valore = input('Inserisci il valore (niente/null = input): ')
        # unit = input("Inserisci l'unità: ")
        formula = input("Inserisci la formula (null = input): ")
        ret[nome] = [valore, unit, formula]

# modifico la stringa null con il valore null effettivo e per i valori farò
for key in ret.keys():
    if isinstance(ret[key][0], str):
        for i in range(0, 3, 2):
            if ret[key][i] == "null" or ret[key][i] == "":
                ret[key][i] = None
    else:
        for i in range(0, 3, 2):
            for j in range(len(ret[key][0])):
                if ret[key][i][j] == "null" or ret[key][i][j] == "":
                    ret[key][i][j] = None

# modifico la stringhe che contengono le formule
for key in ret.keys():
    if isinstance(ret[key][2], str):
        while '^' in ret[key][2]:
            ret[key][2] = ret[key][2].replace('^', 'data["', 1)
            ret[key][2] = ret[key][2].replace('^', '"][0]', 1)
            if '&' in ret[key][2]:
                index = ret[key][2].index('&')
                ret[key][2] = ret[key][2][:index] + '[' + ret[key][2][index + 1:]
                for i in range(index + 1, len(ret[key][2])):
                    if ord('0') <= ord(ret[key][2][i]) <= ord('9'):
                        index = i
                    else:
                        break
                ret[key][2] = ret[key][2][:index + 1] + ']' + ret[key][2][index + 1:]
    elif ret[key][2] is None:
        pass
    else:
        for j in range(len(ret[key][2])):
            while '^' in ret[key][2][j]:
                ret[key][2][j] = ret[key][2][j].replace('^', 'data["', 1)
                ret[key][2][j] = ret[key][2][j].replace('^', '"][0]', 1)
                if '&' in ret[key][2][j]:
                    index = ret[key][2][j].index('&')
                    ret[key][2][j] = ret[key][2][j][:index] + '[' + ret[key][2][j][index + 1:]
                    for i in range(index + 1, len(ret[key][2][j])):
                        if ord('0') <= ord(ret[key][2][j][i]) <= ord('9'):
                            index = i
                        else:
                            break
                    ret[key][2][j] = ret[key][2][j][:index + 1] + ']' + ret[key][2][j][index + 1:]

# li stampo
print('\nRISULTATO\n')
print('{')
for key in ret.keys():
    tmp = ret[key]
    tmp.pop(1)
    print('    "' + key + '": ' + str(tmp) + ',')
print('}')
