import Link  from 'next/link';
import Vars  from '../Vars'; 

export default ({ home, about, project, api }) => (
    <>
        <Link href={Vars.sitePrefix + '/index'}><a className={`m-md home ${home ? 'active' : ''}`}><i className='fas fa-home'/>Home</a></Link>
        <Link href={Vars.sitePrefix + '/about'}><a className={`m-md ${about ? 'active' : ''}`}><i className='fas fa-info'/>About</a></Link>
        <Link href={Vars.sitePrefix + '/docs'}><a className={`m-md ${api ? 'active' : ''}`}><i className="fas fa-book"></i>Docs</a></Link>
    </>
);