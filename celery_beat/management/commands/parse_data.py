from bs4 import BeautifulSoup

from celery_beat.models import Author, Quote, Tags

from django.core.management import BaseCommand

import requests

# set limit of processing quotes per task
QUOTES_LIMIT = 5


class Command(BaseCommand):

    def handle(self, *args, **options):
        parce_data()


def parce_data(url='https://quotes.toscrape.com'):
    page = 1
    created_quotes = 0

    while created_quotes != QUOTES_LIMIT:
        print(f'============ NEW PAGE {page} ============')
        soup_site_data = get_site_data(url + f'/page/{page}')
        print(created_quotes)
        created_quotes = extract_page_needed_data(url=url, soup=soup_site_data, created_quotes=created_quotes)

        if not soup_site_data.find_all('li', {'class': 'next'}):
            print(f'Created {created_quotes} new quotes')
            print('Finish all quotes')
            # send_email_notification()
            break

        page += 1

    if created_quotes == QUOTES_LIMIT:
        print(f'Created {QUOTES_LIMIT} new quotes')


def extract_page_needed_data(url, soup, created_quotes):
    quotes = soup.find_all('div', {'class': 'quote'})

    for quote in quotes:
        quote_text = quote.find('span', {'class': 'text'}).getText()
        quote_author = quote.find('small', {'class': 'author'}).getText()
        quote_author_url = url + quote.find('a', href=True)['href']

        author_defaults = get_author_data(quote_author_url)

        author_model, author_created = Author.objects.get_or_create(
            name=quote_author,
            defaults=author_defaults
        )

        print(quote_author)
        print(quote_text)

        print('author_created: ', author_created)

        quote_model, quote_created = Quote.objects.get_or_create(
            text=quote_text,
            author=author_model
        )

        print('quote_created: ', quote_created)

        tags = quote.find_all('a', {'class': 'tag'})
        tags_model_list = []
        for tag in tags:
            tag_text = tag.getText()
            tag_model, tag_created = Tags.objects.get_or_create(text=tag_text)
            tags_model_list.append(tag_model.id)

        quote_model.tags.add(*tags_model_list)

        print('--------------------------------------------------')

        if quote_created:
            created_quotes += 1

        if created_quotes == QUOTES_LIMIT:
            return created_quotes

    return created_quotes


def get_author_data(url):
    author_soup_data = get_site_data(url)
    try:
        author_data = {'born_date': author_soup_data.find('span', {'class': 'author-born-date'}).getText(),
                       'born_location': author_soup_data.find('span', {'class': 'author-born-location'})
                       .getText().replace('in', '').strip(),
                       'description': author_soup_data.find('div', {'class': 'author-description'})
                       .getText().replace('\n', '').strip()}
    except AttributeError:
        return {}

    return author_data


def get_site_data(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        return soup
    except ConnectionError as e:
        raise e
