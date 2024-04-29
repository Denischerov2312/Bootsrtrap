from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked

import os
import json
from math import ceil


def get_books(filepath):
    with open(filepath, 'r', encoding="utf8") as books_file:
        books = json.loads(books_file.read())
    return books


def split_and_save_page_books(books):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    os.makedirs('pages/', exist_ok=True)
    pages_of_book = chunked(books, 14)
    count_page = ceil(len(books) / 14)
    for number, page in enumerate(pages_of_book, 1):
        filepath = f'pages/index{number}.html'
        if number == 1:
            filepath = 'pages/index.html'
        rendered_page = template.render(books=chunked(page, 2),
                                        count_page=count_page,
                                        current_page=number,
                                        )
        with open(filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def on_reload(books):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    count_page = ceil(len(books) / 14)
    current_page = 1
    rendered_page = template.render(books=chunked(books, 2),
                                    count_page=count_page,
                                    current_page=current_page,
                                    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    books = get_books('books.json')
    split_and_save_page_books(books)
    server = Server()
    server.watch('template.html', lambda: on_reload(books))
    server.serve(root='.')


if __name__ == '__main__':
    main()
