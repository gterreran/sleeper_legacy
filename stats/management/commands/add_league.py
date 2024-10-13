from django.core.management.base import BaseCommand
from stats.bin.db_add import add_league

class Command(BaseCommand):
    help = 'Add a new league to the database.'

    def add_arguments(self, parser):
        parser.add_argument("league_nickname",
                            help="Nickname of the league to add.", type=str)

    def handle(self, *args, **options):
        add_league(league_nickname = options["league_nickname"], output = self.stdout)

