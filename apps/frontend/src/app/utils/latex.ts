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
\\usepackage{fancyhdr}%
%\\usepackage[papersize={21.59cm, 27.94cm}, tmargin=2.0cm, bmargin=2.0cm, lmargin=2.0cm, rmargin=2.0cm]{geometry}%
\\usepackage[a4paper, margin=1cm, bmargin=2cm]{geometry}%
\\usetikzlibrary{fit, shapes.geometric, quotes, angles, through, intersections}%
`.trim();

const studentDataTable = `
\\begin{longtable}{|p{0.475\\linewidth}|p{0.475\\linewidth}|}%
  \\hline%
  Establecimiento:&Profesor(a):%
  \\\\%
  \\hline%
  Asignatura:&Curso:%
  \\\\%
  \\hline%
\\end{longtable}%
`.trim();

const tableUniqueSelection = (
  exercises: {
    statement: string;
    alternatives: string[];
  }[]
) => {
  const latexLines = [
    '\\textbf{Item selección múltiple:} Encierra la alternativa correcta de cada ejercicio.%',
    '\\begin{longtable}{|p{0.475\\linewidth}|p{0.475\\linewidth}|}%',
    '\\hline%',
  ];

  exercises.forEach((exercise, indexExercise) => {
    latexLines.push(
      `\\begin{enumerate}[label=\\arabic*),start=${indexExercise + 1}]%`
    );
    latexLines.push('\\item%');
    latexLines.push(exercise.statement + '%');
    latexLines.push('\\end{enumerate}%');
    latexLines.push('\\begin{enumerate}[label=\\Alph*)]%');
    exercise.alternatives.forEach((alternative) => {
      latexLines.push('\\item%');
      latexLines.push(alternative + '%');
      latexLines.push('\\hfill \\break%');
    });
    latexLines.push('\\end{enumerate}%');

    const isLastExercise = indexExercise + 1 === exercises.length;

    if (indexExercise % 2 === 0) {
      latexLines.push('&%');
    }
    if (indexExercise % 2 === 1 || isLastExercise) {
      latexLines.push('\\\\%');
      latexLines.push(`\\hline%`);
    }
  });

  latexLines.push('\\end{longtable}%');
  return latexLines.join('\n');
};

const completeLatexCode = (body: string) => {
  return [
    packages,
    '\\begin{document}%',
    studentDataTable,
    body,
    '\\end{document}%',
  ].join('\n');
};

export { completeLatexCode, tableUniqueSelection };
