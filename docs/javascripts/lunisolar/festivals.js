import lunisolar from './lunisolar.esm.js';

const yearEve = `12,${lunisolar().lunar.isBigMonth ? 30 : 29}`;

const festivals = [
{
    format: 'MMDD', // 公历
    markers: {
    '0101': { tag: '节日', name: '元旦节' },
    '0214': { tag: '节日', name: '情人节' },
    '0308': { tag: '节日', name: '妇女节' },
    '0401': { tag: '节日', name: '愚人节' },
    '0501': { tag: '节日', name: '国际劳动节' },
    '0601': { tag: '节日', name: '儿童节' },
    '0701': { tag: '纪念日', name: '建党节' },
    '0801': { tag: '节日', name: '建军节' },
    '0910': { tag: '节日', name: '教师节' },
    '1001': { tag: '节日', name: '国庆节' },
    '1024': { tag: '节日', name: '程序员节' },
    '1101': { tag: '节日', name: '万圣节' },
    '1224': { tag: '节日', name: '平安夜' },
    '1225': { tag: '节日', name: '圣诞节' }
    }
}, {
    format: 'lMn,lDn',  // 农历
    markers: {
    '1,1': { tag: '节日', name: '春节' },
    '1,15': { tag: '节日', name: '元宵节' },
    '2,2': { tag: '节日', name: '龙抬头' },
    '5,5': { tag: '节日', name: '端午节' },
    '7,7': { tag: '节日', name: '七夕节' },
    '7,14': { tag: '节日', name: '中元节' },
    '7,18': {tar: '节日', name: '站主生日'},
    '8,15': { tag: '节日', name: '中秋节' },
    '9,9': { tag: '节日', name: '重阳节' },
    '12,8': { tag: '节日', name: '腊八节' },
    [yearEve]: { tag: '节日', name: '除夕' }
    }
}, {
    format: 'M,d,dR',   // 相对日期：公历月的第几个星期几
    markers: {
    '5,0,2': { tag: '节日', name: '母亲节' },
    '6,0,3': { tag: '节日', name: '父亲节' },
    '11,4,4': { tag: '节日', name: '感恩节' },
    }
} ];

export { festivals };