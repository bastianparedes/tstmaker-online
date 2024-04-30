from typing import Union


class Latex:
  def fraction(numerator: Union[str, int, float], denominator: Union[str, int, float]):
    return fr'\dfrac{{{numerator}}}{{{denominator}}}'

  def overline(element: Union[str, int, float]):
    return fr'\overline{{{element}}}'
  
  def decorator_mathrm(fn):
    def newFn(*arg, **kwargs): 
      return fr'\mathrm{{{fn(*arg, **kwargs)}}}'
    return newFn
    
