from api.classes.Abstract import Numeric
from api.classes.Rational import Rational
from typing import Union, List


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
