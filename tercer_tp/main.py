from super_dr_lexer import *
from traductor import *
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
    archivo_fuente = leer_args()
    tokens = lexer(archivo_fuente)
    t = Traductor(tokens)
    t.traducir()
