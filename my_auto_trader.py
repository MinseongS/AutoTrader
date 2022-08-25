import pyupbit
import time
import schedule
import datetime
import logging

# ## 텔레그램 토큰키와 챗아이디를 가지고 있으면 아래의 각각 항목에 대입해주고
# bot = telegram.Bot(token='텔레그램토큰키')  # 본인의 텔레그램 토큰키  넣으세요.
# chat_id = 00000000  # 본인의 텔레그램 챗아이디 넣으세요.
#
#
# def post_message(text):
#     bot.sendMessage(chat_id=chat_id, text=text)  # 텔레그램 알림으로 변경함.
#     print(text)


access = "FPaArdbeEikSluRjR2bn4kniZyY8Gxmd2JpHoTDv"  # upbit 에서 받은 본인의 엑세스키  넣으세요.
secret = "7ZgMctz3Z8Ccwt3ARxwBdg2kIx4xxksDuVWJGPDZ"  # upbit 에서 받은 본인의 시크릿키  넣으세요.


# 로그인
upbit = pyupbit.Upbit(access, secret)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


def trade(num):
    now = datetime.datetime.now()
    file_handler = logging.FileHandler(f"./log{now.year}{now.month}{now.day}.txt")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    cur_val = {}

    asset = get_asset(cur_val)

    trade_list = get_rank(num)

    post_val = {coin: asset * (0.8/num) for coin, _ in trade_list}

    logger.info(f"Total value : {asset:,.0f}")

    sell_list = set(cur_val.keys()) - set(post_val.keys())
    buy_list = set(post_val.keys()) - set(cur_val.keys())
    check_list = set(cur_val.keys()).intersection(set(post_val.keys()))

    logger.info(f"sell list {sell_list}")
    logger.info(f"buy list {buy_list}")
    logger.info(f"check list {check_list}")
    logger.info(f"cur val {cur_val}")
    logger.info(f"post val {post_val}")

    for coin in sell_list:
        volume = (cur_val[coin]) / pyupbit.get_current_price(coin)
        # res = upbit.sell_market_order(coin, volume)
        time.sleep(0.1)
        logger.info(f"sell \t{coin} \t{cur_val[coin]:,.0f} \t{pyupbit.get_current_price(coin):,.0f}")

    for coin in buy_list:
        # res = upbit.buy_market_order(coin, cur_val[coin])
        time.sleep(0.1)
        logger.info(f"buy \t{coin} \t{post_val[coin]:,.0f} \t{pyupbit.get_current_price(coin):,.0f}")

    for coin in check_list:
        if cur_val[coin] < post_val[coin]:
            # res = upbit.buy_market_order(coin, post_val[coin] - cur_val[coin])
            time.sleep(0.1)
            logger.info(f"buy \t{coin} \t{post_val[coin] - cur_val[coin]:,.0f} \t{pyupbit.get_current_price(coin):,.0f}")
        else:
            volume = (cur_val[coin] - post_val[coin]) / pyupbit.get_current_price(coin)
            # res = upbit.sell_market_order(coin, volume)
            time.sleep(0.1)
            logger.info(f"sell \t{coin} \t{cur_val[coin] - post_val[coin]:,.0f} \t{pyupbit.get_current_price(coin):,.0f}")
    return


def get_asset(cur_val):
    balances = upbit.get_balances()
    total = 0
    for b in balances:
        if b['currency'] == 'KRW':
            total += float(b['balance'])
        else:
            coin = b['currency']
            ticker = 'KRW-' + coin
            cur_price = pyupbit.get_current_price(ticker)
            temp = cur_price * float(b['balance'])
            total += temp
            cur_val[ticker] = temp
    return total


def get_rank(num):
    currency_amount = []
    krw_tickers = pyupbit.get_tickers(fiat="KRW")
    # print(krw_tickers, len(krw_tickers))
    # temp = pyupbit.get_ohlcv("KRW-EOS", count=24, interval='minute60')
    # print(temp)
    for cur in krw_tickers:
        temp = pyupbit.get_ohlcv(cur, count=24, interval='minute60')
        if temp is not None:
            currency_amount.append((cur, sum(temp['value'])))
        else:
            print(cur)
        time.sleep(0.1)
    currency_amount.sort(key=lambda x: -x[1])
    logger.info(currency_amount[:num])
    return currency_amount[:num]

trade(5)

schedule.every(60).minutes.do(trade, 5)

while True:
    schedule.run_pending()
    time.sleep(1)

