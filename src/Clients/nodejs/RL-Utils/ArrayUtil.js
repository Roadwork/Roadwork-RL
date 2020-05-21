/**
 * Get the index value of the maximum value in an array
 * e.g. if our array is [2, 6, 3, 5] it will return 1 since 6 is the highest
 */
exports.getIndexOfMaxValue = (arr = []) => {
    return arr.indexOf(Math.max(...arr));
}
  
/**
 * Return the highest value in our array
 */
exports.getMaxValue = (arr = []) => {
    return Math.max(...arr);
}

/**
 * Generate the cartesian product between sets
 * 
 * In other terms: generate all possible combinations of multiple arrays
 * 
 * https://stackoverflow.com/questions/12303989/cartesian-product-of-multiple-arrays-in-javascript
 * 
 * @param {Array} inArr an array of numbers
 */
exports.f = (a, b) => [].concat(...a.map(d => b.map(e => [].concat(d, e))));
exports.cartesianProduct = (a, b, ...c) => (b ? exports.cartesianProduct(exports.f(a, b), ...c) : a);