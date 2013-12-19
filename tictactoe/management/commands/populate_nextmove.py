from django.core.management.base import BaseCommand, CommandError

from ...models import NextMove, Position


class Command(BaseCommand):
    args = ''
    help = ("Populates the database with the information the AI needs"
            " to make its next move.")

    def handle(self, *args, **options):
        self.table = {}

        self._visit(' '*9)

        for state, dct in self.table.iteritems():
            if ' ' not in state: # ditch the draw positions,
                continue         # we want playable ones
            r, c, player = dct['move']
            NextMove.objects.create(state=state, row=r, column=c)

    def _visit(self, position):
        self.table[position] = {'result': None, 'move': None, 'ratio': None}
        player = 'ox'[position.count(' ') % 2]

        plays = [(r, c) for r in xrange(3)
                 for c in xrange(3)
                 if position[3*r + c] == ' ']

        if not plays:
            self.table[position].update(result='draw', ratio=0.0)
            return

        play_mapping, child_mapping = {}, {}
        wins = 0
        for r, c in plays:
            found = False
            result = Position._play(position, (r, c, player))
            play_mapping[result] = (r, c, player)
            for child in Position.expand_symmetry(result):
                if child in self.table:
                    child_mapping[result] = child
                    result = child
                    wins += 1 if self.table[child]['result'] == player else 0
                    found = True
                    break

            if Position._is_won(result):
                self.table[position].update(result=player, move=(r, c, player),
                                            ratio=1.0)
                return

            if found:
                continue

            child_mapping[result] = result
            self._visit(result)
            wins += 1 if self.table[result]['result'] == player else 0

        self.table[position]['ratio'] = wins / len(play_mapping)

        ratio, move, pos = min((self.table[child_mapping[p]]['ratio'], m, p)
                               for p, m in play_mapping.iteritems())
        self.table[position].update(
            result=self.table[child_mapping[pos]]['result'], move=move)
