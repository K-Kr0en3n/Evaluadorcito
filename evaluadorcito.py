import tkinter as tk
from tkinter import messagebox

PREGUNTAS_POR_FILA = 10
CELDA_ANCHO = 4

solucionario = ['c','a','d','d','c','a','c','a','a','d','d','a','d','e','a','c','a','b','a','e','a','b','e','b','c','c','c','a','d','c','e','a','b','a','b','e','d','a','d','e','b','c','d','c','a','c','d','c','a','d','b','b','c','c','d','b','c','a','d','c','c','d','b','c','b','c','c','c','c','c','d','c','d','e','c','b','d','c','b','c']

# Valores iniciales onio
VALOR_CORRECTO = 0.25
VALOR_BLANCO = 0.05
VALOR_ANULADA = 0
VALOR_ERROR = 0

respuestas = []
historial = []

# funciones
def crear_celdas():
    global respuestas
    for widget in frame_tabla.winfo_children():
        widget.destroy()

    respuestas = []
    fila = 1
    columna = 0

    for i in range(len(solucionario)):
        tk.Label(frame_tabla, text=str(i+1)).grid(row=fila*2-1, column=columna)

        e = tk.Entry(frame_tabla, width=CELDA_ANCHO, justify="center", validate='key', validatecommand=(vcmd, '%P'))
        e.grid(row=fila*2, column=columna, padx=2, pady=2)
        e.bind("<Return>", mover_siguiente)
        e.bind("<BackSpace>", retroceder)

        respuestas.append(e)

        columna += 1
        if columna == PREGUNTAS_POR_FILA:
            columna = 0
            fila += 1


def retroceder(event):
    event.widget.delete(0, tk.END)
    idx = respuestas.index(event.widget)
    if idx > 0:
        respuestas[idx - 1].focus_set()
        respuestas[idx - 1].icursor(tk.END)

def mover_siguiente(event):
    try:
        idx = respuestas.index(event.widget)
        if idx + 1 < len(respuestas):
            respuestas[idx + 1].focus_set()
    except:
        pass

def calcular():
    puntaje = 0
    nombre = entry_nombre.get()
    grupo = entry_grupo.get()

    if nombre.strip() == "":
        messagebox.showwarning("Aviso", "Ingrese el nombre del estudiante.")
        return

    for i, entry in enumerate(respuestas):
        r = entry.get().strip().lower()

        if r == '':
            pass
        elif r == '0':
            puntaje += VALOR_BLANCO
        elif r == 'x':
            puntaje += VALOR_ANULADA
        elif r == solucionario[i]:
            puntaje += VALOR_CORRECTO
        else:
            puntaje += VALOR_ERROR

    texto = f"{nombre} | Grupo: {grupo} | Puntaje: {round(puntaje,2)}"
    resultado.set(texto)

    historial.append(texto)
    actualizar_historial()

def actualizar_historial():
    lista_historial.delete(0, tk.END)
    for item in historial:
        lista_historial.insert(tk.END, item)

def abrir_solucionario():
    ventana_sol = tk.Toplevel(ventana)
    ventana_sol.title("Editar Solucionario")

    tk.Label(ventana_sol, text="Ingrese el solucionario separado por comas:").pack(pady=5)

    texto = tk.Text(ventana_sol, height=5, width=60)
    texto.pack()
    texto.insert("1.0", ",".join(solucionario))

    def guardar():
        global solucionario
        data = texto.get("1.0", "end").strip().lower()
        try:
            nuevo = [x.strip() for x in data.split(",") if x.strip() != ""]
            if len(nuevo) == 0:
                raise Exception
            solucionario = nuevo
            crear_celdas()
            ventana_sol.destroy()
        except:
            messagebox.showerror("Error", "Formato inválido.")

    tk.Button(ventana_sol, text="Guardar", command=guardar).pack(pady=10)

def abrir_valores():
    ventana_val = tk.Toplevel(ventana)
    ventana_val.title("Configurar Valores")

    labels = [
        "Valor Respuesta Correcta:",
        "Valor Pregunta en Blanco (0):",
        "Valor Pregunta Anulada (X):",
        "Valor Respuesta Incorrecta:"
    ]

    entries = []

    for i, txt in enumerate(labels):
        tk.Label(ventana_val, text=txt).grid(row=i, column=0, pady=5, sticky="e")
        e = tk.Entry(ventana_val)
        e.grid(row=i, column=1)
        entries.append(e)

    entries[0].insert(0, str(VALOR_CORRECTO))
    entries[1].insert(0, str(VALOR_BLANCO))
    entries[2].insert(0, str(VALOR_ANULADA))
    entries[3].insert(0, str(VALOR_ERROR))

    def guardar_valores():
        global VALOR_CORRECTO, VALOR_BLANCO, VALOR_ANULADA, VALOR_ERROR
        try:
            VALOR_CORRECTO = float(entries[0].get())
            VALOR_BLANCO = float(entries[1].get())
            VALOR_ANULADA = float(entries[2].get())
            VALOR_ERROR = float(entries[3].get())
            ventana_val.destroy()
        except:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")

    tk.Button(ventana_val, text="Guardar Valores", command=guardar_valores)\
        .grid(row=len(labels), column=0, columnspan=2, pady=10)

def limpiar():
    entry_nombre.delete(0, tk.END)
    entry_grupo.delete(0, tk.END)

    for e in respuestas:
        e.delete(0, tk.END)

    resultado.set("")
    if respuestas:
        respuestas[0].focus_set()

# Interfaz uwu
ventana = tk.Tk()
ventana.title("Evaluadorcito") 
ventana.geometry("1100x650")

frame_datos = tk.Frame(ventana)
frame_datos.pack(pady=10)
#Key de confirmacion de respuestas
def validar(P):
    if P == '' or P in 'abcde0x':
        return True
    return False
vcmd = ventana.register(validar)

tk.Label(frame_datos, text="Nombre:").grid(row=0, column=0)
entry_nombre = tk.Entry(frame_datos, width=25)
entry_nombre.grid(row=0, column=1, padx=5)

tk.Label(frame_datos, text="Grupo:").grid(row=0, column=2)
entry_grupo = tk.Entry(frame_datos, width=15)
entry_grupo.grid(row=0, column=3, padx=5)

# Botones
frame_botones = tk.Frame(ventana)
frame_botones.pack()

tk.Button(frame_botones, text="Solucionario", command=abrir_solucionario).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Valores", command=abrir_valores).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Calcular", command=calcular).grid(row=0, column=2, padx=5)
tk.Button(frame_botones, text="Limpiar", command=limpiar).grid(row=0, column=3, padx=5)

frame_contenido = tk.Frame(ventana)
frame_contenido.pack(fill="both", expand=True)

frame_tabla = tk.Frame(frame_contenido)
frame_tabla.pack(side="left", padx=10)

# Leyenda
frame_leyenda = tk.Frame(frame_contenido, relief="groove", bd=2)
frame_leyenda.pack(side="right", padx=10, fill="y")

tk.Label(frame_leyenda, text="LEYENDA", font=("Arial", 12, "bold")).pack(pady=5)
tk.Label(frame_leyenda, text="Alternativas: a, b, c, d, e").pack(anchor="w", padx=10)
tk.Label(frame_leyenda, text="Pregunta en blanco: 0").pack(anchor="w", padx=10)
tk.Label(frame_leyenda, text="Pregunta anulada: X").pack(anchor="w", padx=10)
tk.Label(frame_leyenda, text="ENTER: Avanza de celda").pack(anchor="w", padx=10)
tk.Label(frame_leyenda, text="DELETE: Borrar y retroceder").pack(anchor="w", padx=10)
tk.Label(frame_leyenda, text="!!!Si dejas la casilla en blanco\n se considera que la respuesta\na la pregunta es erronea!!!").pack(anchor="w", padx=10, fill="both")

# Historial
frame_historial = tk.Frame(ventana)
frame_historial.pack(fill="x", pady=5)

tk.Label(frame_historial, text="HISTORIAL", font=("Arial", 11, "bold")).pack()

lista_historial = tk.Listbox(frame_historial, height=6)
lista_historial.pack(fill="x", padx=15)

# Resultado
resultado = tk.StringVar()
tk.Label(ventana, textvariable=resultado, font=("Arial", 12, "bold"), fg="red").pack(pady=5)

crear_celdas()
ventana.mainloop()
