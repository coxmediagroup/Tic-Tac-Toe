    $(document).ready(function() {
        
        var turn = 0;
        
        
        
        $('#hb0').click( function(){
            $(this).css('z-index', '-5');
            if( turn%2 == 0 ){
                jQuery('#x0').css('z-index', '5')    
            }else{
                jQuery('#o0').css('z-index', '5')   
            }
            turn++;
        });
        $('#hb1').click( function(){
            $(this).css('z-index', '-5');
            if( turn%2 == 0 ){
                jQuery('#x1').css('z-index', '5')    
            }else{
                jQuery('#o1').css('z-index', '5')   
            }
            turn++;
        });
        $('#hb2').click( function(){
            $(this).css('z-index', '-5');
            if( turn%2 == 0 ){
                jQuery('#x2').css('z-index', '5')    
            }else{
                jQuery('#o2').css('z-index', '5')   
            }
            turn++;
        });
        $('#hb3').click( function(){
            $(this).css('z-index', '-5');
            if( turn%2 == 0 ){
                jQuery('#x3').css('z-index', '5')    
            }else{
                jQuery('#o3').css('z-index', '5')   
            }
            turn++;
        });
        $('#hb4').click( function(){
            $(this).css('z-index', '-5');
            if( turn%2 == 0 ){
                jQuery('#x4').css('z-index', '5')    
            }else{
                jQuery('#o4').css('z-index', '5')   
            }
            turn++;
        });
        $('#hb5').click( function(){
            $(this).css('z-index', '-5');
            if( turn%2 == 0 ){
                jQuery('#x5').css('z-index', '5')    
            }else{
                jQuery('#o5').css('z-index', '5')   
            }
            turn++;
        });
        $('#hb6').click( function(){
            $(this).css('z-index', '-5');
            if( turn%2 == 0 ){
                jQuery('#x6').css('z-index', '5')    
            }else{
                jQuery('#o6').css('z-index', '5')   
            }
            turn++;
        });
        $('#hb7').click( function(){
            $(this).css('z-index', '-5');
            if( turn%2 == 0 ){
                jQuery('#x7').css('z-index', '5')    
            }else{
                jQuery('#o7').css('z-index', '5')   
            }
            turn++;
        });
        $('#hb8').click( function(){
            $(this).css('z-index', '-5');
            if( turn%2 == 0 ){
                jQuery('#x8').css('z-index', '5')    
            }else{
                jQuery('#o8').css('z-index', '5')   
            }
            turn++;
        });

    });
