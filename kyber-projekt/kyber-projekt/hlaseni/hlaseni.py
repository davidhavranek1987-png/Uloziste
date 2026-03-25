from jinja2 import Template

def generuj_html(results):
    results = results.sort("score", descending=True)
    template = Template("""
    <html>
    <head>
        <title>Analýza článků</title>
    </head>
    <body>
        <h1>Obtížnost textu článků</h1>
        <table border="1">
            <tr>
                <th>Titulek</th>
                <th>Datum</th>
                <th>Délka věty</th>
                <th>Délka slova</th>
                <th>Dlouhá slova</th>
                <th>Unikátní poměr</th>
                <th>Skóre</th>
            </tr>
            {% for r in results %}
            <tr>
                <td>{{ r.title }}</td>
                <td>{{ r.date }}</td>
                <td>{{ r.avg_sentence_length }}</td>
                <td>{{ r.avg_word_length }}</td>
                <td>{{ r.long_word_ratio }}</td>
                <td>{{ r.unique_ratio }}</td>
                <td>{{ r.score }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """)

    html = template.render(results=results.to_dicts())
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)