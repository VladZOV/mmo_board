from ckeditor.fields import RichTextField
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = RichTextField(verbose_name="Содержание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title


class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Response to {self.post.title} by {self.author.username}"


def add_initial_categories(apps, schema_editor):
    Category = apps.get_model('mmo_board', 'Category')
    categories = [
        "Танки", "Хилы", "ДД", "Торговцы", "Гилдмастеры",
        "Квестгиверы", "Кузнецы", "Кожевники", "Зельевары", "Мастера заклинаний"
    ]
    for category_name in categories:
        Category.objects.create(name=category_name)


class Newsletter(models.Model):
    subject = models.CharField(max_length=200, verbose_name="Тема рассылки")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.subject

    def send_emails(self):
        users = User.objects.filter(is_active=True)  # Получаем всех активных пользователей
        for user in users:
            send_mail(
                self.subject,
                self.message,
                'from@example.com',  # Укажите ваш email
                [user.email],  # Отправляем каждому пользователю
                fail_silently=False,
            )
