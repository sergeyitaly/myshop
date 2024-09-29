from modeltranslation.translator import TranslationOptions,translator, TranslationOptions
from .models import Comment

class CommentTranslationOptions(TranslationOptions):
    fields = ('name','comment',)

translator.register(Comment, CommentTranslationOptions)
