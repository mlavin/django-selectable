/*global module:false*/
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    qunit: {
      urls: [
        'http://localhost:<%= server.port %>/selectable/tests/qunit/index.html?jquery=1.10.1&ui=1.10.3',
        'http://localhost:<%= server.port %>/selectable/tests/qunit/index.html?jquery=1.9.1&ui=1.10.3',
        'http://localhost:<%= server.port %>/selectable/tests/qunit/index.html?jquery=1.8.3&ui=1.9.2',
        'http://localhost:<%= server.port %>/selectable/tests/qunit/index.html?jquery=1.7.2&ui=1.8.24',
        'http://localhost:<%= server.port %>/selectable/tests/qunit/index.html?jquery=1.6.4&ui=1.8.24'
      ]
    },
    lint: {
      files: ['selectable/static/selectable/js/*.js']
    },
    watch: {
      files: '<config:lint.files>',
      tasks: 'lint qunit'
    },
    jshint: {
      options: {
        curly: true,
        eqeqeq: true,
        immed: true,
        latedef: true,
        newcap: true,
        noarg: true,
        sub: true,
        undef: true,
        boss: true,
        eqnull: true,
        browser: true,
        undef: true,
        trailing: true,
        indent: 4
      },
      globals: {
        jQuery: true,
        // Django admin globals
        django: true,
        dismissAddAnotherPopup: true,
        windowname_to_id: true,
        html_unescape: true,
        // Optional globals
        djselectableAdminPatch: true,
        djselectableAutoLoad: true,
        // Grappelli namespace
        grp: true
      }
    },
    server: {
      port: 8085
    },
  });

  // Default task.
  grunt.registerTask('default', 'server lint qunit');

};
