import { useState, useEffect } from 'react';
import Pages from '../lib/Pages';


export const useScroll = () => {

    const getScrollState = () => ({
        x: window.pageXOffset,
        y: window.pageYOffset,
        xr: window.pageXOffset / (document.body.offsetWidth - screen.width),
        yr: window.pageYOffset / (document.body.offsetHeight - screen.height),
    });

    const [scroll, setScroll] = useState({ x: 0, y: 0, xr: 0, xy: 0 });
    useEffect(() => {
        const handleScroll = () => {
            setScroll(getScrollState());
        };
        handleScroll();
        window.addEventListener('scroll', handleScroll);
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);
    return scroll;
};

export const useSearch = () => {
    const [open, setOpen] = useState(false);
    const [search, setSearch] = useState('');
    const [results, setResults] = useState([]);

    // Add event listener
    useEffect(() => {
        const keyPress = (e) => {
            // On escape
            if (e.keyCode === 27) {
                setOpen(false);
            }
        };
        document.addEventListener('keydown', keyPress);
        return () => {
            document.removeEventListener('keydown', keyPress);
        }
    }, []);

    return {
        open, search, results,
        change(search) {
            setSearch(search)
            if (search.length > 0) {
                const pages = Pages.$search(search);
                setResults(pages.map(page => ({
                    title    : page.title,
                    href     : page.route,
                    previews : page.$previews(search), 
                })));
            } else {
                setResults([]);
            }
        },
        toggle() {
            setSearch('');
            setOpen(!open);
            setResults([]);
        },
    };
};

const getYOffset = e => {
    let y = 0;
    while (e && !isNaN( e.offsetTop)) {
        y += e.offsetTop - e.scrollTop;
        e = e.offsetParent;
    }
    return y;
};

const ANCHOR_OFFSET = 200;

export const usePageIndex = () => {
    const [index, setIndex] = useState([]);
    
    const scroll = useScroll();

    const handleUpdate = () => {

        const getBestHeader = (best, h) => {
            best.active = false;
            h.active    = false;
            return (h.yOffset - ANCHOR_OFFSET) < scroll.y ? h : best;
        };

        if (index.length) {
            const activeH1 = index.reduce(getBestHeader);
            activeH1.active = true;
            if (activeH1.children.length) {
                const activeH2 = activeH1.children.reduce(getBestHeader);
                activeH2.active = true;
            }
            setIndex(index);
        }
    };

    // Create Index
    useEffect(() => {
        for (const h1 of document.querySelectorAll('.indexable h1')) {
            index.push({
                text     : h1.textContent,
                href     : h1.parentNode.getAttribute('href'),
                active   : false,
                children : [],
                yOffset  : getYOffset(h1),
            });
        }
        let i = 0;
        for (const h2 of document.querySelectorAll('.indexable h2')) {
            const yOffset = getYOffset(h2);
            while (index[i + 1] && index[i + 1].yOffset < yOffset) {
                i++;
            }
            index[i].children.push({
                text     : h2.textContent,
                href     : h2.parentNode.getAttribute('href'),
                active   : false,
                yOffset,
            });
        }
        handleUpdate();
    }, []);

    // Update Index
    useEffect(handleUpdate, [index, scroll]);

    return index;
};