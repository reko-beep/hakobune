from requests import get
from bs4 import BeautifulSoup, NavigableString, Tag
import typing
import json  
from os.path import exists
import re
class Parser:
    def __init__(self) -> None:
        self.data = {

        }

        self.__load()
    
    def __load(self):
        if exists('tti.json'):
             
            with open('tti.json', 'r') as f:
                self.data = json.load(f)

    
    def find_image(self, text: str):

        matches = re.findall(r'<\w+>', text)
        if len(matches) > 0:
            for match in matches:

                to_find = match.replace('<','',99).replace('>','',99)
                for k, img in self.data.items():
                    if to_find.lower() in k.lower():
                        text = text.replace(f'<{to_find}>', img , 1)
        
        return text
    





