from api.classes.Rational import Rational


def test_eq():
  assert Rational(1, 1) == 1
  assert Rational(1, 2) == 0.5


def test_operations():
  assert Rational(2, 5) + Rational(1, 3) == Rational(11, 15)
  assert -Rational(2, 3) == Rational(-2, 3)
  assert Rational(2, -3) ** 4 == Rational(2 ** 4, 3 ** 4)
  assert Rational(4, 3) > Rational(1, 2)
  assert Rational(1, 2) < Rational(4, 3)


def test_simplify():
  rational = Rational(-4, -6)
  assert rational.get_numerator() == -4 and rational.get_denominator() == -6


def test_str():
  rational = Rational(-4, -6)
  assert str(rational) == r'\dfrac{-4}{-6}'

  rational.simplify()
  assert str(rational) == r'\dfrac{2}{3}'


def test_int():
  assert int(Rational(10, 7)) == 1


def test_float():
  assert float(Rational(2, 3)) == 2 / 3
