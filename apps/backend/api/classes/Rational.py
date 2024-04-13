from api.classes.Latex import Latex
from api.classes.Abstract import Numeric
from typing import Union


class Rational(Numeric):
  '''
    numerator: Union[int, float]
    denominator: Union[int, float]
    __is_simplified: bool
    __is_decimal_loaded: bool
    integer_part: Union[None, int]
    non_periodic_decimal_part: Union[None, str]
    periodic_decimal_part: Union[None, str]
  '''

  def __init__(self, numerator: Union[int, float], denominator: Union[int, float]):
    if denominator == 0:
      raise Exception('Denominator can not be Zero')
    self.__numerator = numerator
    self.__denominator = denominator
    self.__is_simplified = False
    self.__is_decimal_loaded = False
    self.__integer_part = None
    self.__non_periodic_decimal_part = None
    self.__periodic_decimal_part = None

  def simplify(self):
    if self.__is_simplified:
      return
    self.__is_simplified = True

    sign = '-' if float(self) < 0 else ''

    # Aquí se amplifica el numerator y el denomiandor para quitar los decimales
    numerator = str(abs(float(self.__numerator)))
    denominator = str(abs(float(self.__denominator)))
    while numerator[numerator.index('.'):] != '.0' or denominator[denominator.index('.'):] != '.0':
      numerator = numerator[:numerator.index('.')] + numerator[numerator.index('.') + 1:numerator.index('.') + 2] + '.' + numerator[numerator.index('.') + 2:]
      if numerator[-1] == '.':
        numerator += '0'
      denominator = denominator[:denominator.index('.')] + denominator[denominator.index('.') + 1:denominator.index('.') + 2] + '.' + denominator[denominator.index('.') + 2:]
      if denominator[-1] == '.':
        denominator += '0'
    numerator = int(float(numerator))
    denominator = int(float(denominator))

    # Aquí se simplifica el numerator con el denominator y determinan self.__numerator y self.__denominator
    for i in list(range(2, min([abs(numerator), abs(denominator), abs(abs(numerator) - abs(denominator))]) + 1)) + [denominator]:
      while numerator % i == denominator % i == 0:
        numerator = int(numerator / i)
        denominator = int(denominator / i)
        if denominator == 1:
          break
    self.__numerator = int(sign + str(numerator))
    self.__denominator = denominator

  def load_decimal(self):
    if self.__is_decimal_loaded:
      return
    self.__is_decimal_loaded = True

    helper = Rational(self.__numerator, self.__denominator)
    helper.simplify()
    numerator = helper.__numerator
    denominator = helper.__denominator

    # Aquí se calcula el múltiplo. self.multiplo
    multiple = 9
    while multiple % denominator != 0:
      multiple = str(multiple)
      if multiple.count('9') == 1:
        multiple = multiple.replace('0', '9')
        multiple += '9'
      else:
        lista = []
        for digito in multiple:
          lista.append(digito)
        lista[lista.count('9') - 1] = '0'
        multiple = ''
        for digito in lista:
          multiple += digito
      multiple = int(multiple)
    self.multiple = str(multiple)

    self.__integer_part = int(numerator // denominator)
    self.__non_periodic_decimal_part = None
    self.__periodic_decimal_part = None

    # Aquí se calcula la def parte decimal no periodica
    if str(multiple).count('0') != 0:
      non_periodic_decimal_part = str(int((abs(numerator) % denominator) * multiple / denominator / int(str(multiple).replace('0', ''))))
      for i in range(0, str(multiple).count('0') - len(non_periodic_decimal_part)):
        non_periodic_decimal_part = '0' + non_periodic_decimal_part
    else:
      non_periodic_decimal_part = ''
    self.__non_periodic_decimal_part = non_periodic_decimal_part

    # Aquí se calcula la parte decimal periódica
    periodic_decimal_part = str(int(((abs(numerator) % denominator) * multiple / denominator) % int(str(multiple).replace('0', ''))))
    if periodic_decimal_part == '0':
      periodic_decimal_part = ''
    else:
      for i in range(0, str(multiple).count('9') - len(periodic_decimal_part)):
        periodic_decimal_part = '0' + periodic_decimal_part
    self.__periodic_decimal_part = periodic_decimal_part

  def get_numerator(self):
    print('AYUDA get_numerator')
    return self.__numerator

  def get_denominator(self):
    print('AYUDA get_denominator')
    return self.__denominator

  def get_integer_part(self):
    return self.__integer_part

  def __add__(self, other):
    if isinstance(other, (int, float)):
      other = Rational(other, 1)
      return self + other
    if isinstance(other, Rational):
      self_helper = Rational(self.__numerator, self.__denominator)
      other_helper = Rational(other.__numerator, other.__denominator)
      self_helper.simplify()
      other_helper.simplify()
      result = Rational(self_helper.__numerator * other_helper.__denominator + other_helper.__numerator * self_helper.__denominator, self_helper.__denominator * other_helper.__denominator)
      result.simplify()
      return result

    raise Exception(f'Can not sum Rational and {type(other)}')

  def __radd__(self, other):
    if isinstance(other, (int, float)):
      return self + other

    raise Exception(f'Can not sum {type(other)} and Rational')

  def __sub__(self, other):
    if isinstance(other, (int, float)):
      other = Rational(other, 1)
      return self - other
    if isinstance(other, Rational):
      self_helper = Rational(self.__numerator, self.__denominator)
      other_helper = Rational(other.__numerator, other.__denominator)
      self_helper.simplify()
      other_helper.simplify()
      result = Rational(self_helper.__numerator * other_helper.__denominator - other_helper.__numerator * self_helper.__denominator, self_helper.__denominator * other_helper.__denominator)
      result.simplify()
      return result

    raise Exception(f'Can not subtract Rational and {type(other)}')

  def __rsub__(self, other):
    if isinstance(other, (int, float)):
      return -(self - other)
    raise Exception(f'Can not subtract {type(other)} and Rational')

  def __mul__(self, other):
    if isinstance(other, (int, float)):
      other = Rational(other, 1)
      return self * other
    if isinstance(other, Rational):
      self_helper = Rational(self.__numerator, self.__denominator)
      other_helper = Rational(other.__numerator, other.__denominator)
      self_helper.simplify()
      other_helper.simplify()
      result = Rational(self_helper.__numerator * other_helper.__numerator, self_helper.__denominator * other_helper.__denominator)
      result.simplify()
      return result

    raise Exception(f'Can not multiply Rational and {type(other)}')

  def __rmul__(self, other):
    if isinstance(other, (int, float)):
      return self * other
    raise Exception(f'Can not multiply {type(other)} and Rational')

  def __truediv__(self, other):
    if (other == 0):
      raise Exception('Can not divide Rational by Zero')

    if isinstance(other, (int, float)):
      other = Rational(other, 1)
      return self / other
    if isinstance(other, Rational):
      self_helper = Rational(self.__numerator, self.__denominator)
      other_helper = Rational(other.__numerator, other.__denominator)
      self_helper.simplify()
      other_helper.simplify()
      result = Rational(self_helper.__numerator * other_helper.__denominator, self_helper.__denominator * other_helper.__numerator)
      result.simplify()
      return result

    raise Exception(f'Can not divide Rational and {type(other)}')

  def __rtruediv__(self, other):
    if (self == 0):
      raise Exception(f'Can not divide {type(other)} by Zero')

    if isinstance(other, (int, float)):
      other = Rational(other, 1)
      return self / other
    if isinstance(other, Rational):
      self_helper = Rational(self.__numerator, self.__denominator)
      other_helper = Rational(other.__numerator, other.__denominator)
      self_helper.simplify()
      other_helper.simplify()
      result = Rational(other_helper.__numerator * self_helper.__denominator, other_helper.__denominator * self_helper.__numerator)
      result.simplify()
      return result

    raise Exception(f'Can not divide {type(other)} by Rational')

  def __pow__(self, other):
    if isinstance(other, (int)):
      if other > 0:
        self_helper = Rational(self.__numerator, self.__denominator)
        self_helper.simplify()
        return Rational(self_helper.__numerator ** other, self_helper.__denominator ** other)

      if other == 0:
        if self == 0:
          raise Exception('Can not raise Rational equals Zero to Zero')
        result = Rational(1, 1)
        result.simplify()
        return result

      if self == 0:
        raise Exception('Can not raise Rational equals Zero to negative number')

      self_helper = Rational(self.__numerator, self.__denominator)
      self_helper.simplify()
      result = Rational(self_helper.__denominator ** abs(other), self_helper.__numerator ** abs(other))
      result.simplify()
      return result

    raise Exception(f'Can not raise Rational to {type(other)}')

  def __rpow__(self, other):
    raise Exception(f'Can not raise {type(other)} to Rational')

  def __neg__(self):
    return Rational(-self.__numerator, self.__denominator)

  def __abs__(self):
    return Rational(abs(self.__numerator), abs(self.__denominator))

  def __str__(self):
    if self.__is_decimal_loaded:
      if not isinstance(self.__integer_part, int):
        raise Exception('integer_part in Rational is None when triyng to get string')
      if not isinstance(self.__non_periodic_decimal_part, str):
        raise Exception('non_periodic_decimal_part in Rational is not str when triyng to get string')
      if not isinstance(self.__periodic_decimal_part, str):
        raise Exception('periodic_decimal_part in Rational is not str when triyng to get string')

      if self.__non_periodic_decimal_part == self.__periodic_decimal_part == '':
        return str(self.__integer_part)
      if self.__non_periodic_decimal_part == '':
        return str(self.__integer_part) + ',' + Latex.overline(self.__periodic_decimal_part)
      if self.__periodic_decimal_part == '':
        return str(self.__integer_part) + ',' + self.__non_periodic_decimal_part
      return str(self.__integer_part) + ',' + self.__non_periodic_decimal_part + Latex.overline(self.__periodic_decimal_part)

    if (self.__is_simplified):
      sign = '-' if float(self) < 0 else ''
      return sign + Latex.fraction(abs(self.__numerator), abs(self.__denominator))

    return Latex.fraction(self.__numerator, self.__denominator)

  def __round__(self, n=0):
    return round(float(self), n)

  def __lt__(self, other):
    if isinstance(other, (int, float)):
      return float(self) < other
    if isinstance(other, Rational):
      return float(self) < float(other)

    raise Exception(f'Can not use "<" operator with Rational and {type(other)}')

  def __eq__(self, other):
    if isinstance(other, (int, float)):
      return float(self) == other
    if isinstance(other, Rational):
      return float(self) == float(other)

    raise Exception(f'Can not use "=" operator with Rational and {type(other)}')

  def __gt__(self, other):
    if isinstance(other, (int, float)):
      return float(self) > other
    if isinstance(other, Rational):
      return float(self) > float(other)

    raise Exception(f'Can not use ">" operator with Rational and {type(other)}')

  def __int__(self):
    return int(self.__numerator / self.__denominator)

  def __float__(self):
    return float(self.__numerator / self.__denominator)
