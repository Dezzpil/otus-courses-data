

def scrape_course_page(content: str):
    # block = body > div.__next > divs[1] > main > divs[0]
    # top = block > section
    #   head = top > divs[1] > divs[1] > divs[1]
    #     title = top > h1 -> text
    #     promo = top > divs[1] -> text
    #   props = top > divs[2]
    #     texts[0...4] -> startAt, level, duration_month, type, schedule
    # vdesc = block > div#vdescription
    #   find text "Для кого этот курс?": -> forwhom
    #   vdesc ul li -> pre_knowledge[]
    #   пропускаю блок "при поддержке" @todo
    # middle = vdesc.sibling
    #   will_give = "Что даст вам этот курс?" + next text
    #   you_will_can[] = middle > ul > li -> text[]
    #
    # course = block > text = "Программа" . sibling -> all text
    # можно еще собрать данные о партнерах
    # можно еще собрать данные об авторах
    # и отзывы?
    # prices[] = block > find text "Полная стоимость со скидкой" . sibling + next texts
    pass
