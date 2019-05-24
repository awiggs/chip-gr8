import Vars from '../Vars';

export default ({ accent }) => (
    <>
        <a target='_blank' href={Vars.github} className={`p-md subtle${accent ? '-accent' : ''}`} >
            <i className='fab fa-github fa-lg' />
        </a>
    </>
);