# main.py

from lexico import Scanner
from sintactico import Parser, Token, leer_tokens
def main():
    with open("ejemplo.py", "r", encoding="utf-8") as archivo:
        texto = archivo.read()

    try:
        # Ejecutar el analizador léxico
        scanner = Scanner(texto)
        tokens = leer_tokens(scanner)

        # Ejecutar el analizador sintáctico
        parser = Parser(tokens)
        resultado = parser.parse_programa()
    
    except SyntaxError as e:
        resultado = str(e)

    with open("salida.txt", "w", encoding="utf-8") as salida:
        salida.write(resultado + "\n")

    print(resultado)

if __name__ == "__main__":
    main()
