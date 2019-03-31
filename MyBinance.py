#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" mybinance.py - Shows specified cryptocurrency values """
# Copyright (c) 2017-2018 ardeshirv@protonmail.com, Licensed under GPLv3+
import time
import color
import urllib3
import platform
from MyBinanceAPI import *
# from binance.exceptions import *
from binance.client import Client


def main():
    print_title_and_copyright()
    try:
        print('Connecting ...')  # , end='')
        mb = MyBinance()
        warnings = errors = 0
        warning_waite_time = error_waite_time = 5
        prices = prev_prices = mb.get_prices()
        # c = mb.get_client()
        # print(c.get_asset_balance(asset='BNB'))
        while True:
            try:
                prices = mb.get_prices()
                if len(prices) == 0:
                    warnings += 1
                    print(('\rWarning-[{0}]: Binance.com dosen\'t respond.' +
                          ' Trying again afyer {1} second...').
                          format(warnings, warning_waite_time), end='')
                    time.sleep(warning_waite_time)
                    print('\r', end='')
                    continue
            except:
                errors += 1
                print(('\r\033[0;31mError-[{0}]: Connection failed.' +
                      ' Trying again after {1} second...\033[0m').
                      format(errors, error_waite_time), end='')
                time.sleep(error_waite_time)
                print('\r', end='')
                mb = MyBinance()
                continue
            BTCUSDT_value = float(prices['BTCUSDT'])
            prev_BTCUSDT_value = float(prev_prices['BTCUSDT'])
            if prev_BTCUSDT_value < BTCUSDT_value:
                color_BTCUSDT = color.BoldGreen
            elif prev_BTCUSDT_value > BTCUSDT_value:
                color_BTCUSDT = color.BoldRed
            else:
                color_BTCUSDT = color.BoldWhite
            BNBUSDTT_value = float(prices['BNBUSDT'])
            prev_BNBUSDTT_value = float(prev_prices['BNBUSDT'])
            if prev_BNBUSDTT_value < BNBUSDTT_value:
                color_BNBUSDTT = color.BoldGreen
            elif prev_BNBUSDTT_value > BNBUSDTT_value:
                color_BNBUSDTT = color.BoldRed
            else:
                color_BNBUSDTT = color.BoldWhite
            NANOBTC_value = float(prices['NANOBTC'])
            prev_NANOBTC_value = float(prev_prices['NANOBTC'])
            if prev_NANOBTC_value < NANOBTC_value:
                color_NANOBTC = color.BoldGreen
            elif prev_NANOBTC_value > NANOBTC_value:
                color_NANOBTC = color.BoldRed
            else:
                color_NANOBTC = color.BoldWhite
            message = ((
                '\033[0;37mBTCUSD\033[0m: {0}{1:.2f}\033[0m, \033[0;37m' +
                'BNBUSDT\033[0m: {2}{3:.2f}\033[0m, \033[0;37mNANOUSD' +
                '\033[0m: {4}{5:.2f}\033[0m').format(
                     color_BTCUSDT, float(prices['BTCUSDT']),
                     color_BNBUSDTT, float(prices['BNBUSDT']),
                     color_NANOBTC, float(prices['NANOBTC']) *
                     float(prices['BTCUSDT'])))
            prev_prices = prices.copy()
            print('\n{0}'.format(message), end='')
            time.sleep(1)
        print(color_norm, end='')
        # print(mb.client.get_withdraw_history())
        # mb.aggregated_trade_websocket('NANOBTC')
        return 0
    except Exception as exp:
        print('\n\033[0;31m{0}\n{1}\033[0m'.format('Error:', str(exp)))
        return -1  # raise exp
    finally:
        print('\033[0m', end='')


class MyBinance:
    def __init__(self):
        urllib3.disable_warnings()
        self.client = Client(get_api_key(), get_api_secret(),
                             {"verify": False, "timeout": 20})

    def get_client(self):
        return self.client

    def get_prices(self):
        dict_prices = {}
        list_prices = self.client.get_all_tickers()
        for item in list_prices:
            # dict_prices.setdefault(item['symbol'], item['price'])
            dict_prices[item['symbol']] = item['price']
        return dict_prices

    def aggregated_trade_websocket(self, str_index):
        # start aggregated trade websocket for NANOBTC
        def process_message(msg):
            print("message type: {0}".format(msg['e']))
            print(msg)
        # do something
        from binance.websockets import BinanceSocketManager
        bm = BinanceSocketManager(self.client)
        bm.start_aggtrade_socket(str_index, process_message)
        bm.start()

    def acts(self):
        # get market depth
        depth = self.client.get_order_book(symbol='NANOBTC')
        # place a test market buy order, to place
        # an actual order use the create_order function
        order = self.client.create_test_order(
            symbol='NANOBTC',
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=100)
        # get all symbol prices
        prices = self.client.get_all_tickers()
        # withdraw 100 ETH
        # check docs for assumptions around withdrawals
        from binance.exceptions import BinanceAPIException
        from binance.exceptions import BinanceWithdrawException
        try:
            result = self.client.withdraw(
                asset='ETH',
                address='<eth_address>',
                amount=100)
        except BinanceAPIException as e:
            print(e)
        except BinanceWithdrawException as e:
            print(e)
        else:
            print("Success")
        # fetch list of withdrawals
        withdraws = self.client.get_withdraw_history()
        # fetch list of ETH withdrawals
        eth_withdraws = self.client.get_withdraw_history(asset='ETH')
        # get a deposit address for BTC
        address = self.client.get_deposit_address(asset='BTC')

        # get historical kline data from any date range
        # fetch 1 minute klines for the last day up until now
        klines = self.client.get_historical_klines(
            "NANOBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
        # fetch 30 minute klines for the last month of 2017
        klines = self.client.get_historical_klines(
            "BNBUSD", Client.KLINE_INTERVAL_30MINUTE,
            "1 Dec, 2017", "1 Jan, 2018")
        # fetch weekly klines since it listed
        klines = self.client.get_historical_klines(
            "NEOBTC", KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

    def distinct_currencies(self, string_symbol):
        den = num = ''
        if string_symbol.endswith('BTC'):
            den = 'BTC'
            num = string_symbol[:-3]
        elif string_symbol.endswith('ETH'):
            den = 'ETH'
            num = string_symbol[:-3]
        elif string_symbol.endswith('BNB'):
            den = 'BNB'
            num = string_symbol[:-3]
        elif string_symbol.endswith('USDT'):
            den = 'USDT'
            num = string_symbol[:-4]
        return (num, den)


def print_title_and_copyright():
    blnColor = False if (platform.system() == 'Windows') else True
    strAppName = "MyBinance"
    strAppYear = "2017-2018"
    strAppDescription = "Shows specified cryptocurrency values"
    strVersion = "1.0"
    strLicense = "GPLv3+"
    strCopyright = "ardeshirv@protonmail.com"
    print(FormatTitle(strAppName, strAppDescription, strVersion, blnColor))
    print(FormatCopyright(strAppYear, strCopyright, strLicense, blnColor))


def FormatTitle(strAppName, strAppDescription, strVersion, blnColor):
    NoneColored = "{} - {} Version {}\n"
    Colored = "\033[1;33m{}\033[0;33m - {} \033[1;33mVersion {}\033[0m"
    strFormat = Colored if blnColor else NoneColored
    return strFormat.format(strAppName, strAppDescription, strVersion)


def FormatCopyright(strAppYear, strCopyright, strLicense, blnColor):
    NoneColored = "Copyright (c) {} {}, Licensed under {}\n\n"
    Colored = ("\033[0;33mCopyright (c) \033[1;33m{} \033[1;34m{}" +
               "\033[0;33m, Licensed under \033[1;33m{}\033[0m\n")
    strFormat = Colored if blnColor else NoneColored
    return strFormat.format(strAppYear, strCopyright, strLicense)


if __name__ == "__main__":
    from sys import exit
    exit(main())


'''
sudo pip3 install -U cryptography
'''
