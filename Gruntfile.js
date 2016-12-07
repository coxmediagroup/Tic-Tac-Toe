module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jshint: {
      files: {
        src: ['tictactoe/board/static/js/**.js']
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');

};
