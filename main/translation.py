from modeltranslation.translator import translator, TranslationOptions
from .models import Stage

class StageTranslationOptions(TranslationOptions):
    fields = ('name',) 
translator.register(Stage, StageTranslationOptions)
