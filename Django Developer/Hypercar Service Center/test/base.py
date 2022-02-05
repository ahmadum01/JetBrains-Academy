# -*- coding: utf-8 -*-
import http.cookiejar
import io
import os
import re
import sqlite3
import urllib
from urllib.request import urlopen

import requests

from hstest import CheckResult, DjangoTest


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))



class HyperCarTest(DjangoTest):

    use_database = False

    COMMON_LINK_PATTERN = '''<a[^>]+href=['"]([a-zA-Z\d/_]+)['"][^>]*>'''
    CSRF_PATTERN = '<input[^>]+name="csrfmiddlewaretoken" ' \
                   'value="(?P<csrf>\w+)"[^>]*>'
    GROUPS_FIRST_PATTERN = '<h4>.*?</h4>.*?<ul>.+?</ul>'
    GROUPS_SECOND_PATTERN = (
        '''<a[^>]+href=['"]([a-zA-Z\d/_]+)['"][^>]*>(.+?)</a>'''
    )
    H2_PATTERN = '<h2>(.+?)</h2>'
    LINK_WITH_TEXT_PATTERN = '''<a[^>]+href=['"]([a-zA-Z\d/_?=]+)['"][^>]*>(.+?)</a>'''
    PARAGRAPH_PATTERN = '<p>(.+?)</p>'
    SRC_PATTERN = '''<source[^>]+src=['"]([a-zA-Z\d/_.]+)['"][^>]*>'''
    DIV_PATTERN = '''<div[^>]*>(.+?)</div>'''
    TEXT_LINK_PATTERN = '''<a[^>]+href=['"][a-zA-Z\d/_]+['"][^>]*>(.+?)</a>'''
    cookie_jar = http.cookiejar.CookieJar()
    USERNAME = 'Test'
    PASSWORD = 'TestPassword123'
    TAG = 'testtag'

    def check_main_header(self) -> CheckResult:
        try:
            page = self.read_page(self.get_url() + 'welcome/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        h2_headers = re.findall(self.H2_PATTERN, page, re.S)
        h2_headers = self.__stripped_list(h2_headers)
        main_header = 'Welcome to the Hypercar Service!'

        is_main_header = False
        for h2_header in h2_headers:
            if main_header in h2_header:
                is_main_header = True
                break

        if not is_main_header:
            return CheckResult.wrong(
                'Main page should contain <h2> element with text "Welcome to the Hypercar Service!"'
            )

        return CheckResult.correct()

    def check_menu_page_links(self):

        menu_links = ["/get_ticket/change_oil","/get_ticket/inflate_tires","/get_ticket/diagnostic"]

        try:
            page = self.read_page(self.get_url() + 'menu/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        links_from_page = re.findall(self.LINK_WITH_TEXT_PATTERN, page, re.S)
        links_from_page = self.__stripped_list_with_tuple(links_from_page)
        print(links_from_page)
        for link in menu_links:
            if link not in links_from_page:
                return CheckResult.wrong(
                    f'Menu page should contain <a> element with href {link}'
                )

        return CheckResult.correct()
    def check_ticket_page_links(self):

        ticket_links = ["get_ticket/inflate_tires","get_ticket/change_oil","get_ticket/change_oil","get_ticket/inflate_tires","get_ticket/diagnostic"]
        result_check = ["Please wait around 0 minutes","Please wait around 0 minutes","Please wait around 2 minutes","Please wait around 9 minutes","Please wait around 14 minutes"]

        i = 0

        for link in ticket_links:
            try:
                divs_from_page = re.findall(self.DIV_PATTERN, self.read_page(self.get_url() + link), re.S)
            except urllib.error.URLError:
                return CheckResult.wrong(
                    f'Cannot connect to the {link}.'
                )
            divs_from_page = self.__stripped_list(divs_from_page)
            if result_check[i] not in divs_from_page:
                return CheckResult.wrong(
                    f'Page page should contain {result_check[i]}'
                )
            i+=1

        return CheckResult.correct()


    def check_ticket_page_links_with_menu(self):

        ticket_links = ["get_ticket/inflate_tires","get_ticket/change_oil","get_ticket/change_oil","get_ticket/inflate_tires","get_ticket/diagnostic"]
        result_check = ["Please wait around 0 minutes","Please wait around 0 minutes","Please wait around 2 minutes","Please wait around 9 minutes","Please wait around 14 minutes"]
        result_check_menu = ["Inflate tires queue: 1", "Change oil queue: 1", "Change oil queue: 2",
                        "Inflate tires queue: 2", "Get diagnostic queue: 1"]
        i = 0

        for link in ticket_links:
            try:
                divs_from_page = re.findall(self.DIV_PATTERN, self.read_page(self.get_url() + link), re.S)
            except urllib.error.URLError:
                return CheckResult.wrong(
                    f'Cannot connect to the {link}.'
                )
            divs_from_page = self.__stripped_list(divs_from_page)
            if result_check[i] not in divs_from_page:
                return CheckResult.wrong(
                    f'Page page should contain {result_check[i]}'
                )
            try:
                divs_from_page = re.findall(self.DIV_PATTERN, self.read_page(self.get_url() + "processing"), re.S)
            except urllib.error.URLError:
                return CheckResult.wrong(
                    f'Cannot connect to the  "/processing".'
                )
            divs_from_page = self.__stripped_list(divs_from_page)
            if result_check_menu[i] not in divs_from_page:
                print(divs_from_page)
                return CheckResult.wrong(
                    f'Page page should contain {result_check_menu[i]}'
                )
            i+=1

        return CheckResult.correct()

    def process_ticket(self):
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        try:
            response = opener.open(self.get_url() + 'processing')
        except urllib.error.URLError:
            return CheckResult.wrong('Not Found: /processing/')
        csrf_options = re.findall(
            b'<input[^>]+value="(?P<csrf>\w+)"[^>]*>', response.read()
        )
        if not csrf_options:
            return CheckResult.wrong('Missing csrf_token in the form')



        try:
            response = opener.open(
                self.get_url() + 'processing',
                data=urllib.parse.urlencode({'csrfmiddlewaretoken': csrf_options[0]}).encode()
            )
        except urllib.error.URLError as err:
            return CheckResult.wrong(f'Cannot signup: {err.reason}')
        return CheckResult.correct()

    def check_next(self):
        ticket_links = ["get_ticket/inflate_tires", "get_ticket/change_oil", "get_ticket/change_oil",
                        "get_ticket/inflate_tires", "get_ticket/diagnostic"]
        result_check = ["Please wait around 0 minutes", "Please wait around 0 minutes", "Please wait around 2 minutes",
                        'Please wait around 7 minutes', "Please wait around 10 minutes"]
        result_check_menu = ["Inflate tires queue: 1", "Change oil queue: 1", "Change oil queue: 2",
                             "Inflate tires queue: 2", "Get diagnostic queue: 1"]
        result_next = ["Waiting for the next client","Waiting for the next client","Next ticket #2","Next ticket #3","Next ticket #1"]
        next_open = [False, False, True, True, True]
        i = 0
        for link in ticket_links:
            try:
                divs_from_page = re.findall(self.DIV_PATTERN, self.read_page(self.get_url() + link), re.S)
            except urllib.error.URLError:
                return CheckResult.wrong(
                    f'Cannot connect to the page "{link}".'
                )
            divs_from_page = self.__stripped_list(divs_from_page)
            if result_check[i] not in divs_from_page:
                sep = "\n"
                return CheckResult.wrong(
                    f'Page "{link}" should contain "{result_check[i]}"\n'
                    f'Found the  following:\n'
                    f'{sep.join(divs_from_page)}'
                )
            if next_open[i]:
                result = self.process_ticket()
                if not result.correct():
                    return result
            try:
                divs_from_page = re.findall(self.DIV_PATTERN, self.read_page(self.get_url() + "next"), re.S)
            except urllib.error.URLError:
                return CheckResult.wrong(
                        f'Cannot connect to the "/next".'
                    )
            divs_from_page = self.__stripped_list(divs_from_page)
            if result_next[i] not in divs_from_page:
                return CheckResult.wrong(
                        f'Page not should contain {result_next[i]}'
                    )
            i += 1

        return CheckResult.correct()




    def __stripped_list(self, list):
        return [item.strip() for item in list]

    def __stripped_list_with_tuple(self, list):
        return [item[0].strip() for item in list]
