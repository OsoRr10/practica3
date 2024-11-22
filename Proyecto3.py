from nltk import CFG, ChartParser
from nltk.tree import Tree
import tkinter as tk
from tkinter import ttk, messagebox

class AnalizadorSintactico:
    def __init__(self):
        self.gramatica = CFG.fromstring("""
            E -> E '+' T | E '-' T | T
            T -> T '*' F | T '/' F | F
            F -> '(' E ')' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
        """)
        self.parser = ChartParser(self.gramatica)

    def analizar(self, expresion_objetivo, derivacion="izquierda"):
        derivaciones = list(self.parser.parse(expresion_objetivo))
        if derivacion == "derecha":
            derivaciones.reverse()
        return derivaciones

    def generar_pasos_derivacion(self, arbol):
        pasos = []

        def generar_pasos(nodo):
            if isinstance(nodo, Tree):
                pasos.append(" ".join(nodo.leaves()))
                for hijo in nodo:
                    generar_pasos(hijo)

        generar_pasos(arbol)
        return pasos

    def construir_ast(self, arbol_derivacion):
        def simplificar(nodo):
            if isinstance(nodo, Tree):
                if nodo.label() in ['+', '-', '*', '/']:
                    return Tree(nodo.label(), [simplificar(hijo) for hijo in nodo])
                elif nodo.label() in ['E', 'T', 'F'] and len(nodo) == 1:
                    return simplificar(nodo[0])
                return Tree(nodo.label(), [simplificar(hijo) for hijo in nodo])
            return nodo

        return simplificar(arbol_derivacion)

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Sintáctico")
        self.analizador = AnalizadorSintactico()
        self.tipo_derivacion = tk.StringVar(value="izquierda")
        self.configurar_interfaz()

    def configurar_interfaz(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Expresión Objetivo:").grid(row=0, column=0, sticky=tk.W)
        self.entrada_expresion = ttk.Entry(frame, width=50)
        self.entrada_expresion.grid(row=1, column=0, columnspan=2)

        ttk.Label(frame, text="Tipo de Derivación:").grid(row=2, column=0, sticky=tk.W)
        ttk.Radiobutton(frame, text="Izquierda", variable=self.tipo_derivacion, value="izquierda").grid(row=3, column=0, sticky=tk.W)
        ttk.Radiobutton(frame, text="Derecha", variable=self.tipo_derivacion, value="derecha").grid(row=4, column=0, sticky=tk.W)

        ttk.Button(frame, text="Mostrar Derivación", command=self.mostrar_derivacion).grid(row=5, column=0)
        ttk.Button(frame, text="Mostrar AST", command=self.mostrar_ast).grid(row=5, column=1)

        self.texto_resultados = tk.Text(frame, wrap=tk.WORD, height=10, width=60)
        self.texto_resultados.grid(row=6, column=0, columnspan=2)

    def mostrar_derivacion(self):
        expresion = self.entrada_expresion.get().strip().split()
        derivacion = self.tipo_derivacion.get()
        derivaciones = self.analizador.analizar(expresion, derivacion)
        arbol = derivaciones[0]
        pasos = self.analizador.generar_pasos_derivacion(arbol)
        self.texto_resultados.delete("1.0", tk.END)
        self.texto_resultados.insert(tk.END, "Pasos de derivación:\n" + "\n".join(pasos))
        arbol.draw()

    def mostrar_ast(self):
        expresion = self.entrada_expresion.get().strip().split()
        derivacion = self.tipo_derivacion.get()
        derivaciones = self.analizador.analizar(expresion, derivacion)
        arbol = derivaciones[0]
        ast = self.analizador.construir_ast(arbol)
        self.texto_resultados.delete("1.0", tk.END)
        self.texto_resultados.insert(tk.END, "Árbol de Sintaxis Abstracta (AST):\n" + ast.pformat())
        ast.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()
