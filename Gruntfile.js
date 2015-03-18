module.exports = function(grunt){

    grunt.registerTask('default', ['build']);
    grunt.registerTask('lint', ['jshint', 'csslint']);
    grunt.registerTask('build', ['lint', 'uglify']);
};