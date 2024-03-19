from django.contrib import admin
from .models import BlogCategory,Posts,Comment,PostView


# Register your models here.
admin.site.register(BlogCategory),
admin.site.register(Posts),
admin.site.register(Comment),
admin.site.register(PostView),