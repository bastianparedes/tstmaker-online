import math
from typing import Union, List
from abc import ABC, abstractmethod
import random


class Numeric(ABC):

  @abstractmethod
  def __init__(self):
    pass

  @abstractmethod
  def __add__(self, other):
    pass

  @abstractmethod
  def __radd__(self, other):
    pass

  @abstractmethod
  def __sub__(self, other):
    pass

  @abstractmethod
  def __rsub__(self, other):
    pass

  @abstractmethod
  def __mul__(self, other):
    pass

  @abstractmethod
  def __rmul__(self, other):
    pass

  @abstractmethod
  def __truediv__(self, other):
    pass

  @abstractmethod
  def __rtruediv__(self, other):
    pass

  @abstractmethod
  def __pow__(self, other):
    pass

  @abstractmethod
  def __rpow__(self, other):
    pass

  @abstractmethod
  def __neg__(self):
    pass

  @abstractmethod
  def __abs__(self) -> Union[int, float]:
    pass

  @abstractmethod
  def __str__(self) -> str:
    pass

  @abstractmethod
  def __round__(self, n=0):
    pass

  @abstractmethod
  def __lt__(self, other) -> bool:
    pass

  @abstractmethod
  def __eq__(self, other) -> bool:
    pass

  @abstractmethod
  def __gt__(self, other) -> bool:
    pass

  @abstractmethod
  def __int__(self) -> int:
    pass

  @abstractmethod
  def __float__(self) -> float:
    pass


class Literal(ABC):

  @abstractmethod
  def __init__(self):
    pass

  @abstractmethod
  def __str__(self):
    pass


class Latex:

  def math_mode(expresion: str):
    return f'$ {expresion} $'

  def fraction(numerator: Union[str, int, float], denominator: Union[str, int, float]):
    return fr' \dfrac{{{numerator}}}{{{denominator}}} '

  def overline(element: Union[str, int, float]):
    return fr' \overline{{{element}}} '
  
  def parenthesis(expression):
    return fr' \left( {expression} \right) '
  
  def brackets(expression):
    return fr' \left[ {expression} \right] '
  
  def degree():
    return r' \degree '
  
  def leq():
    return r' \leq '
  
  def geq():
    return r' \geq '

  def different():
    return r' \neq '
  
  def percentage():
    return r' \% '
  
  def alpha():
    return r' \alpha '
  
  def beta():
    return r' \beta '
  
  def alpha():
    return r' \gamma '
  
  def infinite():
    return r' \infty '
  
  def pi():
    return r'\pi'
  
  def space():
    return r'\ '
  
  def line_break():
    return r' \hfill \break '


class Natural(Numeric):
  """
    self.__number: int
    self.__dividers: Union[None, List[int]]
    self.__is_prime: Union[None, bool]
    self.__is_perfect: Union[None, bool]
  """

  def __init__(self, number: int):
    if not isinstance(number, int):
      raise Exception(f'number in {type(self)} must be intenger')
    if not number > 0:
      raise Exception(f'number in {type(self)} must be greater than zero')

    self.__number = number
    self.__dividers: Union[None, List[int]] = None
    self.__is_prime: Union[None, bool] = None
    self.__is_perfect: Union[None, bool] = None

  def get_dividers(self):
    if self.__dividers is not None:
      return self.__dividers
    self.__dividers = []
    number = 1
    while (number <= self.__number):
      if (self.__number % number == 0):
        self.__dividers.append(number)
      number += 1

    return self.__dividers

  def is_prime(self):
    if isinstance(self.__is_prime, bool):
      return self.__is_prime
    self.__is_prime = len(self.get_dividers()) == 2
    return self.__is_prime

  def is_perfect(self):
    if (self.__is_perfect is not None):
      return self.__is_perfect
    self.__is_perfect = sum(self.get_dividers()) / 2 == self.__number
    return self.__is_perfect

  def __add__(self, other):
    if isinstance(other, int):
      return Natural(int(self) + other)
    if isinstance(other, float):
      return Rational(int(self) + other, 1).simplify()
    if isinstance(other, (Rational)):
      return Rational(int(self) + 1) + other
    if isinstance(other, (Natural)):
      return Natural(int(self), int(other))
    raise Exception(f'Can not sum {type(self)} and {type(other)}')

  def __radd__(self, other):
    return self + other

  def __sub__(self, other):
    if isinstance(other, int):
      return Rational(int(self) - other)
    if isinstance(other, float):
      return Rational(int(self), 1) - other
    if isinstance(other, Rational):
      return Rational(int(self), 1) - other
    if isinstance(other, Natural):
      return Natural(int(self) - int(other))
    raise Exception(f'Can not subtract {type(self)} and {type(other)}')

  def __rsub__(self, other):
    return -(self - other)

  def __mul__(self, other):
    if isinstance(other, int):
      return Natural(int(self) * other)
    if isinstance(other, float):
      return Rational(int(self), 1) * other
    if isinstance(other, Rational):
      return Rational(int(self), 1) * other
    if isinstance(other, Natural):
      return Natural(int(self) * int(other))
    raise Exception(f'Can not multiply {type(self)} and {type(other)}')

  def __rmul__(self, other):
    return self * other

  def __truediv__(self, other):
    if (other == 0):
      raise Exception('Can not divide {type(self)} by Zero')
    if isinstance(other, int):
      return Rational(int(self), other).simplify()
    if isinstance(other, float):
      return Rational(int(self), other).simplify()
    if isinstance(other, Rational):
      return Rational(int(self) * other.__denominator, other.__numerator).simplify()
    if isinstance(other, Natural):
      return Rational(int(self), int(other)).simplify()
    raise Exception(f'Can not divide {type(self)} and {type(other)}')

  def __rtruediv__(self, other):
    if (self == 0):
      raise Exception(f'Can not divide {type(other)} by Zero')

    return other * self ** (-1)

  def __pow__(self, other):
    if isinstance(other, (int)):
      if other > 0:
        return Natural(int(self) ** other)

      if other == 0:
        if self == 0:
          raise Exception(f'Can not raise {type(self)} equals Zero to Zero')
        return Natural(1)

      if self == 0:  # 0 ^ (-*)
        raise Exception(f'Can not raise {type(self)} equals Zero to negative number')
      return Rational(1, int(self) * abs(other))

    if isinstance(other, (Natural)):
      if other > 0:
        return Natural(int(self) ** int(other))

      if other == 0:
        if self == 0:
          raise Exception(f'Can not raise {type(self)} equals Zero to Zero')
        return Natural(1)

      if self == 0:  # 0 ^ (-*)
        raise Exception(f'Can not raise {type(self)} equals Zero to negative number')
      return Rational(1, int(self) * abs(int(other)))

    raise Exception(f'Can not raise {type(self)} to {type(other)}')

  def __rpow__(self, other):
    return other ** int(self)

  def __neg__(self):
    rational = -Rational(int(self), 1)
    rational.simplify()
    return rational

  def __abs__(self):
    return self

  def __str__(self) -> str:
    return str(int(self.__number))

  def __round__(self, n=0):
    return round(self.__number, n)

  def __lt__(self, other) -> bool:
    if isinstance(other, (int, float)):
      return int(self) < other
    if isinstance(other, Rational):
      return int(self) < float(other)
    if isinstance(other, Natural):
      return int(self) < int(other)

    raise Exception(f'Can not use "<" operator with {type(self)} and {type(other)}')

  def __eq__(self, other) -> bool:
    if isinstance(other, (int, float)):
      return int(self) == other
    if isinstance(other, Rational):
      return int(self) == float(other)
    if isinstance(other, Natural):
      return int(self) == int(other)

    raise Exception(f'Can not use "==" operator with {type(self)} and {type(other)}')

  def __gt__(self, other) -> bool:
    if isinstance(other, (int, float)):
      return int(self) > other
    if isinstance(other, Rational):
      return int(self) > float(other)
    if isinstance(other, Natural):
      return int(self) > int(other)

    raise Exception(f'Can not use ">" operator with {type(self)} and {type(other)}')

  def __int__(self):
    return self.__number

  def __float__(self):
    return float(int(self))


class Rational(Numeric):
  '''
    __numerator: Union[int, float]
    __denominator: Union[int, float]
    __is_simplified: bool
    __is_decimal_loaded: bool
    __integer_part: Union[None, int]
    __non_periodic_decimal_part: Union[None, str]
    __periodic_decimal_part: Union[None, str]
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
    if not self.__is_simplified:
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

    return self

  def load_decimal(self):
    if not self.__is_decimal_loaded:
      self.__is_decimal_loaded = True

      helper = Rational(self.__numerator, self.__denominator).simplify()
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
        for _ in range(0, str(multiple).count('9') - len(periodic_decimal_part)):
          periodic_decimal_part = '0' + periodic_decimal_part
      self.__periodic_decimal_part = periodic_decimal_part

    return self

  def get_numerator(self):
    return self.__numerator

  def get_denominator(self):
    return self.__denominator

  def get_integer_part(self):
    return self.__integer_part

  def __add__(self, other):
    if isinstance(other, (int, float)):
      other = Rational(other, 1)
      return self + other
    if isinstance(other, Rational):
      self_helper = Rational(self.__numerator, self.__denominator).simplify()
      other_helper = Rational(other.__numerator, other.__denominator).simplify()
      result = Rational(self_helper.__numerator * other_helper.__denominator + other_helper.__numerator * self_helper.__denominator, self_helper.__denominator * other_helper.__denominator).simplify()
      return result

    raise Exception(f'Can not sum {type(self)} and {type(other)}')

  def __radd__(self, other):
    return self + other

  def __sub__(self, other):
    if isinstance(other, (int, float)):
      other = Rational(other, 1)
      return self - other
    if isinstance(other, Rational):
      self_helper = Rational(self.__numerator, self.__denominator).simplify()
      other_helper = Rational(other.__numerator, other.__denominator).simplify()
      result = Rational(self_helper.__numerator * other_helper.__denominator - other_helper.__numerator * self_helper.__denominator, self_helper.__denominator * other_helper.__denominator).simplify()
      return result

    raise Exception(f'Can not subtract {type(self)} and {type(other)}')

  def __rsub__(self, other):
    return -(self - other)

  def __mul__(self, other):
    if isinstance(other, (int, float)):
      other = Rational(other, 1)
      return self * other
    if isinstance(other, Rational):
      self_helper = Rational(self.__numerator, self.__denominator).simplify()
      other_helper = Rational(other.__numerator, other.__denominator).simplify()
      result = Rational(self_helper.__numerator * other_helper.__numerator, self_helper.__denominator * other_helper.__denominator).simplify()
      return result

    raise Exception(f'Can not multiply {type(self)} and {type(other)}')

  def __rmul__(self, other):
    return self * other

  def __truediv__(self, other):
    if (other == 0):
      raise Exception(f'Can not divide {type(self)} by Zero')

    if isinstance(other, (int, float)):
      other = Rational(other, 1)
      return self / other
    if isinstance(other, Rational):
      self_helper = Rational(self.__numerator, self.__denominator).simplify()
      other_helper = Rational(other.__numerator, other.__denominator).simplify()
      result = Rational(self_helper.__numerator * other_helper.__denominator, self_helper.__denominator * other_helper.__numerator).simplify()
      return result

    raise Exception(f'Can not divide {type(self)} and {type(other)}')

  def __rtruediv__(self, other):
    if (self == 0):
      raise Exception(f'Can not divide {type(other)} by Zero')

    return other * self ** (-1)

  def __pow__(self, other):
    if isinstance(other, (int)):
      if other > 0:
        self_helper = Rational(self.__numerator, self.__denominator).simplify()
        return Rational(self_helper.__numerator ** other, self_helper.__denominator ** other).simplify()

      if other == 0:
        if self == 0:
          raise Exception(f'Can not raise {type(self)} equals Zero to Zero')
        return Rational(1, 1).simplify()

      if self == 0:  # 0 ^ (-*)
        raise Exception(f'Can not raise {type(self)} equals Zero to negative number')

      self_helper = Rational(self.__numerator, self.__denominator).simplify()
      result = Rational(self_helper.__denominator ** abs(other), self_helper.__numerator ** abs(other)).simplify()
      return result

    raise Exception(f'Can not raise {type(self)} to {type(other)}')

  def __rpow__(self, other):
    helper = Rational(self.get_numerator(), self.get_denominator()).simplify()
    if (helper.get_denominator() == 1):
      return other ** self.get_numerator()
    raise Exception(f'Can not raise {type(other)} to Rational')

  def __neg__(self):
    return Rational(-self.__numerator, self.__denominator)

  def __abs__(self):
    return Rational(abs(self.__numerator), abs(self.__denominator))

  def __str__(self):
    if self.__is_decimal_loaded:
      if not isinstance(self.__integer_part, int):
        raise Exception(f'integer_part in {type(self)} is None when triyng to get string')
      if not isinstance(self.__non_periodic_decimal_part, str):
        raise Exception(f'non_periodic_decimal_part in {type(self)} is not str when triyng to get string')
      if not isinstance(self.__periodic_decimal_part, str):
        raise Exception(f'periodic_decimal_part in {type(self)} is not str when triyng to get string')

      if self.__non_periodic_decimal_part == self.__periodic_decimal_part == '':
        return str(self.__integer_part)
      if self.__non_periodic_decimal_part == '':
        return str(self.__integer_part) + ',' + Latex.overline(self.__periodic_decimal_part)
      if self.__periodic_decimal_part == '':
        return str(self.__integer_part) + ',' + self.__non_periodic_decimal_part
      return str(self.__integer_part) + ',' + self.__non_periodic_decimal_part + Latex.overline(self.__periodic_decimal_part)

    if (self.__is_simplified):
      sign = '-' if float(self) < 0 else ''
      if self.__denominator == 1:
        return str(self.__numerator)
      return sign + Latex.fraction(abs(self.__numerator), abs(self.__denominator))

    return Latex.fraction(self.__numerator, self.__denominator)

  def __round__(self, n=0):
    return round(float(self), n)

  def __lt__(self, other):
    if isinstance(other, (int, float)):
      return float(self) < other
    if isinstance(other, Rational):
      return float(self) < float(other)

    raise Exception(f'Can not use "<" operator with {type(self)} and {type(other)}')

  def __eq__(self, other):
    if isinstance(other, (int, float)):
      return float(self) == other
    if isinstance(other, Rational):
      return float(self) == float(other)

    raise Exception(f'Can not use "=" operator with {type(self)} and {type(other)}')

  def __gt__(self, other):
    if isinstance(other, (int, float)):
      return float(self) > other
    if isinstance(other, Rational):
      return float(self) > float(other)

    raise Exception(f'Can not use ">" operator with {type(self)} and {type(other)}')

  def __int__(self):
    return int(self.__numerator / self.__denominator)

  def __float__(self):
    return float(self.__numerator / self.__denominator)



class Trigonometric_function(Numeric):
  """
    self.__fn_name
    self.__degrees: int
    self.__radians: int
  """

  def __init__(self, degrees: Union[int, float], fn_name: str):
    self.__valid_fn_names = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot']

    if not isinstance(degrees, (int, float)):
      raise Exception(f'degrees in {type(self)} must be intenger or float')
    
    if fn_name not in self.__valid_fn_names:
      raise Exception(f'fn_name in {type(self)} must be one of {self.__valid_fn_names}')

    self.__fn_name = fn_name
    self.__degrees = degrees
    self.__radians = math.radians(degrees)

  def get_degrees(self):
    return self.__degrees
  
  def get_radians(self):
    return self.__radians



  def __add__(self, other):
    return float(self) + other

  def __radd__(self, other):
    return other + float(self)

  def __sub__(self, other):
    return float(self) - other

  def __rsub__(self, other):
    return other - float(self)

  def __mul__(self, other):
    return float(self) * other

  def __rmul__(self, other):
    return other * float(self)

  def __truediv__(self, other):
    if (other == 0):
      raise Exception(f'Can not divide {type(self)} function by Zero')
    return float(self) / other

  def __rtruediv__(self, other):
    if (self == 0):
      raise Exception(f'Can not divide {type(other)} by Zero')

    return other * self ** (-1)

  def __pow__(self, other):
    if self == 0 and other <= 0:
      raise Exception(f'Can not raise {type(self)} equals to Zero to lower or equals than Zero')
    return float(self) ** other

  def __rpow__(self, other):
    return other ** float(self)

  def __neg__(self):
    rational = -Rational(self.value, 1)
    rational.simplify()
    return rational

  def __abs__(self):
    return self

  def __str__(self) -> str:
    if self.__fn_name == 'sin':
      return fr'sin({self.__degrees}\degree)'
    
    if self.__fn_name == 'cos':
      return fr'cos({self.__degrees}\degree)'
    
    if self.__fn_name == 'cos':
      return fr'tan({self.__degrees}\degree)'
    
    if self.__fn_name == 'csc':
      return fr'csc({self.__degrees}\degree)'
    
    if self.__fn_name == 'sec':
      return fr'sec({self.__degrees}\degree)'
    
    if self.__fn_name == 'cot':
      return fr'cot({self.__degrees}\degree)'

    raise Exception(f'fn_name in {type(self)} must be one of {self.__valid_fn_names}')

  def __round__(self, n=0):
    return round(float(self, n))

  def __lt__(self, other) -> bool:
    return float(self) < float(other)

  def __eq__(self, other) -> bool:
    return float(self) == float(other)

  def __gt__(self, other) -> bool:
    return float(self) > float(other)

  def __int__(self):
    return int(float(self))

  def __float__(self):
    if self.__fn_name == 'sin':
      return math.sin(self.__radians)
    
    if self.__fn_name == 'cos':
      return math.cos(self.__radians)
    
    if self.__fn_name == 'cos':
      return math.tan(self.__radians)
    
    if self.__fn_name == 'csc':
      return 1 / math.sin(self.__radians)
    
    if self.__fn_name == 'sec':
      return 1 / math.cos(self.__radians)
    
    if self.__fn_name == 'cot':
      return 1 / math.tan(self.__radians)

    raise Exception(f'fn_name in {type(self)} must be one of {self.__valid_fn_names}')
