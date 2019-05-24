import ReactMarkdown from 'react-markdown';

// Components
import Editor from './Editor';

// Libraries
import noSpaceLang from '../lib/no-space-lang';

const evaluators = {
    jsEvaluator(value) {
        try {
            return eval(value).toString();
        } catch(err) {
            return <span className='clr-error'>{err.toString()}</span>;
        }
    },
    echo(value) {
        return value;
    },
};

export const registerEvaluator = (name, evaluator) => {
    evaluators[name] = evaluator;
};

const getHeaderText = ({ children: [{ props: { value }}] }) => {
    return value;
};

const getHeaderId = props => {
    return getHeaderText(props).replace(/\s/g, '').toLowerCase();
};

export default ({ source }) => (
    <ReactMarkdown className='md indexable' source={source} renderers={{

        code({ value, language }) {
            const { lang, immediate, readonly, evaluator, placeholder, nolines } = noSpaceLang(language, { 
                defaults : { lang: '' },
                allowed  : ['lang', 'immediate', 'readonly', 'evaluator', 'placeholder', 'nolines'] 
            });
            return (
                <Editor 
                    initialText={placeholder ? undefined : value} 
                    language={lang} 
                    evaluator={evaluators[evaluator]}
                    placeholder={placeholder ? value : undefined}
                    readonly={readonly} 
                    immediate={immediate}
                    nolines={nolines}
                    nooutput={evaluator ? false : true}
                />
            );
        },

        inlineCode({ value }) {
            if (/^icon:/.test(value)) {
                return <i className={value.split(':')[1]}/>
            }
            return <code>{value}</code>;
        },

        heading(props) {
            const id = getHeaderId(props);
            switch (props.level) {
                case 1: {
                    return <>
                        <a className='anchor-point' id={id} />
                        <a className='anchor' href={'#' + id}>
                            <h1>{props.children}</h1>
                            <br />
                        </a>
                    </>;
                }
                case 2: {
                    return <>
                        <a className='anchor-point' id={id} />
                        <a className='anchor' href={'#' + id}>
                            <h2>{props.children}</h2>
                            <br />
                        </a>
                    </>
                }
                case 3: return <h3 id={getHeaderId(props)}>{props.children}</h3>;
                case 4: return <h4 id={getHeaderId(props)}>{props.children}</h4>;
                case 5: return <h5 id={getHeaderId(props)}>{props.children}</h5>;
                case 6: return <h6 id={getHeaderId(props)}>{props.children}</h6>;
                default: throw new Error('Unknown header depth: ' + props.level);
            }
        },

        table(props) {
            return <table className='table table-striped table-scroll'>{props.children}</table>;
        }

    }} />
);