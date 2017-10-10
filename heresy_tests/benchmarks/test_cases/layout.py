repetitions = 10000

heresy = {
    'context' : {},
    'template_name' : 'test.html',
    'templates' : {
    'test.html' : """
    <% extends("layout.html") %>
    <% blocks.title = 'Hello, world!' %>
    <% with blocks.content: %>
        <h2>Content</h2>
        <p>Lorem ipsum sit amet.
    <% end %>
    """,
    'layout.html' : """
    <html>
    <head>
        <title><%=h blocks.title %></title>
    </head>
    <body>
        <h1><%=h blocks.title %></h1>
        <div class="content">
            <%= blocks.content %>
        </div>
    </body>
    </html>
    """}
}

jinja2 = {
    'context' : {},
    'template_name' : 'test.html',
    'templates' : {
    'test.html' : """
    {% extends "layout.html" %}
    {% block title %}Hello, world!{%endblock%}
    {% block content %}
        <h2>Content</h2>
        <p>Lorem ipsum sit amet.
    {% endblock %}
    """,
    'layout.html' : """
    <html>
    <head>
        <title>{%block title%}{%endblock%}</title>
    </head>
    <body>
        <h1>{{self.title()}}</h1>
        <div class="content">
            {%block content%}{%endblock%}
        </div>
    </body>
    </html>
    """    
    }
}


django = {
    'context' : {},
    'template_name' : 'test.html',
    'templates' : {
    'test.html' : """
    {% extends "layout.html" %}
    {% block title %}Hello, world!{%endblock%}
    {% block content %}
        <h2>Content</h2>
        <p>Lorem ipsum sit amet.
    {% endblock %}
    """,
    'layout.html' : """
    <html>
    <head>
        <title>{%block title%}{%endblock%}</title>
    </head>
    <body>
        <h1>{{self.title}}</h1>
        <div class="content">
            {%block content%}{%endblock%}
        </div>
    </body>
    </html>
    """    
    }
}