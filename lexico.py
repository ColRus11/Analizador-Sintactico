# lexico.py

class Token:
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila 
        self.columna = columna

    def __repr__(self):
        return f"<{self.tipo}, \"{self.valor}\", {self.fila}, {self.columna}>"

class Scanner:
    def __init__(self, texto):
        self.tokens = []
        self.texto = texto
        self.posicion = 0
        self.indent_stack = [0]  # Nivel inicial de indentación
        self.tokenizar()

    def contar_espacios(self, linea):
        return len(linea) - len(linea.lstrip(' '))

    def tokenizar(self):
        for num_fila, linea in enumerate(self.texto.split("\n"), start=1):
            espacios = self.contar_espacios(linea)
            contenido = linea.lstrip()

            if not contenido or contenido.startswith("#"):
                self.tokens.append(Token("NEWLINE", "\\n", num_fila, 1))
                continue

            if espacios > self.indent_stack[-1]:
                self.indent_stack.append(espacios)
                self.tokens.append(Token("INDENT", "indent", num_fila, 1))
            while espacios < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.tokens.append(Token("DEDENT", "dedent", num_fila, 1))

            indice = 0
            while indice < len(contenido):
                if contenido[indice].isspace():
                    indice += 1
                    continue
                palabra = ""
                while indice < len(contenido) and (contenido[indice].isalnum() or contenido[indice] == "_"):
                    palabra += contenido[indice]
                    indice += 1
                if palabra.isdigit():
                    self.tokens.append(Token("tk_entero", palabra, num_fila, indice + 1))
                elif palabra:
                    if palabra in palabras_reservadas_key:
                        self.tokens.append(Token(palabras_reservadas[palabra], palabra, num_fila, indice - len(palabra) + 1))
                    else:
                        self.tokens.append(Token("id", palabra, num_fila, indice - len(palabra) + 1))

                elif contenido[indice] == '"':
                    inicio = indice
                    indice += 1
                    cadena = ""
                    while indice < len(contenido) and contenido[indice] != '"':
                        cadena += contenido[indice]
                        indice += 1
                    if indice < len(contenido) and contenido[indice] == '"':
                        self.tokens.append(Token("tk_cadena", cadena, num_fila, inicio + 1))
                        indice += 1
                    else:
                        raise SyntaxError(f">>> Error léxico(linea:{num_fila},posicion:{indice+1})")

                elif indice + 1 < len(contenido) and contenido[indice:indice + 2] in simbolos_keys:
                    simbolo = contenido[indice:indice + 2]
                    self.tokens.append(Token(simbolos[simbolo], simbolo, num_fila, indice + 1))
                    indice += 2
                elif contenido[indice] in simbolos_keys:
                    simbolo = contenido[indice]
                    self.tokens.append(Token(simbolos[simbolo], simbolo, num_fila, indice + 1))
                    indice += 1
                elif contenido[indice].isdigit():
                    inicio = indice
                    while indice < len(contenido) and contenido[indice].isdigit():
                        indice += 1
                    numero = contenido[inicio:indice]
                    self.tokens.append(Token("tk_entero", numero, num_fila, inicio + 1))
                else:
                    raise SyntaxError(f">>> Error léxico(linea:{num_fila},posicion:{indice+1})")

            self.tokens.append(Token("NEWLINE", "\\n", num_fila, len(contenido) + 1))

        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token("DEDENT", "dedent", num_fila + 1, 1))

    def siguiente_token(self):
        return self.tokens.pop(0) if self.tokens else Token("EOF", "EOF", -1, -1)

    def get_tokens(self):
        print(list(self.tokens))
        return list(self.tokens)


# Definiciones externas
palabras_reservadas = {
    "contains":"contains","while":"while","in":"in","for":"for","None":"None",
    "class": "class","def":"def","True":"True","False":"False",
    "print":"print","return":"return","if":"if","elif":"elif",
    "else":"else","and":"and","or":"or","pass": "pass"
}

palabras_reservadas_key = set(palabras_reservadas.keys())
simbolos = {
    ",":"tk_coma","[":"tk_lizq","]":"tk_lder",":":"tk_dos_puntos",
    "(":"tk_paren_izq",")":"tk_paren_der",".":"tk_punto","=":"tk_asig",
    "->":"tk_ejecuta","==":"tk_igualdad","!=":"tk_diferencia",
    "+":"tk_suma","-":"tk_resta","*":"tk_mult","/":"tk_div", ">": "tk_mayor_que",
    "<": "tk_menor_que",">=": "tk_mayor_igual","<=": "tk_menor_igual",
}
simbolos_keys = set(simbolos.keys())


