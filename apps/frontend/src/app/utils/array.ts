const everyElementIsDifferent = <T>(array: T[]) => {
  const set = new Set();
  for (const element of array) {
    if (set.has(element)) {
      return false;
    }
    set.add(element);
  }
  return true;
};

export { everyElementIsDifferent };
