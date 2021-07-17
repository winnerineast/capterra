import requests
import urllib3
from bs4 import BeautifulSoup
import json


def start_requests(url):
    r = requests.get(url)
    return r.content


def parse_directory(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    movie_list = soup.find_all('a', class_='list-group-item')

    result_list = []
    for item in movie_list:
        software_type = {'title': item.text, 'url': item['href']}
        result_list.append(software_type)
    return result_list


def get_redirect_url(previous_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(previous_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    redirect_url = soup.find('meta', attrs={'http-equiv': 'refresh'})
    actual_url = redirect_url['content'].partition('=')[2]
    try:
        response = requests.get(actual_url, headers=headers)
    except urllib3.exceptions.MaxRetryError as ex:
        print("the website is down.")
        actual_url = str(ex).split('\'')[1]
        print(actual_url)
        return actual_url
    except requests.exceptions.SSLError as ex:
        print("the website is not connected with SSL.")
        actual_url = str(ex).split('\'')[1]
        print(actual_url)
        return actual_url
    return response.url


def parse_software(software_type, html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    item_list = soup.find_all('div', class_='card product-card mb-3 border-primary pt-2')
    result_list = []
    for item in item_list:
        title = item.find(class_='evnt').string
        print(title)
        visit_url = item.find(class_='btn btn-preferred btn-sm text-truncate btn-block evnt')['href']
        website = get_redirect_url('https://www.capterra.com.sg'+visit_url)
        summary = item.find(class_='d-lg-none').get_text()
        software_type = {'type': software_type, 'title': title, 'summary': summary, 'website': website}
        result_list.append(software_type)
    return result_list


def get_page_number(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    page_items = soup.find_all('li', class_='page-item')
    if bool(page_items):
        last_page = page_items[len(page_items) - 2].get_text()
        return int(last_page)
    return 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open('data.json', 'w', encoding='utf-8') as f:
        url = 'https://www.capterra.com.sg/directory'
        text = start_requests(url)
        directory = parse_directory(text)
        for current in directory:
            # print(current['url'])
            text = start_requests(current['url'])
            nPage = get_page_number(text)
            software_list = parse_software(current['title'], text)
            json.dump(software_list, f, ensure_ascii=False, indent=4)
            print(software_list)

            if 1 == nPage: continue

            for i in range(2, nPage + 1):
                new_url = current['url'] + '?page=' + str(i)
                print(new_url)
                text = start_requests(new_url)
                software_list = parse_software(current['title'], text)
                json.dump(software_list, f, ensure_ascii=False, indent=4)
                print(software_list)
