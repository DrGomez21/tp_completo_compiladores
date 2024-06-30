conjunto_primero = {
    'JSON':['L_CORCHETE', 'L_LLAVE'],
    'ELEMENT':['L_CORCHETE', 'L_LLAVE'],
    'ARRAY':['L_CORCHETE'],
    'ELEMENT-LIST':['L_CORCHETE', 'L_LLAVE'],
    'E_PRIMA':['COMA'],
    'OBJECT':['L_LLAVE'],
    'ATTRIBUTE-LIST':['STRING'],
    'A_PRIMA':['COMA'],
    'ATTRIBUTE':['STRING'],
    'ATTRIBUTE-NAME':['STRING'],
    'ATTRIBUTE-VALUE':['L_LLAVE', 'L_CORCHETE', 'STRING', 'NUMBER', 'PR_TRUE', 'PR_FALSE', 'PR_NULL']
}

conjunto_siguiente = {
    'JSON':['EOF'],
    'ELEMENT':['R_CORCHETE', 'R_LLAVE', 'COMA', 'EOF'],
    'ARRAY':['R_CORCHETE', 'R_LLAVE', 'COMA', 'EOF'],
    'ELEMENT-LIST':['R_CORCHETE'],
    'E_PRIMA':['R_CORCHETE'],
    'OBJECT':['R_CORCHETE', 'R_LLAVE', 'COMA', 'EOF'],
    'ATTRIBUTE-LIST':['R_LLAVE'],
    'A_PRIMA':['R_LLAVE'],
    'ATTRIBUTE':['COMA', 'R_LLAVE'],
    'ATTRIBUTE-NAME':['DOS_PUNTOS'],
    'ATTRIBUTE-VALUE':['COMA', 'R_LLAVE']
}

salida = open('traducido.txt', 'w')

class Traductor:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_actual = None
        self.pos = 0
        self.ocurrio_error = False

    def traducir(self):

        self.avanzar_sgte_token()   # Obtener el primer token.
        self.json()

        if not self.ocurrio_error:
            if self.token_actual.comp_lexico != 'EOF':
                print(f'Ocurrio un error al final se encontró {self.token_actual.comp_lexico}')
            else:
                salida.close()

    def match(self, token_esperado):
        
        if self.token_actual.comp_lexico == token_esperado:
            self.avanzar_sgte_token()
        else:
            self.error_esperado(token_esperado)

    def error_esperado(self, comp_lexico):
        print(f'Error sintactico en la linea {self.token_actual.nro_linea}')
        print(f'  * El token actual: {self.token_actual.comp_lexico}')
        print(f'  * Se esperaba: {comp_lexico}')
        self.ocurrio_error = True

    def error(self):
        print(f'Error sintactico en la linea {self.token_actual.nro_linea}')
        print(f'  * El token actual: {self.token_actual.comp_lexico}')
        self.ocurrio_error = True

    def avanzar_sgte_token(self):
        if self.pos < len(self.tokens) - 1:
            self.token_actual = self.tokens[self.pos]
            self.pos += 1
        else:
            self.token_actual.comp_lexico = "EOF"

    def json(self):

        if not self.token_actual.comp_lexico in conjunto_siguiente['JSON']:
            if self.token_actual.comp_lexico == 'L_CORCHETE' or self.token_actual.comp_lexico == 'L_LLAVE':
                self.element()
            else:
                self.error()

    def element(self):

        if not self.token_actual.comp_lexico in conjunto_siguiente['ELEMENT']:
            self.check_input(conjunto_primero['ELEMENT'], conjunto_siguiente['ELEMENT'])

            if self.token_actual.comp_lexico == 'L_CORCHETE':
                self.array()
            elif self.token_actual.comp_lexico == 'L_LLAVE':
                self.object()
            else:
                self.error()

            self.check_input(conjunto_siguiente['ELEMENT'], conjunto_primero['ELEMENT'])

    def array(self):

        if not self.token_actual.comp_lexico in conjunto_siguiente['ARRAY']:
            self.check_input(conjunto_primero['ARRAY'], conjunto_siguiente['ARRAY'])

            if self.token_actual.comp_lexico == 'L_CORCHETE':
                self.match('L_CORCHETE')
                if self.token_actual.comp_lexico == 'R_CORCHETE':
                    self.match('R_CORCHETE')    # Caso de que sea array vacio.
                elif self.token_actual.comp_lexico == 'L_LLAVE' or self.token_actual.comp_lexico == 'L_CORCHETE':   # Caso de que hayan elementos en el array
                    self.element_list()
                    self.match('R_CORCHETE')
                else:
                    self.error() # El array no era vacío, pero tampoco tenía elementos. Es decir, el array no se cerró nunca.
            else:
                self.error()

    def element_list(self):
        salida.write('\n' + '    <item>' + '\n')

        if not self.token_actual.comp_lexico in conjunto_siguiente['ELEMENT-LIST']:
            self.check_input(conjunto_primero['ELEMENT-LIST'], conjunto_siguiente['ELEMENT-LIST'])

            if self.token_actual.comp_lexico == 'L_CORCHETE' or self.token_actual.comp_lexico == 'L_LLAVE':
                self.element()
                salida.write('    </item>' + '\n')
                self.e_prima()
            else:
                self.error()
            self.check_input(conjunto_siguiente['ELEMENT-LIST'], conjunto_primero['ELEMENT-LIST'])
        

    def e_prima(self):

        if not self.token_actual.comp_lexico in conjunto_siguiente['E_PRIMA']:
            self.check_input(conjunto_primero['E_PRIMA'], conjunto_siguiente['E_PRIMA'])

            if self.token_actual.comp_lexico == 'COMA':
                self.match('COMA')
                salida.write('\n' + '    <item>' + '\n')

                self.element()
                salida.write('    </item>' + '\n')

                self.e_prima()
            self.check_input(conjunto_siguiente['E_PRIMA'], conjunto_primero['E_PRIMA'])

    def object(self):

        if not self.token_actual.comp_lexico in conjunto_siguiente['OBJECT']:
            self.check_input(conjunto_primero['OBJECT'], conjunto_siguiente['OBJECT'])

            if self.token_actual.comp_lexico == 'L_LLAVE':
                self.match('L_LLAVE')
                if self.token_actual.comp_lexico == 'R_LLAVE':
                    self.match('R_LLAVE')
                elif self.token_actual.comp_lexico == 'STRING':
                    self.attribute_list()
                    self.match('R_LLAVE')
                else:
                    self.error()
            else:
                self.error()
            self.check_input(conjunto_siguiente['OBJECT'], conjunto_primero['OBJECT'])

    def attribute_list(self):        
        
        if not self.token_actual.comp_lexico in conjunto_siguiente['ATTRIBUTE-LIST']:
            self.check_input(conjunto_primero['ATTRIBUTE-LIST'], conjunto_siguiente['ATTRIBUTE-LIST'])

            if self.token_actual.comp_lexico == 'STRING':
                self.attribute()
                self.a_prima()
            else:
                self.error()
            self.check_input(conjunto_siguiente['ATTRIBUTE-LIST'], conjunto_primero['ATTRIBUTE-LIST'])

    def a_prima(self):

        if not self.token_actual.comp_lexico in conjunto_siguiente['A_PRIMA']:
            self.check_input(conjunto_primero['A_PRIMA'], conjunto_siguiente['A_PRIMA'])

            if self.token_actual.comp_lexico == 'COMA':
                self.match('COMA')
                self.attribute()
                self.a_prima()
            self.check_input(conjunto_siguiente['A_PRIMA'], conjunto_primero['A_PRIMA'])

    def attribute(self):

        salida.write(f'<{self.quitar_comillas(self.token_actual.lexema)}>')
        name = self.token_actual.lexema
        if not self.token_actual.comp_lexico in conjunto_siguiente['ATTRIBUTE']:
            self.check_input(conjunto_primero['ATTRIBUTE'], conjunto_siguiente['ATTRIBUTE'])

            if self.token_actual.comp_lexico == 'STRING':
                self.attribute_name()
                self.match('DOS_PUNTOS')
                self.attribute_value()
                salida.write(f'</{self.quitar_comillas(name)}>' + '\n')
            else:
                self.error()
            self.check_input(conjunto_siguiente['ATTRIBUTE'], conjunto_primero['ATTRIBUTE'])
    
    def attribute_name(self):

        if not self.token_actual.comp_lexico in conjunto_siguiente['ATTRIBUTE-NAME']:
            self.check_input(conjunto_primero['ATTRIBUTE-NAME'], conjunto_siguiente['ATTRIBUTE-NAME'])

            if self.token_actual.comp_lexico == 'STRING':
                self.match('STRING')
            else:
                self.error()
            self.check_input(conjunto_siguiente['ATTRIBUTE-NAME'], conjunto_primero['ATTRIBUTE-NAME'])

    def attribute_value(self):

        if not self.token_actual.comp_lexico in conjunto_siguiente['ATTRIBUTE-VALUE']:
            self.check_input(conjunto_primero['ATTRIBUTE-VALUE'], conjunto_siguiente['ATTRIBUTE-VALUE'])

            if self.token_actual.comp_lexico == 'STRING':
                salida.write(f'{self.token_actual.lexema}')
                self.match('STRING')
            elif self.token_actual.comp_lexico == 'NUMBER':
                salida.write(f'{self.token_actual.lexema}')
                self.match('NUMBER')
            elif self.token_actual.comp_lexico == 'PR_TRUE':
                salida.write(f'{self.token_actual.lexema}')
                self.match('PR_TRUE')
            elif self.token_actual.comp_lexico == 'PR_FALSE':
                salida.write(f'{self.token_actual.lexema}')
                self.match('PR_FALSE')
            elif self.token_actual.comp_lexico == 'PR_NULL':
                salida.write(f'{self.token_actual.lexema}')
                self.match('PR_NULL')
            elif self.token_actual.comp_lexico == 'L_LLAVE' or self.token_actual.comp_lexico == 'L_CORCHETE':
                self.element()
            else:
                self.error()
            self.check_input(conjunto_siguiente['ATTRIBUTE-VALUE'], conjunto_primero['ATTRIBUTE-VALUE'])


    # PANIC MODE.
    def scan_to(self, synchset):
        
        while self.token_actual.comp_lexico not in synchset:
            # print('  > Estoy en el while de scan_to')
            self.avanzar_sgte_token()

    def check_input(self, primero, siguiente):
        
        if self.token_actual.comp_lexico not in primero:
            self.error()
            self.scan_to(primero + siguiente)

    # Estilismo del traductor.
    def quitar_comillas(self, cadena):
        if cadena.startswith('"') and cadena.endswith('"'):
            return cadena[1:-1]
        return cadena

