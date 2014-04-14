$(document).ready(function(){
    
    $('.active_cell').one('click',function(){
        submitCell();
    });

    $('#goFirst, #goSecond').on('click',function(e){
        e.preventDefault();
        var data = {};
        data[$(this).prop('name')] = true;
        $('#goFirst, #goSecond').remove();
        $('#play_header').text('Make your move');
        $.ajax({
            url : '/play/',
            type : 'GET',
            dataType : 'html',
            data : data,
        }).done(function(data){
            $('#ticForm tbody').html(data);
            $('.active_cell').one('click',submitCell)
        }).fail(function(jqXHR,textStatus,errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        });
    });

    function submitCell(data){
        $(this).find('input').val('2');
        var data = $('#ticForm').serialize();
        $('.active_cell').off('click');
        $.ajax({
            url : '/play/',
            type : 'POST',
            dataType : 'html',
            data : data,
        }).done(function(data){
            $('#ticForm tbody').html(data);
            $('.active_cell').one('click',submitCell)
        }).fail(function(jqXHR,textStatus,errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        });
    };

});