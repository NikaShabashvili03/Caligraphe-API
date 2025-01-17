from modeltranslation.translator import translator, TranslationOptions
from .models import Stage, Work

class StageTranslationOptions(TranslationOptions):
    fields = ('name',) 
translator.register(Stage, StageTranslationOptions)


class WorkTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Work, WorkTranslationOptions)
