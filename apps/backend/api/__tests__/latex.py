from api.classes.Latex import Latex

def fraction():
  assert Latex.fraction(1, 2) == r'\dfrac{1}{2}'

def overline():
  assert Latex.fraction(1) == r'\overline{1}'
