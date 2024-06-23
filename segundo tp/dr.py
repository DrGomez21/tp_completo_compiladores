from dr_lexer import lexer
from dr_parser import Parser
from sys import argv

def leer_args():
    if len(argv) == 2:
        ruta_archivo = argv[1]
        return ruta_archivo
    elif len(argv) > 2:
        print("Demasiados argumentos recibidos...")
        exit(-1)
    else:
        print("Error, se esperaba un archivo o ruta al archvio...")
        exit(-1)

if __name__ == "__main__":
    archivo = leer_args()
    tokens = lexer(archivo)  # Generamos los tokens utilizando el lexer
    parser = Parser(tokens)  # Creamos una instancia del parser
    parser.parse()  # Realizamos el análisis sintáctico
