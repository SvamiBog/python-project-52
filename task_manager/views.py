from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):

    template_name = 'index.html'
    extra_context = {
        'title': _('Greetings from Hexlet!'),
        'text': _('Practical programming courses'),
        'button_text': _('Learn more')
        }
