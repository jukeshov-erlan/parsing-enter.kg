from bs4 import BeautifulSoup as bs
import requests
import csv

def get_html(url):
    response = requests.get(url)
    return response.text


def get_total_page(html):
    soup = bs(html, 'lxml')
    page = soup.find('li', class_ = 'pagination-end').find('a').get('href')
    page = page.split('-')[-1]
    return page


def get_data(html):
    soup = bs(html, 'lxml')
    product_list = soup.find_all('div', class_ = 'row')
    for product in product_list:
        try:
            title  = product.find('div', class_ = 'rows').text
            # print(title)
            # print(product_list)
        except:
            title = ''
        try:
            price = product.find('span', class_ = 'price').text
            # print(price)
        except:
            price = ''
        try:
            img = product.find('img').get('src')
            img = 'https://enter.kg' + img
            # print(img)
        except:
            img = ''

        data = {
            'title': title,
            'price': price,
            'image': img
        }

        write_to_csv(data)


def write_to_csv(data):
    with open('db.csv', 'a') as file:
        writer = csv.writer(file)
        # writer.writerow(['title',  'price',   'image'])
        writer.writerow([data['title'],
                         data['price'],
                         data['image']])


def main():
    url = 'https://enter.kg/computers/noutbuki_bishkek'
    html = get_html(url)
    get_data(html)
    page = get_total_page(html)
    for i in range(100, int(page)+1, 100):
        # print(i)
        url = f'https://enter.kg/computers/noutbuki_bishkek/results,{i+1}-{i}'
        # print(url)
        html = get_html(url)
        get_data(html)

main()



