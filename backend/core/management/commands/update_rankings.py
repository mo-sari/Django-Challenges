from django.core.management import BaseCommand
from users.models import User
from django_redis import get_redis_connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        con = get_redis_connection("default")

        ambassadors = User.objects.filter(is_ambassador=True)

        for ambassador in ambassadors:
            print(ambassador.name, float(ambassador.revenue))
            con.zadd('rankings',
                     {ambassador.name: float(ambassador.revenue)})
