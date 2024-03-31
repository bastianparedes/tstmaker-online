// Contenido del archivo document.tex
const fileContents = `
\\documentclass{article}
\\usepackage{amsmath}
\\begin{document}
Hello world3!
\\end{document}
`;

// Crear un objeto FormData
const formData = new FormData();
formData.append('filecontents[]', new Blob([fileContents], { type: 'text/plain' }), 'document.tex');
formData.append('filename[]', 'document.tex');
formData.append('engine', 'pdflatex');
formData.append('return', 'pdf');

// URL a la que enviar la solicitud PUT
const urlApi = 'https://texlive.net/cgi-bin/latexcgi'; // Reemplazar 'URL_DEL_SERVIDOR' por la URL adecuada

// Realizar la solicitud POST
const response = await fetch(urlApi, {
  method: 'POST',
  body: formData
});

response.url

