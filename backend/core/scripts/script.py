from api.models import Comments, Posts
from django.db.models import Count


def run():
    # Find the posts with the most comments and sort them by creation date.
    posts = Posts.objects.prefetch_related('comments_set') \
                        .annotate(comment_count=Count('comments')) \
                        .order_by('-comment_count')[:10]

    for post in posts:
        print(post.caption, post.comment_count, end='\n')
