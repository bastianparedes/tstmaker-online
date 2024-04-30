from api.classes.Abstract import Numeric
from api.classes.Rational import Rational
import math
from typing import Union


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