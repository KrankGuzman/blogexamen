from django.contrib.auth import models as auth_models
from . import models as app_models


# POST: QUERIES #
def get_posts():
    posts_list = list(app_models.Post.objects.all())
    return posts_list


def get_post_by_pk(pk):
    return app_models.Post.objects.get(pk)


def get_posts_by_user(user_pk):
    post_list = []
    user = app_models.User.objects.get(user_pk=user_pk)
    post_records = list(app_models.PostRecord.objects.get(user=user, action="CREATE"))
    for post_record in post_records:
        post_list.append(post_record.post)
    return post_list


def get_records():
    posts_list = list(app_models.PostRecord.objects.all())
    return posts_list


def get_records_of_post(post_pk):
    post = list(app_models.Post.objects.get(post_pk))
    records_list = list(app_models.PostRecord.get(post=post))
    return records_list


def get_tags_of_post(post_pk):
    tags_list = []
    tags = list(app_models.Tag.objects.get(pk=post_pk))
    for tag in tags:
        tags_list.append({tag.pk, tag.name})
    return tags_list


# TAGS: QUERIES #
def get_tags_choices():
    tags_list = []
    tags = list(app_models.Tag.objects.all())
    for tag in tags:
        tags_list.append({tag.pk, tag.name})
    return tags_list


def get_tag_by_pk(tag_pk):
    tag = app_models.Tag.objects.get(tag_pk=tag_pk)
    return tag
