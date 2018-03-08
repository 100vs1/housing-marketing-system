class HmsUtil {
    constructor() {

    }

    getCurrentDate() {
        return this.getCurrentYear() + '-' + this.getCurrentMonth() + '-' + this.getCurrentDay();
    }

    getCurrentYear() {
        let today = new Date();
        return today.getFullYear();
    }

    getCurrentMonth() {
        let today = new Date();
        return today.getMonth() + 1;
    }

    getCurrentDay() {
        let today = new Date();
        return today.getDate();
    }

    getYearFromStr(str) {
        str = str + '';

        return str.substring(0, 4);
    }

    getMonthFromStr(str) {
        str = str + '';

        return str.substring(4, 6);
    }

    getDateToKor(str, spacing) {
        str = str.toString();
        let spacing_val = '';

        if (spacing) {
            spacing_val = ' ';
        }
            
        if (str.length === 8 || str.length === 7) {
            return str.substring(0, 4) + '년' + spacing_val + str.substring(4, 6) + '월' + spacing_val + str.substring(6, 8) + '일';
        }
        
        if (str.length === 6) {
            return str.substring(0, 4) + '년' + spacing_val + str.substring(4, 6) + '월';
        }
        if (str.length === 4) {
            return str += '년';
        }

        return str;
    }

    getRandomHexColor() {
        let letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    setComma(str) {
        if (str) {
            let parts = str.toString().split(".");
            return parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",") + (parts[1] ? "." + parts[1] : "");
        } else {
            return null
        }
    }

    isNull(obj) {
        return !(typeof obj !== "undefined" && obj !== null && obj !== "");
    }

    getNullValue(obj, string) {
        if(this.isNull(obj)) {
            return string
        } else {
            return obj
        }
    }

    getTermArr(start, end, step) {
        let startLength = String(start).length;
        let endLength = String(start).length;

        start = Number(start);
        end = Number(end);

        let ret = [];
        if (startLength === 4 && endLength === 4) {
            let target = start;
            while(target <= end) {
                ret.push(target);
                target += step
            }

        } else if (startLength === 6 && endLength === 6){
            let target = start;
            while(target <= end) {
                ret.push(target);
                if (target % 100 === 12) {
                    target += 89;
                } else {
                    target += step
                }
            }
        } else {
            console.log("Error: Invalid Start, End Value")
        }

        return ret;
    }
}