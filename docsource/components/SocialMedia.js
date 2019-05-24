export default ({ accent }) => (
    <>
        <a target='_blank' href='https://www.linkedin.com/in/ejrbuss/' className={`p-md subtle${accent ? '-accent' : ''}`} >
            <i className='fab fa-linkedin-in fa-lg' />
        </a>
        <a target='_blank' href='https://github.com/ejrbuss' className={`p-md subtle${accent ? '-accent' : ''}`} >
            <i className='fab fa-github fa-lg' />
        </a>
        <a target='_blank' href='https://twitter.com/ejrbuss' className={`p-md subtle${accent ? '-accent' : ''}`} >
            <i className='fab fa-twitter fa-lg' />
        </a>
    </>
);