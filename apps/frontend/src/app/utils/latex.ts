const packages = `
\\documentclass{article}%
\\usepackage[T1]{fontenc}%
\\usepackage[utf8]{inputenc}%
\\usepackage{lmodern}%
\\usepackage{textcomp}%
\\usepackage{lastpage}%
\\usepackage{ragged2e}%
\\usepackage{setspace}%
\\usepackage{longtable}%
\\usepackage{tabularx}%
\\usepackage{gensymb}%
\\usepackage{amsmath}%
\\usepackage{amssymb}%
\\usepackage{enumitem}%
\\usepackage{graphicx}%
\\usepackage{tikz}%
\\usepackage{tkz-euclide}%
\\usepackage{siunitx}%
\\usepackage{fourier}%
\\usetikzlibrary{fit, shapes.geometric, quotes, angles, through, intersections}%
\\usepackage{fancyhdr}%
\\usepackage[papersize={21.59cm, 27.94cm},tmargin=2.0cm,bmargin=2.0cm,lmargin=2.0cm,rmargin=2.0cm]{geometry}%
`.trim();

const completeLatexCode = (body: string) => {
  return `
${packages}
\\begin{document}%
\\normalsize%
\\pagestyle{fancy}%
${body}
\\end{document}%
  `.trim();
};

const exerciseStatements = Object.freeze({
  uniqueSelection: 'Encierra la alternativa correcta de cada ejercicio.',
});

const lineBreak = '\\hfill \\break%';

export { completeLatexCode, exerciseStatements, lineBreak };
