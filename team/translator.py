from modeltranslation.translator import TranslationOptions,translator, TranslationOptions
from .models import TeamMember

class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('name','surname','description')

translator.register(TeamMember, TeamMemberTranslationOptions)
