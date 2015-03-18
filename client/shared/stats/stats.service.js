'use strict';

/*
 * Statistics object returned by factory service
 * Using a factory allow private variables and methods and doesn't require the use of 'this' similar to the revealing module pattern
 * Since services are singletons, they are persisted throughout the life of the app
 */

angular.module('tictactoe')
    .factory('Stats', function(){
        var module,
            stats = [];

        // expect obj to be of form:
        // { winner: player|ai|tie }
        function addStats(obj){
            stats.push[obj];
        }

        // return stats for controller to handle
        function getStats(){
            return stats;
        }

        module = {
            addStats: addStats,
            getStats: getStats
        };

        /* return public api */
        return module;
    });