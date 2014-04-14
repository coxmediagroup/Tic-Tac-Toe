$(document).ready(function(){
    
    $('.active_cell').one('click',function(){
        submitCell();
    });

    setupButtons();

    function setupButtons(){
        $('#goFirst, #goSecond').on('click',function(e){
            e.preventDefault();
            loading();
            var data = {};
            data[$(this).prop('name')] = true;
            $('#goFirst, #goSecond').remove();
            $('#play_header > h2').text('Make your move');
            $.ajax({
                url : '/play/',
                type : 'GET',
                dataType : 'html',
                data : data,
            }).done(function(data){
                $('#ticForm tbody').html(data);
                $('.active_cell').one('click',submitCell)
                finishLoading();
            }).fail(function(jqXHR,textStatus,errorThrown){
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            });
        });
    };

    function submitCell(data){
        loading();
        $(this).find('input').val('2');
        var data = $('#ticForm').serialize();
        $('.active_cell').off('click');
        $.ajax({
            url : '/play/',
            type : 'POST',
            dataType : 'html',
            data : data,
        }).done(function(data){
            if($(data).filter('#play_header').length){
                $('#play_header').replaceWith($(data).filter('#play_header'));
                setupButtons();
            }
            $('#ticForm tbody').html($(data).filter('#trs').find('tr'));
            $('.active_cell').one('click',submitCell)
            finishLoading();
        }).fail(function(jqXHR,textStatus,errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        });
    };

    function loading(){
        var d = $('<div/>',{'id':'loading'}).append($('<img />',{'src':'/static/game/img/ajax-loader.gif'}));
        d.append(' Thinking...');
        $('#table_div').prepend(d);
    };

    function finishLoading(){
        $('#loading').remove();
    };

});