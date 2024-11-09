from django.core.management.base import BaseCommand
from stats.bin.db_add import add_season, add_week


class Command(BaseCommand):
    help = 'Add season to a league.'

    def add_arguments(self, parser):
        parser.add_argument("season_id",
                            help="Sleeper season_id.",
                            type=int)
        parser.add_argument("--league",
                            help="League to add the season to.",
                            required=True, type=str)
        parser.add_argument("--no_matchups",
                            help="Do not fetch all the weekly metchups.",
                            default=0, action='store_true')

    def handle(self, *args, **options):
        add_season(
            season_id=options["season_id"],
            league_nickname=options["league"],
            output=self.stdout)
        if not options["no_matchups"]:
            add_week(
                week_list=[
                    el for el in range(
                        1,
                        19)],
                season_id=options["season_id"],
                output=self.stdout)
