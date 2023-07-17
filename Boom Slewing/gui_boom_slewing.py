from main import *
from tkinter import *


def aggiungiRiga(key, u, i):
    text_fields.append(Entry(input_frame))
    Label(input_frame, text=key + '[' + u + ']', font=('Times New Roman', 12)).grid(row=i+1, column=0, sticky="W")
    text_fields[i].grid(row=i+1, column=1, sticky='W', padx=0, pady=10)


def submit(texts):
    numeri = []
    for text in texts:
        try:
            numeri.append(float(text.get()))
        except ValueError:
            print('ERRORE NEI DATI!')
            return
    creaExcel(numeri)


window = Tk()
window.geometry('700x500')
window.resizable(False, False)
window.title('BOOM-SLEWING')
window.grid_columnconfigure(0, weight=1)
text_fields = []
main_frame = Frame(window)
main_frame.pack(fill=BOTH, expand=1)

canvas_frame = Frame(main_frame)
canvas_frame.pack(fill=BOTH, expand=1)
canvas = Canvas(canvas_frame, bg='white', highlightthickness=0)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)

input_frame = Frame(canvas)
canvas.create_window((0, 0), window=input_frame, anchor="nw")
submit_button = Button(input_frame, command=lambda: submit(text_fields), background='gray', text='SUBMIT')


def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind("<Configure>", on_configure)
canvas.bind_all("<MouseWheel>", on_mousewheel)

i = 0
Label(input_frame, text='BOOM SLEWING', fg='red', font='Helvetica 24 bold').grid(row=0, column=0, sticky="WE", columnspan=2)
for key in keys:
    if isinstance(data[key][1], list):
        for j in range(len(data[key][1])):
            if data[key][2][j]:
                continue
            aggiungiRiga(key, data[key][1][j], i)
            i += 1
    else:
        aggiungiRiga(key, data[key][1], i)
        i += 1
submit_button.grid(row=i+1, column=0, sticky="WE", columnspan=2, pady=10, padx=10)

window.mainloop()
