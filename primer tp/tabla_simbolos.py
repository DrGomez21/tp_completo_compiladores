
# diccionario con simbolos iniciales 
tabla_de_simbolos = {
    r'\[': "L_CORCHETE",
    r'\]': "R_CORCHETE",
    r'\{': "L_LLAVE",
    r'\}': "R_LLAVE",
    r',': "COMA",
    r':': "DOS_PUNTOS",
    r'"(\\.|[^"\\])*"': "STRING",  # Manejo de comillas escapadas dentro de la cadena
    r'-?[0-9]+(\.[0-9]+)?([eE][\+\-]?[0-9]+)?': "NUMBER",  # Manejo de números negativos
    r'true|TRUE': "PR_TRUE", 
    r'false|FALSE': "PR_FALSE", 
    r'null': "PR_NULL"
}