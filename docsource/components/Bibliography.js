import EjrbussMarkdown from './EjrbussMarkdown';

export default ({ content }) => (
    <div className='bibliography'>
        <h1>References</h1>
        {content.map((item, key) => <BibliographyItem index={key} content={item} key={key}/>)}
    </div>
);

const BibliographyItem = ({ index, content }) => (
    <div className='bibliography-item'>
        <div className='index'>[{index + 1}]</div>
        <div className='text'><EjrbussMarkdown source={content} /></div>
    </div>
);