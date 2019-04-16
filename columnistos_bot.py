#!/usr/bin/python3
import argparse
import datetime as dt
import json
import logging
import os
import random
import sys

from urllib.parse import urlencode

import dataset

from pytz import timezone
from TwitterAPI import TwitterAPI


TESTING = os.environ.get('TESTING', 'True') == 'True'
LOG_FOLDER = os.environ.get('LOG_FOLDER', '')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

AUTHORIZED_SCREEN_NAMES = [
    'admin_screen_name',  # Twitter user name of persons that can send DMs
    'another_admin_screen_name',  # and that will receive DM from the bot
    # use 'screen_name' NOT '@screen_name'
]
SQLITE_URL = 'sqlite:///diarios/diarios.sqlite'
HOURS_WAIT_DM = 12
TIMEZONE = 'America/Buenos_Aires'
COMPLETE_NAMES = {
    'clarin': 'Clarín',
    'lanacion': 'La Nación',
    'pagina12': 'Página/12',
    'perfil': 'Perfil',
    'abc': 'ABC Color',
    'lanacionpy': 'La Nación',
    'ultimahora': 'Última Hora',
    'elmercurio': 'El Mercurio',
    'latercera': 'La Tercera',
    't13': 'T13',
    'nacion': 'La Nación',
    'crhoy': 'CRHoy',
    'delfino': 'DelfinoCR',
    'larepublica': 'La República',
}
MIN_NEW_ARTICLES = 2
MIN_PERCENT_SOME = 45


NO_WOMAN = [
    'Ayer en la página principal de {medio} no hubo ninguna columna ' +
    'de opinión {escrita} por mujeres.',

    'Las {total} columnas de opinión de la página principal de {medio}, ' +
    'en el día de ayer, fueron {escritas} por varones.']


NO_WOMAN_DAY = [
    'Ayer y antes de ayer, en la página principal de {medio}, ' +
    'ninguna de las columnas de opinión fue {escrita} por una mujer.',

    'Ayer y antes de ayer, en la página principal de {medio}, ' +
    'todas las columnas de opinión fueron {escritas} por varones.']


NO_WOMAN_DAYS = [
    'Ayer y los {dias} días anteriores, en la página principal de {medio}, ' +
    'ninguna de las columnas de opinión fue {escrita} por una mujer.',

    'Ayer y los {dias} días anteriores, en la página principal de {medio}, ' +
    'todas las columnas de opinión fueron {escritas} por varones.']

ONE_WOMAN = [
    'De las {total} columnas de opinión que publicaron ayer en la página ' +
    'principal de {medio}, solo una fue {escrita} por una mujer.',

    'En la página principal de {medio} ayer publicaron {total} columnas de ' +
    'opinión, solo una fue {escrita} por una mujer.']

SOME_WOMAN = [
    'De las {total} columnas de opinión que publicaron ayer en la página ' +
    'principal de {medio}, {mujeres} fueron {escritas} por mujeres.',

    'En la página principal de {medio} ayer publicaron {total} columnas de ' +
    'opinión, {mujeres} fueron {escritas} por mujeres.']

ONE_MAN = [
    'De las {total} columnas de opinión que publicaron ayer en la página ' +
    'principal de {medio}, solo una fue {escrita} por un varón.',

    'En la página principal de {medio} ayer publicaron {total} columnas de ' +
    'opinión, solo una fue {escrita} por un varón.']


ALL_WOMAN = [
    'Ayer en la página principal de {medio} todas las columnas de opinón ' +
    'fueron {escritas} por mujeres.',

    'Las {total} columnas de opinión de la página principal de {medio}, ' +
    'en el día de ayer, fueron {escritas} por mujeres.']

ALL_WOMAN_DAY = [
    'Ayer y antes de ayer, en la página principal de {medio}, ' +
    'no hubo ninguna columna de opinión {escrita} por varones.',

    'Ayer y antes de ayer, en la página principal de {medio}, ' +
    'todas las columnas de opinión fueron {escritas} por mujeres.']

ALL_WOMAN_DAYS = [
    'Ayer y los {dias} días anteriores, en la página principal de {medio}, ' +
    'no hubo ninguna columna de opinión {escrita} por varones.',

    'Ayer y los {dias} días anteriores, en la página principal de {medio}, ' +
    'todas las columnas de opinión fueron {escritas} por mujeres.']

DAILY_REPORT = [
    'Porcentaje de columnas de opinión publicadas en la página principal ' +
    '{escritas} por mujeres en el día de ayer ({fecha}):',

    'Ayer ({fecha}) en las páginas principales el porcentaje de columnistas ' +
    'de opinión mujeres fue:',

    'De las columnas de opinión publicadas ayer ({fecha}) en las páginas ' +
    'principales, estas son en porcentaje, las que fueron {escritas} por ' +
    'mujeres:',

    'De las columnas de opinión publicadas ayer ({fecha}) en las páginas ' +
    'principales, estas son en porcentaje, las {escritas} por mujeres:'
]


def select_text(stats):
    percent_fem = int(stats['fem'] / stats['total'] * 100)
    logging.info('Stats: {} percent: {}'.format(stats, percent_fem))
    if stats['fem'] == 0 and stats['days'] <= 0:
        selected = random.choice(NO_WOMAN)
    elif stats['fem'] == 0 and stats['medio'] == 'Perfil':
        selected = random.choice(NO_WOMAN)
    elif stats['fem'] == 0 and stats['days'] == 1:
        selected = random.choice(NO_WOMAN)
    elif stats['fem'] == 0 and stats['days'] > 1:
        selected = random.choice(NO_WOMAN)
    elif stats['fem'] == 1:
        selected = random.choice(ONE_WOMAN)
    elif stats['fem'] == stats['total'] - 1:
        selected = random.choice(ONE_MAN)
    elif stats['fem'] == stats['total'] and stats['days'] <= 0:
        selected = random.choice(ALL_WOMAN)
    elif stats['fem'] == stats['total'] and stats['medio'] == 'Perfil':
        selected = random.choice(ALL_WOMAN)
    elif stats['fem'] == stats['total'] and stats['days'] == 1:
        selected = random.choice(ALL_WOMAN)
    elif stats['fem'] == stats['total'] and stats['days'] > 1:
        selected = random.choice(ALL_WOMAN)
    elif percent_fem > MIN_PERCENT_SOME:
        selected = random.choice(SOME_WOMAN)
    else:
        return None

    escrita = random.choice(['escrita', 'firmada'])
    escritas = random.choice(['escritas', 'firmadas'])
    total = stats['total']
    mujeres = stats['fem']
    dias = stats['days']
    logging.info('Pre complet text {}'.format(selected))
    return selected.format(total=total, medio=stats['medio'],
                           escrita=escrita, escritas=escritas,
                           mujeres=mujeres, dias=dias)


def daily_tweet(daily_stats):
    text = random.choice(DAILY_REPORT)
    escritas = random.choice(['escritas', 'firmadas'])
    dia_semana = dt.datetime.strftime(daily_stats[0]['yesterday'], '%w')
    dias_dict = {'0':'dom', '1':'lun', '2':'mar', '3':'mie', '4':'jue', '5':'vie', '6':'sab'} 
    fecha = dias_dict[dia_semana] + dt.datetime.strftime(daily_stats[0]['yesterday'], ' %-d/%-m')
    text = text.format(escritas=escritas, fecha=fecha)

    f_count = 0
    t_count = 0
    for row in daily_stats:
        text += '\n {medio}: {percent} % ({fem} de {total})'.format(
            medio=row['medio'],
            percent=round(row['fem'] / row['total'] * 100),
            fem=row['fem'],
            total=row['total']
        )
        f_count += row['fem']
        t_count += row['total']
    if len(daily_stats) > 1:
        percent_t = round(f_count / t_count * 100)
        text += f'\n ———\n Total: {percent_t} % ({f_count} de {t_count})'
    return text


def test_twitter(api):
    r = api.request('users/show', {'screen_name': AUTHORIZED_SCREEN_NAMES[0]})
    if r.status_code == 200:
        print('Twitter API working')
        print(r.json()['id'])
    else:
        print('Problem connecting to Twitter API')


def screen_names_to_id(api, screen_names):
    """
    screen_names: list of screen names with no leading @
    returns: list of user ids
    """
    r = api.request('users/lookup', {'screen_name': screen_names})
    if r.status_code != 200:
        return False
    return [user['id'] for user in r.json()]


def tweet_text(api, text_to_tweet):
    if TESTING:
        print(text_to_tweet)
        return True
    r = api.request('statuses/update', {'status': text_to_tweet})
    if r.status_code != 200:
        return False
    return True


def send_dm(api, recipient_id, text_to_dm):
    if TESTING:
        print(text_to_dm)
        return True
    event = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": recipient_id
                },
                "message_data": {
                    "text": text_to_dm
                }
            }
        }
    }
    r = api.request('direct_messages/events/new', json.dumps(event))
    if r.status_code != 200:
        logging.error('Problem sending DM, error: {}, message: {}'.format(
            r.status_code, r.text))
        return False
    return True


def check_dms(api, auth_ids):
    if os.path.exists('last_checked_dm.json'):
        with open('last_checked_dm.json') as ld:
            data = json.load(ld)
    else:
        data = {'last_dm': 0}

    r = api.request('direct_messages/events/list')
    db = dataset.connect(SQLITE_URL)
    dms = db['dms']
    authors = db['authors']
    for dm in r.json()['events'][::-1]:
        if int(dm['message_create']['target']['recipient_id']) in auth_ids:
            # dm sent by bot, skip
            continue
        elif int(dm['message_create']['sender_id']) not in auth_ids:
            logging.warning(
                'DM from unauthorized account with id {}'.format(
                    dm['message_create']['sender_id']))
        elif int(dm['id']) <= data['last_dm']:
            continue
        else:
            data['last_dm'] = int(dm['id'])
            response = dm['message_create']['message_data'][
                'text'].strip().split()
            if len(response) != 2:
                send_dm(api, dm['message_create']['sender_id'],
                        "No entiendo el mensaje")
                continue
            elif not authors.find_one(id=response[0]):
                send_dm(api, dm['message_create']['sender_id'],
                        "No encontré al autor con el ID {}".format(
                            response[0]))
                continue
            elif response[1][0].upper() not in ['V', 'F', 'X']:
                send_dm(api, dm['message_create']['sender_id'],
                        "No entendí el genero {}".format(response[1]))
                continue

            author = authors.find_one(id=response[0])
            response[1] = response[1].upper()
            if response[1][0] == 'V':
                response[1] = response[1].replace('V', 'M')

            # someone else already answered
            if not dms.find_one(author_id=response[0]):
                if len(response[1]) == 2 and response[1][1] == '!':
                    authors.update(dict(id=response[0],
                                        gender=response[1][0]),
                                   ['id'])
                    send_dm(api, dm['message_create']['sender_id'],
                            "Los datos de {} ({}) se cambiaron".format(
                                author['author'], author['id']))
                    logging.info('Gender of {} set to {}'.format(
                        author['author'], response[1][0]))
                elif author['gender'] == response[1][0]:
                    send_dm(api, dm['message_create']['sender_id'],
                            "Gracias por los datos de {} ({})".format(
                                author['author'], author['id']))
                else:
                    for admin_id in auth_ids:
                        send_dm(api, admin_id,
                                ("Tu respuesta de {} no coincide con otras "
                                 "cuando se pongan de acuerdo manden {} g! "
                                 "(g = f/v/x)").format(
                                    author['author'], author['id']))
            else:
                authors.update(dict(id=response[0],
                                    gender=response[1][0]),
                               ['id'])
                dms.delete(author_id=response[0])
                send_dm(api, dm['message_create']['sender_id'],
                        "Gracias por los datos de {} ({})".format(
                            author['author'], author['id']))
                logging.info('Gender of {} set to {}'.format(
                    author['author'], response[1][0]))
    with open('last_checked_dm.json', 'w') as lt:
        json.dump(data, lt)

    return True


def send_dms(api, texts_to_dm, auth_ids):
    db = dataset.connect(SQLITE_URL)
    dms = db['dms']
    for admin_id in auth_ids:
        for author_to_dm in texts_to_dm:
            author = author_to_dm['author']
            article = author_to_dm['article']
            ddg_qs = {
                'q': author['author'],
                'iax': 'images',
                'ia': 'images'
            }
            google_qs = {
                'q': author['author'],
                'tbm': 'isch'
            }
            dm = ("Nuevo autor {author} con Id {id}, respondé {id} f "
                  "o {id} v o {id} x\n"
                  "DDG Images: https://duckduckgo.com/?{ddg}\n"
                  "Google Images: https://google.com/search?{google}\n"
                  "Nota: {link}"
                  ).format(
                      author=author['author'],  id=author['id'],
                      ddg=urlencode(ddg_qs), google=urlencode(google_qs),
                      link=article['url']
                  )
            dm_result = send_dm(api, admin_id, dm)
            if not dm_result:
                logging.warning('Sending DM to {} failed'.format(
                    admin_screen_name))
                return False
            # add/update in table of sent DMs
            dms.upsert(dict(author_id=author['id'],
                            added=dt.datetime.utcnow()),
                       ['author_id'])
    return True


def get_author_no_gender():
    authors_no_gender = list()
    db = dataset.connect(SQLITE_URL)
    authors = db['authors']
    articles = db['articles']
    dms = db['dms']

    for author in authors.find(gender=None):
        authors_no_gender.append(author)
    for author in authors.find(gender='A'):
        authors_no_gender.append(author)

    # remove from dms authors with no answer
    past_date = dt.datetime.utcnow() - dt.timedelta(
        hours=HOURS_WAIT_DM)
    if 'dms' in db.tables and 'added' in db['dms'].columns and \
       len(db['dms']) > 0:
        unanswered_dms = dms.find(dms.table.columns.added < past_date)
        for row in unanswered_dms:
            dms.delete(id=row['id'])

        # remove from list to ask authors recently sent
        unsent_authors = [author for author in authors_no_gender
                          if not dms.find_one(author_id=author['id'])]
    else:
        unsent_authors = authors_no_gender

    # add link to last article by authors to send
    unsent_authors_dicts = list()
    for author in unsent_authors:
        last_article = articles.find_one(author_id=author['id'])
        unsent_authors_dicts.append({
            'author': author,
            'article': last_article
        })

    return unsent_authors_dicts


def get_stats(site):
    db = dataset.connect(SQLITE_URL)
    articles = db['articles']
    authors = db['authors']

    today = dt.datetime.now(timezone(TIMEZONE)).date()
    today_with_time = dt.datetime(
        year=today.year,
        month=today.month,
        day=today.day
    )
    yesterday = today_with_time - dt.timedelta(days=1)

    filtered_articles = articles.find(
        articles.table.columns.last_seen > yesterday,
        articles.table.columns.added < today_with_time,
        articles.table.columns.id > site['last_checked_id'],
        site=site['name']
    )

    total = 0
    fem = 0
    last_id = site['last_checked_id']
    for row in filtered_articles:
        total += 1
        author = authors.find_one(id=row['author_id'])
        if author['gender'] == 'F':
            fem += 1
        elif author['gender'] is None:
            return None

        if row['id'] > last_id:
            last_id = row['id']

    if total == 0:
        return None

    gender_days = None
    if fem == 0:
        gender_days = 'F'
    elif fem == total:
        gender_days = 'M'

    if gender_days:
        statement = 'SELECT articles.last_seen FROM articles \
                INNER JOIN authors on author_id = authors.id \
                WHERE authors.gender = :gender_days \
                AND articles.site = :site \
                AND articles.last_seen <= :yesterday \
                ORDER BY articles.last_seen DESC \
                LIMIT 1'
        result = db.query(statement, gender_days=gender_days,
                          site=site['name'], yesterday=yesterday)
        row = next(result, None)
        # TODO chequear que en los días intermedios tenga notas sobre todo por
        # casos como perfil
        # TODO days no sirve por que las notas siguen apareciendo durante las
        # primeras horas del día siguiente, hay que agregar a la BD
        # otra columna/s para llevar la cuenta de días seguidos sin notas de
        # un genero
        if row:
            last_seen = dt.datetime.strptime(
                ''.join(row['last_seen'].rsplit(':', 1)),
                '%Y-%m-%dT%H:%M:%S%z')
            last_seen = last_seen.replace(tzinfo=None)
            days = yesterday - last_seen
    else:
        days = yesterday - yesterday
    return dict(total=total, fem=fem, var=total-fem, days=days.days,
                last_id=last_id, medio=COMPLETE_NAMES[site['name']],
                yesterday=yesterday)


def parse_arguments():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    g.add_argument('-dm', action='store_true', help='Send DMs')
    g.add_argument('-tweet', action='store_true', help='Send tweets')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    return args


def main():
    # argument parsing
    args = vars(parse_arguments())

    # logging
    logging.basicConfig(
        filename=LOG_FOLDER + 'columnistos.log',
        format='%(asctime)s %(name)s %(levelname)8s: %(message)s',
        level=LOG_LEVEL)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.info('Starting script')

    # keys
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    api = TwitterAPI(consumer_key, consumer_secret,
                     access_token, access_token_secret)
    auth_ids = screen_names_to_id(api, AUTHORIZED_SCREEN_NAMES)
    db = dataset.connect(SQLITE_URL)

    # DMs
    if args['dm']:
        logging.info('Checking if DM needed')
        logging.info('Need to send/process DM')
        check_dms(api, auth_ids)
        data_to_send = get_author_no_gender()
        logging.debug(data_to_send)
        send_dms(api, data_to_send, auth_ids)

    if args['tweet']:
        logging.info('Checking if ready to tweet')
        if 'sites' not in db.tables:
            sites = db.create_table('sites')
            sites_in_articles = db['articles'].distinct('site')
            for row in sites_in_articles:
                sites.insert(dict(name=row['site'], last_checked_id=0))

        daily_stats = list()
        for row in db['sites']:
            stats = get_stats(row)
            if stats:
                daily_stats.append(stats)
                if stats['total'] > MIN_NEW_ARTICLES:
                    text_to_tweet = select_text(stats)
                    logging.info('About to tweet for {} with {}'.format(
                        row['name'], text_to_tweet))
                    if text_to_tweet and tweet_text(api, text_to_tweet):
                        logging.info('Individual tweet for {} sent'.format(
                            row['name']))
                else:
                    logging.info(
                        'Not enough new articles for {}, stats: {}'.format(
                            row['name'], stats))
                # update last_checked_id
                db['sites'].update(dict(name=row['name'],
                                        last_checked_id=stats['last_id']),
                                   ['name'])

        if len(daily_stats) > 0:
            text_to_tweet = daily_tweet(daily_stats)
            if text_to_tweet and tweet_text(api, text_to_tweet):
                logging.info('Resume tweeted')
            else:
                logging.warning('Resume failed')
        else:
            logging.info('No resume to send')
    logging.info('Script finished')


if __name__ == '__main__':
    main()
