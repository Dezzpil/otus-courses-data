import sqlite3

ddl = '''
CREATE TABLE IF NOT EXISTS courses(
  slug text primary key,
  title text,
  promo text,
  duration int,
  presentType text,
  audience text,
  benefits text,
  plan text,
  priceFull int,
  priceDisc int,
  pending bool
)
'''

# ddl = 'DROP TABLE courses'

if __name__ == '__main__':
    con = sqlite3.connect("otus.db")
    cur = con.cursor()
    cur.execute(ddl)
    print(cur.execute('select count(*) from courses').fetchall())
