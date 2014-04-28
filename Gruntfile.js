/*jslint node:true */
"use strict";

var env = (process.env.NODE_ENV === 'production') ? 'production' : 'development';

// List of client side javascript libraries
var lib_js_list = [
    'static/js/libs/jquery/jquery-1.10.2.min.js',
    'static/js/libs/angular/angular.min.js'
];

// List of tic-tac-toe javascript files
var tictactoe_js_list = [
    'static/js/controllers/*.js'
];

var gruntConfig = {
    pkg: require('./package.json'),

    jshint: {
        options: {
            curly: true,
            laxbreak: true,
            es3: true,
            eqnull: true,
            browser: true,
            jquery: true
        },
        tictactoe_js: {
            src: ['static/js/controllers/*.js']
        }
    },

    uglify: {
        development: {
            options: {
                mangle: false,
                preserveComments: 'all',
                compress: false,
                beautify: true
            },
            files: {
                'static/js/tictactoe.dev.js': [lib_js_list, tictactoe_js_list]
            }
        },
        production: {
            options: {
                mangle: true,
                preserveComments: false,
                compress: {
                    unused: false
                }
            },
            files: {
                'static/js/tictactoe.min.js': [lib_js_list, tictactoe_js_list]
            }
        }
    },

    watch: {
        tictactoe_js: {
            files: [tictactoe_js_list],
            tasks: ['jshint:tictactoe_js']
        },
        compress_js: {
            files: [tictactoe_js_list],
            tasks: ['uglify']
        }
    }
};

// Keep just the right ENV
delete gruntConfig.uglify[env === 'production' ? 'development' : 'production'];

module.exports = function(grunt) {
    // Project configuration
    grunt.initConfig(gruntConfig);

    // Default task(s)
    grunt.registerTask('default', ['watch']);

    // Load the plugins
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('build', ['jshint:tictactoe_js', 'uglify']);
};
