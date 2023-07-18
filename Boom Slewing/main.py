# Creazione di un programma per creare un file Excel con le informazioni relative al boom slewing.

from dataCalculator import *
from tkinter import *


# FUNZIONI ----------------------------------------------------------------------
# i due eventi relativi alla finestra associati al ridimensionamento e alla rotella del mouse
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# Aggiunge una riga nella finestra con il formato --> Descrizione [   ] unità_di_misura
def aggiungi_riga(descrizione, unita_di_misura, n_riga):
    text_fields.append(Entry(input_frame, width=10, background='#e8f0ff'))
    Label(input_frame, text=descrizione, font='Helvetica 12', background='white', padx=10).grid(row=n_riga+1, column=0, sticky="W")
    text_fields[-1].grid(row=n_riga+1, column=1, sticky='W', padx=0, pady=10)
    Label(input_frame, text=unita_di_misura, font='Helvetica 12', background='white').grid(row=n_riga+1, column=2, sticky="W", padx=10)


# Aggiunge una riga nella finestra con il formato --> Chiave [   ] unita_di_misura
def aggiungi_riga_multipla(key, unita_di_misura, i):
    text_fields.append(Entry(input_frame))
    Label(input_frame, text=key + ' [' + unita_di_misura + ']', font=('Times New Roman', 12)).grid(row=i+1, column=0, sticky="W")
    text_fields[i].grid(row=i+1, column=1, sticky='W', padx=0, pady=10)


# Crea un file Excel con i dati inseriti dall'utente
def submit(texts):
    numeri = []
    for text in texts:
        try:
            numeri.append(float(text.get()))
        except ValueError:
            print('ERRORE NEI DATI!')
            return
    crea_excel(numeri)
    exit(1)


# INTERFACCIA UTENTE -------------------------------------------------------------

# Creazione della finestra dotata di scrollbar
window = Tk()
window.geometry('800x600')
window.resizable(False, False)
window.title('Boom Slewing Excel File Creator')

# Organizzazione in sezioni logiche
main_frame = Frame(window)
main_frame.pack(fill=BOTH, expand=1)

# Creazione di un canvas con scrollbar per inserire molte righe nella finestra
canvas_frame = Frame(main_frame)
canvas_frame.pack(fill=BOTH, expand=1)
canvas = Canvas(canvas_frame, bg='white', highlightthickness=0)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
input_frame = Frame(canvas)
input_frame.pack(side=TOP, fill=X, padx=10, pady=10)
input_frame.configure(background='white')
canvas.create_window((0, 0), window=input_frame, anchor="nw")
canvas.bind("<Configure>", on_configure)
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Posizionamento titolo
Label(input_frame, text='Boom Slewing Excel File Creator', fg='#002975', font='Helvetica 22 bold', background='white').grid(row=0, column=0, padx=0, pady=15, columnspan=3)

# Inserimento di ogni riga nella finestra
i = 0
text_fields = []
for key in KEYS:
    if isinstance(data[key][1], list):
        for j in range(len(data[key][1])):
            if data[key][2][j]:
                continue
            aggiungi_riga_multipla(key, data[key][1][j], i)
            i += 1
    else:
        aggiungi_riga_multipla(key, data[key][1], i)
        i += 1

# Pulsante per creare il file Excel
submit_button = Button(input_frame, command=lambda: submit(text_fields), background='#b3deff', text='CREA FILE EXCEL', font='Helvetica 12 bold', width=20, height=1)
submit_button.grid(row=i + 1, column=0, sticky="s", padx=15, pady=20, columnspan=3)

# Aggiunta di colori e spaziatura per migliorare la presentazione grafica della pagina
window.configure(background='#f2f2f2')
canvas.configure(background='#f2f2f2')
scrollbar.configure(background='#d9d9d9')
submit_button.configure(foreground='#002975')
input_frame.configure(background='#f2f2f2', padx=30, pady=20)
for widget in input_frame.winfo_children():
    if isinstance(widget, Label):
        widget.configure(background='#f2f2f2')
    elif isinstance(widget, Entry):
        widget.configure(background='#e8f0ff', font='Helvetica 12', borderwidth=0, highlightthickness=1, highlightbackground='#d9d9d9', highlightcolor='#d9d9d9')

# Avvio della finestra
window.mainloop()

# Fine del programma
exit(0)
