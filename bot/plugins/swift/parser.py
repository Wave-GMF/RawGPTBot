import requests
import random
from lxml import html

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/89.0"
]

header_xpath = '/html/body/div[1]/div/main/div/div[1]/section/div/div/div[1]/div/div[1]/h1'
body_xpath = '/html/body/div[1]/div/main/div/div[1]/section/div/div/div[1]/div/div[1]/h2'
bank_xpath = '/html/body/div[1]/div/main/div/div[1]/section/div/div/div[1]/div/div[1]/p'

def fetch_html(url: str) -> list[int, str]:
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return [200, response.text]
        elif response.status_code == 404:
            return [404, ""]
        else:
            return [response.status_code, ""]
            
    except requests.exceptions.RequestException as e:
        print(str(e))
        return [response.status_code, str(e)]
    
def parse_swift(swift_code=str) -> str:
    swift_url = f'https://wise.com/gb/swift-codes/{swift_code}'

    code, content = fetch_html(swift_url)

    if code == 404:
        return 'Wrong swift code'
    
    if code != 200:
        return f'Parse error\n {code} - {content}'
    
    tree = html.fromstring(content)

    header = tree.xpath(header_xpath)
    body = tree.xpath(body_xpath)
    bank = tree.xpath(bank_xpath)

    if len(header) == 0 or len(body) == 0 or len(bank) == 0:
        return 'Site layout has been changed'

    return f'{header[0].text_content()}\n{body[0].text_content()}\n\n{bank[0].text_content()}'