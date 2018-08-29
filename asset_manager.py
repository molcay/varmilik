import json
from typing import Dict, Type
from functools import reduce
from tabulate import tabulate
from currency_checker import CurrencyChecker


class Asset:
    def __init__(self, name: str, amount: float or int, price: float or int, unit_price: float or int):
        self.name = name
        self.amount = float(amount)
        self.price = float(price)
        self.unit_price = float(unit_price)
    
    def __repr__(self):
        return f"{self.name} => A: {self.amount}, P: {self.price}, UP: {self.unit_price}"
    
    def __add__(self, c):
        return Asset(self.name, self.amount + c.amount, self.price + c.price, (self.unit_price + c.unit_price) / 2)


class AssetManager:
    __FIELD_LIST_FOR_TOTAL = ['prices', 'now', 'profits']
    __MAIN_SEPARATOR = "#" * 75
    __SUB_SEPARATOR = "#" * 50

    def __init__(self, arg):
        self.arg = arg
        self.file = arg.file
        self.data = self.asset_from_transactions()
        self.checker = CurrencyChecker(list(self.data.keys()))
        self.total = { 'currency_list': [] }
        self.total.update({f: [] for f in self.__FIELD_LIST_FOR_TOTAL })

    def asset_from_transactions(self) -> Dict[str, any]:
        with open(self.file, 'r') as fh: # TODO: handle not found file case
            transactions = json.loads(fh.read())

        data = {}
        for asset_name, txns in transactions.items():
            asset = []
            for txn in txns:
                sorted_by_value = sorted(txn.items(), key=lambda kv: kv[0])
                params = list(map(lambda x: x[1], sorted_by_value))
                asset.append(Asset(asset_name, *params))

            res = reduce(lambda x1, x2: x1 + x2, asset)
            data[asset_name] = res
        
        return data
    
    def calculate_total(self):
        ttl = { k: round(sum(self.total[k]), 2) for k in self.__FIELD_LIST_FOR_TOTAL }

        # print("""TOTAL:
        #     Paid: {prices}  TL
        #     Have: {now}  TL
        #     Profit: {profits}  TL""".format(**ttl))
        # print(self.__MAIN_SEPARATOR)
        return ttl

    def run(self) -> None:
        currencies = self.checker.get()        
        self.total['currency_list'] = list([f"{ck} ({cv.price})" for ck, cv in currencies.items()]) + ["TOTAL"]

        for k, v in currencies.items():
            my_asset = self.data[k]
            now_asset_in_try, price, profit = (round(p, 2) for p in [
                    my_asset.amount * v.price, 
                    my_asset.price, 
                    (my_asset.amount * v.price) - my_asset.price
                ])
            
            # print(self.__MAIN_SEPARATOR)
            # print(f"""{v}
            # {self.__SUB_SEPARATOR}
            # You Paid: {price} TL
            # You Have: {now_asset_in_try} TL
            # Your Profit: {profit} TL
            # {self.__SUB_SEPARATOR}""")
            self.total['prices'].append(price)
            self.total['now'].append(now_asset_in_try)
            self.total['profits'].append(profit)
        
        ttl = self.calculate_total()
        for t, k in ttl.items():
            self.total[t].append(k)

        print(tabulate(self.total, ["Paid", "Have", "Profit"], tablefmt="fancy_grid"))
        