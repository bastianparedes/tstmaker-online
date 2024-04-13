from api.classes.Latex import Latex


def test_fraction():
  assert Latex.fraction(1, 2) == r'\dfrac{1}{2}'


def test_overline():
  assert Latex.overline(1) == r'\overline{1}'
