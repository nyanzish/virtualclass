from django.contrib import admin
from .models import(
    UserProfile,
    Class_table,
    Subjects,
    Teacher_apply,
    Subjects_overview,
    Subscription,
    PaymentRecords,
    Upload_topics,
    Math,
    Physics,
    Chemistry,
    Biology,
    Geography,
    English,
    History,
    Islam,
    CRE,
    Agriculture,
    Computer,
    TechnicalDrawing,
    Art,
    French,
    German,
    Chinese,
    Luganda,
    GeneralPaper,
    Comment

)


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Class_table)
admin.site.register(Subjects)
admin.site.register(Teacher_apply)
admin.site.register(Subjects_overview)
admin.site.register(Upload_topics)
admin.site.register(Subscription)
admin.site.register(PaymentRecords)
admin.site.register(Math)
admin.site.register(Physics)
admin.site.register(Chemistry)
admin.site.register(Biology)
admin.site.register(Geography)
admin.site.register(English)
admin.site.register(History)
admin.site.register(Islam)
admin.site.register(CRE)
admin.site.register(Agriculture)
admin.site.register(Computer)
admin.site.register(TechnicalDrawing)
admin.site.register(Art)
admin.site.register(French)
admin.site.register(German)
admin.site.register(Chinese)
admin.site.register(Luganda)
admin.site.register(GeneralPaper)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'topic', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)