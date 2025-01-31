from api.models import Comments, Posts
from django.db.models import Count
from django.db import connection
from pprint import pprint


def run():
    #  Retrieve posts that have at least one comment with specific keywords in their content.
    # sql queries
    # first solution
    # select posts.caption, posts.id, comments.contents
    # from posts
    # join comments on posts.id = comments.post_id
    # where comments.contents like '%Earum%'

    # second solution
    # with outputtable as(
    #     select *
    #     from posts
    #     join comments on posts.id = comments.post_id
    #     )
    # select count(*)
    # from outputtable
    # where outputtable.contents like '%Earum%'

    # django orm query
    # posts = Posts.objects.prefetch_related('comments_set') \
    #                      .filter(comments__contents__icontains='Earum') \
    #                      .distinct()

    # print(len(posts))
    # print(connection.queries)

    # raw sql in django
    query = """
    select posts.caption, posts.id, comments.contents
    from posts
    join comments on posts.id = comments.post_id
    where comments.contents like %s
    """
    with connection.cursor() as coursor:
        coursor.execute(query, ["%Earum%"])
        result = coursor.fetchall()

    print(len(result))
