from django.db import models, transaction

import re

from . import validators

WINNING_SEQUENCES = (
    # row wins
    ('A1', 'B1', 'C1'),
    ('A2', 'B2', 'C2'),
    ('A3', 'B3', 'C3'),

    # col wins
    ('A1', 'A2', 'A3'),
    ('B1', 'B2', 'B3'),
    ('C1', 'C2', 'C3'),

    # diagonal wins
    ('A1', 'B2', 'C3'),
    ('A3', 'B2', 'C1')
)


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player = models.CharField(max_length=1, validators=[validators.is_x_or_o])
    ip = models.GenericIPAddressField()
    winner = models.CharField(max_length=1, blank=True, validators=[validators.is_x_or_o])


    @staticmethod
    @transaction.commit_on_success
    def create_or_append(pk, ip, player, so_far):
        try:
            if not pk:
                raise Game.DoesNotExist
                
            gmodel = Game.objects.get(pk=pk)
            ml = gmodel.move_list()
            if ml == so_far:
                return gmodel
            elif so_far.startswith(ml):
                so_far = so_far.split('-')
                ml = ml.split('-')
                while len(ml) < len(so_far):
                    gmodel.moves.create(cell=so_far[len(ml)])
                    ml.append(so_far[len(ml)])
                return gmodel
            else:
                raise Game.DoesNotExist

        except Game.DoesNotExist:
            gmodel = Game(ip=ip, player=player  )
            gmodel.save()
            so_far = so_far.split('-')
            for c in so_far:
                gmodel.moves.create(cell=c)
            return gmodel

    def move_list(self):
        return '-'.join([m.cell for m in self.moves.all()])


    def find_winner(self):
        board = {}

        player = 'X'
        for move in self.moves.all():
            board[move.cell] = player
            player = 'O' if player == 'X' else 'X'

        for player in 'XO':
            for seq in WINNING_SEQUENCES:
                count = 0
                for c in seq:
                    if board.get(c) == player:
                        count += 1

                if count == 3:
                    return player

        used = 0
        if len(board) == 9 and '' not in board.values():
            return 'D'


        return ''


class Move(models.Model):
    class Meta:
        unique_together = (('game', 'cell'),)
        ordering = ['created']
    created = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, related_name='moves')
    cell = models.CharField(max_length=2, validators=[validators.is_cell])

    def save(self, *args, **kwargs):
        ret = super(Move, self).save(*args, **kwargs)
        self.game.winner = self.game.find_winner()
        self.game.save()
        return ret
