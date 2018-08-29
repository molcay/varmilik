import requests
from typing import List
from pyquery import PyQuery
from abc import ABC, abstractmethod


class BaseCurrency(ABC):
    @abstractmethod
    def set_price(self, price):
        pass


class CurrencyOnEnPara(BaseCurrency):
    def __init__(self, name, transaction_type, selector):
        self.name = name
        self.transaction_type = transaction_type
        self.selector = selector
        self.price = None
    
    def set_price(self, price_as_str):
        self.price = float(price_as_str.replace(" TL", "").replace(",", "."))

    def __repr__(self):
        return f"{self.name} {self.transaction_type} {self.price}"


class CurrencyChecker:
    def __init__(self, currency_list: List[str]):
        self.currency_list = currency_list
    
    def __repr__(self):
        return f"Currency Checker for {', '.join(self.currency_list)}"
    
    def set_price(self, cur, price):
        cur.set_price(price)
        return cur
    
    def set_pq(self, response):
        self.pq = PyQuery(response.text)
    
    def select(self, selector):
        return self.pq(selector).text()

    def get(self):
        """
        # dolar_alis = CurrencyOnEnPara("USD", "Alış", "#pnlContent > span:nth-child(1) > dl:nth-child(1) > dd:nth-child(2) > div:nth-child(1) > span:nth-child(1)")
        # dolar_satis = CurrencyOnEnPara("USD", "Satış", "#pnlContent > span:nth-child(1) > dl:nth-child(1) > dd:nth-child(3) > div:nth-child(1) > span:nth-child(1)")
        # euro_alis = CurrencyOnEnPara("EUR", "Alış", "#pnlContent > span:nth-child(2) > dl:nth-child(1) > dd:nth-child(2) > div:nth-child(1) > span:nth-child(1)")
        # euro_satis = CurrencyOnEnPara("EUR", "Satış", "#pnlContent > span:nth-child(2) > dl:nth-child(1) > dd:nth-child(3) > div:nth-child(1) > span:nth-child(1)")
        # gold_alis = CurrencyOnEnPara("GOLD", "Alış", "#pnlContent > span:nth-child(3) > dl:nth-child(1) > dd:nth-child(2) > div:nth-child(1) > span:nth-child(1)")
        # gold_satis = CurrencyOnEnPara("GOLD", "Satış", "#pnlContent > span:nth-child(3) > dl:nth-child(1) > dd:nth-child(3) > div:nth-child(1) > span:nth-child(1)")
        """
        url = "https://www.qnbfinansbank.enpara.com/doviz-kur-bilgileri/doviz-altin-kurlari.aspx"
        resp = requests.get(url)
        self.set_pq(resp)
        
        currency_selectors = {
            'GOLD': CurrencyOnEnPara("GOLD", "Alış", "#pnlContent > span:nth-child(3) > dl:nth-child(1) > dd:nth-child(2) > div:nth-child(1) > span:nth-child(1)"),
            'USD': CurrencyOnEnPara("USD", "Alış", "#pnlContent > span:nth-child(1) > dl:nth-child(1) > dd:nth-child(2) > div:nth-child(1) > span:nth-child(1)"),
            'EUR': CurrencyOnEnPara("EUR", "Alış", "#pnlContent > span:nth-child(2) > dl:nth-child(1) > dd:nth-child(2) > div:nth-child(1) > span:nth-child(1)"),
        }

        return {
            c: self.set_price(sc, self.select(sc.selector)) for c, sc in currency_selectors.items() if c in self.currency_list
        }
