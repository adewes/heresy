repetitions = 10

context = {'table' : [dict(a=1,b=2,c=3,d=4,e=5,f=6,g=7,h=8,i=9,j=10)
          for x in range(1000)]}

heresy = {
    'context' : context,
    'template_name' : 'test.html',
    'templates' : {
    'test.html' : """<table>
    <% for row in table: %>
        <tr>
            <% for col in row.values(): %><td><%=h col %></td><% end %>
        </tr>
    <% end %>
    </table>
    """}
}

jinja2 = {
    'context' : context,
    'template_name' : 'test.html',
    'templates' : {
    'test.html' : """<table>
    {% for row in table %}
        <tr>
            {% for col in row.values() %}<td>{{col|escape}}</td> {% endfor %}
        </tr>
    {% endfor %}
    </table>
    """    
    }
}

django = {
    'context' : context,
    'template_name' : 'test.html',
    'templates' : {
    'test.html' : """<table>
    {% for row in table %}
        <tr>
            {% for col in row.values %}<td>{{col|escape}}</td> {% endfor %}
        </tr>
    {% endfor %}
    </table>
    """    
    }
}