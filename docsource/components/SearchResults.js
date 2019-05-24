import Router from 'next/router';

const SearchResult = ({ title, previews, href }) => 
    <div className='search-result' onClick={() => {Router.push(href)}}>
        <div className='title'>{title}</div>
        <div className='text'>{previews.map((preview, key) => 
            <p key={key}>{preview}</p>)}
        </div>
    </div>

const NoResults = () => 
    <div className='no-results'>
        <h1><code>{'nil'}</code></h1>
        Oops! There's nothing but <code>nil</code> here. Try searching something else.
    </div>;

export default ({ searchCtx }) =>
    <div onClick={searchCtx.toggle} className={searchCtx.open ? 'search-results open' : 'search-results'}>
        <div className='container grid-md'>
            {searchCtx.search.length && !searchCtx.results.length
                ? <NoResults />
                : searchCtx.results.map(({ title, previews, href }, key) => 
                    <SearchResult key={key} title={title} previews={previews} href={href} />
                )
            }
        </div>
    </div>;