import { useState } from 'react';
import _ from 'lodash';

const Tani = {

    Tile({ x, y, delayIndex }) {
        const [hover, setHover] = useState(false);
        return (
            <polygon 
                className={`tile ${hover ? 'hover' : ''}`}
                points={`${x} ${y}, ${x} ${y + 10}, ${x + 10} ${y + 10}, ${x + 10} ${y}`}
                style={{ animationDelay: delayIndex * 0.1 + 's' }}
                onMouseEnter={() => setHover(true)}
                onMouseLeave={() => setTimeout(() => setHover(false), 150)}
            />
        );
    },

    Hline({ y, width, delay=0.1, delayIndex }) {
        return <path 
            className='lh'
            d={`M0 ${y * 10 + 10} H${width}`}
            style={{ animationDelay: delayIndex * delay + 's' }}
        />
    },

    HLines({ n, width, delay, reverse }) {
        return _.range(n).map((y, key) =>
            <Tani.Hline key={key} y={y} width={width} delay={delay} delayIndex={reverse ? n - key : key} />
        );
    },

    Vline({ x, height, delay=0.1, delayIndex }) {
        return <path 
            className='lv'
            d={`M${x * 10 + 10} 0 V${height}`} 
            style={{ animationDelay: delayIndex * delay + 's' }}
        />
    },

    VLines({ n, height, delay, reverse }) {
        return _.range(n).map((x, key) =>
            <Tani.Vline key={key} x={x} height={height} delay={delay} delayIndex={reverse ? n - key : key} />
        );
    },

};

export default Tani;