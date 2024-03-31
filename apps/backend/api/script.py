import requests


def fn(latex_code: str):
  # Example latex code
  """
  \\documentclass{article}
  \\usepackage{amsmath}
  \\begin{document}
  Hello world4!
  \\end{document}
  """

  response = requests.post('https://texlive.net/cgi-bin/latexcgi', files={
      'filecontents[]': ('document.tex', latex_code, 'text/plain'),
      'filename[]': 'document.tex',
      'engine': 'pdflatex',
      'return': 'pdf'
  })
  return response.url
