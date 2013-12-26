from django.template import Context as DjangoContext
from django.template import Template as DjangoTemplate
import django.template.loader
from django.conf import settings

settings.configure()

def test(template_name,context,templates):

    context = DjangoContext(context)

    def find_template(template_name):
        template = DjangoTemplate(templates[template_name])
        return template,template_name

    django.template.loader.find_template = find_template
    django_tmpl,source = find_template(template_name)

    def run_test():
        """Heresy template"""
        res = django_tmpl.render(context)
        return res

    return run_test
