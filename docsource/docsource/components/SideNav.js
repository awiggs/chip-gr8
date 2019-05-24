import React from 'react';

import { usePageIndex } from '../lib/hooks';

const NavItem = ({ active, href, text, children }) => (
    <li className={active ? 'nav-item active' : 'nav-item'}>
        <a href={href}>{text}</a>
        {children && <ul className='nav inner'>{children}</ul>}
    </li>
);

export default () => {
    const index = usePageIndex();
    return <div className='side-nav text-center hide-xl'>
        <ul className='nav outer d-inline-block text-left'>
            {index.map(({ active: active, href, text, children }, key) => (
                <NavItem key={key} active={active} href={href} text={text}>
                    {children && children.map(({ active, href, text }, key) => (
                        <NavItem key={key} active={active} href={href} text={text} />
                    ))}
                </NavItem>
            ))}
        </ul>
    </div>;
};