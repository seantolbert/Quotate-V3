from django.contrib import admin
from .models import Quote, Source, ReviewQuote

admin.site.register(Quote)
admin.site.register(Source)
admin.site.register(ReviewQuote)
