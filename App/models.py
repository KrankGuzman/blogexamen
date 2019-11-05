from django.db import models
from django.contrib.auth.models import *

from . import choices as app_choices


class UserPicture(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	picture = models.ImageField(
		default="default_user_picture.png",
		null=True,
		blank=True,
	)


# POST #
class Post(models.Model):
	title = models.CharField(
		null=False,
		max_length=256,
		verbose_name='Titulo'
	)
	text = models.CharField(
		null=False,
		max_length=256,
		verbose_name='Texto'
	)
	status = models.CharField(
		default="DRAFT",
		choices=app_choices.post_status_choices,
		null=False,
		max_length=256,
		verbose_name="Estatus"
	)
	record_create = {}
	record_edit = {}

	comments = []

	def __str__(self):
		return str(self.title)


# POST HISTORY #
class PostRecord(models.Model):
	post = models.ForeignKey(
		Post,
		on_delete=models.CASCADE
	)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	date = models.DateTimeField(
		auto_now=True
	)
	action = models.CharField(
		choices=app_choices.post_actions_choices,
		null=False,
		max_length=256
	)

	def __str__(self):
		return str(self.action) + ": " + str(self.post) + " by " + str(self.user)


# RATE OF POST #
class RateOfPost(models.Model):
	post = models.ForeignKey(
		Post,
		on_delete=models.CASCADE
	)
	rate = models.IntegerField(
		null=False
	)

	def __str__(self):
		return str(self.rate)


# TAG #
class Tag(models.Model):
	name = models.CharField(
		null=False,
		max_length=256
	)

	def __str__(self):
		return str(self.name)


# TAGS OF POST #
class TagOfPost(models.Model):
	post = models.ForeignKey(
		Post,
		on_delete=models.CASCADE
	)
	tag = models.ForeignKey(
		Tag,
		on_delete=models.CASCADE
	)

	def __str__(self):
		return str(self.post) + " is of " + str(self.tag)


# COMMENT #
class PostComment(models.Model):
	post = models.ForeignKey(
		Post,
		on_delete=models.CASCADE
	)
	text = models.CharField(
		null=False,
		max_length=256,
		verbose_name='Texto'
	)
	record_create = {}
	record_edit = {}

	def __str__(self):
		return "Comment of " + str(self.post)


# COMMENT RECORD #
class PostCommentRecord(models.Model):
	post_comment = models.ForeignKey(

		PostComment,
		on_delete=models.CASCADE
	)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	date = models.DateTimeField(
		auto_now=True
	)
	action = models.CharField(
		choices=app_choices.comment_actions_choices,
		null=False,
		max_length=256
	)

	def __str__(self):
		return str(self.action) + ": " + str(self.post_comment) + " by " + str(self.user)
