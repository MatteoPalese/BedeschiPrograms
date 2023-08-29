# se l'unità di misura è adimensionale inserire -, altrimenti con il vuoto potrebbe dare un errore
# per le formule inserire tra "" o '' il nome della variabile e data['nome'] verrà messo in automatico
# per facilitare l'inserimento delle formule scrivere il nome della variabile circondato da ^nomeFoglio?nomeVariabile^, e se c'è una posizione mettere &index (index sarà un numero)

ret = dict()
nome, valore, unit, formula, cella = '', None, '', '', ''
line_index = 0
print('CREAZIONE DI CHIAVI E VALORI AUTOMATIZZATA')

# prendo i dati
with open('input.txt', 'r') as f:  # apre il file di testo e leggi le righe
    lines = f.readlines()  # crea una lista, ogni riga è un elemento
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    while True:
        print(f'------------------------\n\nUltimo valore inserito = {nome}')
        if lines[line_index] == 'y':
            print(f'Vuoi ottenere il risultato (y / n) --> {lines[line_index]}')
            break

        nome = lines[line_index]
        line_index += 1
        print(f"\n------------------------\nInserisci il nome della variabile: {nome}")

        ''' PARTE NON AGGIORNATA RIGUARDO ALLA LETTURA DEI DATI DA FILE!!!
    
        if input('Contiene più di un valore? (y / n) --> ') == 'y':
          valori, units, formule, celle = [], [], [], []
          for i in range(100):  # se ha più di cento valori mi dispiace
            valori.append(None)
            # units.append(input(f"Inserisci l'unità n. {i}: "))
            formule.append(input(f"Inserisci la formula n.{i + 1}: "))
            celle.append(input(f"Inserisci la cella n.{i + 1}: "))
            if input("I valori sono finiti? (y / n) --> ") == 'y':
              break
            try:  # mi assicuro che non ci siano due variabili con lo stesso nome
              tmp = ret[nome]
            except KeyError:
              ret[nome] = [valori, units, formule, celle]
              continue
            if input(
                'Hai scritto due variabili con lo stesso nome, vuoi cambiarlo? (y / n) --> '
            ) == 'y':
              nome = input(f'Inserisci il nuovo nome (nome precedente: {nome}) --> ')
            ret[nome] = [valori, units, formule, celle]
        else:
          valore = None
          # unit = input("Inserisci l'unità: ")
          formula = input("Inserisci la formula (invio se il dato è di input) --> ")
          cella = input("Inserisci la cella --> ")
          ret[nome] = [valore, unit, formula, cella]
        '''
        valore = None
        # unit = input("Inserisci l'unità: ")
        formula = lines[line_index]
        print(f"Inserisci la formula (invio se il dato è di input) --> {formula}")
        line_index += 2

        ret[nome] = [valore, formula]

'''
# modifico la stringa null con il valore null effettivo e per i valori farò
for key in ret.keys():
  if isinstance(ret[key][1], str):
    for i in range(0, 2, 2):
      if ret[key][i] == "null" or ret[key][i] == "":
        ret[key][i] = None
  else:
    for i in range(0, 2, 2):
      for j in range(len(ret[key][0])):
        if ret[key][i][j] == "null" or ret[key][i][j] == "":
          ret[key][i][j] = None
'''

# modifico la stringhe che contengono le formule
for key in ret.keys():
    if isinstance(ret[key][1], str):
        while '^' in ret[key][1]:
            ret[key][1] = ret[key][1].replace('^', 'data["',
                                              1).replace('^', '"][0]',
                                                         1).replace('?', '"]["')
            if '&' in ret[key][1]:
                index = ret[key][1].index('&')
                ret[key][1] = ret[key][1][:index] + '[' + ret[key][1][index + 1:]
                for i in range(index + 1, len(ret[key][1])):
                    if ord('0') <= ord(ret[key][2][i]) <= ord('9'):
                        index = i
                    else:
                        break
                ret[key][1] = ret[key][1][:index + 1] + ']' + ret[key][1][index + 1:]
    elif ret[key][1] is None:
        pass
    else:
        for j in range(len(ret[key][1])):
            while '^' in ret[key][1][j]:
                ret[key][1][j] = ret[key][1][j].replace('^', 'data["', 1).replace(
                    '^', '"][0]', 1).replace('?', '"]["')
                if '&' in ret[key][1][j]:
                    index = ret[key][1][j].index('&')
                    ret[key][1][
                        j] = ret[key][1][j][:index] + '[' + ret[key][1][j][index + 1:]
                    for i in range(index + 1, len(ret[key][1][j])):
                        if ord('0') <= ord(ret[key][1][j][i]) <= ord('9'):
                            index = i
                        else:
                            break
                    ret[key][1][j] = ret[key][1][j][:index +
                                                     1] + ']' + ret[key][1][j][index + 1:]

# li stampo
print('\nRISULTATO\n')
print('{')
for key in ret.keys():
    print('    "' + key + '": ' + str(ret[key]) + ',')
print('}')
