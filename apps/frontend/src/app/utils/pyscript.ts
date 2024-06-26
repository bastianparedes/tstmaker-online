/* eslint-disable @typescript-eslint/no-explicit-any */

const runPythonCode = async (pythonFnCode: string) => {
  loadPyScript();
  const nameWindowProperty = (() => {
    const letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    let resultado = '';
    for (let i = 0; i < 50; i++) {
      const indiceAleatorio = Math.floor(Math.random() * letras.length);
      resultado += letras[indiceAleatorio];
    }
    return resultado;
  })();

  const fullCode = [
    'from pyscript import ffi, window',
    pythonFnCode,
    'result = fn()',
    `window.${nameWindowProperty} = ffi.to_js(fn())`,
  ].join('\n');

  console.log(fullCode);

  const pyScript = document.createElement('py-script');
  pyScript.id = nameWindowProperty;
  pyScript.innerHTML = fullCode;
  document.head.appendChild(pyScript);

  return new Promise((resolve) => {
    Object.defineProperty(window, nameWindowProperty, {
      set: (value) => {
        resolve(value);
        delete (window as any)[nameWindowProperty];
        document.querySelector(`#${nameWindowProperty}`)?.remove();
      },
      configurable: true,
    });
  });
};

let pyScriptIsLoaded = false;
const loadPyScript = () => {
  if (pyScriptIsLoaded) return;
  pyScriptIsLoaded = true;
  const pyScript = document.createElement('script');
  pyScript.type = 'module';
  pyScript.src = 'https://pyscript.net/releases/2024.6.2/core.js';
  document.head.appendChild(pyScript);
};

export { runPythonCode, loadPyScript };
