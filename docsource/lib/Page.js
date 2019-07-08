import _ from 'lodash';

const MAX_PREVIEWS = 3;

export default class Page {

    constructor(data) {
        Object.assign(this, data);
        if (this.date) {
            const [month, day, year] = this.date.split('-');
            this.date = new Date(
                parseInt(year, 10), 
                parseInt(month, 10) - 1,
                parseInt(day, 10),
            );
        }
    }

    $search(searchText) {
        const regex = new RegExp(_.escapeRegExp(_.escape(searchText)), 'i');
        return this.$searchRegex(regex);
    }

    $searchRegex(regex) {
        if (this.title && regex.test(this.title)) {
            return true;
        }
        if (this.subtitle && regex.test(this.subtitle)) {
            return true;
        }
        if (this.$formattedDate && regex.test(this.$formattedDate)) {
            return true;
        }
        if (this.plainTxt && regex.test(this.plainTxt)) {
            return true;
        }
        return false;
    }

    $previews(searchText) {
        const regex    = new RegExp(`(${_.escapeRegExp(_.escape(searchText))})`, 'gi');
        const lines    = [this.title || '', this.subtitle || '', this.$formattedDate || '', ...this.plainTxt.split('\n')];
        const previews = [];

        for (const line of lines) {
            if (regex.test(line)) {
                previews.push(<span dangerouslySetInnerHTML={{
                    __html: line.replace(regex, `<mark>$1</mark>`) + '...',
                }} />)
                if (previews.length === MAX_PREVIEWS) {
                    previews.push(<span dangerouslySetInnerHTML={{
                        __html: '<i>Some results have been hidden</i>.',
                    }} />);
                    break;
                }
            }
        }
        return previews;
    }

    get $day() {
        if (this.date) {
            return this.date.getUTCDate();
        };
    }

    get $month() {
        if (this.date) {
            return this.date.getUTCMonth();
        }
    }

    get $year() {
        if (this.date) {
            return this.date.getUTCFullYear();
        }
    }

    get $formattedDate() {
        const months = [
            'January', 
            'February', 
            'March', 
            'April', 
            'May', 
            'June', 
            'July', 
            'August', 
            'September', 
            'October', 
            'November', 
            'December',
        ];
        if (isNaN(this.$month) || isNaN(this.$day) || isNaN(this.$year)) {
            return false;
        }
        return `${months[this.$month]} ${this.$day} ${this.$year}`;
    }

}

Page.compareDates = (page1, page2) => {
    return page2.date - page1.date;
};