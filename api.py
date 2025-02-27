from fake_useragent import UserAgent
import requests
import time

# Список курсов на сайте
# https://otus.ru/catalog/courses?education_types=course'

ua = UserAgent()
headers = {
    "User-Agent": ua.random
}
items_total_cnt = 0


def get_courses_links_from_api(offset: int):
    global items_total_cnt
    mark = f'{offset}-{offset+20}:'
    print(f'{mark} getting courses data with offset')
    url = f'https://otus.ru/api/catalog.entity.list?education_types=course&limit=20&offset={offset}&search='
    response = requests.get(url, headers=headers)

    print(f'{mark} response status {response.status_code}')
    if response.status_code == 200:
        body = response.json()
        status = body['status']
        print(f'{mark} body status is {status}')
        if status == 'ok' and 'data' in body:
            items = body['data']['items'] if 'items' in body['data'] else []
            print(f'{mark} items len {len(items)}')
            if len(items):
                with open('eda/2025-02-27/urls.txt', 'a') as file:
                    for item in items:
                        items_total_cnt += 1
                        slug = item['slug']
                        print(f'{mark} {items_total_cnt}. {slug}')
                        file.write(f'https://otus.ru/lessons/{slug}\n')
            else:
                # кончились
                return -1
        else:
            with open('./offset.txt') as file:
                file.write(str(offset))
            raise RuntimeError(f'got status != ok or no data in response from OTUS Api on offset {offset}')

        print(f'{mark} sleeping...')
        time.sleep(5)
        return offset + 20
    elif response.status_code == 429:  # Too Many Requests
        retry_after = int(response.headers.get("Retry-After", 10))  # Default to 10 seconds
        time.sleep(retry_after)
        return offset
    else:
        with open('./offset.txt') as file:
            file.write(str(offset))
        raise RuntimeError(f'got response code {response.status_code} from OTUS Api on offset {offset}')


if __name__ == '__main__':
    offset = 0
    try:
        with open('./offset.txt') as file:
            offset = int(file.read())
    except OSError:
        print(f'there is no offset.txt, offset = {offset}')

    while offset >= 0:
        offset = get_courses_links_from_api(offset)
