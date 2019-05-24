// Components
import Boot            from '../components/Boot';
import Navbar          from '../components/Navbar';
import SideNav         from '../components/SideNav';
import Footer          from '../components/Footer';
import SearchResults   from '../components/SearchResults';
import EjrbussMarkdown from '../components/EjrbussMarkdown';
import Places          from '../components/Places';
import Logo            from '../components/Logo';


// Libraries
import Pages from '../lib/Pages';
import Vars  from '../Vars';
import { useSearch } from '../lib/hooks';

export default ({ pageName }) => {
    const page      = Pages[pageName];
    const searchCtx = useSearch();
    return (
        <>
            <div id='page'>
            <Boot { ...page } />
                <Navbar 
                    searchCtx={searchCtx}
                    showScrollMarker
                    showSearch
                    leftLinks={<Places home />}
                    rightLinks={<a href={Vars.github} className='p-md subtle-accent'>
                        <i className='fab fa-github fa-lg' />
                    </a>}
                />
                <SideNav />
                <SearchResults searchCtx={searchCtx} />
                <div className='content container grid-md docs'>
                    <Logo />
                    <p className='text-center subtext p-md'>{page.version}</p>
                    <div className='text-center clr-accent subtitle'>
                        <EjrbussMarkdown source={page.subtitle} />
                    </div>
                    <EjrbussMarkdown source={page.content} />
                </div>
            </div>
            <Footer />
        </>
    );
};