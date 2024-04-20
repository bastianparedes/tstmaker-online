from api.classes.Abstract import Numeric
from api.classes.Rational import Rational
from typing import Union, List

class Natural(Numeric):
  """
    __number: Union[int, float]
    denominator: Union[int, float]
    __is_simplified: bool
    __is_decimal_loaded: bool
    integer_part: Union[None, int]
    non_periodic_decimal_part: Union[None, str]
    periodic_decimal_part: Union[None, str]
  """
  def __init__(self, number: int):
    if type(number) != int: raise Exception('number in Natural must be intenger')
    if not number > 0: raise Exception('number in Natural must be greater than zero')

    self.__number = number
    self.__dividers: Union[None, List[int]] = None
    self.__is_prime: Union[None, bool] = None
    self.__is_perfect: Union[None, bool] = None
  
  def get_dividers(self):
    if self.__dividers != None: return self.__dividers
    self.__dividers = []
    number = 1
    while (number <= self.__number):
      if (self.__number % number == 0): self.__dividers.append(number)
      number += 1
    
    return self.__dividers

  def is_prime(self):
    if type(self.__is_prime) == bool: return self.__is_prime
    self.__is_prime = len(self.get_dividers()) == 2
    return self.__is_prime

  def is_perfect(self):
    if (self.__is_perfect != None): return self.__is_perfect
    self.__is_perfect = sum(self.get_dividers()) / 2 == self.__number
    return self.__is_perfect

  def __add__(self, other):
    if isinstance(other, int): return Natural(self.value + other)
    if isinstance(other, float): return Rational(self.value + other, 1).simplify()
    if isinstance(other, (Rational)): return Rational(self.value + 1) + other
    if isinstance(other, (Natural)): return Natural(self.value, other.value)
    raise Exception(f'Can not sum Natural and {type(other)}')

  def __radd__(self, other):
    return self + other

  def __sub__(self, other):
    if isinstance(other, int): return Rational(self.value - other)
    if isinstance(other, float): return Rational(self.value, 1) - other
    if isinstance(other, Rational): return Rational(self.value, 1) - other
    if isinstance(other, Natural): return Natural(self.value - other.value)
    raise Exception(f'Can not subtract Natural and {type(other)}')

  def __rsub__(self, other):
    return -(self - other)

  def __mul__(self, other):
    if isinstance(other, int): return Natural(self.value * other)
    if isinstance(other, float): return Rational(self.value, 1) * other
    if isinstance(other, Rational): return Rational(self.value, 1) * other
    if isinstance(other, Natural): return Natural(self.value * other.value)
    raise Exception(f'Can not multiply Natural and {type(other)}')

  def __rmul__(self, other):
    return self * other

  def __truediv__(self, other):
    if (other == 0):
      raise Exception('Can not divide Natural by Zero')
    if isinstance(other, int): return Rational(self.value,  other).simplify()
    if isinstance(other, float): return Rational(self.value, other).simplify()
    if isinstance(other, Rational): return Rational(self.value * other.__denominator, other.__numerator).simplify()
    if isinstance(other, Natural): return Rational(self.value, other.value).simplify()
    raise Exception(f'Can not divide Natural and {type(other)}')

  def __rtruediv__(self, other):
    if (self == 0):
      raise Exception(f'Can not divide {type(other)} by Zero')
    
    return other * self ** (-1)

  def __pow__(self, other):
    if isinstance(other, (int)):
      if other > 0:
        return Natural(self.value ** other)

      if other == 0:
        if self == 0:
          raise Exception(f'Can not raise {type(self)} equals Zero to Zero')
        return Natural(1)

      if self == 0: # 0 ^ (-*)
        raise Exception(f'Can not raise {type(self)} equals Zero to negative number')
      return Rational(1, self.value * abs(other))
    
    if isinstance(other, (Natural)):
      if other > 0:
        return Natural(self.value ** other.value)

      if other == 0:
        if self == 0:
          raise Exception(f'Can not raise {type(self)} equals Zero to Zero')
        return Natural(1)

      if self == 0: # 0 ^ (-*)
        raise Exception(f'Can not raise {type(self)} equals Zero to negative number')
      return Rational(1, self.value * abs(other.value))

    raise Exception(f'Can not raise {type(self)} to {type(other)}')

  def __rpow__(self, other):
    return other ** self.value

  def __neg__(self):
    rational = -Rational(self.value, 1)
    rational.simplify()
    return rational

  def __abs__(self):
    return self

  def __str__(self) -> str:
    return str(int(self.__number))

  def __round__(self):
    return self

  def __lt__(self, other) -> bool:
    if isinstance(other, (int, float)):
      return self.value < other
    if isinstance(other, Rational):
      return self.value < float(other)
    if isinstance(other, Natural):
      return self.value < other.value

    raise Exception(f'Can not use "<" operator with {type(self)} and {type(other)}')

  def __eq__(self, other) -> bool:
    if isinstance(other, (int, float)):
      return self.value == other
    if isinstance(other, Rational):
      return self.value == float(other)
    if isinstance(other, Natural):
      return self.value == other.value

    raise Exception(f'Can not use "==" operator with {type(self)} and {type(other)}')

  def __gt__(self, other) -> bool:
    if isinstance(other, (int, float)):
      return self.value > other
    if isinstance(other, Rational):
      return self.value > float(other)
    if isinstance(other, Natural):
      return self.value > other.value

    raise Exception(f'Can not use ">" operator with {type(self)} and {type(other)}')

  def __int__(self):
    return int(self.value)

  def __float__(self):
    return float(self.value)