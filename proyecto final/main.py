import tkinter as tk
from tkinter import ttk
import sys
import io
import analizador_lexico  # Importar el archivo analizador_lexico.py

# Variables globales para almacenar variables definidas
variables = {}

# Clase para redirigir la salida estándar a un widget de texto
class StdoutRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")

# Función para analizar la entrada del usuario y ejecutar el código
def analyze_input():
    input_text = entry.get("1.0", "end-1c")
    
    # Limpiar variables globales antes de ejecutar el nuevo código
    global variables
    variables = {}
    
    # Limpiar consola de salida
    console_output.config(state="normal")
    console_output.delete("1.0", tk.END)

    # Redirigir salida estándar al widget de texto
    sys.stdout = io.StringIO()
    sys.stdout = StdoutRedirector(console_output)

    # Actualizar la tabla de salida y mostrar resultado de validez
    tokens, lexeme_count, valid = analizador_lexico.parse_input(input_text)
    
    # Mostrar resultados de análisis léxico y sintáctico en la tabla
    if tokens is not None:
        # Limpiar tabla
        for row in token_tree.get_children():
            token_tree.delete(row)

        # Insertar datos en la tabla
        for token, lexeme in tokens:
            token_tree.insert("", "end", values=(token, lexeme, lexeme_count.get(lexeme, 0)))

        if valid:
            valid_var.set("La cadena es válida.")
            valid_label.config(fg="green")  # Cambiar color del texto a verde
        else:
            valid_var.set("La cadena es inválida.")
            valid_label.config(fg="red")  # Cambiar color del texto a rojo

    # Ejecutar el código solo si el análisis léxico y sintáctico es correcto
    if valid:
        try:
            exec(input_text, variables)
        except Exception as e:
            print("Error de ejecución:", e)

        # Restaurar la salida estándar
        sys.stdout = sys.__stdout__

# Crear la ventana principal
window = tk.Tk()
window.title("Análisis Léxico y Sintáctico")

# Función para configurar la expansión de columnas y filas
def configure_grid():
    for i in range(3):
        window.grid_columnconfigure(i, weight=1)
    window.grid_rowconfigure(1, weight=1)

# Estilo de la interfaz
bg_color = "#f0f0f0"
window.configure(bg="#E6E6FA")  # Cambiar el color de fondo de la ventana a lavanda

label_font = ("Arial", 12, "bold")  # Establecer el texto en negrita
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# Crear los elementos de la interfaz
input_label = tk.Label(window, text="Ingrese la cadena de texto:", bg=bg_color, font=label_font)
entry = tk.Text(window, width=50, height=10, font=entry_font)  # Cambiar Entry a Text y ajustar altura
analyze_button = tk.Button(window, text="Analizar", command=analyze_input, font=button_font)

valid_var = tk.StringVar()
valid_label = tk.Label(window, textvariable=valid_var, bg=bg_color, font=label_font)  # Sin color de fondo

# Crear la tabla para mostrar los resultados
token_tree = ttk.Treeview(window, columns=("Token", "Lexema", "Cantidad"), show="headings", height=10)
token_tree.heading("Token", text="Token")
token_tree.heading("Lexema", text="Lexema")
token_tree.heading("Cantidad", text="Cantidad")
token_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")  # Centrar la tabla en la ventana

# Consola de salida
console_label = tk.Label(window, text="Consola de salida:", bg=bg_color, font=label_font)
console_output = tk.Text(window, height=10, font=entry_font, state="disabled")

# Colocar los elementos en la ventana usando la cuadrícula
input_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
analyze_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
valid_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
console_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
console_output.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

# Configurar expansión de columnas y filas
configure_grid()

# Iniciar el bucle de eventos
window.mainloop()