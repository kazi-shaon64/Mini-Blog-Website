from django.contrib import admin
from .models import Post, Comment, Like


# =========================
# POST ADMIN
# =========================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "author",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
    )

    list_filter = (
        "author",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 10

    readonly_fields = (
        "created_at",
    )

    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Post Information",
            {
                "fields": (
                    "title",
                    "content",
                )
            },
        ),

        (
            "Author Information",
            {
                "fields": (
                    "author",
                    "created_at",
                )
            },
        ),
    )


# =========================
# COMMENT ADMIN
# =========================

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "author",
        "post",
        "created_at",
    )

    search_fields = (
        "content",
        "author__username",
        "post__title",
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


# =========================
# LIKE ADMIN
# =========================

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "post",
        "created_at",
    )

    search_fields = (
        "user__username",
        "post__title",
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )