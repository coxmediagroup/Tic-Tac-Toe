function updateGame(board, reporter) {
    $.ajax({type: 'POST', url: '/api/v2/play', dataType: 'json', data: JSON.stringify(board.read()), processData: false, beforeSend: function () {
        board.disable();
        reporter.think();
    }, success: function (data, status, jqxhr) {
        board.write(data.data);
        reporter.updateStatus(data.data.status);
        if (data.data.status == 'active') {
            board.enable();
        }
    }});
}

$(document).ready(function () {
    alert('started');
    $('.space').hover(function () {
        console.log($(this).children('i'));
    });
    $('.space').click(function () {
        conole.log($(this).children('i'));
    });
});