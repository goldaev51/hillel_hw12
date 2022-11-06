import datetime
import random

from django.core.management.base import BaseCommand
from django.db.models import Min, Max
from faker import Faker

from annotations.models import Author, Publisher, Book, Store


class Command(BaseCommand):

    def handle(self, *args, **options):
        # filling db with data
        self.create_authors()
        self.create_publishers()
        self.create_books()
        self.create_stores()
        self.stdout.write(self.style.SUCCESS('Database filled!'))

    def create_authors(self):
        cnt = 100
        fake = Faker()
        authors = list()

        # loop for creation authors in loop for needed cnt
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
        cnt = 30
        publishers = list()

        # loop for creation authors in loop for needed cnt
        for i in range(cnt):
            name = f'Publisher_{i}'
            publisher = Publisher(name=name)
            # add publisher obj to publishers list
            publishers.append(publisher)

        # create publishers in model
        Publisher.objects.bulk_create(publishers)
        self.stdout.write(self.style.SUCCESS(f'Created {cnt} publishers'))

    def create_books(self):
        cnt = 200

        # get min and max id from author model
        author_id = Author.objects.aggregate(min_id=Min('id'), max_id=Max('id'))
        # get min and max id from publisher model
        publisher_id = Publisher.objects.aggregate(min_id=Min('id'), max_id=Max('id'))

        # loop for creation books in loop for needed cnt
        for i in range(cnt):
            name = f'Book_{i}'
            pages = random.randint(1, 1000)
            price = round(random.uniform(1, 1000), 2)
            rating = float(round(random.uniform(1, 100), 2))
            # get random date
            pubdate = make_random_date()

            # create book object without connections of publisher and authors
            book = Book(name=name, pages=pages, price=price, rating=rating, pubdate=pubdate)

            # get publisher randomly by randint from min_id to max_id
            publisher = Publisher.objects.get(pk=random.randint(publisher_id['min_id'], publisher_id['max_id']))
            # add random publisher to book
            book.publisher = publisher
            book.save()

            # get randomly selected authors from 1 to 4 to add them to book
            for k in range(random.randint(1, 4)):
                # get author randomly by randint from min_id to max_id
                author = Author.objects.get(pk=random.randint(author_id['min_id'], author_id['max_id']))
                # add author to created book
                book.authors.add(author)


        self.stdout.write(self.style.SUCCESS(f'Created {cnt} books'))

    def create_stores(self):
        cnt = 100

        # get min and max id from book model
        book_id = Book.objects.aggregate(min_id=Min('id'), max_id=Max('id'))

        # loop for creation stores in loop for needed cnt
        for i in range(cnt):
            name = f'Store_{i}'

            store = Store(name=name)

            store.save()

            # get randomly selected books from 1 to 50 to add them to store
            for k in range(random.randint(1, 50)):
                # get book randomly by randint from min_id to max_id
                book = Book.objects.get(pk=random.randint(book_id['min_id'], book_id['max_id']))
                # add book to created store
                store.books.add(book)


        self.stdout.write(self.style.SUCCESS(f'Created {cnt} stores'))


# create random date between 01.10.1900 and 2022.10.30
def make_random_date():
    start_date = datetime.date(1900, 10, 1)
    end_date = datetime.date(2022, 10, 30)
    num_days = (end_date - start_date).days
    rand_days = random.randint(1, num_days)
    random_date = start_date + datetime.timedelta(days=rand_days)
    return random_date
