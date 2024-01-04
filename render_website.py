import json
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_books(filepath='books.json'):
    with open(filepath, 'r', encoding="utf8") as books_file:
        books_json = books_file.read()
    books = json.loads(books_json)
    return books


def on_reload(books):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(books=books)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    books = get_books('25books_json.json')
    on_reload(books)

    server = Server()
    server.watch('template.html', lambda: on_reload(books))
    server.serve(root='.')


if __name__ == '__main__':
    main()
