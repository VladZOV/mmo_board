from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from .models import Category, Post, Response, Newsletter
from django import forms


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at')
    actions = ['send_newsletter']

    def send_newsletter(self, request, queryset):
        for newsletter in queryset:
            newsletter.send_emails()
        self.message_user(request, "Рассылка успешно отправлена.")
    send_newsletter.short_description = "Отправить выбранные рассылки"


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'accepted')
    list_filter = ('accepted', 'created_at')
    search_fields = ('text',)

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Response)
admin.site.register(Newsletter, NewsletterAdmin)
