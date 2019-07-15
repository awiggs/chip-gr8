import EjrbussMarkdown from './EjrbussMarkdown';

export default ({ timeline }) => (
    <div className='timeline'>
        {timeline.map((item, key) => <TimeLineItem {...item} key={key}/>)}
    </div>
);

const TimeLineItem = ({ title, content }) => (
    <div className='timeline-item'>
        <div className="timeline-left">
            <a className="timeline-icon icon-lg" />
        </div>
        <div className="timeline-content">
            <div className='timeline-title'>{title}</div>
            <EjrbussMarkdown source={content} />
        </div>
    </div>
);