import tkinter as tk
from tkinter import filedialog
from pathlib import Path

# Crea una finestra vuota
root = tk.Tk()
root.withdraw()

# Mostra la finestra di dialogo per selezionare il percorso e il nome del file
file_path = filedialog.asksaveasfilename(defaultextension='.txt')

# Crea il file vuoto utilizzando pathlib
Path(file_path).touch()

print(f'File creato in: {file_path}')
