const everyElementIsDifferent = <T>(array: T[]) => {
  const set = new Set();
  for (const element of array) {
      let serializedElement = JSON.stringify(element);
      if (set.has(serializedElement)) {
          return false;
      }
      set.add(serializedElement);
  }
  return true;
}

const arrayIncludesElement = <T, U>(array: T[], element: U) => {
  return array.some(item => {
    return JSON.stringify(item) === JSON.stringify(element);
  });
}

export { everyElementIsDifferent, arrayIncludesElement };

