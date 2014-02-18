/**
 * Created with PyCharm.
 * User: henryadam
 * Date: 2/16/14
 * Time: 1:37 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {
    boxes = $('.well');
    maxHeight = Math.max.apply(
        Math, boxes.map(function () {
            return $(this).height();
        }).get());
    boxes.height(maxHeight);

    var the_board = ['','','','','','','','',''];

    $("[id^='cell']").each(function(index,value){
        if ($(value).children().html() == "None") $(this).children().html('');
    });

    $("[id^='cell']").on("click",function(e){
        //here we build the board from the cell
        $(this).children().html('O')
        var x = $("[id^='cell']").map(function(){return $(this).children().html()}).get().slice();
        $.each(x,function(index, value){
            if (!value.length || value == "None") x[index] = null
        });
        console.log(x);
        s = '/?board=' + JSON.stringify(x);
        window.location = s;

    });

});
