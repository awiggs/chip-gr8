export default ({ content }) => (
    <div class='bibliography'>
        {content.map((item, key) => <BibliographyItem {...item} key={key}/>)}
    </div>
);

const BibliographyItem = ({ title, content }) => (
    <div className='bibliography-item'>
        <h1>{title}</h1>
        <p>{content}</p>
    </div>
);