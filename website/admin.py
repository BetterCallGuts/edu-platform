from django.contrib import admin
from .models import GloblaChatBot, ChatBotForEP, Logo, GlobalVars
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from custom_admin.admin import admin_site
from django.utils.html import mark_safe


User = get_user_model()


class ChatBotAdmin(admin.ModelAdmin):
    list_display = [ "Prompt"]
    search_fields = ["Prompt"]


class ChatBotForEPAdmin(admin.ModelAdmin):
    list_display = ["episode", "Prompt"]
    list_filter = ["episode"]
    search_fields = ["Prompt"]



class LogoAdmin(admin.ModelAdmin):
    pass

class GlobalVarsAdmin(admin.ModelAdmin):
   list_editable = ["Value"]
   list_display_links = ["Key"]
   list_display = ["Key", "Value"]
   search_fields = ["Key", "Value"]

admin_site.register(GloblaChatBot, ChatBotAdmin)
admin_site.register(ChatBotForEP, ChatBotForEPAdmin)
admin_site.register(Logo, LogoAdmin)
admin_site.register(GlobalVars, GlobalVarsAdmin)

