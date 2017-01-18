def fail():
    raise RuntimeError()

def parse_html(html):
    from bs4 import BeautifulSoup

    b=BeautifulSoup(html, "html.parser")
    if not b:
        fail()
    if not len(b.select("html"))==1:
        fail()

    return b