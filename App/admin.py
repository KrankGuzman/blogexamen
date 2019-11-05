from django.contrib import admin

from . import models as app_models


admin.site.register(app_models.Post)
admin.site.register(app_models.PostRecord)
admin.site.register(app_models.RateOfPost)
admin.site.register(app_models.Tag)
admin.site.register(app_models.TagOfPost)
admin.site.register(app_models.PostComment)
admin.site.register(app_models.PostCommentRecord)
