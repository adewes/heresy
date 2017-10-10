from heresy.loaders import FileLoader
from heresy import Environment, RenderContext

import click

@click.command("compile")
@click.argument("filename")
@click.option("--templates", multiple=True, default=[])
def compile(filename, templates, context={}):
    context = {
        'foobar' : 'test'
    }
    loader = FileLoader(paths=templates+('',))
    env = Environment(loader)
    heresy_context = RenderContext(context)
    heresy_tmpl = env.get_template(filename)
    heresy_tmpl.compile()
    res = heresy_tmpl.render(heresy_context)
    print(res)
