import ScrollMarker from './ScrollMarker';
import React        from 'react';

export default ({ leftLinks, rightLinks, showSearch, showScrollMarker, searchCtx }) => (
    <header className='navbar'>
        {showScrollMarker ? <ScrollMarker /> : null}
        <section className='navbar-section container grid-md'>
            <div className='left'>
                {leftLinks}
            </div>
            <div className='fill-width'>
                <div className='float-right hide-xs text-sm center'>
                    {showSearch && <>
                        <input 
                            type='text' 
                            placeholder='Type to search...' 
                            ref={e => e && e.focus()} 
                            onChange={e => searchCtx.change(e.target.value)} 
                            value={searchCtx.search}
                            className={searchCtx.open ? 'open' : 'closed'}
                        /> 
                        <a onClick={searchCtx.toggle} className='p-md subtle-accent'>
                            <i className={searchCtx.open
                                ? 'fas fa-times fa-lg clr-accent'
                                : 'fas fa-search fa-lg'
                            } />
                        </a>
                    </>}
                    {rightLinks}
                </div>
                <div className={`search hide-xs text-sm ${searchCtx.open ? 'open' : ''}`} />
            </div>
        </section>
    </header>
);