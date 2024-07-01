import ast


def has_imports(code_str: str):
  tree = ast.parse(code_str)
  for node in ast.walk(tree):
    if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
      return True
  return False


def has_exec(code_str: str):
  tree = ast.parse(code_str)
  for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'exec':
      return True
  return False


def has_eval(code_str: str):
  tree = ast.parse(code_str)
  for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'eval':
      return True
  return False


def has_print(code_str: str):
  tree = ast.parse(code_str)
  for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
      return True
  return False


def has_for_loop(code_str: str):
  tree = ast.parse(code_str)
  for node in ast.walk(tree):
    if isinstance(node, ast.For) or isinstance(node, ast.AsyncFor):
      return True
  return False


def has_while_loop(code_str: str):
  tree = ast.parse(code_str)
  for node in ast.walk(tree):
    if isinstance(node, ast.While):
      return True
  return False


def code_is_valid(code_str: str):
  fns = [has_imports, has_exec, has_eval, has_print, has_for_loop, has_while_loop]
  for fn in fns:
    is_not_valid = fn(code_str)
    if is_not_valid:
      return False
  return True
