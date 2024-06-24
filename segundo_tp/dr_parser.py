class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_actual = None
        self.token_siguiente = 0
        self.ocurrio_error = False
        self.sync_tokens = {'L_LLAVE', 'R_LLAVE', 'L_CORCHETE', 'R_CORCHETE', 'COMA', 'DOS_PUNTOS'}

    def parse(self):
        self.avanzar_sgte_token()
        self.json()
        if not self.ocurrio_error:
            if self.token_actual is not None:
                self.error('Se esperaba el final del archivo')
            else:
                print('Aceptacion')
        else: 
            print('Ocurrio algun error durante el parseo')

    def avanzar_sgte_token(self):
        if self.token_siguiente < len(self.tokens):
            self.token_actual = self.tokens[self.token_siguiente]
            self.token_siguiente += 1
        else:
            self.token_actual = None    # Ya no hay tokens por leer.

    def error(self, mensaje):
        if self.token_actual:
            print(f'  * Error sintáctico: En la linea {self.token_actual.nro_linea} no se esperaba {self.token_actual.lexema}')
        else:
            print(f'  * Error sintáctico: {mensaje} al final')
        self.ocurrio_error = True
        self.sincronizar()

    def sincronizar(self):
        while self.token_actual and self.token_actual.comp_lexico not in self.sync_tokens:
            self.avanzar_sgte_token()
        if self.token_actual and self.token_actual.comp_lexico in self.sync_tokens:
            self.avanzar_sgte_token()

    def match(self, esperado):
        if self.token_actual and self.token_actual.comp_lexico == esperado:
            self.avanzar_sgte_token()
        else:
            self.error(f'Se esperaba {esperado}')

    def json(self):
        self.element()
        if not self.ocurrio_error:
            self.match('EOF')

    def element(self):
        if self.token_actual and self.token_actual.comp_lexico == 'L_LLAVE':
            self.object()
        elif self.token_actual and self.token_actual.comp_lexico == 'L_CORCHETE':
            self.array()
        else:
            self.error('Se esperaba { o [')

    def array(self):
        self.match('L_CORCHETE')
        if self.token_actual and self.token_actual.comp_lexico == 'R_CORCHETE':
            self.match('R_CORCHETE')
        else:
            self.element_list()
            self.match('R_CORCHETE')

    def element_list(self):
        self.element()
        self.e_prima()

    def e_prima(self):
        if self.token_actual and self.token_actual.comp_lexico == 'COMA':
            self.match('COMA')
            self.element()
            self.e_prima()

    def object(self):
        self.match('L_LLAVE')
        if self.token_actual and self.token_actual.comp_lexico == 'R_LLAVE':
            self.match('R_LLAVE')
        else:
            self.attribute_list()
            self.match('R_LLAVE')

    def attribute_list(self):
        self.attribute()
        self.a_prima()

    def a_prima(self):
        if self.token_actual and self.token_actual.comp_lexico == 'COMA':
            self.match('COMA')
            self.attribute()
            self.a_prima()

    def attribute(self):
        self.attribute_name()
        self.match('DOS_PUNTOS')
        self.attribute_value()

    def attribute_name(self):
        self.match('STRING')

    def attribute_value(self):
        if self.token_actual and self.token_actual.comp_lexico == 'L_LLAVE':
            self.object()
        elif self.token_actual and self.token_actual.comp_lexico == 'L_CORCHETE':
            self.array()
        elif self.token_actual and self.token_actual.comp_lexico == 'STRING':
            self.match('STRING')
        elif self.token_actual and self.token_actual.comp_lexico == 'NUMBER':
            self.match('NUMBER')
        elif self.token_actual and self.token_actual.comp_lexico == 'PR_TRUE':
            self.match('PR_TRUE')
        elif self.token_actual and self.token_actual.comp_lexico == 'PR_FALSE':
            self.match('PR_FALSE')
        elif self.token_actual and self.token_actual.comp_lexico == 'PR_NULL':
            self.match('PR_NULL')
        else:
            self.error('Se esperaba un null, FALSE, TRUE, NUMBER, STRING, { o [')