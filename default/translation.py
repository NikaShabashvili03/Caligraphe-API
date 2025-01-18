from modeltranslation.translator import translator, TranslationOptions
from .models import Stage, Service

class StageTranslationOptions(TranslationOptions):
    fields = ('name',) 
translator.register(Stage, StageTranslationOptions)


class ServiceTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Service, ServiceTranslationOptions)
