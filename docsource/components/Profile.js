export default ({ src, name, position, right=false, children }) => right 
    ? (
        <div className='profile'>
            <div className='container columns'>
                <div className='col-8 col-sm-12 hide-sm'>
                    <div className='profile-name'>{name}</div>
                    <div className='profile-position'>{position}</div>
                    <div className='profile-content'>
                        {children}
                    </div>
                </div>
                <div className='col-4 col-sm-12'>
                    <img src={src} className={right ? 'right' : 'left'} />
                </div>
                <div className='col-sm-12 show-sm'>
                    <div className='profile-name'>{name}</div>
                    <div className='profile-position'>{position}</div>
                    <div className='profile-content'>
                        {children}
                    </div>
                </div>
            </div>
        </div>
    ) : (
        <div className='profile'>
            <div className='container columns'>
                <div className='col-4 col-sm-12'>
                    <img src={src} className={right ? 'right' : 'left'} />
                </div>
                <div className='col-8 col-sm-12'>
                    <div className='profile-name'>{name}</div>
                    <div className='profile-position'>{position}</div>
                    <div className='profile-content'>
                        {children}
                    </div>
                </div>
            </div>
        </div>
    );