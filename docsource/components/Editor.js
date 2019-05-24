import React, { useState, useEffect, useRef } from 'react';
import hljs                                   from 'highlight.js';
import _                                      from 'lodash';

import { spacesToTab, lines as countLines } from '../lib/string-util';

const TAB_KEY = 9;

const defaultEvaluator = () => (
    <span className='clr-error'>No Evaluator!</span>
);

export default ({
    initialText = '',               // The starting text of the editor field
    placeholder = '',               // Placeholder text for the editor field
    language    = '',               // The editor language (highlighting/display)
    evaluator   = defaultEvaluator, // The text evaluator for the output
    readonly    = false,            // Whether the editor field should be editable 
    immediate   = false,            // Whether the evaluator should be called immediately
    nooutput    = false,            // Whether the output section should be shown
    nolines     = false,            // Whether the line numbers should be shown
}) => {
    const [text, setText] = useState(initialText);
    const [refresh, setRefresh] = useState(false);
    const [output, setOutput] = useState(immediate ? evaluator(initialText) : '');
    const [lines, setLines] = useState(countLines(initialText));
    const [height, setHeight] = useState(0);

    const inputRef = useRef();

    useEffect(() => {
        if (inputRef.current) {
            handleChange({ target: inputRef.current });
        }
    }, [inputRef]);

    const handleKeyDown = e => {
        // If the tab key was pressed insert the appropriate number of spaces
        if (e.keyCode === TAB_KEY) {
            const value    = e.target.value;
            const start    = e.target.selectionStart;
            const end      = e.target.selectionEnd;
            const startStr = value.substring(0, start);
            const spaces   = spacesToTab(startStr);
            e.target.value = startStr + ' '.repeat(spaces) + value.substring(end);
            e.target.selectionStart += spaces; 
            e.preventDefault();
        }
    };

    const handleChange = e => {
        const value      = e.target.value;
        const lines      = countLines(value);
        const lineHeight = parseInt(window.getComputedStyle(e.target).lineHeight);
        setLines(lines);
        setHeight((lines + 1) * lineHeight + 'px');
        setText(value);
    };

    const handleClick = () => {
        setRefresh(true);
        setOutput(evaluator(text));
        setTimeout(() => setRefresh(false)); 
    };
    
    return <div className='editor'>
        <div className='code' data-lang={language}>
            {!nolines && <div className='gutter'>
                {_.range(lines).map(i => (
                    <span key={i} className='line-number'>{i + 1}</span>    
                ))}
            </div>}
            <div className='text'>
                {readonly 
                    ? hljs.getLanguage(language)
                        ? <pre dangerouslySetInnerHTML={{ __html: hljs.highlight(language, text).value }} />
                        : <pre>{text}</pre>
                    : <textarea 
                        value={text}
                        placeholder={placeholder} 
                        onKeyDown={handleKeyDown} 
                        onChange={handleChange}
                        style={{ height }}
                        ref={inputRef}
                    />
                }
            </div>
        </div>
        {!nooutput && <div className='output'>
            <a onClick={handleClick} className='subtle-accent clr-text'><i className='fas fa-play fa-lg'></i></a>
            <pre className={refresh ? 'text refresh' : 'text'}>{output}</pre>
        </div>}
    </div>;
};