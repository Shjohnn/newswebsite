from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
import os


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nomi")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def __str__(self):
        return self.name


class News(models.Model):
    """Yangilik modeli"""
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name="Kategoriya"
    )

    content = models.TextField( verbose_name="To'liq matn", blank=True, null=True)

    image = models.ImageField(upload_to='news/%Y/%m/%d/', verbose_name="Asosiy rasm")
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='news',
        verbose_name="Muallif"
    )

    # Statistika
    views = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar")
    reading_time = models.PositiveIntegerField(default=0, verbose_name="O'qish vaqti (daqiqa)")

    # Status
    is_published = models.BooleanField(default=True, verbose_name="Chop etilgan")


    # Vaqt
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Chop etilgan vaqti")

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['-views']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Slug yaratish
        if not self.slug:
            self.slug = slugify(self.title)
            # Agar slug mavjud bo'lsa, oxiriga raqam qo'shish
            if News.objects.filter(slug=self.slug).exists():
                count = 1
                while News.objects.filter(slug=f"{self.slug}-{count}").exists():
                    count += 1
                self.slug = f"{self.slug}-{count}"

        # O'qish vaqtini hisoblash (1 daqiqada 200 so'z o'qiladi deb hisoblanadi)
        if self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, word_count // 200)

        super().save(*args, **kwargs)

        # Rasmni optimize qilish
        if self.image:
            self.optimize_image()

    def optimize_image(self):
        """Rasmni compress qilish va optimize qilish"""
        try:
            img = Image.open(self.image.path)

            # Rasmni kichraytirish (max 1200px kenglik)
            if img.width > 1200:
                ratio = 1200 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((1200, new_height), Image.LANCZOS)

            # RGB formatga o'tkazish (RGBA uchun)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            # Sifatli siqish
            img.save(self.image.path, 'JPEG', quality=85, optimize=True)
        except Exception as e:
            print(f"Rasm optimize qilishda xatolik: {e}")

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    @property
    def comments_count(self):
        """Tasdiqlangan izohlar soni"""
        return self.comments.filter(is_approved=True).count()

    @property
    def next_news(self):
        """Keyingi yangilik"""
        return News.objects.filter(
            created_at__gt=self.created_at,
            is_published=True
        ).order_by('created_at').first()

    @property
    def previous_news(self):
        """Oldingi yangilik"""
        return News.objects.filter(
            created_at__lt=self.created_at,
            is_published=True
        ).order_by('-created_at').first()


class Comment(models.Model):
    """Izoh modeli"""
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Yangilik"
    )
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Xabar")
    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.news.title[:30]}"


class ContactMessage(models.Model):
    """Aloqa xabarlari modeli"""
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")

    class Meta:
        verbose_name = "Aloqa xabari"
        verbose_name_plural = "Aloqa xabarlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject[:30]}"


class Comment(models.Model):
    """Izoh modeli"""
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Yangilik"
    )
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Xabar")
    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.news.title[:30]}"