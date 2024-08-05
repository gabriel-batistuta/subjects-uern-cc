from bs4 import BeautifulSoup
from requests import get
from typing import Union
import json

def get_page(url:str) -> BeautifulSoup:
    return BeautifulSoup(get(url).content, 'html.parser')

def get_page_soup(url: Union[str, BeautifulSoup]) -> BeautifulSoup:
    if isinstance(url, str):
        page = get_page(url)
    else:
        page = url
    return page

def get_course_info(course_url: Union[str, BeautifulSoup]) -> dict:
    page = get_page_soup(course_url)
    container = page.find('table', {'class': 'table table-striped table-condensed'})
    trs_tags = container.find_all('tr')

    course_info = {}
    for tr in trs_tags:
        key = tr.find('th').text.strip().replace(':', '').lower().strip()
        value = tr.find('td').text.strip()
        course_info[key] = value
    
    return course_info

def get_hours_info(course_url: Union[str, BeautifulSoup]) -> dict:
    page = get_page_soup(course_url)
    container = page.find_all('table', {'class': 'table table-striped table-condensed'})[1]
    trs_tags = container.find_all('tr')

    hours_dict = {}
    for tr in trs_tags:
        key = tr.find('th').text.strip().replace(':', '').lower().strip()
        value = tr.find('td').text.strip()
        hours_dict[key] = value
    
    return hours_dict

def get_subjects(course_url: Union[str, BeautifulSoup]) -> list[dict]:
    page = get_page_soup(course_url)
    container = page.find('table', {'class': 'table table-striped table-condensed', 'style':'font-size:12px;'})
    # print(container.prettify())
    trs_tags = container.find_all('tr')
    header_row = trs_tags[0]
    headers = header_row.find_all('th')
    subjects_headers = [] 
    for head in headers:
        subjects_headers.append(head.text.strip())
    
    trs_tags.pop(0)
    subjects_list = []
    for tr in trs_tags:
        subject = {}
        td_tags = tr.find_all('td')
        if len(td_tags) < 5:
            continue
        for key, value in zip(subjects_headers, td_tags):
            if key == '' and value.text.strip() == '':
                continue
            else:
                subject[key] = value.text.strip()
            # subject[head] = td_tags[subjects_headers[i]].text.strip()
        subjects_list.append(subject)

    return subjects_list

def make_json(course:dict) -> None:
    with open('course_info.json', 'w') as f:
        json.dump(course, f, indent=4, ensure_ascii=False)