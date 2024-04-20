from abc import ABC, abstractmethod
from typing import Union


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
