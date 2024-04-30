def decorator_add_spaces(fn):
  def newFn(*arg, **kwarg):
    return f' {fn(*arg, **kwarg)} '
  return newFn

class Math:
  def parenthesis(expression):
    return fr'\left( {expression} \right)'
  
  @decorator_add_spaces
  def brackets(expression):
    return fr'\left[{expression}\right]'
  
  @decorator_add_spaces
  def degree():
    return r'\degree'
  
  @decorator_add_spaces
  def leq(expression):
    return r'\leq'
  
  @decorator_add_spaces
  def leq(expression):
    return r'\geq'

  @decorator_add_spaces
  def different():
    return r'\neq'
  
  @decorator_add_spaces
  def percentage():
    return r'\%'