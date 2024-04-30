import os
import json
from math import ceil

from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked


BOOKS_ON_PAGE_COUNT = 14
BOOK_COUTN_IN_LINE = 2


def get_books(filepath):
    with open(filepath, 'r', encoding="utf8") as books_file:
        books = json.load(books_file)
    return books


def split_and_save_page_books(books):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    os.makedirs('pages/', exist_ok=True)
    pages_of_book = chunked(books, BOOKS_ON_PAGE_COUNT)
    page_count = ceil(len(books) / BOOKS_ON_PAGE_COUNT)
    for number, page in enumerate(pages_of_book, 1):
        filepath = f'pages/index{number}.html'
        if number == 1:
            filepath = 'pages/index.html'
        rendered_page = template.render(books=chunked(page, BOOK_COUTN_IN_LINE),
                                        page_count=page_count,
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
    page_count = ceil(len(books) / BOOKS_ON_PAGE_COUNT)
    current_page = 1
    rendered_page = template.render(books=chunked(books, BOOK_COUTN_IN_LINE),
                                    page_count=page_count,
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
