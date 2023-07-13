import openpyxl
from openpyxl import Workbook, load_workbook


trav_file = load_workbook('Travelling.xlsx') # carico il file Excel completo

trav_sheet = trav_file.active # carico il foglio singolo, l'unico che è presente, TRAVELLING

trav_sheet['E15'].value = 10 # modifico il valore

trav_file.save('Travelling2.xlsx') # salvo le modifiche in un file con stesso nome, perciò mantengo lo stesso file .xlsx
