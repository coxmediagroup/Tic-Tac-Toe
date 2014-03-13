from tic_tac_toe.models import Game

def get_game(request):
    # get our game
    game_id = request.session.get('game_id')

    if game_id != None: # if we found a game id in the session
        try:
            # try to load the game in the session
            game = Game.objects.get(pk=game_id)
        except ObjectDoesNotExist:
            # if we can't load it, pretend we never saw the id
            game_id = None

    if game_id == None:
        # if we don't have a game yet, create one and store it
        game = Game()
        game.setup_new_game()
        request.session['game_id'] = game.id

    return game

def _get_player_of_type(game, is_ai):
    if game.player_one.is_ai == is_ai:
        return game.player_one
    return game.player_two
def get_human_player(game):
    return _get_player_of_type(game, False)
def get_ai_player(game):
    return _get_player_of_type(game, True)
