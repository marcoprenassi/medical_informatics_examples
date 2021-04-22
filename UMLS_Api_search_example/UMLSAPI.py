#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:33:12 2021

@author: saramarceglia
@author: marcoprenassi (Object Oriented reformat)
"""

import requests
import json
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import datetime

"""
This is an Object Oriented experiment for UMLS - APIs
"""


# static hardcoded file system config class
class Config:
    ticket_granting_ticket_filename = 'TGT.txt'


# static class to collect all the url compositions (and api key)
class RESTUrlAndHeader:
    api_key = None
    url_target = "https://utslogin.nlm.nih.gov/cas/v1/api-key"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)" \
                            " AppleWebKit/537.36 (KHTML, like Gecko) " \
                            "Chrome/39.0.2171.95 Safari/537.36"
    data = "service=http%3A%2F%2Fumlsks.nlm.nih.gov"
    cui_url = "https://uts-ws.nlm.nih.gov/rest/content/current/CUI/"
    search_page_url = "https://uts-ws.nlm.nih.gov/rest/search/current?string="
    ticket_granting_ticket_expires_in = 8 #hours


# APIKeyRequest: POST to get a ticket granting ticket (TGT) (valid up to 8 hours)
class APIKeyRequest:
    tag = None
    api_key = None
    timestamp = None

    def __init__(self, api_key):
        self.api_key = api_key

    def check_ticket_granting_ticket(self):
        file_pointer = None
        try:
            file_pointer = open(Config.ticket_granting_ticket_filename, 'r+')
        except FileNotFoundError:
            try:
                file_pointer = open('TGT.txt', 'w')
                print('Ticket Granting Ticket non found, creating new file: TGT.txt')
                url_st = self.post()
                json.dump([datetime.datetime.now().isoformat(), url_st], file_pointer)
                file_pointer.close()
                return url_st
            except ValueError:
                print('TGT.txt not found and folder not accessible')
        try:
            json_ticket_granting_ticket = json.load(file_pointer)
            if json_ticket_granting_ticket[1] is None:
                print('empty file, requesting new Ticket Granting Ticket')
                url_st = self.post()
                json.dump([datetime.datetime.now().isoformat(), url_st], file_pointer)
            else:
                time_before = datetime.datetime.fromisoformat(json_ticket_granting_ticket[0])
                timespan = (datetime.datetime.now() - time_before)
                print(timespan)
                if timespan >= datetime.timedelta(hours=RESTUrlAndHeader.ticket_granting_ticket_expires_in):
                    print("Old request, requesting a new Ticket Granting Ticket")
                    url_st = self.post()
                    json.dump([datetime.datetime.now().isoformat(), url_st], file_pointer)
                else:
                    print("Request still valid until ", (time_before + datetime.timedelta(hours=8)).isoformat())
                    return json_ticket_granting_ticket[1]
        except IOError:
            print(ValueError.args, "  Something bad happened")
        finally:
            file_pointer.close()

    def post(self):
        data = "apikey=" + self.api_key
        apiKeyRequestObject = requests.post(RESTUrlAndHeader.url_target, headers=RESTUrlAndHeader.headers, data=data)
        soup = BeautifulSoup(apiKeyRequestObject.text, features="html.parser")
        tag = soup.form
        url_st = tag.attrs['action']
        return url_st


# APISingleTicket: POST to get the service single ticket from the
# ticket-granting ticket, single operation
class APISingleTicket:
    api_key = None
    apiKeyRequestObject = None

    # post granting ticket to obtain the single ticket
    def __init__(self, api_key):
        self.apiKey = api_key
        self.apiKeyRequestObject = APIKeyRequest(api_key)

    def ticket(self):
        url_st = self.apiKeyRequestObject.check_ticket_granting_ticket()
        resp_post_st = requests.post(url_st, headers=RESTUrlAndHeader.headers, data=RESTUrlAndHeader.data)
        return resp_post_st.text


class UMLSAPI:
    apiKeyObject = None
    apiSingleTicketObject = None
    result_list_dataframe = None

    def __init__(self, api_key):
        RESTUrlAndHeader.api_key = api_key
        self.apiKeyObject = APIKeyRequest(api_key=api_key)
        self.apiSingleTicketObject = APISingleTicket(api_key=api_key)

    @staticmethod
    def compose_cui(cui):
        return RESTUrlAndHeader.cui_url + cui + "?"

    def test_cui(self):  # GET term from CUI
        TEST_CUI = "C0009044"
        add_ticket = self.compose_cui(cui=TEST_CUI) + "ticket=" + self.apiSingleTicketObject.ticket()
        resp_get_cui = requests.get(add_ticket)
        cui_resp = resp_get_cui.json()
        cui_def = cui_resp['result']
        cui_name = cui_def['name']
        print(json.dumps(cui_def) + " --- " + json.dumps(cui_name))

    def search(self, search_term):
        # GET CUI from term (a new ST should be requested!)
        ticket_string = self.apiSingleTicketObject.ticket()
        base_get_url = RESTUrlAndHeader.search_page_url + search_term + "&ticket=" + ticket_string
        resp_get_term = requests.get(base_get_url)
        term_response = resp_get_term.json()
        response_result = term_response['result']
        result_list = response_result['results']
        self.result_list_dataframe = pd.DataFrame(result_list)
        return result_list

    def __str__(self):
        table = tabulate(self.result_list_dataframe, headers=['CUI', 'Source Dictionary', 'URI', 'Name'],
                         tablefmt='fancy_grid')
        return table
