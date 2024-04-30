import os
import json
import argparse
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


def split_and_save_page_books(books, dest_folder):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    os.makedirs(dest_folder, exist_ok=True)
    pages_of_book = chunked(books, BOOKS_ON_PAGE_COUNT)
    page_count = ceil(len(books) / BOOKS_ON_PAGE_COUNT)
    for number, page in enumerate(pages_of_book, 1):
        filepath = f'{dest_folder}index{number}.html'  #TODO прописать через join
        if number == 1:
            filepath = f'{dest_folder}index.html'   #TODO прописать через join
        rendered_page = template.render(books=chunked(page, BOOK_COUTN_IN_LINE),
                                        page_count=page_count,
                                        current_page=number,
                                        dest_folder=dest_folder
                                        )
        with open(filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def on_reload(books, dest_folder):
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
                                    dest_folder=dest_folder,
                                    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest_folder', type=str, default='pages/',
                        help='Папка с итоговыми страницами')
    parser.add_argument('--books_file', type=str, default='books.json',
                        help='Указывается json-файл с данными о книгах')
    return parser.parse_args()


def main():
    args = get_args()
    books = get_books(args.books_file)
    split_and_save_page_books(books, args.dest_folder)
    server = Server()
    server.watch('template.html', lambda: on_reload(books, args.dest_folder))
    server.serve(root='.')


if __name__ == '__main__':
    main()
