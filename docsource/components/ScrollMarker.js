import React from 'react';
import { useScroll } from '../lib/hooks';

export default () => {
    const width = useScroll().yr * 100 + '%';
    return (
        <div className='scroll-marker' style={{ width }} />
    );
};