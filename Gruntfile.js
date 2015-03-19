module.exports = function(grunt){

    grunt.initConfig({
        jshint: {
            files: [
                'client/app/*.js',
                'client/app/**/*.js',
                'client/shared/**/*.js'
            ]
        },
        csslint: {

        }
    });

    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-uglify');

    grunt.registerTask('default', ['build']);
    grunt.registerTask('lint', ['jshint', 'csslint']);
    grunt.registerTask('build', ['lint', 'uglify']);
};