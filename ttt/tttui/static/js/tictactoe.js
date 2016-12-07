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
  var cell_coord_map = {
    '00': 'upper_left',
    '10': 'upper_center',
    '20': 'upper_right',
    '01': 'center_left',
    '11': 'center',
    '21': 'center_right',
    '02': 'lower_left',
    '12': 'lower_center',
    '22': 'lower_right'
  };
  var cell_name_map = {
    'upper_left': '00',
    'upper_center': '10',
    'upper_right': '20',
    'center_left': '01',
    'center': '11',
    'center_right': '21',
    'lower_left': '02',
    'lower_center': '12',
    'lower_right': '22'
  };
  $('.ttt_new').click(function(e) {
      e.preventDefault();
      $.post('/api/v1/game/', '{}', null, 'json').done(function(obj) {
          var uri = obj.resource_uri.split('/');
          var game = uri[uri.length - 2];
          window.location.assign('/' + game);
      }).fail(function() {
          alert('oops');
      });
  });
  $('.ttt_board').each(function(index, board) {
    board = $(board);
    var game_id = board.children('#ttt_game_id')[0].value;
    var player = board.children('#ttt_player')[0].value;
    if(player === "1") {
      player = 'x';
    } else {
      player = 'o';
    }
    var player_token = player.toUpperCase();
    board.children('.ttt_cell').click(function(event) {
      var source = $(event.target);
      if(source.hasClass('ttt_x') || source.hasClass('ttt_o') || source.hasClass('ttt_done')) return;
      var id = source[0].id.slice(-2);
      var cell = cell_coord_map[id];

      var data = {};

      if(player === 'x') {
          data[cell] = 1;
      } else {
          data[cell] = -1;
      }
    
      url = '/api/v1/game/' + game_id + '/';
      $.ajax({
        'url': url,
        'type': 'POST',
        'headers': {"X-HTTP-Method-Override": "PATCH"},
        'data': JSON.stringify(data),
        'dataType': 'json',
        'success': function(content, response) {
            var isEnded = (content.ended !== null);
            for(var cell in content.board) {
              var $cell = $('#ttt_cell_' + cell_name_map[cell]);
              if(isEnded) $cell.addClass('ttt_done');
              if(content.board[cell] === 1) {
                 $cell.addClass('ttt_x');
                 $cell.children('span').text('X');
              } else if(content.board[cell] === -1) {
                 $cell.addClass('ttt_o');
                 $cell.children('span').text('O');
              }
            }
            if(isEnded) {
                board.children('.ttt_cell').addClass('ttt_done');
                $('.ttt_new').show();
            }
        },
        'error': function() {
            alert('Something bad happened');
        }
      }); //end ajax
    }); // end board children
  }); // end board
});


