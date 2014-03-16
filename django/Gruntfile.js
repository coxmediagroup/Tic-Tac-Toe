module.exports = function(grunt) {
  'use strict';

  var STATIC = 't3/static/t3/';
  var LESS = STATIC + 'less/';
  var JS = STATIC + 'js/';
  var COMPONENTS = STATIC + '/components/';

  grunt.initConfig({
    less: {
      dev: {
        options: {
          paths: [COMPONENTS + 'bootstrap/less']
        },
        files: {
          't3/static/t3/css/style.css': 't3/static/t3/less/style.less'
        }
      }
    },
    jshint: {
      files: {
        src: [JS + '**/*.js']
      },
      options: {
        jshintrc: true
      }
    },
    watch: {
      jshint: {
        files: [JS + '/**/*.js'],
        tasks: ['jshint']
      },
      less: {
        files: [LESS + '/*.less'],
        tasks: ['less']
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-jshint');

  grunt.registerTask('develop', ['watch']);
};
