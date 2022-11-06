import datetime
import random

from django.core.management.base import BaseCommand
from django.db.models import Min, Max
from faker import Faker

from annotations.models import Author, Publisher, Book, Store


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.create_authors()
        self.create_publishers()
        self.create_books()
        self.create_stores()
        self.stdout.write(self.style.SUCCESS('Database filled!'))

    def create_authors(self):
        cnt = 100
        fake = Faker()
        authors = list()

        for i in range(cnt):
            name = fake.first_name()
            age = random.randint(15, 100)
            author = Author(name=name, age=age)
            authors.append(author)

        Author.objects.bulk_create(authors)
        self.stdout.write(self.style.SUCCESS(f'Created {cnt} authors'))

    def create_publishers(self):
        cnt = 30
        publishers = list()

        for i in range(cnt):
            name = f'Publisher_{i}'
            publisher = Publisher(name=name)
            publishers.append(publisher)

        Publisher.objects.bulk_create(publishers)
        self.stdout.write(self.style.SUCCESS(f'Created {cnt} publishers'))

    def create_books(self):
        cnt = 200

        author_id = Author.objects.aggregate(min_id=Min('id'), max_id=Max('id'))
        publisher_id = Publisher.objects.aggregate(min_id=Min('id'), max_id=Max('id'))

        for i in range(cnt):
            name = f'Book_{i}'
            pages = random.randint(1, 1000)
            price = round(random.uniform(1, 1000), 2)
            rating = float(round(random.uniform(1, 100), 2))
            pubdate = make_random_date()

            book = Book(name=name, pages=pages, price=price, rating=rating, pubdate=pubdate)

            publisher = Publisher.objects.get(pk=random.randint(publisher_id['min_id'], publisher_id['max_id']))
            book.publisher = publisher

            book.save()

            for k in range(random.randint(1, 4)):
                author = Author.objects.get(pk=random.randint(author_id['min_id'], author_id['max_id']))
                book.authors.add(author)


        self.stdout.write(self.style.SUCCESS(f'Created {cnt} books'))

    def create_stores(self):
        cnt = 100

        book_id = Book.objects.aggregate(min_id=Min('id'), max_id=Max('id'))

        for i in range(cnt):
            name = f'Store_{i}'

            store = Store(name=name)

            store.save()

            for k in range(random.randint(1, 50)):
                book = Book.objects.get(pk=random.randint(book_id['min_id'], book_id['max_id']))
                store.books.add(book)


        self.stdout.write(self.style.SUCCESS(f'Created {cnt} stores'))


def make_random_date():
    start_date = datetime.date(1900, 10, 1)
    end_date = datetime.date(2022, 11, 30)
    num_days = (end_date - start_date).days
    rand_days = random.randint(1, num_days)
    random_date = start_date + datetime.timedelta(days=rand_days)
    return random_date
