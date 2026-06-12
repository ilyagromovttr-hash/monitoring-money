import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class CBRService:
    @staticmethod
    def get_daily_rates():
        """Получает актуальные курсы валют на сегодняшний день."""
        url = "http://www.cbr.ru/scripts/XML_daily.asp"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return {}
            
            root = ET.fromstring(response.content)
            rates = {}
            for valute in root.findall('Valute'):
                char_code = valute.find('CharCode').text
                name = valute.find('Name').text
                value = valute.find('Value').text.replace(',', '.')
                nominal = float(valute.find('Nominal').text)
                
                rates[char_code] = {
                    'name': name,
                    'value': float(value) / nominal,
                    'id': valute.get('ID')
                }
            return rates
        except Exception:
            return {}

    @staticmethod
    def get_history(valute_id, date_start, date_end):
        """Получает историю курса валюты за указанный период (формат: DD/MM/YYYY)."""
        url = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date_start}&date_req2={date_end}&VAL_NM_RQ={valute_id}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return [], []
            
            root = ET.fromstring(response.content)
            dates = []
            values = []
            for record in root.findall('Record'):
                date_str = record.get('Date')
                value = record.find('Value').text.replace(',', '.')
                nominal = float(record.find('Nominal').text)
                
                dates.append(datetime.strptime(date_str, '%d.%m.%Y'))
                values.append(float(value) / nominal)
            return dates, values
        except Exception:
            return [], []