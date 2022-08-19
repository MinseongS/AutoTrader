import telegram
import pyupbit
import time
import schedule


# ## 텔레그램 토큰키와 챗아이디를 가지고 있으면 아래의 각각 항목에 대입해주고
# bot = telegram.Bot(token='텔레그램토큰키')  # 본인의 텔레그램 토큰키  넣으세요.
# chat_id = 00000000  # 본인의 텔레그램 챗아이디 넣으세요.
#
#
# def post_message(text):
#     bot.sendMessage(chat_id=chat_id, text=text)  # 텔레그램 알림으로 변경함.
#     print(text)
#
#
access = "Dddyixi3RpVjVD4XfIyP7xmIebpfKU1Xt4FKumpE"  # upbit 에서 받은 본인의 엑세스키  넣으세요.
secret = "aGItZYSG3xZJu1MCAbjpSBwfejMMTqFHQsDRBf4a"  # upbit 에서 받은 본인의 시크릿키  넣으세요.
#
# 로그인
upbit = pyupbit.Upbit(access, secret)
#
# # 임의로 5개 코인을 골랐으니 각자 맘에 드는 코인으로 변경해서 사용하세요.
# # 갯수는 상관 없습니다만 현금 시드가 확보되어 있어야 매수가 되겠지요...^^;
# # 아래는 샘플로 도지코인, 리플코인, 이더리움 코인, 이더리움 클래식 코인, 에이다 코인임
coins = ['BTC', 'ETH']
ratio = [0.6, 0.2]
#
#
balances = upbit.get_balances()
print(balances)
cur_price = pyupbit.get_current_price('KRW-BTC')
print(cur_price)
def get_asset():
    balances = upbit.get_balances()
    total = 0
    for b in balances:
        if b['currency'] == 'KRW':
            total += float(b['balance'])
        else:
            coin = b['currency']
            ticker = 'KRW-' + coin
            cur_price = pyupbit.get_current_price(ticker)
            total += cur_price * float(b['balance'])
    return total
print(get_asset())

# # 해당 코인 보유수량 반환
# def get_balance(coin):
#     """잔고 조회"""
#     balances = upbit.get_balances()
#     for b in balances:
#         if b['currency'] == coin:
#             if b['balance'] is not None:
#                 return float(b['balance'])
#             else:
#                 return 0
#         time.sleep(0.2)
#     return 0
#
#
# # 해당 코인 매수평균단가 반환
# def get_avg_buy_price(coin):
#     """잔고 조회"""
#     balances = upbit.get_balances()
#     for b in balances:
#         if b['currency'] == coin:
#             if b['avg_buy_price'] is not None:
#                 return float(b['avg_buy_price'])
#             else:
#                 return 0
#         time.sleep(0.2)
#     return 0
#
#
# # 시장가 매도 함수
# def sell(coin, percent):
#     amount = get_balance(coin)  # upbit.get_balance(coin)
#     ticker = 'KRW-' + coin
#     cur_price = pyupbit.get_current_price(ticker)
#     total = amount * cur_price
#
#     old_price = get_avg_buy_price(coin)
#     old_total = amount * old_price
#
#     if total > 5001 and total >= old_total * percent:
#         # 시장가 매도 인데 매수시점보다 percent 상승했으면 매도 진행함.
#         res = upbit.sell_market_order(ticker, amount)
#         strMsg = coin + " : 시장가 매도 =" + str(res)
#         post_message(strMsg)
#
#
# # 시장가 매수 함수
# def buy(coin):
#     money = upbit.get_balance("KRW")
#     if money >= 10000:
#         money = 10000  # 1만원으로 고정함 코인이 5개니까 총 5만원으로 운용함.
#
#     amount = get_balance(coin)  # upbit.get_balance(coin)
#     old_price = get_avg_buy_price(coin)
#     old_total = amount * old_price
#
#     if old_total < 5001 and money >= 10000:
#         ticker = 'KRW-' + coin
#         res = upbit.buy_market_order(ticker, money)
#         strMsg = coin + " : 시장가 매수 =" + str(res)
#         post_message(strMsg)
#
#
# def buy_job():
#     # 매수
#     # 단, 이미 보유하고 있으면 추가 매수는 안함.
#     for coin in coins:
#         buy(coin)
#         time.sleep(0.2)
#
#
# def sell_job_10():
#     # 매도
#     # 단, 10% 이상 수익율이면 매도 아니면 홀딩
#     percent = 1.10
#     for coin in coins:
#         sell(coin, percent)
#         time.sleep(0.2)
#
#
# def sell_job_03():
#     # 매도 시간은 오전 8시50분
#     # 단, 3% 이상 수익율이면 매도 아니면 홀딩
#     percent = 1.03
#     for coin in coins:
#         sell(coin, percent)
#         time.sleep(0.2)
#
#     # 연습용임
#
#
# def test_job():
#     now = time.localtime()
#     strMsg = "%04d/%02d/%02d %02d:%02d:%02d" % (
#     now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
#     post_message(strMsg)
#     # 출처: https://technote.kr/264 [TechNote.kr]
#
# telegram
#
#
#
# # 실제 실행구문
# strMsg = "==예약 매수 매도 autotrader 시작=="
# post_message(strMsg)
#
# while True:
#     schedule.run_pending()  # 스케쥴 실행
#     time.sleep(1)
