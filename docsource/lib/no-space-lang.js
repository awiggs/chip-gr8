export default (source, options) => {
    const { defaults, allowed } = options;
    const result                = defaults || {};
    parseExpr(source, result, allowed);
    return result;
};

const parseExpr = (expr, result, allowed) => {
    for (const pair of expr.split('-')) {
        parsePair(pair, result, allowed);
    }
};

const parsePair = (pair, result, allowed) => {
    const [key, atom] = pair.split(':');
    if (key) {
        if (allowed) {
            if (!allowed.includes(key)) {
                throw new Error(`${key} is not allowed!`);
            }
        }
        if (atom) {
            result[key] = parseAtom(atom); 
        } else {
            result[key] = true;
        }
    }
};

const parseAtom = (atom) => {
    if (atom === 'true')    { return true; }
    if (atom === 'false')   { return false; }
    if (/^\d+$/.test(atom)) { return parseInt(atom, 10); }
    return atom;
};