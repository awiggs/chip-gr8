import Link  from 'next/link';
import Vars  from '../Vars'; 

export default ({ home, api }) => (
    <>
        <Link href={Vars.sitePrefix + '/index'}><a className={`m-md ${home ? 'active' : ''}`}><i className='fas fa-home' />Home</a></Link>
        <Link href={Vars.sitePrefix + '/api'}><a className={`m-md ${api ? 'active' : ''}`}><i className='fas fa-book' />API</a></Link>
        <Link href={Vars.sitePrefix + '/download'}><a className='m-md'><i className='fas fa-cloud-download-alt' />Download</a></Link>
    </>
);