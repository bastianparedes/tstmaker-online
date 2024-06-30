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

export { everyElementIsDifferent };
