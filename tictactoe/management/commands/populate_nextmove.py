from django.core.management.base import BaseCommand, CommandError

from ...models import NextMove, Position


class Command(BaseCommand):
    args = ''
    help = ("Populates the database with the information the AI needs"
            " to make its next move.")

    def handle(self, *args, **options):
        self.table = {}

        # recursively find the reachable positions, collapsing down
        # the positions that are effectively the same due to symmetry
        self._visit(' '*9)

        self.stdout.write(
            "{0} essentially different positions found.".format(
                len(self.table)))

        # clear out any old ones that were in the db
        NextMove.objects.all().delete()

        for state, dct in self.table.iteritems():
            if dct['move'] is None: # ditch the endgame positions,
                continue            # we want playable ones
            r, c, player = dct['move']
            NextMove.objects.create(state=state, row=r, column=c)

    def _visit(self, position):
        # result: 'x', 'o', or 'draw'
        # move: (r, c, player) where player is 'x' or 'o'
        # losses: the number of losing moves for this position for this player
        self.table[position] = {'result': None, 'move': None, 'losses': None}

        player, other = ('x', 'o') if position.count(' ') % 2 else ('o', 'x')

        if Position._is_won(position):
            # a position that is won will always be due to the move of
            # the previous player, so this position is maximally bad
            # for the current player
            self.table[position].update(result=other, losses=9)
            return

        plays = [(r, c) for r in xrange(3)
                 for c in xrange(3)
                 if position[3*r + c] == ' ']

        if not plays:
            # this position is ok for the current player, since it
            # isn't an outright loss, and there is no more trouble we
            # can get into
            self.table[position].update(result='draw', losses=0)
            return

        play_mapping, child_mapping = {}, {}
        losses = 0
        for r, c in plays:
            found = False
            result = Position._play(position, (r, c, player))

            # for a raw result position, which move was used
            play_mapping[result] = (r, c, player)

            # for a given raw position, which symmetric equivalent can
            # be found in the table
            child_mapping[result] = result

            for child in Position.expand_symmetry(result):
                if child in self.table:
                    child_mapping[result] = child
                    if self.table[child]['result'] == other:
                        losses += 1
                    found = True
                    break

            if found:
                continue

            self._visit(result)
            if self.table[result]['result'] == other:
                losses += 1

        # We want to choose the move that maximizes the number of losing
        # moves available to the other player.
        L, move, pos = max((self.table[child_mapping[p]]['losses'], m, p)
                           for p, m in play_mapping.iteritems())

        self.table[position].update(
            result=self.table[child_mapping[pos]]['result'],
            losses=losses, move=move
        )
