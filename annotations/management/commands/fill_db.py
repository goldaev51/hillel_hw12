import datetime
import random

from annotations.models import Author, Book, Publisher, Store

from django.core.management.base import BaseCommand

from faker import Faker


class Command(BaseCommand):

    def handle(self, *args, **options):
        # filling db with data
        self.create_authors()
        self.create_publishers()
        self.create_books()
        self.create_stores()
        self.stdout.write(self.style.SUCCESS('Database filled!'))

    def create_authors(self):
        cnt = 500
        fake = Faker()
        authors = list()

        # create authors in loop for needed cnt
        for i in range(cnt):
            name = fake.first_name()
            age = random.randint(15, 100)
            author = Author(name=name, age=age)
            # add author obj to authors list
            authors.append(author)

        # create authors in model
        Author.objects.bulk_create(authors)
        self.stdout.write(self.style.SUCCESS(f'Created {cnt} authors'))

    def create_publishers(self):
        cnt = 100
        publishers = list()

        # create publishers in loop for needed cnt
        for i in range(cnt):
            name = f'Publisher_{i}'
            publisher = Publisher(name=name)
            # add publisher obj to publishers list
            publishers.append(publisher)

        # create publishers in model
        Publisher.objects.bulk_create(publishers)
        self.stdout.write(self.style.SUCCESS(f'Created {cnt} publishers'))

    def create_books(self):
        cnt = 1000

        # get author ids
        author_ids = Author.objects.values_list('id', flat=True)
        author_ids_cnt = author_ids.count() - 1
        # get publisher ids
        publisher_ids = Publisher.objects.values_list('id', flat=True)
        publisher_ids_cnt = publisher_ids.count() - 1

        # create books in loop for needed cnt
        for i in range(cnt):
            name = f'Book_{i}'
            pages = random.randint(1, 1000)
            price = round(random.uniform(1, 1000), 2)
            rating = float(round(random.uniform(1, 100), 2))
            # get random date
            pubdate = make_random_date()

            # create book object without connections of publisher and authors
            book = Book(name=name, pages=pages, price=price, rating=rating, pubdate=pubdate)

            # get publisher randomly by randint from publisher ids
            random_publisher_pk = random.randint(0, publisher_ids_cnt)
            publisher = Publisher.objects.get(pk=publisher_ids[random_publisher_pk])
            # add random publisher to book
            book.publisher = publisher
            book.save()

            # get randomly selected authors from 1 to 4 to add them to book
            random_authors_ids = list()
            for k in range(random.randint(1, 4)):
                # get author randomly by randint from author ids
                random_author_pk = random.randint(0, author_ids_cnt)
                random_authors_ids.append(author_ids[random_author_pk])

            # add authors to created book
            book.authors.add(*random_authors_ids)

        self.stdout.write(self.style.SUCCESS(f'Created {cnt} books'))

    def create_stores(self):
        cnt = 400

        # list of book ids
        book_ids = Book.objects.values_list('id', flat=True)
        book_ids_cnt = book_ids.count() - 1

        # create stores in loop for needed cnt
        for i in range(cnt):
            name = f'Store_{i}'

            store = Store(name=name)

            store.save()

            # get randomly selected books from 1 to 50 to add them to store
            random_books_ids = list()
            for k in range(random.randint(1, 50)):
                # get random book ids
                random_book_id = random.randint(0, book_ids_cnt)
                random_books_ids.append(book_ids[random_book_id])

            # add books to store
            store.books.add(*random_books_ids)

        self.stdout.write(self.style.SUCCESS(f'Created {cnt} stores'))


# create random date between 01.10.1900 and 2022.10.30
def make_random_date():
    start_date = datetime.date(1900, 10, 1)
    end_date = datetime.date(2022, 10, 30)
    num_days = (end_date - start_date).days
    rand_days = random.randint(1, num_days)
    random_date = start_date + datetime.timedelta(days=rand_days)
    return random_date
