// included from django doc on using jquery with django's csrf protection
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

// my code
$(function() {
  $('.ttt_board').each(function(index, board) {
    board = $(board);
    var game_id = board.children('#ttt_game_id')[0].value;
    var player_token = board.children('#ttt_player')[0].value.toUpperCase();
    board.children('.ttt_cell').click(function(event) {
      var source = $(event.target);
      if(source.hasClass('ttt_x') || source.hasClass('ttt_o') || source.hasClass('ttt_done')) return;
      var id = source[0].id.slice(-2);
      var col = id.charAt(0);
      var row = id.charAt(1);
    
      url = window.location.href + 'move'
      $.ajax({
        'url': url,
        'type': 'POST',
        'data': { 'player':'x', 'col':col, 'row':row },
        'dataType': 'json',
        'success': function(content, response)
          {
            source[0].innerHTML = player_token;
            if(content['player'] !== '-')
            {
                var cell = $('#ttt_cell_' + content['col'] + content['row'])
                cell.addClass('ttt_' + content['player']);
                cell.innerHTML = content['player'].toUpperCase();
            }
          },
        'error': function()
          {
            alert('Something bad happened');
          }
        }); //end ajax
    }); // end board children
  }); // end board
});


