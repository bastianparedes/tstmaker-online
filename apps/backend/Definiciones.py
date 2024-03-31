from random import choice, shuffle
import math

def es_int_o_float(posible_numero) -> bool:
  if len(str(posible_numero)) == 0:
    return False
  if isinstance(posible_numero, (int, float)):
    return True
  posible_numero = str(posible_numero)  
  if posible_numero.count('.') >= 2:
    return False
  posible_numero = str(posible_numero)
  for caracter in '.0123456789':
    posible_numero = posible_numero.replace(caracter, '')
  return len(posible_numero) == 0 # si al quitar los números y el punto el largo queda en 0, significa que sí era número

def mathrm(contenido):
  if isinstance(contenido, (Racional, Natural, Complex, Root, Log, Par)):
    return contenido.show
  elif es_int_o_float(contenido):
    return str(contenido)
  elif isinstance(contenido, str):
    if contenido=='':
      return ''
    else:
      return fr'\mathrm{{{contenido}}}'
  else:
    return fr'\mathrm{{{contenido}}}'
    
def sin(argumento, grados=True):
  if grados:
    return math.sin(argumento*math.pi/180)
  else:
    return math.sin(argumento)

def cos(argumento, grados=True):
  if grados:
    return math.cos(argumento*math.pi/180)
  else:
    return math.cos(argumento)

def tan(argumento, grados=True):
  if grados:
    return math.tan(argumento*math.pi/180)
  else:
    return math.tan(argumento)

# Fracción que separa verticalmente
def fraccion(numerador, denominador):
  return fr'\dfrac{{{mathrm(numerador)}}}{{{mathrm(denominador)}}}'

#Subíndice
def sub(base,subindice):
  return fr'{{{mathrm(base)}}}_{{{mathrm(subindice)}}}'

#Punto multiplicación
def por():
  return  r'\cdot '

#Raíz de cualquier índice
def raiz(subradical, indice=2):
  if indice==2 or indice=='2' or indice=='2.0':
    return fr'\sqrt{{{mathrm(subradical)}}}'
  elif indice==1 or indice=='1' or indice=='1.0':
    return subradical
  else:
    return fr'\sqrt[{{{mathrm(indice)}}}]{{{mathrm(subradical)}}}'

#Potencia
def potencia(base, exponente='', parentesis_automatico=True, quitar_1=False):
  if isinstance(base, (Racional, Natural, Complex, Root, Term, Pol)):
    base = base.show
  if isinstance(exponente, (Racional, Natural, Complex, Root, Term, Pol)):
    exponente = exponente.show
  if exponente in [1, '1', '1.0'] and quitar_1:
    exponente=''
  if not parentesis_automatico or exponente=='':
    return fr'{{{mathrm(base)}}}^{{{mathrm(exponente)}}}'
  if str(base).isnumeric():
    if 0<=int(base):
      return f'{{{mathrm(base)}}}^{{{mathrm(exponente)}}}'
    else:
      return f'{{({mathrm(base)})}}^{{{mathrm(exponente)}}}'
  else:
    if len(str(base))==1:
      return f'{{{mathrm(base)}}}^{{{mathrm(exponente)}}}'
    else:
      return f'{{({mathrm(base)})}}^{{{mathrm(exponente)}}}'

#Vector. La flecha no se estira.
def vector(v):
  return fr'\overrightarrow{{{mathrm(v)}}}'

#Línea encima
def linea(nombre, azar=True):
  nombre = str(nombre)
  if azar:
    nombre = list(nombre)
    shuffle(nombre)
    nombre = ''.join(nombre)
  return fr'\overline{{{mathrm(nombre)}}}'
#PI
def PI():
  return r'\pi'
#Infinito
def INF():
  return r'\infty'
#Coeficiente binomial
def coeficiente_binomial(n, k):
  return r'\begin{pmatrix}' + mathrm(n) + r'\\' + mathrm(k) + r'\end{pmatrix}'
#Logaritmos
def logaritmo(argumento, base='', parentesis_automatico=True):
  if isinstance(base, (int, float, Racional, Natural)):
    if base==10:
      base=''
  if parentesis_automatico==False:
    return fr'\log_{{{mathrm(base)}}}{{{mathrm(argumento)}}}'
  if isinstance(argumento, Racional):
    argumento = argumento.show
  if isinstance(base, Racional):
    base = base.show
  if str(argumento).isnumeric():
    if 0<=int(argumento):
      return fr'\log_{{{mathrm(base)}}}{{{mathrm(argumento)}}}'
    else:
      return fr'\log_{{{mathrm(base)}}}{{({mathrm(argumento)})}}'
  else:
    if len(str(argumento))==1:
      return fr'\log_{{{mathrm(base)}}}{{{mathrm(argumento)}}}'
    else:
      return fr'\log_{{{mathrm(base)}}}{{({mathrm(argumento)})}}'
#Abre un entorno matemático
def Matematica(contenido, arreglar_espacios=True):
  contenido = str(contenido)
  if arreglar_espacios:
    contenido = contenido.replace(' ', r'\ ')
  contenido = contenido.replace('(', r'\left(').replace(')', r'\right)')
  contenido = contenido.replace('°', r'\degree')
  contenido = contenido.replace('%', r'\%')
  contenido = contenido.replace('<=', r'\leq')
  contenido = contenido.replace('>=', r'\geq')
  return fr'${mathrm(contenido)}$'
#Transforma una letra normal a letra de conjunto
def letra_conjunto(letra):
  return fr'\mathbb{{{letra}}}'
#Genera una ecuación con todo desordenado, se considera que todo está originalmente en el lado izquierdo
def ecuacion_azar(*terminos, lista_de_terminos=[], simbolo='='):
  '''Recuerda que los términos debes introducirlos como si estuvieran todos en el lado izquierdo, con tan solo un 0 en el lado derecho'''
  diccionario_simbolos_invertidos = {'=':'=', r'\leq':r'\geq', r'\geq':r'\leq', '<':'>', '>':'<', '= ':'= ', r'\leq ':r'\geq ', r'\geq ':r'\leq ', '< ':'> ', '> ':'< '}
  terminos = list(terminos)+list(lista_de_terminos)
  lista_izquierda = [0]
  lista_derecha = [0]
  positivo_o_negativo = Racional(choice([-1,1]))
  if positivo_o_negativo<0:
    simbolo = diccionario_simbolos_invertidos[simbolo]
  for termino in terminos:
    lado = choice(['izquierda', 'derecha'])
    if lado=='izquierda':
      lista_izquierda.append(positivo_o_negativo*termino)
    elif lado=='derecha':
      lista_derecha.append(positivo_o_negativo*Racional(-1)*termino)
  return Pol(lista_de_terminos=lista_izquierda, azar=True)+ simbolo +Pol(lista_de_terminos=lista_derecha, azar=True)


def calcular_factorial(n):
  if isinstance(n, Racional):
    n = n.numerador
  if n==0 or n==1:
    return 1
  else:
    return n * calcular_factorial(n-1)


def primo(numero):
  if numero<=0:
    return False
  else:
    cantidad_de_divisores = 0
    for intento in range(1, numero+1):
      if numero%intento==0:
        cantidad_de_divisores += 1
    return cantidad_de_divisores==2


def elegir(inicio, fin, *excluidos):
  lista_provisional = list(range(inicio, fin))
  for numero in excluidos:
    if numero in lista_provisional:
      lista_provisional.remove(numero)
  return choice(lista_provisional)



def MCD(*lista_de_numeros, lista=[]):
  '''solo acepta int'''
  #Junta las listas
  lista_de_numeros = sorted(list(lista_de_numeros) + lista)
  #Transforma en 0 los repetidos
  for numero in lista_de_numeros:
    lista_de_numeros[lista_de_numeros.index(numero)] = abs(numero)
    if 1 < lista_de_numeros.count(numero):
      lista_de_numeros[lista_de_numeros.index(numero)] = 0

  #Quita los ceros de la lista
  while 0 in lista_de_numeros:
    lista_de_numeros.remove(0)

  if 1 in lista_de_numeros:
    return Racional(1)


  #Calcula la lista de numeros restados y determina el menor de todos. Ese número será el límite al buscar los divisores
  numero_menor = lista_de_numeros[0]
  numero_mayor = lista_de_numeros[-1]
  lista_de_numeros_restados = []
  for numero in lista_de_numeros:
    if lista_de_numeros.index(numero)==lista_de_numeros.index(numero_mayor):
      break
    else:
      lista_de_numeros_restados.append( lista_de_numeros[lista_de_numeros.index(numero)+1] -numero)
  numero_menor = min([numero_menor] + lista_de_numeros_restados)

  if numero_menor==1:
    return Racional(1)

  #Calcula todos los divisores
  maximo_divisor = 1
  for posible_divisor in range(2, numero_menor+1):
    se_pudo_dividir = True
    while se_pudo_dividir == True:
      for numero in lista_de_numeros:
        if numero % posible_divisor ==0:
          lista_de_numeros[lista_de_numeros.index(numero)] = int(numero/posible_divisor)
        elif numero % posible_divisor !=0:
          se_pudo_dividir = False
          break
      if se_pudo_dividir:
        maximo_divisor *= posible_divisor
  return maximo_divisor



def MCM(*lista_de_numeros, lista=[]):
  '''Solo acepta int, float, Racional, Natural'''
  lista_de_numeros = sorted(list(lista_de_numeros) + lista)
  #Transforma en 0 los repetidos
  for numero in lista_de_numeros:
    lista_de_numeros[lista_de_numeros.index(numero)] = abs(numero)
    if 1 < lista_de_numeros.count(numero):
      lista_de_numeros[lista_de_numeros.index(numero)] = 0

  #Quita los ceros de la lista
  while 0 in lista_de_numeros:
    lista_de_numeros.remove(0)

  #buscara el multiplo del mayor que sea el mcm
  numero_mayor = max(lista_de_numeros)
  factor = 0
  se_encontro_mcm = False
  while not se_encontro_mcm:
    factor += 1
    for numero in lista_de_numeros:
      if numero_mayor*factor % numero != 0:
        break
      else:
        if numero==numero_mayor:
          se_encontro_mcm = True

  return numero_mayor*factor



#================================================================================================================================================================
#================================================================================================================================================================
#================================================================================================================================================================
#================================================================================================================================================================
#================================================================================================================================================================
#================================================================================================================================================================
#================================================================================================================================================================
#================================================================================================================================================================





class Racional:
  '''self
  signo     str + o -     multiplo          str
  numerador   int       parte_entera        str
  denominador int       parte_decimal_no_periodica  str
  show    str       parte_decimal_periodica   str
  raiz()    raiconal/str  show_decimal        str
  '''
  def __init__(self, primer_numero=1, segundo_numero=1, cargar_decimal=False):
    self.diccionario_de_letras_y_exponentes = {}
    self.factor_literal = ''
    self.lista_de_terminos = [self]
    self.factor_comun = self
    self.factor_numerico = self

    #Determina el numerador, el denominador y el self.signo a partir de int o float
    if isinstance(primer_numero, (int, float, str)) and isinstance(segundo_numero, (int, float, str)):
      numerador = float(primer_numero)
      denominador = float(segundo_numero)
      if 0<=numerador*denominador:
        self.signo = '+'
      else:
        self.signo = '-'

    #Convierte en Racional los int, float y Naturales si solo uno de los argumentos no lo es
    else:
      if isinstance(primer_numero, (int, float)):
        primer_numero = Racional(primer_numero)
      
      if isinstance(segundo_numero, (int, float)):
        segundo_numero = Racional(segundo_numero)
      
      if isinstance(primer_numero, Natural):
        primer_numero = Racional(primer_numero.numero)
      
      if isinstance(segundo_numero, Natural):
        segundo_numero = Racional(segundo_numero.numero)

    #Calcula numerador, denominador y self signo a partir de dos Racionales
    if isinstance(primer_numero, Racional) and isinstance(segundo_numero, Racional):
      numerador = primer_numero.numerador*segundo_numero.denominador
      denominador = primer_numero.denominador*segundo_numero.numerador
      if 0<=numerador*denominador:
        self.signo = '+'
      else:
        self.signo = '-'




    # Genera error si el denominador es 0.
    # Establece denominador 1 si el numerador es 0
    if float(denominador)==0:
      raise Exception('El denominador es 0 en Racional')
    if float(numerador)==0:
      numerador = 0
      denominador = 1


    # Aquí se amplifica el numerador y el denomiandor para quitar los decimales
    numerador = str(abs(float(numerador)))
    denominador = str(abs(float(denominador)))
    while numerador[numerador.index('.'):]!='.0' or denominador[denominador.index('.'):]!='.0':
      numerador = numerador[:numerador.index('.')] + numerador[numerador.index('.')+1:numerador.index('.')+2] + '.' + numerador[numerador.index('.')+2:]
      if numerador[-1]=='.':
        numerador += '0'
      denominador = denominador[:denominador.index('.')] + denominador[denominador.index('.')+1:denominador.index('.')+2] + '.' + denominador[denominador.index('.')+2:]
      if denominador[-1]=='.':
        denominador += '0'
    numerador = int(float(numerador))
    denominador = int(float(denominador))


    # Aquí se simplifica el numerador con el denominador y determinan self.numerador y self.denominador
    for i in list(range(2, min([abs(numerador), abs(denominador), abs(abs(numerador)-abs(denominador))]) +1))+[denominador]:
      while numerador%i == denominador%i == 0:
        numerador=int(numerador/i)
        denominador=int(denominador/i)
        if denominador==1:
          break
    self.numerador = int(self.signo + str(numerador))
    self.denominador = denominador


    #Aquí se determina la fracción simplificada en self.show
    if denominador==1:
      self.show = str(self.numerador)
    elif self.signo == '+':
        self.show = fraccion(numerador, denominador)
    else:
      self.show = self.signo + fraccion(numerador, denominador)


    #Aquí se calcula la parte entera sin signo
    self.parte_entera = str(numerador//self.denominador)

    # Determina el resto
    self.resto = self.numerador%self.denominador

    # Determina el show_mixto
    if self.denominador==1 or self.numerador<self.numerador or self.parte_entera=='0':
      self.show_mixto = self.show
    else:
      self.show_mixto = str(int(self.signo+self.parte_entera)) + fraccion(self.resto, self.denominador)

    #Carga la parte decimal del Racional. El self.show ahora meustra el decimal en lugar de la fraccion.
    if cargar_decimal:
      self.decimal()
    

  def decimal(self):
    #Aquí se calcula el múltiplo. self.multiplo
    multiplo = 9
    while multiplo % self.denominador != 0:
      multiplo = str(multiplo)
      if multiplo.count('9') == 1:
        multiplo = multiplo.replace('0', '9')
        multiplo += '9'
      else:
        lista = []
        for digito in multiplo:
          lista.append(digito)
        lista[lista.count('9')-1] = '0'
        multiplo = ''
        for digito in lista:
          multiplo += digito
      multiplo = int(multiplo)
    self.multiplo = str(multiplo)


    #Aquí se calcula la def parte decimal no periodica
    if str(multiplo).count('0') != 0:
      parte_decimal_no_periodica = str(int((abs(self.numerador)%self.denominador)*multiplo/self.denominador/ int(str(multiplo).replace('0', ''))))
      for i in range(0, str(multiplo).count('0') - len(parte_decimal_no_periodica)):
        parte_decimal_no_periodica = '0' + parte_decimal_no_periodica
    else:
      parte_decimal_no_periodica = ''
    self.parte_decimal_no_periodica = parte_decimal_no_periodica

    #Aquí se calcula la parte decimal periódica
    parte_decimal_periodica = str(int(((abs(self.numerador)%self.denominador)*multiplo/self.denominador)   %   int(str(multiplo).replace('0', ''))))
    if parte_decimal_periodica == '0':
      parte_decimal_periodica = ''
    else:
      for i in range(0, str(multiplo).count('9') - len(parte_decimal_periodica)):
        parte_decimal_periodica = '0' + parte_decimal_periodica
    self.parte_decimal_periodica = parte_decimal_periodica

    #Aquí se junta todo el decimal

    if self.signo == '-':

      if self.parte_decimal_no_periodica == self.parte_decimal_periodica == '':
        self.show = self.signo + self.parte_entera.replace('-','')
      elif self.parte_decimal_no_periodica == '':
        self.show = self.signo + self.parte_entera.replace('-','') + ',' + fr'\overline{{{self.parte_decimal_periodica}}}'
      elif self.parte_decimal_periodica == '':
        self.show = self.signo + self.parte_entera.replace('-','') + ',' + self.parte_decimal_no_periodica
      else:
        self.show = self.signo + self.parte_entera.replace('-','') + ',' + self.parte_decimal_no_periodica + fr'\overline{{{self.parte_decimal_periodica}}}'
    else:
      if self.parte_decimal_no_periodica == self.parte_decimal_periodica == '':
        self.show = self.parte_entera.replace('-','')
      elif self.parte_decimal_no_periodica == '':
        self.show = self.parte_entera.replace('-','') + ',' +  fr'\overline{{{self.parte_decimal_periodica}}}'
      elif self.parte_decimal_periodica == '':
        self.show = self.parte_entera.replace('-','') + ',' + self.parte_decimal_no_periodica
      else:
        self.show = self.parte_entera.replace('-','') + ',' + self.parte_decimal_no_periodica + fr'\overline{{{self.parte_decimal_periodica}}}'

    return self





  def __add__(self, other):
    if isinstance(other, (int, float)):
      return Racional(self.numerador*Racional(other).denominador+self.denominador*Racional(other).numerador, self.denominador*Racional(other).denominador)
    elif isinstance(other, str):
      return self.show + other
    elif isinstance(other, Racional):
      return Racional(self.numerador*other.denominador+self.denominador*other.numerador, self.denominador*other.denominador)
    elif isinstance(other, Natural):
      return Racional(self.numerador+other.numero*self.denominador, self.denominador)
    elif isinstance(other, Complex):
      return Complex(self+other.re, other.im)
    elif isinstance(other, Root):
      return Pol(self, other)
    elif isinstance(other, Log):
      if isinstance(other.valor , Racional):
        return self+other.valor
      else:
        return Pol(self, other)
    elif isinstance(other, Pol):
      return Pol(lista_de_terminos = [self]+other.lista_de_terminos, reducir=True)
    elif isinstance(other, Fraction):
      return Fraction(self.numerador*other.denominador+other.numerador*self.denominador, self.denominador*other.denominador)

  def __radd__(self, other):
    if isinstance(other, (int, float)):
      return self+other
    elif isinstance(other, str):
      return other + self.show

  def __sub__(self, other):
    if isinstance(other, (int, float)):
      return Racional(self.numerador*Racional(other).denominador-self.denominador*Racional(other).numerador, self.denominador*Racional(other).denominador)
    elif isinstance(other, str):
      raise Exception('No se ha programado la resta Racional - str')
    elif isinstance(other, Racional):
      return Racional(self.numerador*other.denominador-self.denominador*other.numerador, self.denominador*other.denominador)
    elif isinstance(other, Natural):
      return Racional(self.numerador-other.numero*self.denominador, self.denominador)
    elif isinstance(other, Complex):
      return Complex(self-other.re, -other.im)
    elif isinstance(other, Root):
      return Pol(self, -other)
    elif isinstance(other, Log):
      if isinstance(other.valor , Racional):
        return self-other.valor
      else:
        raise Exception('No se ha programado Racional-Log sin valor')
    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(-termino)
      return Pol(lista_de_terminos = [self]+lista_provisional)
    elif isinstance(other, Fraction):
      return Fraction(self.numerador*other.denominador-other.numerador*self.denominador, self.denominador*other.denominador)

  def __rsub__(self, other):
    if isinstance(other, (int, float)):
      return Racional(Racional(other).numerador*self.denominador-Racional(other).denominador*self.numerador, Racional(other).denominador*self.denominador)
    elif isinstance(other, str):
      return other + (-self).show

  def __mul__(self, other):
    if isinstance(other, (int, float)):
      return Racional(self.numerador*Racional(other).numerador, self.denominador*Racional(other).denominador)
    elif isinstance(other, str):
      return Term(self, {other:1})
    elif isinstance(other, dict):
      return Term(self, other)
    elif isinstance(other, Racional):
      return Racional(self.numerador*other.numerador, self.denominador*other.denominador)
    elif isinstance(other, Natural):
      return Racional(self.numerador*other.numero, self.denominador)
    elif isinstance(other, Complex):
      return Complex(self*other.re, self*other.im)
    elif isinstance(other, Root):
      return Root(other.radicando, other.indice, Racional(self.numerador*other.parte_descompuesta.numerador, self.denominador*other.parte_descompuesta.denominador))
    elif isinstance(other, Log):
      if isinstance(other.valor , Racional):
        return self*other.valor
      else:
        return Log(other.argumento, other.base, self*other.parte_descompuesta)
    elif isinstance(other, Term):
      return Term(self*other.factor_numerico, other.diccionario_de_letras_y_exponentes)
    elif isinstance(other, TermRoot):
      return TermRoot(Root(other.raiz_completa.radicando, other.raiz_completa.indice, self*other.raiz_completa.parte_descompuesta), other.termino)
    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(self*termino)
      return Pol(lista_de_terminos=lista_provisional, reducir=True)
    elif isinstance(other, Fraction):
      return Fraction(self.numerador*other.numerador, self.denominador*other.denominador)
    elif isinstance(other, Par):
      return Par(self*other.x, self*other.y)

  def __rmul__(self, other):
    if isinstance(other, (int, float)):
      return self*other
    elif isinstance(other, str):
      return self*other

  def __truediv__(self, other):
    if isinstance(other, (int, float)):
      return Racional(self.numerador*Racional(other).denominador, self.denominador*Racional(other).numerador)
    elif isinstance(other, str):
      return fraccion(self.numerador,Term(self.denominador,{other:1}))
    elif isinstance(other, Racional):
      return Racional(self.numerador*other.denominador, self.denominador*other.numerador)
    elif isinstance(other, Natural):
      return Racional(self.numerador, self.denominador*other.numero)
    elif isinstance(other, Complex):
      return Complex(Racional(self*other.re, other.re**2+other.im**2), Racional(-self*other.im, other.re**2+other.im**2))
    elif isinstance(other, Root):
      return Root(other.radicando**(other.indice-1), other.indice, self/(other.parte_descompuesta*other.radicando))
    elif isinstance(other, Log):
      if isinstance(other.valor , Racional):
        return self/other.valor
      else:
        return Fraction(self,other)
    elif isinstance(other, Term):
      diccionario_provisional = {}
      for letra in other.diccionario_de_letras_y_exponentes:
        diccionario_provisional[letra] = -other.diccionario_de_letras_y_exponentes[letra]
      return Term(self/other.factor_numerico, diccionario_provisional)
    elif isinstance(other, TermRoot):
      return TermRoot(self/other.raiz_completa, 1/other.termino)
    elif isinstance(other, Pol):
      divisor = Racional(MCD(self.numerador, other.factor_comun.numerador), MCD(self.denominador, other.factor_comun.denominador))
      return fraccion(self.show, (other/divisor).show)
    elif isinstance(other, Fraction):
      return Fraction(self.numerador*other.denominador, self.denominador*other.numerador)

  def __rtruediv__(self, other):
    if isinstance(other, (int, float)):
      return Racional(Racional(other).numerador*self.denominador, Racional(other).denominador*self.numerador)
    elif isinstance(other, str):
      return Term(1/self, {other:1})

  def __mod__(self, other):
    if isinstance(other, int) and self.denominador==1:
      return Racional(self.numerador%other)
    elif isinstance(other, Racional) and self.denominador==other.denominador==1:
      return Racional(self.numerador%other.numerador)
    elif isinstance(other, Natural) and self.denominador:
      return Racional(self.numerador%other.numero)
    else:
      raise Exception('Se intentó utilizar la operación % con un Racional cuyo denominador no es 1, o se intentó la operación con un float')

  def __rmod__(self, other):
    return other%self

  def __pow__(self, other):
    if isinstance(other, (int, float)):
      if other<0:
        self, other = Racional(self.denominador, self.numerador), abs(other)
      return Root(Racional(self.numerador**Racional(other).numerador, self.denominador**Racional(other).numerador), Racional(other).denominador)
    elif isinstance(other, str):
      return potencia(self, other)
    elif isinstance(other, Racional):
      if other<0:
        self, other = Racional(self.denominador, self.numerador), abs(other)
      return Root(Racional(self.numerador**other.numerador, self.denominador**other.numerador), other.denominador)
    elif isinstance(other, Natural):
      if other<0:
        self, other = Racional(self.denominador, self.numerador), abs(other)
      return Racional(self.numerador**other.numero, self.denominador**other.numero)

  def __rpow__(self, other):
    if isinstance(other, (int, float)):
      return Racional(other)**self
    elif isinstance(other, (str)):
      if self==0:
        return Racional(1)
      elif self==1:
        return Term(1,{other:1})
      else:
        return raiz(potencia(other, self.numerador, quitar_1=True), self.denominador)

  def __neg__(self):
    return Racional(-self.numerador, self.denominador)

  def __abs__(self):
    return Racional(abs(self.numerador), self.denominador)

  def __str__(self):
    return self.show

  def __round__(self,n=0):
    return round(self.numerador/self.denominador,n)

  def __lt__(self, other):
    if isinstance(other, (int, float)):
      return self.numerador*Racional(other).denominador < Racional(other).numerador*self.denominador
    elif isinstance(other, Racional):
      return self.numerador*other.denominador < other.numerador*self.denominador
    elif isinstance(other, Natural):
      return self.numerador < other.numero*self.denominador
    elif isinstance(other, Root):
      return float(self) < float(other)
    elif isinstance(other, Log):
      return float(self) < float(other)
    else:
      return False

  def __eq__(self, other):
    if isinstance(other, (int, float)):
      return self.numerador*Racional(other).denominador == Racional(other).numerador*self.denominador
    elif isinstance(other, Racional):
      return self.numerador*other.denominador == other.numerador*self.denominador
    elif isinstance(other, Natural):
      return self.numerador == other.numero*self.denominador
    elif isinstance(other, Log):
      if isinstance(other.valor , Racional):
        return self.numerador*other.valor.denominador == other.valor.numerador*self.denominador
      else:
        return False
    else:
      return False

  def __gt__(self, other):
    if isinstance(other, (int, float)):
      return self.numerador*Racional(other).denominador > Racional(other).numerador*self.denominador
    elif isinstance(other, Racional):
      return self.numerador*other.denominador > other.numerador*self.denominador
    elif isinstance(other, Natural):
      return self.numerador > other.numero*self.denominador
    elif isinstance(other, Root):
      return float(self) > float(other)
    elif isinstance(other, Log):
      return float(self) > float(other)
    else:
      return False

  def __int__(self):
    return int(self.numerador/self.denominador)

  def __float__(self):
    return self.numerador/self.denominador

  def __le__(self, other):
    return self<other or self==other

  def __ge__(self, other):
    return self>other or self==other

  def __ne__(self, other):
    return not self==other

  def __iadd__(self, other):
    return self+other

  def __isub__(self, other):
    return self-other

  def __imul__(self, other):
    return self*other  

  def __idiv__(self, other):
    return self/other

  def __ipow__(self, other):
    return self**other



class Natural:
  '''self
  signo                 str +
  numero                int
  show                str
  lista_de_divisores          list
  lista_de_no_divisores         list
  primo                 bool
  lista_descomposicion_en_primos    list
  lista_primos_divisores        list
  cantidad_De_digitos         int
  valores_posicionales        dict
  números de los valores posicionales int
  '''

  def __init__(self, numero):
    self.diccionario_de_letras_y_exponentes = {}
    self.factor_literal = ''
    self.lista_de_terminos = [self]

    if isinstance(numero, Racional):
      if numero.denominador!=1:
        raise Exception('Se ha ingresado un número decimal como un número Natural')
      else:
        numero = numero.numerador
    if numero<0:
      raise Exception('Se ha ingresado un número negativo como un número Natural')
    self.signo = '+'
    self.numero = numero
    self.show = str(numero)
    self.lista_de_divisores = []
    self.lista_de_no_divisores = []
    self.lista_descomposicion_en_primos = []
    self.lista_primos_divisores = []
    self.cantidad_de_digitos = len(str(numero))


    # Aquí se determinan los valores posicionales hasta la unidad de billon.
    self.unidad = 0
    self.decena = 0
    self.centena = 0
    self.unidad_de_mil = 0
    self.decena_de_mil = 0
    self.centena_de_mil = 0
    self.unidad_de_millon = 0
    self.decena_de_millon = 0
    self.centena_de_millon = 0
    self.unidad_de_mil_de_millon = 0
    self.decena_de_mil_de_millon = 0
    self.centena_de_mil_de_millon = 0
    self.unidad_de_billon = 0
    self.valores_posicionales = {0:'unidad', 1:'decena', 2:'centena', 3:'unidad_de_mil', 4:'decena_de_mil', 5:'centena_de_mil', 6:'unidad_de_millon', 7:'decena_de_millon', 8:'centena_de_millon', 9:'unidad_de_mil_millon', 10:'decena_de_mil_millon', 11:'centena_de_mil_millon', 12:'unidad_de_billón'}
    for posicion in self.valores_posicionales:
      if posicion < self.cantidad_de_digitos:
        exec('self.'+self.valores_posicionales[posicion]+' = '+str(numero)[-posicion-1])



    _copia = numero

    for intento in range(1, numero+1):
      #Completa la lista de los divisores
      if numero%intento==0:
        self.lista_de_divisores.append(intento)
      #Completa la lista de los no divisores
      else:
        self.lista_de_no_divisores.append(intento)
      #Completa la lista de la descomposición en primos
      while _copia%intento==0 and primo(intento):
        self.lista_descomposicion_en_primos.append(intento)
        _copia = int(_copia/intento)

    #Determina si el Natural es primo o no
    if len(self.lista_de_divisores)==2:
      self.primo=True
    else:
      self.primo=False

    #Determina los divisores primos
    for numero in self.lista_descomposicion_en_primos:
      if numero not in self.lista_primos_divisores:
        self.lista_primos_divisores.append(numero)
    self.factor_numerico = self

  def __add__(self, other):
    if isinstance(other, (int, float)):
      return Racional(self.numero*Racional(other).denominador+Racional(other).numerador, Racional(other).denominador)
    elif isinstance(other, str):
      return self.show + other
    elif isinstance(other, Racional):
      return Racional(self.numero*other.denominador+other.numerador, other.denominador)
    elif isinstance(other, Natural):
      return Racional(self.numero+other.numero)
    elif isinstance(other, Complex):
      return Complex(self.numero+other.re, other.im)
    elif isinstance(other, Root):
      return Pol(self, other)
    elif isinstance(other, Log):
      if isinstance(other.valor , Racional):
        return self.numero+other.valor
      else:
        raise Exception('No se ha programado Natural+Log sin valor')
    elif isinstance(other, Pol):
      return Pol(lista_de_terminos = [self]+other.lista_de_terminos, reducir=True)    
    

  def __radd__(self, other):
    if isinstance(other, (int, float)):
      return self+other
    elif isinstance(other, str):
      return other + self.show

  def __sub__(self, other):
    if isinstance(other, (int, float)):
      return Racional(self.numero*Racional(other).denominador-Racional(other).numerador, Racional(other).denominador)
    elif isinstance(other, Racional):
      return Racional(self.numero*other.denominador-other.numerador, other.denominador)
    elif isinstance(other, Natural):
      return Racional(self.numero-other.numero)
    elif isinstance(other, Complex):
      return Complex(self.numero-other.re, -other.im)
    elif isinstance(other, Root):
      return Pol(self, -other)
    elif isinstance(other, Log):
      if isinstance(other.valor , Racional):
        return self.numero-other.valor
      else:
        raise Exception('No se ha programado Natural-Log sin valor')
    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(-termino)
      return Pol(lista_de_terminos = [self]+lista_provisional)

  def __rsub__(self, other):
    if isinstance(other, (int, float)):
      return Racional(Racional(other).numerador-self.numero*Racional(other).denominador, Racional(other).denominador)
    elif isinstance(other, str):
      return other + (-self).show

  def __mul__(self, other):
    if isinstance(other, (int, float)):
      return Racional(self.numero*Racional(other).numerador, Racional(other).denominador)
    elif isinstance(other, str):
      return Term(Racional(self.numero), {other:1})
    elif isinstance(other, dict):
      return Term(Racional(self.numero), other)
    elif isinstance(other, Racional):
      return Racional(self.numero*other.numerador, other.denominador)
    elif isinstance(other, Natural):
      return Racional(self.numero*other.numero)
    elif isinstance(other, Complex):
      return Complex(self.numero*other.re, self.numero*other.im)
    elif isinstance(other, Root):
      return Root(other.radicando, other.indice, Racional(self.numero*other.parte_descompuesta.numerador, other.parte_descompuesta.denominador))
    elif isinstance(other, Log):
      if isinstance(other.valor , Racional):
        return self.numero*other.valor
      else:
        return Log(other.argumento, other.base, self.numero*other.parte_descompuesta)
    elif isinstance(other, Term):
      return Term(self.numero*other.factor_numerico, other.diccionario_de_letras_y_exponentes)
    elif isinstance(other, TermRoot):
      return TermRoot(Root(other.raiz_completa.radicando, other.raiz_completa.indice, self*other.raiz_completa.parte_descompuesta), other.termino)
    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(self*termino)
      return Pol(lista_de_terminos=lista_provisional, reducir=True)

  def __rmul__(self, other):
    if isinstance(other, (int, float)):
      return self*other
    elif isinstance(other, str):
      return self*other

  def __truediv__(self, other):
    if isinstance(other, (int, float)):
      return Racional(self.numero, other)
    elif isinstance(other, str):
      return fraccion(self.numero, other)
    elif isinstance(other, Racional):
      return Racional(self.numero*other.denominador, other.numerador)
    elif isinstance(other, Natural):
      return Racional(self.numero, other.numero)
    elif isinstance(other, Complex):
      return Complex(Racional(self*other.re, other.re**2+other.im**2), Racional(-self*other.im, other.re**2+other.im**2))
    elif isinstance(other, Root):
      return Root(other.radicando**(other.indice-1), other.indice, self.numero/(other.parte_descompuesta*other.radicando))
    elif isinstance(other, Log):
      if isinstance(other.valor , Racional):
        return self.numero/other.valor
      else:
        return Fraction(self,other)
    elif isinstance(other, Term):
      diccionario_provisional = {}
      for letra in other.diccionario_de_letras_y_exponentes:
        diccionario_provisional[letra] = -other.diccionario_de_letras_y_exponentes[letra]
      return Term(self.numero/other.factor_numerico, diccionario_provisional)
    elif isinstance(other, TermRoot):
      return TermRoot(self/other.raiz_completa, 1/other.termino)
    elif isinstance(other, Pol):
      divisor = Racional(MCD(self.numero, other.factor_comun.numerador), MCD(1, other.factor_comun.denominador))
      return fraccion(Racional(self.numero*divisor.denominador,divisor.numerador).show, (other/divisor).show)

  def __rtruediv__(self, other):
    if isinstance(other, (int, float)):
      return self*other
    elif isinstance(other, str):
      return Term(Racional(1,self.numero), other)

  def __mod__(self, other):
    if isinstance(other, int):
      return self.numero%other
    elif isinstance(other, Racional) and other.denominador==1:
      return self.numero%other.numerador
    elif isinstance(other, Natural):
      return self.numero%other.numero
    else:
      raise Exception('Se intentó utilizar la operación % con un Racional cuyo denominador no es 1, o se intentó la operación con un float')

  def __rmod__(self, other):
    return other%self.numero

  def __pow__(self, other):
    if isinstance(other, (int, float)):
      return Root(self.numero**Racional(other))
    elif isinstance(other, str):
      return potencia(self.numero, other)
    elif isinstance(other, Racional):
      return Root(self.numero**other)
    elif isinstance(other, Natural):
      return Racional(Racional(self.numero)**other.numero)

  def __rpow__(self, other):
    if isinstance(other, (int, float)):
      return Racional(other)**self.numero
    elif isinstance(other, (str)):
      if self==0:
        return Racional(1)
      elif self==1:
        return Term(1,{other:1})
      else:
        return potencia(other, self.numero)

  def __neg__(self):
    return Racional(-self.numero)

  def __abs__(self):
    return Racional(abs(self.numero))

  def __str__(self):
    return self.show

  def __lt__(self, other):
    if isinstance(other, (int, float)):
      return self.numero < other
    elif isinstance(other, Racional):
      return self.numero*other.denominador < other.numerador
    elif isinstance(other, Natural):
      return self.numero < other.numero
    elif isinstance(other, Root):
      return float(self) < float(other)
    elif isinstance(other, Log):
      return float(self) < float(other)
    else:
      return False

  def __eq__(self, other):
    if isinstance(other, (int, float)):
      return self.numero == other
    elif isinstance(other, Racional):
      return self.numero*other.denominador == other.numerador
    elif isinstance(other, Natural):
      return self.numero == other.numero
    elif isinstance(other, Log):
      if isinstance(other.valor , Racional):
        return self.numero*other.valor.denominador == other.valor.numerador
      else:
        return False
    else:
      return False

  def __gt__(self, other):
    if isinstance(other, (int, float)):
      return self.numero > other
    elif isinstance(other, Racional):
      return self.numero*other.denominador > other.numerador
    elif isinstance(other, Natural):
      return self.numero > other.numero
    elif isinstance(other, Root):
      return float(self) < float(other)
    elif isinstance(other, Log):
      return float(self) < float(other)
    else:
      return False

  def __int__(self):
    return self.numero

  def __float__(self):
    return float(self.numero)

  def __le__(self, other):
    return self<other or self==other

  def __ge__(self, other):
    return self>other or self==other

  def __ne__(self, other):
    return not self==other

  def __iadd__(self, other):
    return self+other

  def __isub__(self, other):
    return self-other

  def __imul__(self, other):
    return self*other  

  def __idiv__(self, other):
    return self/other

  def __ipow__(self, other):
    return self**other



class Complex:
  '''self
  re          Racional
  im          Racional
  show        str
  Par         Par
  modulo        Root
  '''
  def __init__(self, parte_real, parte_imaginaria=0, determinar_conjugado=True):
    self.diccionario_de_letras_y_exponentes = {}
    self.factor_literal = ''
    self.lista_de_terminos = [self]

    #Adapta las partes para que sean Racionales si son int, float o Naturales
    if isinstance(parte_real, (int, float, Natural)):
      parte_real = Racional(parte_real)    
    if isinstance(parte_imaginaria, (int, float, Natural)):
      parte_imaginaria = Racional(parte_imaginaria)

    #Adapta las partes si alguna es otro complejo
    if isinstance(parte_real, Complex) and not isinstance(parte_imaginaria, Complex):
      parte_real      =   parte_real.re
      parte_imaginaria  =   parte_real.im + parte_imaginaria
    if isinstance(parte_real, Complex) and not isinstance(parte_imaginaria, Complex):
      parte_real      =   parte_real - parte_imaginaria.im
      parte_imaginaria  =   parte_imaginaria.re
    if isinstance(parte_real, Complex) and not isinstance(parte_imaginaria, Complex):
      parte_real      =   parte_real.re - parte_imaginaria.im
      parte_imaginaria  =   parte_real.im + parte_imaginaria.re


    #Determina self parte real
    self.re = parte_real

    #Determina self parte imaginaria
    self.im = parte_imaginaria

    #Determina self show forma par ordenado
    self.Par = Par(self.re, self.im)

    #Transforma a Racional si la parte imaginaria es 0
    if self.im==0:
      if isinstance(self.re, Racional):
        self.__class__ = Racional
        self.__init__(self.re)
        return None
      elif isinstance(self.re, Root):
        self.__class__ = Root
        self.__init__(self.re.radicando, self.re.indice, self.re.parte_descompuesta)
        return None
    #Determina el self show
    self.show = Pol(self.re, Term(self.im, {'i':1})).show
    self.factor_numerico = self

  def conjugate(self):
    return Complex(self.re, -self.im)

  def __add__(self, other):
    if isinstance(other, (int, float)):
      return Complex(self.re+other, self.im)
    elif isinstance(other, str):
      return self.show + other
    elif isinstance(other, Racional):
      return Complex(self.re+other, self.im)
    elif isinstance(other, Natural):
      return Complex(self.re+other.numero, self.im)
    elif isinstance(other, Complex):
      return Complex(self.re+other.re, self.im+other.im)
    elif isinstance(other, Root):
      return Pol(self, other)
    elif isinstance(other, Pol):
      return Pol(lista_de_terminos = [self]+other.lista_de_terminos, reducir=True)

  def __radd__(self, other):
    if isinstance(other, (int, float)):
      return Complex(self.re+other, self.im)
    elif isinstance(other, str):
      return other + self.show

  def __sub__(self, other):
    if isinstance(other, (int, float)):
      return Complex(self.re-other, self.im)
    elif isinstance(other, Racional):
      return Complex(self.re-other, self.im)
    elif isinstance(other, Natural):
      return Complex(self.re-other.numero, self.im)
    elif isinstance(other, Complex):
      return Complex(self.re-other.re, self.im-other.im)
    elif isinstance(other, Root):
      return Pol(self, -other)
    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(-termino)
      return Pol(lista_de_terminos = [self]+lista_provisional)

  def __rsub__(self, other):
    if isinstance(other, (int, float)):
      return Complex(other-self.re, -self.im)
    elif isinstance(other, str):
      return other + (-self).show

  def __mul__(self, other):
    if isinstance(other, (int, float)):
      return Complex(self.re*other, self.im*other)
    elif isinstance(other, str):
      return Term(self, {other:1})
    elif isinstance(other, dict):
      return Term(self, other)
    elif isinstance(other, Racional):
      return Complex(self.re*other, self.im*other)
    elif isinstance(other, Natural):
      return Complex(self.re*other.numero, self.im)
    elif isinstance(other, Complex):
      return Complex(self.re*other.re-self.im*other.im, self.re*other.im+self.im*other.re)
    elif isinstance(other, Root):
      return Root(other.radicando, other.indice, self*other.parte_descompuesta)
    elif isinstance(other, TermRoot):
      return TermRoot(self*other.raiz_completa, other.termino)
    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(self*termino)
      return Pol(lista_de_terminos=lista_provisional, reducir=True)

  def __rmul__(self, other):
    if isinstance(other, (int, float)):
      return Complex(self.re*other, self.im*other)

  def __truediv__(self, other):
    if isinstance(other, (int, float)):
      return Complex(self.re/other, self.im/other)
    elif isinstance(other, str):
      return fraccion(self.show, other)
    elif isinstance(other, Racional):
      return Complex(self.re/other, self.im/other)
    elif isinstance(other, Complex):
      return Complex(Racional(self.re*other.re+self.im*other.im, other.re*other.re+other.im*other.im), Racional(self.im*other.re-self.re*other.im, other.re*other.re+other.im*other.im))
    elif isinstance(other, Root):
      return Complex(self.re/other, self.im/other)
    elif isinstance(other, TermRoot):
      return TermRoot(self/other.raiz_completa, 1/other.termino)
    elif isinstance(other, Pol):
      divisor = Racional(MCD(self.re.numerador, self.im.numerador, other.factor_comun.numerador), MCD(self.re.denominador, self.im.denominador, other.factor_comun.denominador))
      return fraccion(Complex(self.re/divisor, self.im/divisor).show, (other/divisor).show)

  def __rtruediv__(self, other):
    if isinstance(other, (int, float)):
      return Complex(other*self.re, -other*self.im)/(self.re**2+self.im**2)
    elif isinstance(other, str):
      return fraccion(other, self)

  def __neg__(self):
    return Complex(-self.re, -self.im)

  def __abs__(self):
    return Root(self.re**2+self.im**2)

  def __pow__  (self, other):
    if isinstance(other, int):
      if other==0:
        return Racional(1)
      elif 0<other:
        resultado = 1
        for _ in range(0, other):
          resultado = resultado*self
        return resultado
      elif other<0:
        resultado = 1
        for _ in range(other, 0):
          resultado = resultado/self
        return resultado

  def __str__(self):
    return self.show

  def __eq__(self, other):
    if isinstance(other, (int, float)):
      return self.re==other and self.im==0
    elif isinstance(other, Racional):
      return self.re==other and self.im==0
    elif isinstance(other, Natural):
      return self.re==other.numero and self.im==0
    if isinstance(other, Complex):
      return self.re==other.re and self.im==other.im
    else:
      return False

  def __le__(self, other):
    return self<other or self==other

  def __ge__(self, other):
    return self>other or self==other

  def __ne__(self, other):
    return not self==other

  def __iadd__(self, other):
    return self+other

  def __isub__(self, other):
    return self-other

  def __imul__(self, other):
    return self*other  

  def __idiv__(self, other):
    return self/other

  def __ipow__(self, other):
    return self**other



class UnidadImaginaria(Complex):
  def __init__(self):
    self.re = Racional(0)
    self.im = Racional(1)
    self.show = 'i'
  def __pow__(self, other):
    if isinstance(other, int):
      if other%4==0:
        return Complex(1)
      elif other%4==1:
        return Complex(0,1)
      elif other%4==2:
        return Racional(-1)
      elif other%4==3:
        return Complex(0,-1)
    else:
      raise Exception('Se elevó la unidad imaginaria con expotennte no int')



class Root:
  '''self
  radicando       Racional
  indice        Racional
  parte_descompuesta  Racional
  show        str
  '''
  def __init__(self, radicando, indice=Racional(2), parte_descompuesta=Racional(1), descomponer=False, simplificar_indice=False):
    self.diccionario_de_letras_y_exponentes = {}
    self.factor_literal = ''
    self.lista_de_terminos = [self]

    if isinstance(radicando, Root):
      self.radicando, self.indice, self.parte_descompuesta = radicando.parte_descompuesta**radicando.indice*radicando.radicando, indice*radicando.indice, Racional(parte_descompuesta)
    else:
      self.radicando = Racional(radicando)
      self.indice = Racional(indice)
      self.parte_descompuesta = Racional(parte_descompuesta)

    #Arregla el índice si es negativo
    if self.indice<0:
      self.indice = abs(self.indice)
      self.radicando = self.radicando**(-1)

    #Arregla el índice si es un decimal. Lo hace elevando el radicando.
    if self.indice.denominador != 1:
      self.radicando = self.radicando**self.indice.numerador
      self.indice = Racional(self.indice.denominador)

    if self.indice.numerador%2==0 and self.radicando<0:
      raise Exception('Se intentó calcular una raiz índice par y radicando negativo')

    elif indice==0:
      raise Exception('Se intentó calcular una raiz con índice 0')

    #Arregla el radicando si es negativo, lo hace sacando el menos de la raiz
    elif self.indice.numerador%2==1 and radicando<0:
      self.parte_descompuesta = -self.parte_descompuesta
      self.radicando = abs(self.radicando)
    
    self.signo = self.parte_descompuesta.signo


    #Aquí se calcula la raiz
    numerador_encontrado = False
    denominador_encontrado = False
    for intento in range(int(self.radicando.numerador**(1/self.indice.numerador)-1), int(self.radicando.numerador**(1/self.indice.numerador)+1)):
      if intento**self.indice.numerador==self.radicando.numerador:
        raiz_numerador = intento
        numerador_encontrado = True
        break
    for intento in range(int(self.radicando.denominador**(1/self.indice.numerador)-1), int(self.radicando.denominador**(1/self.indice.denominador)+1)):
      if intento**self.indice.numerador==self.radicando.denominador:
        raiz_denominador = intento
        denominador_encontrado = True
        break

     #Transforma a Racional en caso de que se encuentren las raíces 
    if numerador_encontrado and denominador_encontrado:
      self.__class__ = Racional
      self.__init__(self.parte_descompuesta*raiz_numerador, raiz_denominador)
      self.radicando = Racional(1)
      self.indice = Racional(1)
      self.parte_descompuesta = self
      return None

    elif self.parte_descompuesta==0:
      self.__class__ = Racional
      self.__init__(0)
      self.radicando = Racional(0)
      self.indice = Racional(1)
      self.parte_descompuesta = self
      return None


    #Simplifica el indice con el exponente del radicando si lo pide
    if simplificar_indice:
      divisores = []
      for numero in Natural(self.indice.numerador).lista_de_divisores:
        divisores = [numero] + divisores
      divisores.remove(1)
      divisores.remove(int(indice))

      numerador = int(self.radicando.numerador)
      denominador = int(self.radicando.denominador)
      indice = int(indice)
      for divisor in divisores:
        numerador_encontrado = False
        denominador_encontrado = False
      
        for intento in range(int(numerador**(1/divisor)-1), int(numerador**(1/divisor)+1)):
          if intento**divisor==numerador:
            raiz_numerador = intento
            numerador_encontrado = True
            break
        for intento in range(int(denominador**(1/divisor)-1), int(denominador**(1/divisor)+1)):
          if intento**divisor==denominador:
            raiz_denominador = intento
            denominador_encontrado = True
            break
        if numerador_encontrado and denominador_encontrado:
          self.indice = self.indice/divisor
          self.radicando = Racional(raiz_numerador, raiz_denominador)
          break



    #Descompone la raiz si lo pide, busca los factores primos y divideo o multiplica de ser necesario
    if descomponer:
      indice = int(self.indice.numerador)

      numerador = Natural(abs(self.radicando.numerador))
      for numero_primo in numerador.lista_primos_divisores:
        cantidad_de_apariciones = numerador.lista_descomposicion_en_primos.count(numero_primo)
        if 0 < cantidad_de_apariciones // indice:
          self.parte_descompuesta = self.parte_descompuesta*numero_primo**(cantidad_de_apariciones // indice)
          self.radicando = self.radicando / numero_primo**((cantidad_de_apariciones // indice)*indice)

      denominador = Natural(abs(self.radicando.denominador))
      for numero_primo in denominador.lista_primos_divisores:
        cantidad_de_apariciones = denominador.lista_descomposicion_en_primos.count(numero_primo)
        if 0 < cantidad_de_apariciones // indice:
          self.parte_descompuesta = self.parte_descompuesta / numero_primo**(cantidad_de_apariciones // indice)
          self.radicando = self.radicando * numero_primo**((cantidad_de_apariciones // indice)*indice)


    #Determina el self.show en caso de que la raiz sea inexacta
    if self.parte_descompuesta.denominador==1:
      if self.parte_descompuesta==1:
        self.show = raiz(self.radicando, self.indice)
      elif self.parte_descompuesta==-1:
        self.show = '-'+raiz(self.radicando, self.indice)
      else:
        self.show = self.parte_descompuesta.show+raiz(self.radicando, self.indice)
    else:
      if self.parte_descompuesta.numerador==1:
        self.show = fraccion(raiz(self.radicando, self.indice), self.parte_descompuesta.denominador)
      elif self.parte_descompuesta.numerador==-1:
        self.show = '-' + fraccion(raiz(self.radicando, self.indice), self.parte_descompuesta.denominador)
      else:
        if self.signo == '-':
          self.show = '-' + fraccion(str(abs(self.parte_descompuesta.numerador))+raiz(self.radicando, self.indice), self.parte_descompuesta.denominador)
        elif self.signo == '+':
          self.show = fraccion(str(self.parte_descompuesta.numerador)+raiz(self.radicando, self.indice), self.parte_descompuesta.denominador)

      self.factor_numerico = self

  def __add__(self, other):
    if isinstance(other, str):
      return self.show + other
    elif isinstance(other, Root) and self.radicando==other.radicando and self.indice==other.indice:
      return Root(self.radicando, self.indice, self.parte_descompuesta+other.parte_descompuesta)
    elif isinstance(other, Pol):
      return Pol(lista_de_terminos = [self]+other.lista_de_terminos, reducir=True)
    elif isinstance(other, Fraction):
      return Fraction(self*other.denominador+other.numerador, other.denominador)

  def __radd__(self, other):
    if isinstance(other, str):
      return other + self.show

  def __sub__(self, other):
    if isinstance(other, Root) and self.radicando==other.radicando and self.indice==other.indice:
      return Root(self.radicando, self.indice, self.parte_descompuesta-other.parte_descompuesta)

    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(-termino)
      return Pol(lista_de_terminos = [self]+lista_provisional)
    elif isinstance(other, Fraction):
      return Fraction(self*other.denominador-other.numerador, other.denominador)

  def __rsub__(self, other):
    return other.show+(-self.show)

  def __mul__(self, other):
    if isinstance(other, (int, float, Racional, Natural)):
      return Root(self.radicando, self.indice, self.parte_descompuesta*other)
    elif isinstance(other, str):
      return TermRoot(self, Term(1,{other:1}))
    elif isinstance(other, dict):
      return TermRoot(self, Term(1,other))
    elif isinstance(other, Root):
      return Root(self.radicando**(MCM(self.indice.numerador, other.indice.numerador)/self.indice.numerador)  *  other.radicando**(MCM(self.indice.numerador, other.indice.numerador)/other.indice.numerador), MCM(self.indice.numerador, other.indice.numerador), self.parte_descompuesta*other.parte_descompuesta)
    elif isinstance(other, TermRoot):
      return TermRoot(self*other.raiz_completa, other.termino)
    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(self*termino)
      return Pol(lista_de_terminos=lista_provisional, reducir=True)
    elif isinstance(other, Fraction):
      return Fraction((self*self.parte_descompuesta.denominador)*other.numerador, self.parte_descompuesta.denominador*other.denominador)

  def __rmul__(self, other):
    if isinstance(other, (int, float)):
      return Root(self.radicando, self.indice, other*self.parte_descompuesta)
    elif isinstance(other, str):
      return TermRoot(self, Term(1,{other:1}))

  def __truediv__(self, other):
    if isinstance(other, (int, float, Racional, Natural)):
      return Root(self.radicando, self.indice, self.parte_descompuesta/other)
    elif isinstance(other, str):
      return fraccion(self.show, other)
    elif isinstance(other, Root):
      return Root(self.radicando**(MCM(self.indice.numerador, other.indice.numerador)/self.indice.numerador)  /  other.radicando**(MCM(self.indice.numerador, other.indice.numerador)/other.indice.numerador), MCM(self.indice.numerador, other.indice.numerador), self.parte_descompuesta/other.parte_descompuesta)
    elif isinstance(other, TermRoot):
      return TermRoot(self/other.raiz_completa, 1/other.termino)
    elif isinstance(other, Pol):
      divisor = Racional(MCD(self.parte_descompuesta.numerador, other.factor_comun.numerador), MCD(self.parte_descompuesta.denominador, other.factor_comun.denominador))
      return fraccion(Root(self.radicando,self.indice,self.parte_descompuesta/divisor).show, (other/divisor).show)
    elif isinstance(other, Fraction):
      return Fraction((self*self.parte_descompuesta.denominador)*other.denominador, self.parte_descompuesta.denominador*other.numerador)

  def __rtruediv__(self, other):
    if isinstance(other, (int, float)):
      return Root(self.radicando**(self.indice-1), self.indice, other/(self.parte_descompuesta*self.radicando))
    elif isinstance(other, str):
      return fraccion(other, self.show)

  def __neg__(self):
    return Root(self.radicando,self.indice,-self.parte_descompuesta)

  def __pow__(self, other):
    if isinstance(other, (int, float, Natural)):
      return Root(self.radicando**Racional(other).numerador, self.indice*Racional(other).denominador, self.parte_descompuesta**Racional(other))
    if isinstance(other, Racional):
      return Root(self.radicando**other.numerador, self.indice*other.denominador, self.parte_descompuesta**other)

  def __str__(self):
    return self.show

  def __round__(self,n=0):
    return round(float(self.radicando)**float(1/self.indice)*float(self.parte_descompuesta), n)

  def __abs__(self):
    return Root(self.radicando, self.indice, abs(self.parte_descompuesta))

  def __lt__(self, other):
    if isinstance(other, (int, float, Racional, Natural)):
      other = Root(other, 1, 1)
    if isinstance(other, Racional) and int(self.signo+'1')*abs(self.parte_descompuesta)**(self.indice.numerador)*self.radicando < int(other.signo+'1')*abs(other)**self.indice.numerador:
      return True
    if isinstance(other, Root) and int(self.signo+'1')*abs(self.parte_descompuesta)**(self.indice*other.indice)*self.radicando**other.indice < int(other.signo+'1')*abs(other.parte_descompuesta)**(other.indice*self.indice)*other.radicando**self.indice:
      return True
    elif isinstance(other, Log):
      return float(self) < float(other)
    else:
      return False

  def __eq__(self, other):
    if isinstance(other, Root):
      return int(self.signo+'1')*abs(self.parte_descompuesta)**(self.indice*other.indice)*self.radicando**other.indice == int(other.signo+'1')*abs(other.parte_descompuesta)**(other.indice*self.indice)*other.radicando**self.indice
    else:
      return False

  def __gt__(self, other):
    if isinstance(other, (int, float, Racional, Natural)):
      other = Root(other, 1, 1)
    if isinstance(other, Racional) and int(self.signo+'1')*abs(self.parte_descompuesta)**(self.indice.numerador)*self.radicando > int(other.signo+'1')*abs(other)**self.indice.numerador:
      return True
    elif isinstance(other, Root) and int(self.signo+'1')*abs(self.parte_descompuesta)**(self.indice*other.indice)*self.radicando**other.indice > int(other.signo+'1')*abs(other.parte_descompuesta)**(other.indice*self.indice)*other.radicando**self.indice:
      return True
    elif isinstance(other, Log):
      return float(self) > float(other)
    else:
      return False

  def __int__(self):
    return int(float(self.radicando)**float(1/self.indice)*float(self.parte_descompuesta))

  def __float__(self):
    return float(self.radicando)**float(1/self.indice)*float(self.parte_descompuesta)

  def __le__(self, other):
    return self<other or self==other

  def __ge__(self, other):
    return self>other or self==other

  def __ne__(self, other):
    return not self==other

  def __iadd__(self, other):
    return self+other

  def __isub__(self, other):
    return self-other

  def __imul__(self, other):
    return self*other  

  def __idiv__(self, other):
    return self/other

  def __ipow__(self, other):
    return self**other



class Log:
  '''self
  argumento   Racional/Root
  base    Racional/Root
  show    str
  valor     Racional/None
  parte_descompuesta    Racional
  '''
  def __init__(self, argumento, base=10, parte_descompuesta=Racional(1)):
    self.parte_descompuesta = Racional(parte_descompuesta)
    if isinstance(argumento, (int, float, Natural)):
      argumento = Racional(argumento)
    if isinstance(base, (int, float, Natural)):
      base = Racional(base)
    if argumento==0:
      raise Exception('El argumento en un Log es 0')
    if base in [0,1]:
      raise Exception(f'La base en un Log es {base}')
    self.argumento = argumento
    self.base = base
    if self.parte_descompuesta==1:
      self.show = logaritmo(self.argumento, self.base, parentesis_automatico=False)
    elif self.parte_descompuesta==-1:
      self.show = '-'+logaritmo(self.argumento, self.base, parentesis_automatico=False)
    else:
      self.show = self.parte_descompuesta.show + logaritmo(self.argumento, self.base, parentesis_automatico=False)



    #Trabaja el ARGUMENTO
    indice_de_argumento = Racional(1)
    if isinstance(argumento, Root):
      argumento, indice_de_argumento = argumento.radicando, Racional(argumento.indice.numerador)
    if isinstance(argumento, Racional):
      # numerador de argumento
      tiene_raiz = True
      numerador_de_argumento = Natural(argumento.numerador)
      if not numerador_de_argumento==1:
        exponente_de_numerador_de_argumento = numerador_de_argumento.lista_descomposicion_en_primos.count(numerador_de_argumento.lista_primos_divisores[0])
      else:
        exponente_de_numerador_de_argumento = 1
      base_de_numerador_de_argumento = 1
      for numero_primo in numerador_de_argumento.lista_primos_divisores:
        base_de_numerador_de_argumento = base_de_numerador_de_argumento*numero_primo
        if not numerador_de_argumento.lista_descomposicion_en_primos.count(numero_primo):
          tiene_raiz = False
          break
      if tiene_raiz == False:
        exponente_de_numerador_de_argumento = 1
        base_de_numerador_de_argumento = argumento.numerador
      # denominador de argumento
      tiene_raiz = True
      denominador_de_argumento = Natural(argumento.denominador)
      if not denominador_de_argumento==1:
        exponente_de_denominador_de_argumento = denominador_de_argumento.lista_descomposicion_en_primos.count(denominador_de_argumento.lista_primos_divisores[0])
      else:
        exponente_de_denominador_de_argumento = 1
      base_de_denominador_de_argumento = 1
      for numero_primo in denominador_de_argumento.lista_primos_divisores:
        base_de_denominador_de_argumento = base_de_denominador_de_argumento*numero_primo
        if not denominador_de_argumento.lista_descomposicion_en_primos.count(numero_primo):
          tiene_raiz = False
          break
      if tiene_raiz == False:
        exponente_de_denominador_de_argumento = 1
        base_de_denominador_de_argumento = argumento.denominador
      # arregla los exponentes 1
      if base_de_numerador_de_argumento==1:
        exponente_de_numerador_de_argumento = exponente_de_denominador_de_argumento
      elif base_de_denominador_de_argumento==1:
        exponente_de_denominador_de_argumento = exponente_de_numerador_de_argumento
      #Simplifica los exponentes del argumento
      exponentes_de_argumento_simplificados = Racional(exponente_de_numerador_de_argumento, exponente_de_denominador_de_argumento)
      numero_por_el_que_se_simplificaron_los_exponentes_del_argumento = Racional(exponente_de_numerador_de_argumento, exponentes_de_argumento_simplificados.numerador)
      exponente_de_argumento = numero_por_el_que_se_simplificaron_los_exponentes_del_argumento
    



    #Trabaja la BASE
    indice_de_base = Racional(1)
    if isinstance(base, Root):
      base, indice_de_base = base.radicando, Racional(base.indice.numerador)
    if isinstance(base, Racional):
      # numerador de base
      tiene_raiz = True
      numerador_de_base = Natural(base.numerador)
      if not numerador_de_base==1:
        exponente_de_numerador_de_base = numerador_de_base.lista_descomposicion_en_primos.count(numerador_de_base.lista_primos_divisores[0])
      base_de_numerador_de_base = 1
      for numero_primo in numerador_de_base.lista_primos_divisores:
        base_de_numerador_de_base = base_de_numerador_de_base*numero_primo
        if not numerador_de_base.lista_descomposicion_en_primos.count(numero_primo):
          tiene_raiz = False
          break
      if tiene_raiz == False:
        exponente_de_numerador_de_base = 1
        base_de_numerador_de_base = base.numerador
      # denominador de base
      tiene_raiz = True
      denominador_de_base = Natural(base.denominador)
      if not denominador_de_base==1:
        exponente_de_denominador_de_base = denominador_de_base.lista_descomposicion_en_primos.count(denominador_de_base.lista_primos_divisores[0])
      base_de_denominador_de_base = 1
      for numero_primo in denominador_de_base.lista_primos_divisores:
        base_de_denominador_de_base = base_de_denominador_de_base*numero_primo
        if not denominador_de_base.lista_descomposicion_en_primos.count(numero_primo):
          tiene_raiz = False
          break
      if tiene_raiz == False:
        exponente_de_denominador_de_base = 1
        base_de_denominador_de_base = base.denominador
      # arregla los exponentes 1
      if base_de_numerador_de_base==1:
        exponente_de_numerador_de_base = exponente_de_denominador_de_base
      elif base_de_denominador_de_base==1:
        exponente_de_denominador_de_base = exponente_de_numerador_de_base
      #Simplifica los exponentes del base
      exponentes_de_base_simplificados = Racional(exponente_de_numerador_de_base, exponente_de_denominador_de_base)
      numero_por_el_que_se_simplificaron_los_exponentes_de_la_base = Racional(exponente_de_numerador_de_base, exponentes_de_base_simplificados.numerador)
      exponente_de_base = numero_por_el_que_se_simplificaron_los_exponentes_de_la_base


    # determina su valor en caso de poder calcularse
    if self.argumento==1:
      self.valor = Racional(0)
    elif base_de_numerador_de_argumento==base_de_numerador_de_base and base_de_denominador_de_argumento==base_de_denominador_de_base and exponentes_de_argumento_simplificados==exponentes_de_base_simplificados:
      self.valor = self.parte_descompuesta * Racional(exponente_de_argumento/indice_de_argumento, exponente_de_base/indice_de_base)
    elif base_de_numerador_de_argumento==base_de_denominador_de_base and base_de_denominador_de_argumento==base_de_numerador_de_base and exponentes_de_argumento_simplificados==exponentes_de_base_simplificados**(-1):
      self.valor = self.parte_descompuesta * -Racional(exponente_de_argumento/indice_de_argumento, exponente_de_base/indice_de_base)
    else:
      self.valor = self



  def __add__(self, other):
    if isinstance(other, (int, float)):
      return Log(self.argumento**self.parte_descompuesta*other**self.base, self.base)
    elif isinstance(other, str):
      return self.show + other
    elif isinstance(other, Racional):
      return Log(self.argumento**self.parte_descompuesta*other**self.base, self.base)
    elif isinstance(other, Natural):
      return Log(self.argumento**self.parte_descompuesta*other**self.base, self.base)
    elif isinstance(other, Complex):
      raise Exception('Se intentó sumar un Log con un Complex')
    elif isinstance(other, Root):
      return Log(self.argumento**self.parte_descompuesta*other**self.base, self.base)
    elif isinstance(other, Log):
      if self.base!=other.base:
        raise Exception('se intentó sumar logaritmos de distintas bases')
      return Log(self.argumento*other.argumento, self.base, self.parte_descompuesta)
    elif isinstance(other, Pol):
      raise Exception('Se intentó sumar un Log con un Pol')

  def __radd__(self, other):
    if isinstance(other, (int, float)):
      return self+other
    elif isinstance(other, str):
      return other + self.show

  def __sub__(self, other):
    if isinstance(other, (int, float)):
      return Log(self.argumento**self.parte_descompuesta/other**self.base, self.base)
    elif isinstance(other, str):
      return self.show + other
    elif isinstance(other, Racional):
      return Log(self.argumento**self.parte_descompuesta/other**self.base, self.base)
    elif isinstance(other, Natural):
      return Log(self.argumento**self.parte_descompuesta/other**self.base, self.base)
    elif isinstance(other, Complex):
      raise Exception('Se intentó restar un Log con un Complex')
    elif isinstance(other, Root):
      return Log(self.argumento**self.parte_descompuesta/other**self.base, self.base)
    elif isinstance(other, Log):
      if self.base!=other.base:
        raise Exception('se intentó restar logaritmos de distintas bases')
      return Log(self.argumento/other.argumento, self.base, self.parte_descompuesta/other.parte_descompuesta)
    elif isinstance(other, Pol):
      raise Exception('Se intentó restar un Log con un Pol')

  def __rsub__(self, other):
    if isinstance(other, (int, float)):
      return other+(-self)
    elif isinstance(other, str):
      return other + (-self).show

  def __mul__(self, other):
    if isinstance(other, (int, float)):
      return Log(self.argumento, self.base, self.parte_descompuesta*other)
    elif isinstance(other, str):
      return Term(self, {other:1})
    elif isinstance(other, dict):
      return Term(self, other)
    elif isinstance(other, Racional):
      return Log(self.argumento, self.base, self.parte_descompuesta*other)
    elif isinstance(other, Natural):
      return Log(self.argumento, self.base, self.parte_descompuesta*other)
    elif isinstance(other, Complex):
      raise Exception('Se intentó multiplicar Log con Complex')
    elif isinstance(other, Root):
      return Log(self.argumento, self.base, self.parte_descompuesta*other)
    elif isinstance(other, Log):
      if isinstance(self.valor , Racional) and isinstance(other.valor , Racional):
        return self.valor*other.valor
      elif isinstance(self.valor , Racional) and isinstance(other.valor , Log):
        return Log(other.argumento, other.base, self.valor*other.parte_descompuesta)
      elif isinstance(self.valor , Log) and isinstance(other.valor , Racional):
        return Log(self.argumento, self.base, self.parte_descompuesta*other.valor)
      else:
        raise Exception('Se intentó multiplicar dos Log que no tienen valor')
    elif isinstance(other, Term):
      return Term(self*other.factor_numerico, other.diccionario_de_letras_y_exponentes)
    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(self*termino)
      return Pol(lista_de_terminos=lista_provisional, reducir=True)

  def __rmul__(self, other):
    return self*other

  def __truediv__(self, other):
    if isinstance(other, (int, float)):
      return Log(self.argumento, self.base, self.parte_descompuesta/other)
    elif isinstance(other, Racional):
      return Log(self.argumento, self.base, self.parte_descompuesta/other)
    elif isinstance(other, Natural):
      return Log(self.argumento, self.base, self.parte_descompuesta/other)
    elif isinstance(other, Log):
      if isinstance(self.valor , Racional) and isinstance(other.valor , Racional):
        return self.valor/other.valor
      elif isinstance(self.valor , Log) and isinstance(other.valor , Racional):
        return Log(self.argumento, self.base, self.parte_descompuesta/other.valor)
      else:
        return Fraction(self, other)

  def __rtruediv__(self, other):
    if isinstance(other, (int, float)):
      return Fraction(other, self)

  def __pow__(self, other):
    pass

  def __neg__(self):
    return Log(self.argumento, self.base, -self.parte_descompuesta)

  def __abs__(self):
    return Log(self.argumento, self.base, -self.parte_descompuesta) if float(self) < 0 else self

  def __str__(self):
    return self.show

  def __round__(self,n=0):
    if isinstance(self.valor , Racional):
      return round(self.valor, n)
    elif isinstance(self.valor , Log):
      return round(float(self), n)

  def __lt__(self, other):
    return float(self) < float(other)

  def __eq__(self, other):
    if isinstance(other, (int, float, Racional, Natural)):
      if isinstance(self.valor, Racional):
        return self.valor==other
      else:
        return False
    elif isinstance(other, Root):
      return False
    elif isinstance(other, Log):
      raise Exception('No se ha programado una forma de igualar dos Log')
    else:
      return False

  def __gt__(self, other):
    return float(self) > float(other)

  def __int__(self):
    if isinstance(self.valor , Racional):
      return int(self.valor)
    elif isinstance(self.valor , Log):
      return int(math.log(float(self.argumento), float(self.base))*self.parte_descompuesta)

  def __float__(self):
    if isinstance(self.valor , Racional):
      return float(self.valor)
    elif isinstance(self.valor , Log):
      return math.log(float(self.argumento), float(self.base))*float(self.parte_descompuesta)

  def __le__(self, other):
    return self<other or self==other

  def __ge__(self, other):
    return self>other or self==other

  def __ne__(self, other):
    return not self==other

  def __iadd__(self, other):
    return self+other

  def __isub__(self, other):
    return self-other

  def __imul__(self, other):
    return self*other  

  def __idiv__(self, other):
    return self/other

  def __ipow__(self, other):
    return self**other



class Term:
  '''self
  factor_numerico           Racional
  diccionario_de_letras_y_exponentes  dict
  factor_literal            str
  show                str
  '''
  def __init__(self, factor_numerico=1, diccionario_de_letras_y_exponentes={}, azar_letras=False):
    self.lista_de_terminos = [self]
    if isinstance(factor_numerico, (int, float, Natural)):
      self.factor_numerico = Racional(factor_numerico)
    else:
      self.factor_numerico = factor_numerico

    #Convierte en diccionario el único str ingresado, el cual será el único elemento del factor literal y tendrá exponente 1
    if isinstance(diccionario_de_letras_y_exponentes, str):
      diccionario_de_letras_y_exponentes = {diccionario_de_letras_y_exponentes:1}

    #Ordena el diccionario
    factor_literal = ''
    _copia = diccionario_de_letras_y_exponentes
    diccionario_de_letras_y_exponentes = {}
    lista_de_copia = sorted(_copia)
    for letra in lista_de_copia:
      if _copia[letra]!=0:
        diccionario_de_letras_y_exponentes[letra] = _copia[letra]

    #Quita las letras con exponente 0 y genera self.diccionario_de_letras_y_exponentes. Además genera una lista con las letras para poder escribir las letras en desorden de ser necesario.
    for letra in diccionario_de_letras_y_exponentes:
      if diccionario_de_letras_y_exponentes[letra]==0:
        del diccionario_de_letras_y_exponentes[letra]
    self.diccionario_de_letras_y_exponentes = diccionario_de_letras_y_exponentes
    lista_de_letras = list(diccionario_de_letras_y_exponentes)

    #Genera el factor literal
    if azar_letras:
      shuffle(lista_de_letras)
    for letra in lista_de_letras:
      if diccionario_de_letras_y_exponentes[letra]==0:
        pass
      elif diccionario_de_letras_y_exponentes[letra]==1:
        factor_literal += letra
      else:
        factor_literal += potencia(letra, diccionario_de_letras_y_exponentes[letra], quitar_1=True)
    self.factor_literal = factor_literal

    #Determina el self.show y cambia la clase de ser necesario
    if self.factor_numerico==0:
      self.__class__ = Racional
      self.__init__(0)
      return None
    if self.factor_literal=='':
      if isinstance(self.factor_numerico , Racional):
        self.__class__ = Racional
        self.__init__(self.factor_numerico.numerador, self.factor_numerico.denominador)
        return None
      elif isinstance(self.factor_numerico , Complex):
        self.__class__ = Complex
        self.__init__(self.factor_numerico.re, self.factor_numerico.im)
        return None
      elif isinstance(self.factor_numerico , Root):
        self.__class__ = Root
        self.__init__(self.factor_numerico.radicando, self.factor_numerico.indice, self.factor_numerico.parte_descompuesta)
        return None
    if isinstance(self.factor_numerico, Root):
      self.__class__ = TermRoot
      self.__init__(self.factor_numerico, Term(1, self.diccionario_de_letras_y_exponentes))
      return None
    if self.factor_numerico==1:
      self.show = self.factor_literal
    elif self.factor_numerico==-1:
      self.show = '-' + self.factor_literal
    elif isinstance(factor_numerico, Complex) and self.factor_numerico.re!=0:
      self.show = '('+ self.factor_numerico.show +')'+ self.factor_literal
    else:
      self.show = self.factor_numerico.show + self.factor_literal

  def isnumeric(self):
    return False

  def __add__(self, other):
    if isinstance(other, Term) and self.diccionario_de_letras_y_exponentes==other.diccionario_de_letras_y_exponentes:
      return Term(self.factor_numerico + other.factor_numerico, self.diccionario_de_letras_y_exponentes)
    elif isinstance(other, str):
      return self.show + other
    elif isinstance(other, Pol):
      return Pol(lista_de_terminos = [self]+other.lista_de_terminos, reducir=True)
    else:
      return Pol(self, other)

  def __radd__(self, other):
    if isinstance(other, str):
      return other + self.show

  def __sub__(self, other):
    if isinstance(other, Term) and self.diccionario_de_letras_y_exponentes==other.diccionario_de_letras_y_exponentes:
      return Term(self.factor_numerico - other.factor_numerico, self.diccionario_de_letras_y_exponentes)
    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(-termino)
      return Pol(lista_de_terminos = [self]+lista_provisional)
    else:
      return Pol(self, -other)

  def __rsub__(self, other):
    if isinstance(other, str):
      return other + (-self).show

  def __mul__(self, other):
    if isinstance(other, (int, float, Racional, Natural, Complex, Root)):
      return Term(self.factor_numerico*other, self.diccionario_de_letras_y_exponentes)
    elif isinstance(other, str):
      return self*Term(1, {other:1})
    elif isinstance(other, dict):
      return self*Term(1, {other:1})
    elif isinstance(other, Term):
      diccionario_provisional = dict(self.diccionario_de_letras_y_exponentes)
      for letra in other.diccionario_de_letras_y_exponentes:
        if letra in diccionario_provisional:
          diccionario_provisional[letra] += other.diccionario_de_letras_y_exponentes[letra]
        else:
          diccionario_provisional[letra] = other.diccionario_de_letras_y_exponentes[letra]
      return Term(self.factor_numerico*other.factor_numerico, diccionario_provisional)
    elif isinstance(other, TermRoot):
      return TermRoot(other.raiz_completa, self*other.termino)
    elif isinstance(other, Pol):
      lista_provisional = []
      for termino in other.lista_de_terminos:
        lista_provisional.append(self*termino)
      return Pol(lista_de_terminos=lista_provisional, reducir=True)

  def __rmul__(self, other):
      return self*other

  def __truediv__(self, other):
    if isinstance(other, (int, float, Racional, Natural, Root)):
      return Term(self.factor_numerico/other, self.diccionario_de_letras_y_exponentes)
    elif isinstance(other, Term):
      diccionario_provisional = dict(self.diccionario_de_letras_y_exponentes)
      for letra in other.diccionario_de_letras_y_exponentes:
        if letra in diccionario_provisional:
          diccionario_provisional[letra] -= other.diccionario_de_letras_y_exponentes[letra]
        else:
          diccionario_provisional[letra] = -(other.diccionario_de_letras_y_exponentes[letra])
      return Term(self.factor_numerico/other.factor_numerico, diccionario_provisional)
    elif isinstance(other, TermRoot):
      return TermRoot(other.raiz_completa, self/other.termino)
    elif isinstance(other, Pol):
      divisor = Racional(MCD(self.factor_numerico.numerador, other.factor_comun.numerador), MCD(self.factor_numerico.denominador, other.factor_comun.denominador))
      return fraccion(Term(self.factor_numerico/divisor,self.diccionario_de_letras_y_exponentes).show, (other/divisor).show)

  def __rtruediv__(self, other):
    if isinstance(other, (int, float)):
      diccionario_provisional = {}
      for letra in self.diccionario_de_letras_y_exponentes:
        diccionario_provisional[letra] = -self.diccionario_de_letras_y_exponentes[letra]
    return Term(other/self.factor_numerico, diccionario_provisional)

  def __neg__(self):
    return Term(-self.factor_numerico, self.diccionario_de_letras_y_exponentes)

  def __pow__(self, other):
    if isinstance(other, int):
      diccionario_provisional = dict(self.diccionario_de_letras_y_exponentes)
      for letra in diccionario_provisional:
        diccionario_provisional[letra] = diccionario_provisional[letra]*other
      return Term(self.factor_numerico**other, diccionario_provisional)

  def __str__(self):
    return self.show

  def __eq__(self, other):
    if isinstance(other, Term):
      return self.factor_numerico==other.factor_numerico and self.diccionario_de_letras_y_exponentes==other.diccionario_de_letras_y_exponentes
    else:
      return False

  def __le__(self, other):
    return self<other or self==other

  def __ge__(self, other):
    return self>other or self==other

  def __ne__(self, other):
    return not self==other

  def __iadd__(self, other):
    return self+other

  def __isub__(self, other):
    return self-other

  def __imul__(self, other):
    return self*other  

  def __idiv__(self, other):
    return self/other

  def __ipow__(self, other):
    return self**other



class TermRoot:
  '''self
  factor_numerico           Racional
  raiz_completa             Root
  raiz_incompleta           Root
  termino               Term
  diccionario_de_letras_y_exponentes  dict
  show                str
  '''
  def __init__(self, raiz, termino):
    self.lista_de_terminos = [self]
    #Cambia la clase si el termino no tiene parte parte literal
    if not isinstance(raiz, Root) and not isinstance(termino, Term):
      if isinstance(raiz, (int, float)):
        raiz = Racional(raiz)
      if isinstance(termino, (int, float)):
        termino = Racional(termino)
      object = raiz*termino
      if isinstance(object, Racional):
        self.__class__ = Racional
        self.__init__(object.numerador, object.denominador)
        return None
      elif isinstance(object, Natural):
        self.__class__ = Natural
        self.__init__(object.numero)
        return None
      elif isinstance(object, Complex):
        self.__class__ = Complex
        self.__init__(object.re, object.im)
        return None
      elif isinstance(object, Root):
        self.__class__ = Root
        self.__init__(object.radicando, object.indice, object.parte_descompuesta)
        return None

    elif not isinstance(termino, Term):
      self.__class__ = Root
      self.__init__(raiz.radicando, raiz.indice, raiz.parte_descompuesta*termino)
      return None

    #Cambia la clase si el número no es del tipo raiz
    elif not isinstance(raiz, Root):
      self.__class__ = Term
      self.__init__(raiz*termino.factor_numerico, termino.diccionario_de_letras_y_exponentes)
      return None

    # La raiz no tendrá parte descompuesta. El término no tiene factor numérico.
    raiz = termino.factor_numerico*raiz
    termino = Term(1, termino.diccionario_de_letras_y_exponentes)
    self.factor_numerico = raiz.parte_descompuesta
    self.raiz_completa = raiz
    self.raiz_incompleta = Root(raiz.radicando, raiz.indice)
    self.termino = termino
    self.diccionario_de_letras_y_exponentes = termino.diccionario_de_letras_y_exponentes
    self.show = raiz.show + termino.show

  def isnumeric(self):
    return False

  def __add__(self, other):
    if isinstance(other, str):
      return self.show+other
    elif isinstance(other, TermRoot):
      if self.raiz_incompleta==other.raiz_incompleta and self.termino==other.termino:
        return TermRoot((self.factor_numerico+other.factor_numerico)*self.raiz_incompleta, self.termino)

  def __radd__(self, other):
    if isinstance(other, str):
      return other+self.show

  def __sub__(self, other):
    if isinstance(other, TermRoot):
      if self.raiz_incompleta==other.raiz_incompleta and self.termino==other.termino:
        return TermRoot((self.factor_numerico-other.factor_numerico)*self.raiz_incompleta, self.termino)

  def __rsub__(self, other):
    pass

  def __mul__(self, other):
    if isinstance(other, (int, float, Racional, Natural, Complex, Root, Term)):
      return TermRoot(self.raiz_completa, self.termino*other)
    elif isinstance(other, str):
      return TermRoot(self.raiz_completa, self.termino*Term(1, {other:1}))
    elif isinstance(other, dict):
      return TermRoot(self.raiz_completa, self.termino*Term(1, other))
    elif isinstance(other, TermRoot):
      return TermRoot(self.raiz_completa*other.raiz_completa, self.termino*other.termino)

  def __rmul__(self, other):
    pass

  def __truediv__(self, other):
    if isinstance(other, (int, float, Racional, Natural, Complex, Root, Term)):
      return TermRoot(self.raiz_completa, self.termino/other)
    elif isinstance(other, str):
      return TermRoot(self.raiz_completa, self.termino/Term(1, {other:1}))
    elif isinstance(other, dict):
      return TermRoot(self.raiz_completa, self.termino/Term(1, other))
    elif isinstance(other, TermRoot):
      return TermRoot(self.raiz_completa/other.raiz_completa, self.termino/other.termino)

  def __rtruediv__(self, other):
    pass

  def __neg__(self):
    return TermRoot(-self.raiz_completa, self.termino)

  def __pow__(self, other):
    return TermRoot(self.raiz_completa**other, self.termino**other)

  def __str__(self):
    return self.show

  def __eq__(self, other):
    if isinstance(other, TermRoot):
      return self.raiz_completa==other.raiz_completa and self.termino==other.termino
    else:
      return False

  def __le__(self, other):
    return self<other or self==other

  def __ge__(self, other):
    return self>other or self==other

  def __ne__(self, other):
    return not self==other

  def __iadd__(self, other):
    return self+other

  def __isub__(self, other):
    return self-other

  def __imul__(self, other):
    return self*other  

  def __idiv__(self, other):
    return self/other

  def __ipow__(self, other):
    return self**other



class Par:
  '''self
  x     Racional
  y     Racional
  show  str
  abs()   Racional/Root
  '''
  def __init__(self, x=None, y=None, r=None, alpha=None):
    if r!=None and alpha!=None:
      r, alpha = float(r), float(alpha)
      x, y = round(r*cos(alpha),2), round(r*sin(alpha),2)
      self.r, self.alpha = Racional(r), Racional(alpha)
    if isinstance(x, (int, float, Natural)):
      x = Racional(x)
    if isinstance(y, (int, float, Natural)):
      y = Racional(y)
    self.x = x
    self.y = y
    self.show = f'({mathrm(self.x)}, {mathrm(self.y)})'

  def distancia(self, other):
    return Root((self.x-other.x)**2+(self.y-other.y)**2)
  
  def unitario(self):
    return self / abs(self)

  def __add__(self, other):
    if isinstance(other, Par):
      return Par(self.x+other.x, self.y+other.y)
    elif isinstance(other, str):
      return self.show + other

  def __radd__(self, other):
    if isinstance(other, str):
      return other + self.show

  def __sub__(self, other):
    return Par(self.x-other.x, self.y-other.y)

  def __rsub__(self, other):
    if isinstance(other, str):
      return other + (-self).show

  def __mul__(self, other):
    if isinstance(other, (int, float, Racional, Natural, Complex, Root)):
      return Par(self.x*other, self.y*other)
    elif isinstance(other, Par):
      return self.x*other.x + self.y*other.y

  def __rmul__(self, other):
    if isinstance(other, (int, float)):
      return Par(self.x*other, self.y*other)

  def __truediv__(self, other):
    if isinstance(other, (int, float, Racional, Natural, Root)):
      return Par(self.x / other, self.y / other)

  def __neg__(self):
    return Par(-self.x, -self.y)

  def __str__(self):
    return self.show

  def __eq__(self, other):
    if isinstance(other, Par):
      return self.x==other.x and self.y==other.y
    elif isinstance(other, Complex):
      return self.x==other.re and self.y==other.im
    else:
      return False

  def __abs__(self):
    return Root(self.x**2 + self.y**2)

  def __le__(self, other):
    return self<other or self==other

  def __ge__(self, other):
    return self>other or self==other

  def __ne__(self, other):
    return not self==other

  def __iadd__(self, other):
    return self+other

  def __isub__(self, other):
    return self-other

  def __imul__(self, other):
    return self*other  

  def __idiv__(self, other):
    return self/other

  def __ipow__(self, other):
    return self**other



class Pol:
  '''self
  factor_comun
  lista_de_terminos
  show
  '''

  def __init__(self, *terminos, lista_de_terminos=[], reducir=False, azar=False, parentesis=False, reducir_raices=False):
    self.parentesis = parentesis
    self.lista_de_terminos = []
    terminos = list(terminos)+list(lista_de_terminos)
    lista_de_elementos_sin_raices = []
    lista_de_raices = []
    lista_de_TermRoot = []
    lista_de_Fraction = []
    lista_de_log = []
    lista_de_numeradores_factores_numericos = []
    lista_de_denominadores_factores_numericos = []
    self.show = ''
    terminos = list(terminos)
    if azar:
      shuffle(terminos)

    #quita los ceros
    while 0 in terminos:
      terminos.remove(0)

    #transforma a clase Term los valores ingresados y recolecta los numeradores y denominadores de sus factores numéricos. Excluye los casos en los que el factor numérico es 0
    for elemento in terminos:
      if isinstance(elemento, (int, float)):
        elemento=Racional(elemento)
        self.lista_de_terminos.append(elemento)
        lista_de_elementos_sin_raices.append(elemento)
        lista_de_numeradores_factores_numericos.append(abs(elemento.numerador))
        lista_de_denominadores_factores_numericos.append(elemento.denominador)

      elif isinstance(elemento, Racional):
        self.lista_de_terminos.append(elemento)
        lista_de_elementos_sin_raices.append(elemento)
        lista_de_numeradores_factores_numericos.append(abs(elemento.numerador))
        lista_de_denominadores_factores_numericos.append(elemento.denominador)

      elif isinstance(elemento, Natural):
        elemento=Racional(elemento.numero)
        self.lista_de_terminos.append(elemento)
        lista_de_elementos_sin_raices.append(elemento)
        lista_de_numeradores_factores_numericos.append(abs(elemento.numerador))
        lista_de_denominadores_factores_numericos.append(1)

      elif isinstance(elemento, Complex):
        self.lista_de_terminos.append(elemento)
        lista_de_elementos_sin_raices.append(Term(elemento.re))
        lista_de_elementos_sin_raices.append(Term(elemento.im, {'i':1}))
        lista_de_numeradores_factores_numericos.append(abs(elemento.im.numerador))
        lista_de_denominadores_factores_numericos.append(abs(elemento.im.denominador))
        if elemento.re!=0:
          lista_de_numeradores_factores_numericos.append(abs(elemento.re.numerador))
          lista_de_denominadores_factores_numericos.append(abs(elemento.re.denominador))

      elif isinstance(elemento, str):
        self.lista_de_terminos.append(Term(1, {elemento:1}))
        lista_de_elementos_sin_raices.append(Term(1, {elemento:1}))
        lista_de_numeradores_factores_numericos.append(1)
        lista_de_denominadores_factores_numericos.append(1)

      elif isinstance(elemento, dict):
        self.lista_de_terminos.append(Term(1, elemento))
        lista_de_elementos_sin_raices.append(Term(1, elemento))
        lista_de_numeradores_factores_numericos.append(1)
        lista_de_denominadores_factores_numericos.append(1)

      elif isinstance(elemento, Term):
        self.lista_de_terminos.append(elemento)
        lista_de_elementos_sin_raices.append(elemento)
        lista_de_numeradores_factores_numericos.append(abs(elemento.factor_numerico.numerador))
        lista_de_denominadores_factores_numericos.append(elemento.factor_numerico.denominador)

      elif isinstance(elemento, Root):
        if reducir_raices:
          elemento = Root(elemento.radicando, elemento.indice, elemento.parte_descompuesta, descomponer=True, simplificar_indice=True)
        self.lista_de_terminos.append(elemento)
        lista_de_raices.append(Term(elemento))
        lista_de_numeradores_factores_numericos.append(abs(elemento.parte_descompuesta.numerador))
        lista_de_denominadores_factores_numericos.append(elemento.parte_descompuesta.denominador)

      elif isinstance(elemento, Log):
        if reducir_raices and isinstance(elemento.valor, Racional):
          self.lista_de_terminos.append(elemento.valor)
          lista_de_elementos_sin_raices.append(Term(elemento.valor))
          lista_de_numeradores_factores_numericos.append(abs(elemento.valor.numerador))
          lista_de_denominadores_factores_numericos.append(elemento.valor.denominador)
        else:
          self.lista_de_terminos.append(elemento)
          lista_de_log.append(elemento)
          lista_de_numeradores_factores_numericos.append(elemento.parte_descompuesta.numerador)
          lista_de_denominadores_factores_numericos.append(elemento.parte_descompuesta.denominador)

      elif isinstance(elemento, TermRoot):
        if reducir_raices:
          elemento = Root(elemento.raiz_completa.radicando, elemento.raiz_completa.indice, elemento.raiz_completa.parte_descompuesta, descomponer=True, simplificar_indice=True)*elemento.termino
        self.lista_de_terminos.append(elemento)
        lista_de_TermRoot.append(elemento)
        lista_de_numeradores_factores_numericos.append(abs(elemento.raiz_completa.parte_descompuesta.numerador))
        lista_de_denominadores_factores_numericos.append(elemento.raiz_completa.parte_descompuesta.denominador)

      elif isinstance(elemento, Fraction):
        self.lista_de_terminos.append(elemento)
        lista_de_Fraction.append(Term(1,{elemento.show:1}))
        lista_de_numeradores_factores_numericos.append(abs(elemento.numerador.factor_comun.numerador))
        lista_de_denominadores_factores_numericos.append(elemento.numerador.factor_comun.denominador)


    #Cambia la clase si no hay elementos
    if len(self.lista_de_terminos) == 0:
      self.__class__ = Racional
      self.__init__(0)
      return None

    #Calcula el self.factor_común encontrando el numerador común y el denominador común
    self.factor_comun = Racional(MCD(lista=lista_de_numeradores_factores_numericos), MCD(lista=lista_de_denominadores_factores_numericos))

    #Genera la lista reducida si se pide
    if reducir:
      #Términos sin raíces
      lista_provisional = []
      for termino in lista_de_elementos_sin_raices:
        el_termino_se_sumo_a_otro = False
        for termino_reducido in lista_provisional:
          if termino.diccionario_de_letras_y_exponentes == termino_reducido.diccionario_de_letras_y_exponentes:
            lista_provisional[lista_provisional.index(termino_reducido)] = termino_reducido + termino
            el_termino_se_sumo_a_otro = True
            break
        if not el_termino_se_sumo_a_otro:
          lista_provisional.append(termino)
      lista_reducida_sin_raices = lista_provisional

      #Tipo Root
      lista_provisional = []
      for termino in lista_de_raices:
        el_termino_se_sumo_a_otro = False
        for termino_reducido in lista_provisional:
          if termino / termino.parte_descompuesta == termino_reducido / termino_reducido.parte_descompuesta:
            lista_provisional[lista_provisional.index(termino_reducido)] = termino_reducido + termino
            el_termino_se_sumo_a_otro = True
            break
        if not el_termino_se_sumo_a_otro:
          lista_provisional.append(termino)
      lista_reducida_de_raices = lista_provisional

      #TermRoot
      lista_provisional = []
      for termino in lista_de_TermRoot:
        el_termino_se_sumo_a_otro = False
        for termino_reducido in lista_provisional:
          if termino.diccionario_de_letras_y_exponentes==termino_reducido.diccionario_de_letras_y_exponentes and termino.raiz_incompleta==termino_reducido.raiz_incompleta:
            lista_provisional[lista_provisional.index(termino_reducido)] = termino_reducido + termino
            el_termino_se_sumo_a_otro = True
            break
        if not el_termino_se_sumo_a_otro:
          lista_provisional.append(termino)
      lista_reducida_de_TermRoot = lista_provisional

      suma_de_fracciones = 0
      for fract in lista_de_Fraction:
        suma_de_fracciones += fract
      lista_reducida_Fraction = [suma_de_fracciones]

      self.lista_de_terminos = lista_reducida_sin_raices + lista_reducida_Fraction + lista_reducida_de_raices + lista_reducida_de_TermRoot + lista_de_log
      self.__init__(lista_de_terminos=self.lista_de_terminos)
      return None


    # por segunda vez quita los ceros de nuevo y cambia de clase si no hay elementos
    while 0 in self.lista_de_terminos:
      self.lista_de_terminos.remove(0)
    if len(self.lista_de_terminos) == 0:
      self.__class__ = Racional
      self.__init__(0)
      return None


    #Determina el self.show
    if len(self.lista_de_terminos)==1:
      self.show = self.lista_de_terminos[0].show
    elif 2<=len(self.lista_de_terminos):
      self.show = self.lista_de_terminos[0].show
      for termino in self.lista_de_terminos[1:]:
        if termino.show[0] == '-':
          self.show = self.show + termino.show
        else:
          self.show = self.show + '+' + termino.show
    if self.show=='':
      self.show = '0'
    if parentesis:
      self.show = '('+ self.show +')'


    #Transforma el polinomio en caso de que solo haya un elemento
    if len(self.lista_de_terminos)==1:
      unico_elemento = self.lista_de_terminos[0]
      if isinstance(unico_elemento, Racional):
        self.__class__ = Racional
        self.__init__(unico_elemento.numerador, unico_elemento.denominador)
        return None
      elif isinstance(unico_elemento, Natural):
        self.__class__ = Natural
        self.__init__(unico_elemento.numero)
        return None
      elif isinstance(unico_elemento, Root):
        self.__class__ = Root
        self.__init__(unico_elemento.radicando, unico_elemento.indice, unico_elemento.parte_descompuesta)
        return None
      elif isinstance(unico_elemento, Term):
        self.__class__ = Term
        self.__init__(unico_elemento.factor_numerico, unico_elemento.factor_literal)
        return None
      elif isinstance(unico_elemento, TermRoot):
        self.__class__ = TermRoot
        self.__init__(unico_elemento.raiz, unico_elemento.termino)
        return None

  def isnumeric(self):
    return False

  def __add__(self, other):
    if isinstance(other, (int, float)):
      return Pol(lista_de_terminos=self.lista_de_terminos + [other], reducir=True)
    elif isinstance(other, str):
      return self.show + other
    elif isinstance(other, dict):
      return Pol(lista_de_terminos=self.lista_de_terminos + [Term(Racional(1), other)], reducir=True)
    elif isinstance(other, Racional):
      return Pol(lista_de_terminos=self.lista_de_terminos + [other], reducir=True)
    elif isinstance(other, Natural):
      return Pol(lista_de_terminos=self.lista_de_terminos + [other], reducir=True)
    elif isinstance(other, Complex):
      return Pol(lista_de_terminos=self.lista_de_terminos + [other], reducir=True)
    elif isinstance(other, Pol):
      return Pol(lista_de_terminos = self.lista_de_terminos+other.lista_de_terminos, reducir=True)
    elif isinstance(other, Fraction):
      return Fraction(self*other.denominador+other.numerador, other.denominador)

  def __radd__(self, other):
    if isinstance(other, (int, float)):
      return Pol(lista_de_terminos=[other] + self.lista_de_terminos, reducir=True)
    elif isinstance(other, str):
      return other + self.show

  def __sub__(self, other):
    if isinstance(other, (int, float)):
      return Pol(lista_de_terminos=self.lista_de_terminos + [-other], reducir=True)
    elif isinstance(other, str):
      raise Exception('No se ha programado la resta Pol - str')
    elif isinstance(other, Racional):
      return Pol(lista_de_terminos=self.lista_de_terminos + [-other], reducir=True)
    elif isinstance(other, Natural):
      return Pol(lista_de_terminos=self.lista_de_terminos + [-other], reducir=True)
    elif isinstance(other, Complex):
      return Pol(lista_de_terminos=self.lista_de_terminos + [-other], reducir=True)
    elif isinstance(other, Pol):
      return Pol(lista_de_terminos = [self.lista_de_terminos]+(-other).lista_de_terminos, reducir=True)
    elif isinstance(other, Fraction):
      return Fraction(self*other.denominador-other.numerador, other.denominador)

  def __rsub__(self, other):
    if isinstance(other, (int, float)):
      lista_provisional = []
      for termino in self.lista_de_terminos:
        lista_provisional.append(-termino)
      return Pol(lista_de_terminos=[other] + lista_provisional, reducir=True)
    elif isinstance(other, str):
      return other + (-self).show

  def __mul__(self, other):
    if isinstance(other, (int, float, str, dict, Racional, Natural, Complex, Root, Term, TermRoot)):
      lista_provisional = []
      for termino in self.lista_de_terminos:
        lista_provisional.append(termino*other)
      return Pol(lista_de_terminos=lista_provisional , reducir=True)
    elif isinstance(other, Pol):
      lista_provisional =[]
      for termino_1 in self.lista_de_terminos:
        for termino_2 in other.lista_de_terminos:
          lista_provisional.append(termino_1*termino_2)
      return Pol(lista_de_terminos=lista_provisional , reducir=True)
    elif isinstance(other, Fraction):
      return Fraction(self*other.numerador, other.denominador)

  def __rmul__(self, other):
    return self*other

  def __truediv__(self, other):
    lista_provisional = []
    if isinstance(other, (int, float, str, dict, Racional, Natural, Complex, Root, Term, TermRoot)):
      for termino in self.lista_de_terminos:
        lista_provisional.append(termino/other)
      return Pol(lista_de_terminos=lista_provisional , reducir=True)
    elif isinstance(other, Pol):
      return fraccion(self, other)
    elif isinstance(other, Fraction):
      return Fraction(self*other.denominador, other.numerador)

  def __rtruediv__(self, other):
    if isinstance(other, int, float):
      divisor = Racional(MCD(self.factor_comun.numerador, Racional(other).numerador), MCD(self.factor_comun.denominador, Racional(other).denominador))
      return fraccion(other/divisor, (self/divisor).show)
    elif isinstance(other, str):
      return fraccion(other, self.show)

  def __neg__(self):
    lista_provisional = []
    for termino in self.lista_de_terminos:
      lista_provisional.append(-termino)
    return Pol(lista_de_terminos=lista_provisional , reducir=True)

  def __pow__(self, other):
    if isinstance(other, int):
      resultado = Racional(1)
      for _ in range(0, other):
        resultado = resultado*self
      if other<0:
        return Fraction(1,resultado)
      if 0<=other:
        return resultado
    else:
      raise Exception('No se ha programado la forma de elevar los Pol a otra cosa que no sea int')

  def __str__(self):
    return self.show

  def __eq__(self, other):
    selfReducido = Pol(lista_de_terminos=self.lista_de_terminos,reducir=True).lista_de_terminos
    otherReducido = Pol(lista_de_terminos=other.lista_de_terminos,reducir=True).lista_de_terminos
    return {object.show for object in selfReducido} == {object.show for object in otherReducido}

  def __int__(self):
    return int(float(self))

  def __float__(self):
    aproximacion = 0
    for termino in self.lista_de_terminos:
      aproximacion = aproximacion + float(termino)
    return aproximacion

  def __ne__(self, other):
    return not self==other

  def __iadd__(self, other):
    return self+other

  def __isub__(self, other):
    return self-other

  def __imul__(self, other):
    return self*other  

  def __idiv__(self, other):
    return self/other

  def __ipow__(self, other):
    return self**other

  def __iter__(self):
    self.__indexForLoop = 0
    return self
  
  def __next__(self):
    if self.__indexForLoop == len(self.lista_de_terminos):
      raise StopIteration
    self.__indexForLoop += 1
    return self.lista_de_terminos[self.__indexForLoop - 1]

  def __getitem__(self, i):
    if isinstance(i, slice):#Tiene dos puntos
      return Pol(lista_de_terminos=self.lista_de_terminos[i])
    else:#no tiene dos puntos
      return Pol(self.lista_de_terminos[i])




class Fraction:
  '''self
  numerador       Pol  *Cambia si es de un solo término
  denominador     Pol  *Cambia si es de un solo término
  show        str
  '''
  def __init__(self, numerador, denominador=1, simplificar=False):
    self.lista_de_terminos = [self]
    self.numerador = numerador
    self.denominador = denominador
    if not isinstance(self.numerador, Pol):
      self.numerador = Pol(self.numerador)
    if not isinstance(self.denominador, Pol):
      self.denominador = Pol(self.denominador)

    comun_divisor = Racional(MCD(self.numerador.factor_comun.numerador, self.denominador.factor_comun.numerador), MCD(self.numerador.factor_comun.denominador, self.denominador.factor_comun.denominador))

    if simplificar:
      self.numerador = Pol(lista_de_terminos=self.numerador.lista_de_terminos, reducir=True)
      self.denominador = Pol(lista_de_terminos=self.denominador.lista_de_terminos, reducir=True)
      comun_divisor = Racional(MCD(self.numerador.factor_comun.numerador, self.denominador.factor_comun.numerador), MCD(self.numerador.factor_comun.denominador, self.denominador.factor_comun.denominador))
      if self.numerador/self.numerador.factor_comun == self.denominador/self.denominador.factor_comun:
        self.numerador = self.numerador.factor_comun
        self.denominador = self.denominador.factor_comun
      elif -self.numerador/self.numerador.factor_comun == self.denominador/self.denominador.factor_comun:
        self.numerador = -self.numerador.factor_comun
        self.denominador = self.denominador.factor_comun
      else:
        self.numerador = self.numerador/comun_divisor
        self.denominador = self.denominador/comun_divisor
        comun_divisor = Racional(1)

    #Cambia la clase si el denominador es igual a 1
    if self.denominador==Pol(1):
      if isinstance(self.numerador, (int, float, Racional, Natural)):
        self.__class__ = Racional
        self.__init__(self.numerador)
        return None
      elif isinstance(self.numerador, Complex):
        self.__class__ = Complex
        self.__init__(self.numerador.re, self.numerador.im)
        return None
      elif isinstance(self.numerador, UnidadImaginaria):
        self.__class__ = Complex
        self.__init__(0,1)
        return None
      elif isinstance(self.numerador, Root):
        self.__class__ = Root
        self.__init__(self.numerador.radicando, self.numerador.indice, self.numerador.parte_descompuesta)
        return None
      elif isinstance(self.numerador, Term):
        self.__class__ = Term
        self.__init__(self.numerador.factor_numerico, self.numerador.diccionario_de_letras_y_exponentes)
        return None
      elif isinstance(self.numerador, TermRoot):
        self.__class__ = TermRoot
        self.__init__(self.numerador.raiz_completa, self.numerador.termino)
        return None
      elif isinstance(self.numerador, Pol):
        self.__class__ = Pol
        self.__init__(lista_de_terminos=self.numerador.lista_de_terminos)
        return None
      elif isinstance(self.numerador, Fraction):
        self.__init__(self.numerador.numerador, self.numerador.denominador)
        return None

    if isinstance(self.numerador , Racional) and isinstance(self.denominador , Racional):
      self.__class__ = Racional
      self.__init__(self.numerador, self.denominador)
      return None

    self.show = fraccion(self.numerador, self.denominador)

  def isnumeric(self):
    return False

  def __add__(self, other):
    if isinstance(other, (int, float)):
      other = Racional(other)
      return Fraction(self.numerador*other.denominador+other.numerador*self.denominador, self.denominador*other.denominador)
    elif isinstance(other, str):
      return self.show+other
    elif isinstance(other, Racional):
      return Fraction(self.numerador*other.denominador+other.numerador*self.denominador, self.denominador*other.denominador)
    elif isinstance(other, Natural):
      other = Racional(other)
      return Fraction(self.numerador*other.denominador+other.numerador*self.denominador, self.denominador*other.denominador)
    elif isinstance(other, Complex):
      return Fraction(self.numerador+other.numerador*self.denominador, self.denominador)
    elif isinstance(other, Pol):
      return Fraction(self.numerador+other.numerador*self.denominador, self.denominador)
    elif isinstance(other, Fraction):
      return Fraction(self.numerador*other.denominador+other.numerador*self.denominador, self.denominador*other.denominador)

  def __radd__(self, other):
    if isinstance(other, (int, float)):
      return Fraction(self.numerador*other.denominador+other.numerador*self.denominador, self.denominador*other.denominador)
    elif isinstance(other, str):
      return other + self.show

  def __sub__(self, other):
    if isinstance(other, (int, float)):
      other = Racional(other)
      return Fraction(self.numerador*other.denominador-other.numerador*self.denominador, self.denominador*other.denominador)
    elif isinstance(other, Racional):
      return Fraction(self.numerador*other.denominador-other.numerador*self.denominador, self.denominador*other.denominador)
    elif isinstance(other, Natural):
      other = Racional(other)
      return Fraction(self.numerador*other.denominador-other.numerador*self.denominador, self.denominador*other.denominador)
    elif isinstance(other, Complex):
      return Fraction(self.numerador-other.numerador*self.denominador, self.denominador)
    elif isinstance(other, Pol):
      return Fraction(self.numerador-other.numerador*self.denominador, self.denominador)
    elif isinstance(other, Fraction):
      return Fraction(self.numerador*other.denominador-other.numerador*self.denominador, self.denominador*other.denominador)

  def __rsub__(self, other):
    if isinstance(other, (int, float)):
      other = Racional(other)
      return other-self

  def __mul__(self, other):
    if isinstance(other, (Racional, Fraction)):
      return Fraction(self.numerador*other.numerador, self.denominador*other.denominador)
    else:
      return Fraction(self.numerador*other, self.denominador)

  def __rmul__(self, other):
    return Fraction(other*self.numerador, self.denominador)

  def __truediv__(self, other):
    if isinstance(other, (int, float)):
      other = Racional(other)
      return Fraction(self.numerador*other.denominador, self.denominador*other.numerador)
    elif isinstance(other, str):
      return Fraction(self.numerador, self.denominador*other)
    elif isinstance(other, Racional):
      return Fraction(self.numerador*other.denominador, self.denominador*other.numerador)
    elif isinstance(other, Natural):
      return Fraction(self.numerador, self.denominador*other)
    elif isinstance(other, Complex):
      return Fraction(self.numerador, self.denominador*other)
    elif isinstance(other, Pol):
      return Fraction(self.numerador, self.denominador*other)
    elif isinstance(other, Fraction):
      return Fraction(self.numerador*other.denominador, self.denominador*other.numerador)


  def __rtruediv__(self, other):
    if isinstance(other, int, float):
      other = Racional(other)
      return Fraction(self.denominador*other, self.numerador)
    elif isinstance(other, str):
      return Fraction(self.denominador*other, self.numerador)

  def __neg__(self):
    return Fraction(-self.numerador, self.denominador)

  def __pow__(self, other):
    return Fraction(self.numerador**other, self.denominador**other)

  def __str__(self):
    return self.show

  def __lt__(self, other):
    return float(self) < float(other)

  def __eq__(self, other):
    if isinstance(other, Fraction):
      return self.numerador==other.numerador and self.denominador==other.denominador

  def __gt__(self, other):
    return float(self) > float(other)

  def __le__(self, other):
    return self<other or self==other

  def __ge__(self, other):
    return self>other or self==other

  def __int__(self):
    return int(float(self.numerador)/float(self.denominador))

  def __float__(self):
    return float(self.numerador)/float(self.denominador)

  def __ne__(self, other):
    return not self==other

  def __iadd__(self, other):
    return self+other

  def __isub__(self, other):
    return self-other

  def __imul__(self, other):
    return self*other  

  def __idiv__(self, other):
    return self/other

  def __ipow__(self, other):
    return self**other








class Recta:
  '''self
  m            Racional
  n            Racional
  show_funcion       str
  show_ecuacion_principal  str
  show_ecuacion_general  str
  f            Racional
  fi             Racional
  '''
  def __init__(self, punto_1, punto_2=None, pendiente=None):
    #Define la self pendiente
    if pendiente == None:
      self.m = (punto_2.y-punto_1.y)/(punto_2.x-punto_1.x)
    else:
      self.m = Racional(pendiente)
    #Define el self coeficiente de posicion
    self.n = self.m*(-punto_1.x)+punto_1.y
    #Define la función
    self.show_funcion = 'f(x)='+Pol(self.m*'x', self.n)
    #Define la ecuación principal
    self.show_ecuacion_principal = 'y='+Pol(self.m*'x', self.n)
    #Define la ecuación general
    self.show_ecuacion_general = choice([1,-1])*Pol(-self.m*self.m.denominador*'x', Term(self.m.denominador,'y'), -self.n*self.m.denominador)+'=0'

  def isnumeric(self):
    return False

  def f(self,x):
    return self.m*x+self.n

  def fi(self,y):
    return (y-self.n)/self.m

  def __eq__(self, other):
    if isinstance(other, Recta):
      return self.m==other.m and self.n==other.n
    else:
      return False

  def punto_de_interseccion(self, other):
    return Par((other.n-self.n)/(self.m-other.m), self.f((other.n-self.n)/(self.m-other.m)))


class Circunferencia:
  '''self
  show_ecuacion_principal str
  show_ecuacion_general   str
  h             Racional / Root
  k             Racional / Root
  centro          Par
  radio           Racional / Root
  diametro        Racional / Root
  perimetro         Racional / Root
  area          Racional / Root
  '''
  def __init__(self,h,k,r):
    if not isinstance(h, Root):
      h = Racional(h)
    if not isinstance(k, Root):
      k = Racional(k)
    if not isinstance(r, Root):
      r = Racional(r)
    self.show_ecuacion_principal = potencia(Pol('x',-h),2)+'+'+potencia(Pol('y',-k),2)+'='+r**2
    self.show_ecuacion_general = Pol({'x':2}, {'y':2}, -2*h*'x', -2*k*'y', h**2+k**2-r**2)+'=0'
    self.h = h
    self.k = k
    self.centro = Par(h,k)
    self.radio = r
    self.diametro = 2*r
    self.perimero = 2*r*PI()
    self.area = r**2*PI()

  def isnumeric(self):
    return False

  def __eq__(self, other):
    if  isinstance(other, Circunferencia):
      return self.h==other.h and self.k==other.k and self.radio==other.radio
    else:
      return False




def fraccion_factorial(numerador, denominador):
  lista_numerador = [1]
  for i in numerador:
    if i==0 or i==1:
      continue
    lista_numerador.extend(list(range(2, i+1)))

  lista_denominador = [1]
  for i in denominador:
    if i==0 or i==1:
      continue
    lista_denominador.extend(list(range(2, i+1)))

  diccionario_numerador = {}
  diccionario_denominador = {}
  for i in lista_numerador:
    diccionario_numerador[i] = lista_numerador.count(i)
  for i in lista_denominador:
    diccionario_denominador[i] = lista_denominador.count(i)

  for i in diccionario_denominador:
    if i==1:
      continue
    if i in diccionario_numerador:
      diccionario_numerador[i] -= 1
      diccionario_denominador[i] -= 1

  numerador = 1
  denominador = 1

  for i in diccionario_numerador:
    numerador *= i**diccionario_numerador[i]
  for i in diccionario_denominador:
    denominador *= i**diccionario_denominador[i]

  return Racional(numerador, denominador)

