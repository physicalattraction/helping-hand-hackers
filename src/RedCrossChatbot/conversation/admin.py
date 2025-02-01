from django.contrib import admin

from conversation.models import Conversation, ConversationLine


class ConversationLineInline(admin.TabularInline):
    model = ConversationLine
    extra = 0


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    inlines = [ConversationLineInline]
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user']
