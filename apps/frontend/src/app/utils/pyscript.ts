const runPythonCode = (code: string) => {
  const pyScript = document.createElement('py-script');
  pyScript.innerHTML = code;
  document.head.appendChild(pyScript);
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
