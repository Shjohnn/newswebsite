from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name']

    def news_count(self, obj):
        return obj.news.count()

    news_count.short_description = 'Yangiliklar soni'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'author',
        'views',
    ]
    list_filter = [
        'is_published',
        'category',
        'created_at',
        'author'
    ]
    search_fields = ['title', 'content',]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'reading_time', 'created_at', 'updated_at', 'image_preview_large']

    fieldsets = (
        ('Asosiy Ma\'lumotlar', {
            'fields': ('title', 'slug', 'category', 'author')
        }),
        ('Kontent', {
            'fields': ( 'content',)
        }),
        ('Rasm', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Parametrlar', {
            'fields': ('is_published', 'published_at')
        }),
        ('Statistika', {
            'fields': ('views', 'reading_time', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = 'Rasm'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="300" style="border-radius: 10px;" />',
                obj.image.url
            )
        return "-"

    image_preview_large.short_description = 'Rasm ko\'rinishi'

    actions = ['make_published', 'make_unpublished', 'make_featured', ]

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} ta yangilik chop etildi.")

    make_published.short_description = "Tanlangan yangiliklarni chop etish"

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} ta yangilik yashirildi.")

    make_unpublished.short_description = "Tanlangan yangiliklarni yashirish"

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} ta yangilik featured qilindi.")

    make_featured.short_description = "Featured qilish"

    def make_breaking(self, request, queryset):
        queryset.update(is_breaking=True)
        self.message_user(request, f"{queryset.count()} ta yangilik tezkor qilindi.")

    make_breaking.short_description = "Tezkor yangilik qilish"



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'news', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']

    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} ta izoh tasdiqlandi.")

    approve_comments.short_description = "Tanlangan izohlarni tasdiqlash"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} ta izoh rad etildi.")

    disapprove_comments.short_description = "Tanlangan izohlarni rad etish"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'name', 'email', 'subject', 'message']

    fieldsets = (
        ('Xabar Ma\'lumotlari', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} ta xabar o'qilgan deb belgilandi.")

    mark_as_read.short_description = "O'qilgan deb belgilash"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} ta xabar o'qilmagan deb belgilandi.")

    mark_as_unread.short_description = "O'qilmagan deb belgilash"