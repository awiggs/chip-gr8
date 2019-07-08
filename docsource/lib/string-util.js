module.exports = {

    tab(str, n=4, init=false) {
        return str.replace(init ? /^|\n/g : /\n/g, '\n' + ' '.repeat(n));
    },

    spacesToTab(str, n=4) {
        let count = 0;
        for (const c of str) {
            if (c == '\n') {
                count = 0;
            } else {
                count = (count + 1) % n;
            }
        }
        return n - count;
    },

    lines(str) {
        return str.split('\n').length;
    },
    
}