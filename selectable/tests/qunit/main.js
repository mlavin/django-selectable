/*global require, QUnit*/

require.config({
    baseUrl: '../../static/selectable/js/',
    paths: {
        selectable: 'jquery.dj.selectable'
    },
    shim: {
        selectable: {
            exports: 'jQuery'
        }
    }
});

require(['test-methods.js', 'test-events.js', 'test-options.js'], function () {
    //Tests loaded, run Tests
    QUnit.load();
    QUnit.start();
});