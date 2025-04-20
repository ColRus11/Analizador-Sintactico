# sintactico.py

class Token: 
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def __repr__(self):
        return f"<{self.tipo}, {self.valor}, {self.fila}, {self.columna}>"


class Parser: 
    def __init__(self, tokens):
        self.tokens = tokens
        self.actual = 0

    def avanzar(self):
        if self.actual < len(self.tokens) - 1:
            self.actual += 1

    def token_actual(self):
        return self.tokens[self.actual]

    def consumir(self, tipo_esperado):
        token = self.token_actual()
        if token.tipo == tipo_esperado:
            self.avanzar()
            return token
        else:
            self.error(token, [tipo_esperado])

    def error(self, token, esperados):
        lexema = f'"{token.valor}"'
        esperados_str = ", ".join(f'"{e}"' for e in esperados)
        mensaje = f"<{token.fila},{token.columna}> Error sintactico: se encontro: {lexema}; se esperaba: {esperados_str}."
        raise SyntaxError(mensaje)

    def parse_programa(self):
        self.parse_list()
        token = self.token_actual()
        if token.tipo != "EOF":
            self.error(token, ["EOF"])
        return "El analisis sintactico ha finalizado exitosamente."

    def parse_list(self):
        while True:
            tipo = self.token_actual().tipo
            if tipo in ["id", "def", "if", "return", "class", "print", "while", "for",
                        "None", "True", "False", "bool", "object", "str", "elif", "else",
                        "and", "or", "pass", "contains", "in"]:
                self.parse_stmt()
            elif tipo == "NEWLINE":
                self.consumir("NEWLINE")
            elif tipo in ["DEDENT", "EOF"]:
                break
            else:
                self.error(self.token_actual(), ["id", "def", "if", "class", "return"])

    def parse_stmt(self):
        tipo = self.token_actual().tipo
        if tipo == "id":
            self.parse_simple()
        elif tipo == "if": 
            self.parse_if()
        elif tipo == "def":
            self.parse_def()
        elif tipo == "class":
            self.parse_class()
        elif tipo == "return":
            self.parse_return()
        elif tipo == "pass":
            self.consumir("pass")
            self.consumir("NEWLINE")
        elif tipo == "while":
            self.parse_while()
        elif tipo == "for":
            self.parse_for()
        elif tipo == "break":
            self.consumir("break")
            self.consumir("NEWLINE")
        elif tipo == "continue":
            self.consumir("continue")
            self.consumir("NEWLINE")
        elif tipo == "print":
            self.parse_print()
        else:
            self.error(self.token_actual(), ["id", "if", "def", "class", "return", "pass", "while", "for", "break", "continue", "print"])

    def parse_class(self):
        self.consumir("class")
        self.consumir("id")

        if self.token_actual().tipo == "tk_paren_izq":
            self.consumir("tk_paren_izq")
            if self.token_actual().tipo in ["id", "object", "str"]:
                self.avanzar()
            else:
                self.error(self.token_actual(), ["id"])
            self.consumir("tk_paren_der")

        self.consumir("tk_dos_puntos")
        self.parse_suite()


    def parse_simple(self):
        self.parse_expr()
        self.consumir("NEWLINE")

    def parse_expr(self):
        self.parse_test()
        while self.token_actual().tipo == "tk_asig":
            self.consumir("tk_asig")
            self.parse_test()

    def parse_test(self):
        self.parse_or()
        while self.token_actual().tipo in ["tk_igualdad", "tk_diferencia", "tk_mayor_que", "tk_menor_que", "tk_mayor_igual", "tk_menor_igual"]:
            token = self.token_actual()
            if token.tipo in ["tk_igualdad", "tk_diferencia", "tk_mayor_que", "tk_menor_que", "tk_mayor_igual", "tk_menor_igual"]:
                self.consumir(token.tipo)
                self.parse_or()

    def parse_term(self):
        self.parse_fact()
        while self.token_actual().tipo in ["tk_mult", "tk_div"]:
            self.consumir(self.token_actual().tipo)
            self.parse_fact()

    def parse_fact(self):
        token = self.token_actual()
        if token.tipo == "id":
            self.avanzar()
            while self.token_actual().tipo in ["tk_paren_izq", "tk_lizq", "tk_punto"]:
                if self.token_actual().tipo == "tk_paren_izq":
                    self.parse_call()
                elif self.token_actual().tipo == "tk_lizq":
                    self.parse_subscript()
                elif self.token_actual().tipo == "tk_punto":
                    self.consumir("tk_punto")
                    self.consumir("id")

        elif token.tipo == "tk_paren_izq":
            self.consumir("tk_paren_izq")
            self.parse_test()
            self.consumir("tk_paren_der")

        elif token.tipo == "tk_resta":
            self.consumir("tk_resta")
            self.parse_fact()
            
        elif token.tipo in ["tk_entero", "tk_cadena", "True", "False", "None", "str", "int", "float", "bool"]:
            self.avanzar()

        elif token.tipo == "tk_lizq":
            self.parse_listas()
            
        else:
            self.error(token, ["id", "tk_entero", "tk_cadena", "True", "False", "None", "str", "int", "float", "bool"])

    def parse_if(self):
        self.consumir("if")
        self.parse_test()
        self.consumir("tk_dos_puntos")
        self.parse_suite()
        while self.token_actual().tipo == "elif":
            self.consumir("elif")
            self.parse_test()
            self.consumir("tk_dos_puntos")
            self.parse_suite()
        if self.token_actual().tipo == "else":
            self.consumir("else")
            self.consumir("tk_dos_puntos")
            self.parse_suite()

    def parse_suite(self):
        self.consumir("NEWLINE")
        self.consumir("INDENT")
        self.parse_list()
        self.consumir("DEDENT")

    def parse_def(self):
        self.consumir("def")
        self.consumir("id")
        self.consumir("tk_paren_izq")
        
        if self.token_actual().tipo == "id":
            self.parse_param()
            
        self.consumir("tk_paren_der")

        if self.token_actual().tipo == "tk_ejecuta":
            self.consumir("tk_ejecuta")
            self.consumir("id")
            
        self.consumir("tk_dos_puntos")
        self.parse_suite()

    def parse_param(self):
        self.consumir("id")
        if self.token_actual().tipo == "tk_dospuntos":
            self.consumir("tk_dospuntos")
            if self.token_actual().tipo in ["id", "object", "str", "int", "float", "bool"]:
                self.avanzar()
            else:
                self.error(self.token_actual(), ["id", "object", "str", "int", "float", "bool"])
        
        while self.token_actual().tipo == "tk_coma":
            self.consumir("tk_coma")
            self.consumir("id")
            if self.token_actual().tipo == "tk_dospuntos":
                self.consumir("tk_dospuntos")
                if self.token_actual().tipo in ["id", "object", "str", "int", "float", "bool"]:
                    self.avanzar()
                else:
                    self.error(self.token_actual(), ["id", "object", "str", "int", "float", "bool"])

    def parse_call(self):
        self.consumir("tk_paren_izq")
        if self.token_actual().tipo != "tk_paren_der":
            self.parse_arg()
        self.consumir("tk_paren_der")

    def parse_arg(self):
        self.parse_test()
        while self.token_actual().tipo == "tk_coma":
            self.consumir("tk_coma")
            self.parse_test()

    def parse_equal(self):
        self.parse_arith()
        while self.token_actual().tipo in ["tk_igualdad", "tk_diferencia"]:
            self.consumir(self.token_actual().tipo)
            self.parse_arith()

    def parse_arith(self):
        self.parse_term()
        while self.token_actual().tipo in ["tk_suma", "tk_resta"]:
            self.consumir(self.token_actual().tipo)
            self.parse_term()

    def parse_or(self):
        self.parse_and()
        while self.token_actual().tipo == "or":
            self.consumir("or")
            self.parse_and()

    def parse_and(self):
        self.parse_equal()
        while self.token_actual().tipo == "and":
            self.consumir("and")
            self.parse_equal()

    def parse_listas(self):
        self.consumir("tk_lizq")
        while self.token_actual().tipo in ["NEWLINE", "INDENT", "DEDENT"]:
            self.avanzar() 

        if self.token_actual().tipo in ["id", "tk_entero", "tk_cadena", "True", "False", "None", "tk_lizq", "tk_paren_izq"]:
            self.parse_test()
            while self.token_actual().tipo == "tk_coma":
                self.consumir("tk_coma")
                while self.token_actual().tipo in ["NEWLINE", "INDENT", "DEDENT"]:
                    self.avanzar()
                self.parse_test()

        while self.token_actual().tipo in ["NEWLINE", "INDENT", "DEDENT"]:
            self.avanzar()

        self.consumir("tk_lder")

    def parse_subscript(self):
        self.consumir("tk_lizq")
        self.parse_test()
        self.consumir("tk_lder")

    def parse_return(self):
        self.consumir("return")
        if self.token_actual().tipo != "NEWLINE":
            self.parse_test()
        self.consumir("NEWLINE")
    
    def parse_while(self):
        self.consumir("while")
        self.parse_test()
        self.consumir("tk_dos_puntos")
        self.parse_suite()

    def parse_for(self):
        self.consumir("for")
        self.consumir("id")
        self.consumir("in")
        self.parse_test()
        self.consumir("tk_dos_puntos")
        self.parse_suite()
    
    def parse_print(self):
        self.consumir("print")
        self.consumir("tk_paren_izq")
        if self.token_actual().tipo != "tk_paren_der":
            self.parse_arg()
        self.consumir("tk_paren_der")
        self.consumir("NEWLINE")


def leer_tokens(scanner):
    tokens = scanner.tokens[:]
    tokens.append(Token("EOF", "EOF", -1, -1))
    return tokens