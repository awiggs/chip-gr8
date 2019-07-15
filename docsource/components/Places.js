import Link  from 'next/link';
import Vars  from '../Vars'; 

export default ({ home, about, project }) => (
    <>
        <Link href={Vars.sitePrefix + '/index'}><a className={`m-md ${home ? 'active' : ''}`}><i className='fas fa-home' />Home</a></Link>
        <Link href={Vars.sitePrefix + '/project'}><a className={`m-md ${project ? 'active' : ''}`}>Project</a></Link>
        <Link href={Vars.sitePrefix + '/about'}><a className={`m-md ${about ? 'active' : ''}`}>About</a></Link>
    </>
);