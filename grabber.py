import re
from bs4 import BeautifulSoup


def grab_data(soup):
    data = {}

    block_tag = soup.find(id='__next').find_all('div')[1].find('main').find('div')
    top_tag = block_tag.find('section').find('div').find_next_sibling()
    head = top_tag.find('h1')
    data['title'] = head.string
    data['promo'] = head.find_next_sibling().get_text(separator=' ').strip()

    data['duration'] = 0
    data['presentType'] = 'Онлайн'
    try:
        props_tags = top_tag.find_next_sibling().find_all('p')
        for tag in props_tags:
            if 'мес' in tag.string:
                data['duration'] = int(re.sub(r'\D+', '', tag.string, flags=re.U | re.I))
            elif 'лайн' in tag.string:
                data['presentType'] = tag.string
    except AttributeError:
        pass

    data['audience'] = ''
    try:
        course_for_tag = block_tag.find(string=re.compile(r'(для кого этот курс)|(курс для)|(кому.*курс)', re.I | re.U)).parent.parent
        audience = re.sub(r'\s+', ' ', course_for_tag.get_text(separator=' '), flags=re.M).strip()
        data['audience'] = re.sub(r'(^.+\?)', '', audience, flags=re.M | re.I)
    except AttributeError:
        pass

    data['benefits'] = ''
    try:
        benefit_top_tag = block_tag.find(string=re.compile(r'результат.*получите', re.I))
        if benefit_top_tag is None:
            benefit_top_tag = block_tag.find(string=re.compile(r'даст.*курс', re.I))
        if benefit_top_tag is None:
            benefit_top_tag = block_tag.find(string=re.compile(r'особенности программы', re.I))
        if benefit_top_tag is None:
            benefit_top_tag = block_tag.find(string=re.compile(r'курсе.*ждет', re.I))

        benefits_tag = benefit_top_tag.parent.parent
        benefits_text = re.sub(r'(^.+\?)', '', benefits_tag.get_text(separator=' '), flags=re.M | re.I)
        data['benefits'] = re.sub(r'\s+', ' ', benefits_text, flags=re.M).strip()
    except AttributeError:
        pass

    data['plan'] = ''
    try:
        course_plan_tag = block_tag.find('h2', string=re.compile(r'программа', re.I | re.U)).parent.parent
        course_plan_text = course_plan_tag.get_text(separator=' ')
        course_plan_text = re.sub(r'программа|ступень|тема|дз|(/+)|([0-9]+)|:', '', course_plan_text, flags=re.I | re.M)
        data['plan'] = re.sub(r'\s+', ' ', course_plan_text, flags=re.M).strip()
    except AttributeError:
        pass

    # todo стоимость вакансий на рынке

    data['priceFull'] = 0
    data['priceDisc'] = 0
    prices = block_tag.find(string=re.compile(r'полная стоимость', re.I | re.U))
    if prices is not None:
        prices_tag = prices.parent.parent
        prices = re.findall(r'\d+\s*\d+', prices_tag.get_text(separator=' ', strip=True))
        prices = list(map(lambda p: int(re.sub(r'\s+', '', p.replace('\xa0', ''))), prices))
        if len(prices) > 1:
            data['priceFull'] = prices[1]
            data['priceDisc'] = prices[0]
        elif len(prices) == 1:
            data['priceFull'] = prices[0]

    data['pending'] = False
    is_pending = block_tag.find(string=re.compile('сообщить о старте', re.I))
    if is_pending is not None:
        data['pending'] = True

    return data


if __name__ == '__main__':
    with open('errors/itsm.html') as f:
        soup = BeautifulSoup(f, 'html.parser')
        item = grab_data(soup)
        print(item)


