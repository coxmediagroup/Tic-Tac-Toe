var $table, $comment, ai_player, player, losses = 0;
var winner, game_finished = false;
var url_play;
var taunting_strs = [" What's goining on? Maybe try harder.",
                     " Wow, that's embarrassing, maybe give up?",
                     " Yawn ... think I'm gonna take a nap."];

function get_state_from_table() {
    var state = '';
    $table.find("td").each(function (i, e) {
        if ($(e).hasClass('x'))
            state += 'x';
        else if ($(e).hasClass('o'))
            state += 'o';
        else
            state += 'e';
    });
    return state;
}

function set_state_to_table(state) {
    $table.find("td").each(function (i, e) {
        $(e).removeClass("x o e X O");
        $(e).addClass(state[i]);
    });
}

function reset_table() {
    $table.removeClass("locked");
    set_state_to_table("eeeeeeeee");
    $comment.text("You are playing as " + player.toUpperCase());
    game_finished = false;
    winner = false;
    if (ai_player == 'x')
        make_next_ai_play(true);
}

function update_game_finished() {
    if ($table.find(".X").length) {
        game_finished = true;
        winner = 'x';
        return true;
    }
    if ($table.find(".O").length) {
        game_finished = true;
        winner = 'o';
        return true;
    }
    if (!$table.find(".e").length) {
        game_finished = true;
        winner = false;
        return true;
    }
    return false;
}

function set_player(to_player) {
    player = to_player;
    ai_player = player=='o' ? 'x': 'o';
    reset_table();
}

function make_next_ai_play(empty) {
    state = empty ? '': get_state_from_table();
    $table.addClass('locked');

    $.getJSON(url_play, {state: state,
                         ai_player: ai_player},
              function (data) {
                  set_state_to_table(data.state);
                  $table.removeClass("locked");
                  update_game_finished();
                  if (game_finished) {
                      if (winner == ai_player) {
                          increment_losses();
                          $comment.text("You lost!");
                      } else if (winner == player) {
                          $comment.text("Oops! You Won! That wasn't supposed to happen.");
                      } else {
                          $comment.text("It's a draw!");
                      }
                  }
              });
}

function increment_losses() {
    losses += 1;
    var taunting = losses;
    if (losses > 10)
        taunting += " Wow, that's a lot of losses. Just stop!"
    else if (losses%2 == 0)
        taunting += taunting_strs[(Math.floor(losses/2)-1)%taunting_strs.length];
    $("#losses").text(taunting);
}
