import json
import requests
from bs4 import BeautifulSoup


def get_parsed_page(url: str) -> object:
    parser = "html.parser"
    try:
        req = requests.get(url)
    except requests.exceptions.RequestException:
        return None
    status_code = str(req.status_code)
    if status_code.startswith('2'):
        return BeautifulSoup(req.text, parser)
    else:
        return None


def get_product_name_info_auchan(soup: object) -> str:
    try:
        info = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))
    except ValueError:
        return ''
    else:
        return info['name']


def get_product_price_info_auchan(soup: object) -> int:
    try:
        info = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))
    except ValueError:
        return 0
    else:
        try:
            price = float(info['offers']['price'])
            price = int(price)
        except (TypeError, ValueError):
            return 0
        else:
            return price


def get_product_info(url: str):
    product = {'name': '', 'price': 0, 'shop': ''}
    soup = get_parsed_page(url=url)
    if soup is not None:
        product_name = get_product_name_info_auchan(soup=soup)
        product_price = get_product_price_info_auchan(soup=soup)
        if product_name != '' and product_price != 0:
            product['name'] = product_name
            product['price'] = product_price
            product['url'] = url
            return product
        else:
            return None
    else:
        return None


def main():
    product = get_product_info("https://online.auchan.hu/shop/elelmiszer/italok-kakao-tea-kave/kave-es-kaveizesito/szemes-kave/tchibo-barista-espresso-szemes-porkolt-kave-1000-g.p121693/992173.v3658888")
    if product is not None:
        print(f'product name: {product["name"]}')
        print(f'product price: {product["price"]}')


if __name__ == "__main__":
    main()