$(document).ready(function(){
    
    $('.active_cell').one('click',submitCell)

    function submitCell(){
        $(this).find('input').val(2);
        var data = $('#ticForm').serialize();
        $('.active_cell').off('click')
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