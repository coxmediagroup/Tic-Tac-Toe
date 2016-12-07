//waits for required layers, then requires the agx.currentPage resource, which
//in turn calls the generated javascript on the page
if(!agx.currentPage)agx.currentPage={};
agx.currentPage.waiter = agx.wait_for_events([],
    function(){
        dojo.require('ag.controllers.TicTacToe');

        dojo.addOnLoad(function(){
            controller = new ag.controllers.TicTacToe(agx.currentPage);
            agx.currentPage.controller = controller;
        });
    }
);
