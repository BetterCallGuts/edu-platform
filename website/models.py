from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from .views import extract_text_from_pdf

class GlobalVars(models.Model):

    Key   = models.CharField(max_length=100, verbose_name=_("Key"))
    Value = models.TextField(max_length=100, verbose_name=_("Value"))

    



class GloblaChatBot(models.Model):
    Prompt = models.TextField(max_length=1000)


    def __str__(self):
        return self.Prompt
    
    class Meta:
        verbose_name = _('Global Chat Bot')
        verbose_name_plural = _('Global Chat Bots')

class ChatBotForEP(models.Model):
    Prompt = models.TextField(max_length=1000)
    episode = models.ForeignKey(
        "course.Episode",
        on_delete=models.CASCADE,
        related_name="chatbots",
        verbose_name=_("Episode")
    )
    pdf = models.FileField(
        upload_to="pdf/",
        verbose_name=_("PDF File"),
        blank=True,
        null=True
    )
    text = models.TextField(
        max_length=1000,
        verbose_name=_("Text"),
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
  
        if self.pdf:
            extracted_text = extract_text_from_pdf(self.pdf.path)
            if extracted_text:
   
                if self.text:
                    self.text += "\n" + extracted_text
                else:
                    self.text = extracted_text

        super().save(*args, **kwargs)

    def __str__(self):
        return self.Prompt

    class Meta:
        verbose_name = _('Chat Bot For Episodes')
        verbose_name_plural = _('Chat Bots For Episodes')
class Logo(models.Model):
    logo = models.ImageField(upload_to="logo/", verbose_name=_("Logo"))