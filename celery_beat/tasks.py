from bs4 import BeautifulSoup

from celery import shared_task

from django.core.mail import send_mail

import requests

from .models import Author, Quote, Tags

# set limit of processing quotes per task
QUOTES_LIMIT = 5


@shared_task
def parse_data(url='https://quotes.toscrape.com'):
    page = 1
    created_quotes = 0

    while created_quotes != QUOTES_LIMIT:
        print(f'============ NEW PAGE {page} ============')
        soup_site_data = get_site_data(url + f'/page/{page}')
        print(created_quotes)
        created_quotes, finish_page_quotes = extract_page_needed_data(url=url,
                                                                      soup=soup_site_data,
                                                                      created_quotes=created_quotes)

        if not soup_site_data.find_all('li', {'class': 'next'}) and finish_page_quotes:
            print(f'Created {created_quotes} new quotes')
            print('Finish all quotes')
            send_email_notification()
            break

        page += 1

    if created_quotes == QUOTES_LIMIT:
        print(f'Created {QUOTES_LIMIT} new quotes')


def extract_page_needed_data(url, soup, created_quotes):
    # find all quotes on page
    quotes = soup.find_all('div', {'class': 'quote'})

    for quote in quotes:

        if created_quotes == QUOTES_LIMIT:
            return created_quotes, False

        quote_text = quote.find('span', {'class': 'text'}).getText()
        quote_author = quote.find('small', {'class': 'author'}).getText()
        quote_author_url = url + quote.find('a', href=True)['href']

        author_defaults = get_author_data(quote_author_url)

        author_model, author_created = Author.objects.get_or_create(
            name=quote_author,
            defaults=author_defaults
        )

        print(quote_author)
        print('author_created: ', author_created)

        quote_model, quote_created = Quote.objects.get_or_create(
            text=quote_text,
            author=author_model
        )

        print(quote_text)
        print('quote_created: ', quote_created)

        # get quote's tags
        tags = quote.find_all('a', {'class': 'tag'})
        tags_model_list = []
        for tag in tags:
            tag_text = tag.getText()
            tag_model, tag_created = Tags.objects.get_or_create(text=tag_text)
            tags_model_list.append(tag_model.id)

        # add tags to quote
        quote_model.tags.add(*tags_model_list)

        print('--------------------------------------------------')

        if quote_created:
            created_quotes += 1

    return created_quotes, True


def get_author_data(url):
    try:
        author_soup_data = get_site_data(url)

        author_data = {'born_date': author_soup_data.find('span', {'class': 'author-born-date'}).getText(),
                       'born_location': author_soup_data.find('span', {'class': 'author-born-location'})
                       .getText().replace('in', '').strip(),
                       'description': author_soup_data.find('div', {'class': 'author-description'})
                       .getText().replace('\n', '').strip()}
    except (AttributeError, ConnectionError):
        return {}

    return author_data


def get_site_data(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        return soup
    except ConnectionError as e:
        raise e


def send_email_notification():
    send_mail(
        'Report parse site',
        'Finish process parse site',
        'no-reply@gmail.com',
        ['admin@gmail.com'],
        fail_silently=False,
    )
