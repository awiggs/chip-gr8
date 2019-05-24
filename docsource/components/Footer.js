import SocialMedia from './SocialMedia';
import Copyright   from './Copyright';
import Love        from './Love';

export default ({ 
    left   = <SocialMedia />,
    right  = <Copyright className='text-right subtext' />,
    center = <Love />
}) => (
    <footer>
        <div className='container grid-md'>
            <div className='columns'>
                <div className='column col-3 hide-sm'>{left}</div>
                <div className='column col-6 col-sm-12'>{center}</div>
                <div className='column col-3 hide-sm'>{right}</div>
            </div>
        </div>
    </footer>
);