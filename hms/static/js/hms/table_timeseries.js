const CONFIG = [
    {
        "value": "yearly",
        "text": "년 별",
        "checked": false,
        "standard": [1]
    },
    {
        "value": "halfly",
        "text": "반기 별",
        "checked": false,
        "standard": [1, 6]
    },
    {
        "value": "quarterly",
        "text": "분기 별",
        "checked": false,
        "standard": [1, 4, 7, 10]
    },
    {
        "value": "monthly",
        "text": "월 별",
        "checked": true,
        "standard": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }
];

class Timeseries {
    constructor() {
        this.config = {}
    }


}