import Link  from 'next/link';
import Vars  from '../Vars'; 

export default ({ home, about, reference }) => (
    <>
        <Link href={Vars.sitePrefix + '/index'}><a className={`m-md ${home ? 'active' : ''}`}><i className='fas fa-home' />Home</a></Link>
        <Link href={Vars.sitePrefix + '/about'}><a className={`m-md ${about ? 'active' : ''}`}>About</a></Link>
        <Link href={Vars.sitePrefix + '/reference'}><a className={`m-md ${reference ? 'active' : ''}`}>Reference</a></Link>
    </>
);