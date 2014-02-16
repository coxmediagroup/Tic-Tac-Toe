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

});
