    $(document).ready(function() {
        
        var turn = 0;
        var board = '_________';
        var team = ['x', 'o'];
        var send = "";
        
        function strIns(s, index) { return s.substring(0,index) + team[turn%2] + s.substring(index+1); }
        
        
        function update(send){
            if(turn <= 1){
                jQuery('#cpuGo').fadeOut(350);
            }
            jQuery.getJSON(send, function(data) {
                
                var nextMarker = data.nextMarker;
                var winner = data.winner;
                var gameOver = data.complete;
                var next = data.next;
                
                var selectString = '#' + nextMarker + next ;
                var moveString = '#hb' + next;
                jQuery(moveString).css('z-index', '-5');
                jQuery(selectString).css('z-index', '5');
                board = strIns(board, next);
                turn++;
                if(turn == 9){
                    update('/ttt/move/' + board +'/' + team[turn%2]);
                }
                else if( gameOver == true ){
                    jQuery('#results').html("<h1> Game over!</h1>");
                    if( winner != "" ){
                        jQuery('#results').html("<h1> We have a winner: " + winner + "</h1>");
                    }
                }
            });
        }

        $('#cpuGo').click( function(){
            send = '/ttt/move/' + board +'/' + team[turn%2] ;
            update(send);

        });

        $('#hb0').click( function(){
            $(this).css('z-index', '-5');
            board = strIns(board, 0);
            if( turn%2 == 0 ){
                
                jQuery('#x0').css('z-index', '5')    
            }else{
                jQuery('#o0').css('z-index', '5')   
            }
            turn++;
            send = '/ttt/move/' + board + '/' + team[turn%2] ;
            /* Block here */
            update(send);

        });
        $('#hb1').click( function(){
            $(this).css('z-index', '-5');
            board = strIns(board, 1);
            if( turn%2 == 0 ){
                jQuery('#x1').css('z-index', '5')    
            }else{
                jQuery('#o1').css('z-index', '5')   
            }
            turn++;
            send = '/ttt/move/' + board + '/' + team[turn%2] ;
            update(send);
            
        });
        $('#hb2').click( function(){
            $(this).css('z-index', '-5');
            board = strIns(board, 2);
            if( turn%2 == 0 ){
                jQuery('#x2').css('z-index', '5')    
            }else{
                jQuery('#o2').css('z-index', '5')   
            }
            turn++;
            send = '/ttt/move/' + board + '/' + team[turn%2] ;
            update(send);
        });
        $('#hb3').click( function(){
            $(this).css('z-index', '-5');
            board = strIns(board, 3);
            if( turn%2 == 0 ){
                jQuery('#x3').css('z-index', '5')    
            }else{
                jQuery('#o3').css('z-index', '5')   
            }
            turn++;
            send = '/ttt/move/' + board + '/' + team[turn%2] ;
            update(send);
        });
        $('#hb4').click( function(){
            $(this).css('z-index', '-5');
            board = strIns(board, 4);
            if( turn%2 == 0 ){
                jQuery('#x4').css('z-index', '5')    
            }else{
                jQuery('#o4').css('z-index', '5')   
            }
            turn++;
            send = '/ttt/move/' + board + '/' + team[turn%2] ;
            update(send);
        });
        $('#hb5').click( function(){
            $(this).css('z-index', '-5');
            board = strIns(board, 5);
            if( turn%2 == 0 ){
                jQuery('#x5').css('z-index', '5')    
            }else{
                jQuery('#o5').css('z-index', '5')   
            }
            turn++;
            send = '/ttt/move/' + board + '/' + team[turn%2] ;
            update(send);
        });
        $('#hb6').click( function(){
            $(this).css('z-index', '-5');
            board = strIns(board, 6);
            if( turn%2 == 0 ){
                jQuery('#x6').css('z-index', '5')    
            }else{
                jQuery('#o6').css('z-index', '5')   
            }
            turn++;
            send = '/ttt/move/' + board + '/' + team[turn%2] ;
            update(send);
        });
        $('#hb7').click( function(){
            $(this).css('z-index', '-5');
            board = strIns(board, 7);
            if( turn%2 == 0 ){
                jQuery('#x7').css('z-index', '5')    
            }else{
                jQuery('#o7').css('z-index', '5')   
            }
            turn++;
            send = '/ttt/move/' + board + '/' + team[turn%2] ;
            update(send);
        });
        $('#hb8').click( function(){
            $(this).css('z-index', '-5');
            board = strIns(board, 8);
            if( turn%2 == 0 ){
                jQuery('#x8').css('z-index', '5')    
            }else{
                jQuery('#o8').css('z-index', '5')   
            }
            turn++;
            send = '/ttt/move/' + board + '/' + team[turn%2] ;
            update(send);
        });

    });
