# Proyecto 2: Analizador Sintáctico Lenguaje Python

## Descripción

Dado un programa en lenguaje Python, la tarea consiste en realizar el **análisis sintáctico**. Nos enfocamos en detectar y reportar **errores sintácticos** generados. El programa debe:

- Leer un archivo `.py` como entrada.
- Realizar el análisis sintáctico.
- Generar un archivo `.txt` con la información del análisis.

---

## Salidas

- Si el programa es **válido** según la gramática de Python, debe mostrar:

El analisis sintactico ha finalizado exitosamente.

- Si el programa contiene **errores sintácticos**, debe abortar el análisis y reportar **el primer error sintáctico detectado** con el formato:

<linea,columna> Error sintactico: se encontro: "lexema del token encontrado"; se esperaba: lista de tokens esperados separados por comas.


---

## Consideraciones gramaticales

- Se consideran todas las construcciones sintácticas definidas en el "Language Manual and Reference" de Python.

---

## Errores sintácticos

Formato de reporte:

- `<linea,columna>`: Número de línea y columna donde se detectó el error.
- **Lexema encontrado**: Caracter o palabra leída donde ocurrió el error.
- **Tokens esperados**: Lista de nombres de tokens esperados, entre comillas y separados por comas.

Ejemplo:

Para el código:

def contains(items:[int ,)

Debe mostrar:

<1,24> Error sintactico: se encontro: ","; se esperaba: "]".

---

## Restricciones

No se deben utilizar herramientas que hagan parsing automático como:

- BISON
- NLTK.py
- ANTLR
- Parser.py
- PLY.YACC.py
- O cualquier otra librería que facilite el parseo de expresiones.

---

## Requerimientos

- Lenguaje: **Python 3.x** (recomendado Python 3.10 o superior)

### Instalaciones necesarias

Antes de correr el proyecto, asegúrate de tener instalado:

python3 --version
# Debe mostrar Python 3.10.x o superior

En caso de no tenerlo instalado:

sudo apt update
sudo apt install python3

### Cómo ejecutar el proyecto

1. Colocar los archivos lexico.py, sintactico.py, ejemplo.py y main.py en la misma carpeta.
2. Ejecutar el main desde la terminal:

python3 main.py

3. Se generará en consola o en un archivo `.txt` el resultado del análisis.

---

