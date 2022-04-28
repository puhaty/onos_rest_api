import http.client
import mimetypes
import json
import random
conn = http.client.HTTPSConnection("zsutstockserver.azurewebsites.net")
payload = ''
headers = {}

def get_stock_exchanges():
    payload = ''
    headers = {}
    conn.request("GET", "/api/stockexchanges", payload, headers)
    res = conn.getresponse()
    data = res.read()
    temp = data.decode("utf-8").split(',')
    cities = []
    for i in range(0, len(temp)):
        cities.append(temp[i].strip('[]"'))
    #print(cities)
    return cities

def get_shares_list(city):
    headers = {
        'Cookie': 'ARRAffinity=17d4a7379fd5208547170b80243178455a569b5053598ccf1b21a534dff90a54; ARRAffinitySameSite=17d4a7379fd5208547170b80243178455a569b5053598ccf1b21a534dff90a54'
    }
    conn.request("GET", "/api/shareslist/" + city, payload, headers)
    res = conn.getresponse()
    data = res.read()
    temp = data.decode("utf-8").split(',')
    shares = []
    for i in range(0, len(temp)):
        shares.append(temp[i].strip('[]"'))
    #print(shares)
    return shares

def get_share_price_sell(city, share):
    payload = ''
    headers = {
        'Cookie': 'ARRAffinity=17d4a7379fd5208547170b80243178455a569b5053598ccf1b21a534dff90a54; ARRAffinitySameSite=17d4a7379fd5208547170b80243178455a569b5053598ccf1b21a534dff90a54'
    }

    conn.request("GET", "/api/shareprice/" + city + "?share=" + share, payload, headers)
    res = conn.getresponse()
    data = res.read()
    temp = data.decode("utf-8").split(',')
    price = float(temp[5].strip('"price":'))
    #print(data.decode("utf-8"))
    return price

def get_share_price_buy(city, share):
    payload = ''
    headers = {
        'Cookie': 'ARRAffinity=17d4a7379fd5208547170b80243178455a569b5053598ccf1b21a534dff90a54; ARRAffinitySameSite=17d4a7379fd5208547170b80243178455a569b5053598ccf1b21a534dff90a54'
    }

    conn.request("GET", "/api/shareprice/" + city + "?share=" + share, payload, headers)
    res = conn.getresponse()
    data = res.read()
    temp = data.decode("utf-8").split(',')
    price = float(temp[1].strip('"price":'))
    #print(data.decode("utf-8"))
    return price

def client_data():
    payload = ''
    headers = {
        'Authorization': 'Basic MDExNDk4MDNAcHcuZWR1LnBsOk1hdGNoZWNoMTIy'
    }
    conn.request("GET", "/api/client", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def sell(city, share, amount, price):
    payload = json.dumps({
        "stockExchange": city,
        "share": share,
        "amount": amount,
        "price": price
    })
    headers = {
        'Authorization': 'Basic MDExNDk4MDNAcHcuZWR1LnBsOk1hdGNoZWNoMTIy',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/selloffer", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def buy_1(city, share, price):

    payload = json.dumps({
        "stockExchange": city,
        "share": share,
        "amount": 1,
        "price": price + 100000
    })

    headers = {
        'Authorization': 'Basic MDExNDk4MDNAcHcuZWR1LnBsOk1hdGNoZWNoMTIy',
        'Content-Type': 'application/json'
    }

    conn.request("POST", "/api/buyoffer", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def buy_amount(city, share, amount):
    for i in range(0, amount):
        price = get_share_price_buy(city, share)
        buy_1(city, share, price)

def grade():
    payload = ''
    headers = {
        'Authorization': 'Basic MDExNDk4MDNAcHcuZWR1LnBsOk1hdGNoZWNoMTIy',
        'Cookie': 'ARRAffinity=17d4a7379fd5208547170b80243178455a569b5053598ccf1b21a534dff90a54; ARRAffinitySameSite=17d4a7379fd5208547170b80243178455a569b5053598ccf1b21a534dff90a54'
    }
    conn.request("GET", "/api/grade", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def get_amount():
    amount = {}
    payload = ''
    headers = {
        'Authorization': 'Basic MDExNDk4MDNAcHcuZWR1LnBsOk1hdGNoZWNoMTIy'
    }
    conn.request("GET", "/api/client", payload, headers)
    res = conn.getresponse()
    data = res.read()
    list = data.decode("utf-8").split(',')
    del list[0]
    del list[0]
    list[0] = list[0].lstrip('"shares":{')
    list[0] = list[0].strip('}}')

    if(list[0] != ''):
        for i in range(0, len(list)):
            temp = (list[i].split(':'))
            key = temp[0].strip('"}}"')
            value = int(temp[1].strip('"}}"'))
            amount[key] = value
    return amount

def get_amount_share(city, share):
    payload = ''
    headers = {
        'Cookie': 'ARRAffinity=17d4a7379fd5208547170b80243178455a569b5053598ccf1b21a534dff90a54; ARRAffinitySameSite=17d4a7379fd5208547170b80243178455a569b5053598ccf1b21a534dff90a54'
    }
    conn.request("GET", "/api/shareprice/" + city + "?share=" + share, payload, headers)
    res = conn.getresponse()
    data = res.read()
    temp = data.decode("utf-8").split(',')
    amount_share = temp[3].strip('"amount":')
    amount_share = amount_share.strip('{}')
    return int(amount_share)


def buy_number_letters(number_of_shares):
    end = False
    cities = get_stock_exchanges()
    temp = get_shares_list(cities[0])
    buy_1(cities[0], temp[0], get_share_price_buy(cities[0], temp[0]))
    for i in range(0, len(cities)):
        if(end == False):
            shares = get_shares_list(cities[i])
            for j in range(0, len(shares)):
                amount = get_amount()
                amount_counter = len(amount.keys())
                if(amount_counter >= number_of_shares + 1):
                    break
                else:
                    for k in range(0, len(shares[j])):
                        amount = get_amount()
                        if(len(amount.keys()) >= number_of_shares + 1):
                            break
                        else:
                            if ((len(amount.keys()) >= number_of_shares) and (amount[shares[j]] == len(shares[j]))):
                                break
                            if (amount[shares[j]] < len(shares[j])):
                                price = get_share_price_buy(cities[i], shares[j])
                                buy_1(cities[i], shares[j], price)
                            else:
                                if(j < len(shares) - 1):
                                    if(shares[j+1] in amount.keys()):
                                        continue
                                    else:
                                        amount = get_amount()
                                        if (len(amount.keys()) == number_of_shares):
                                            continue
                                        else:
                                            buy_1(cities[i], shares[j + 1], get_share_price_buy(cities[i], shares[j + 1]))
                                            continue
                                else:
                                    shares = get_shares_list(cities[i + 1])
                                    if (shares[0] in amount.keys()):
                                        continue
                                    else:
                                        price = get_share_price_buy(cities[i + 1], shares[0])
                                        buy_1(cities[i + 1], shares[0], price)
                                        break
                amount = get_amount()
                if ((len(amount.keys()) >= number_of_shares) and (amount[shares[j + 1]] == len(shares[j]))):
                    end = True
                    break
        else:
            break

def buy_all():
    cities = get_stock_exchanges()
    counter = 0
    for i in range(0, len(cities)):
        shares = get_shares_list(cities[i])
        for j in range(0, len(shares)):
            counter += 1
            buy_amount(cities[i], shares[j], counter)
            '''
            shares_amount_ = get_amount_share(cities[i], shares[j])
            if (shares_amount_ <= 50):
                shares_amount_ = random.randrange(1, 50)
                print(shares_amount_, "q")
                buy_amount(cities[i], shares[j], shares_amount_)
            if(shares_amount_ > 50 and shares_amount_ <= 100):
                shares_amount_ = random.randrange(1, 70)
                print(shares_amount_, "w")
                buy_amount(cities[i], shares[j], shares_amount_)
            if (shares_amount_ > 100 and shares_amount_ <= 200):
                shares_amount_ = random.randrange(1, 70)
                print(shares_amount_, "e")
                buy_amount(cities[i], shares[j], shares_amount_)
            if (shares_amount_ > 200 and shares_amount_ <= 500):
                shares_amount_ = random.randrange(1, 70)
                print(shares_amount_, "r")
                buy_amount(cities[i], shares[j], shares_amount_)
            if (shares_amount_ > 500 and shares_amount_ <= 1000):
                shares_amount_ = random.randrange(1, 70)
                print(shares_amount_, "t")
                buy_amount(cities[i], shares[j], shares_amount_)
            if (shares_amount_ > 1000 and shares_amount_ <= 3000):
                shares_amount_ = random.randrange(1, 70)
                print(shares_amount_, "u")
                buy_amount(cities[i], shares[j], shares_amount_)
            if (shares_amount_ > 3000 and shares_amount_ <= 10000):
                shares_amount_ = random.randrange(1, 70)
                print(shares_amount_, "i")
                buy_amount(cities[i], shares[j], shares_amount_)
            else:
                shares_amount_ = random.randrange(1, 70)
                print(shares_amount_, "x")
                buy_amount(cities[i], shares[j], shares_amount_)
            '''

def sell_all():
    amount_ = get_amount()
    while (len(amount_.keys()) > 0):
        cities = get_stock_exchanges()
        for i in range(0, len(cities)):
            dict = get_amount()
            for k, v in dict.items():
                while v >= 0:
                    sell(cities[i], k, 1, 0.1)
                    v -= 1
                    #print(k, v, cities[i])
        amount_ = get_amount()
        print(len(amount_.keys()))

#######################################################

#kupno co najmniej jednego:
'''
client_data()
sell_all()

buy_amount("Warszawa", "PKNORLEN", 5)
client_data()
grade()
'''
#######################################################

#kupno co najmniej 49:
'''
client_data()
sell_all()

buy_amount("Warszawa", "PKNORLEN", 50)
client_data()
grade()
'''
######################################################

#kupno wg ilości liter w spółce;
'''
client_data()
sell_all()

buy_number_letters(40)
amount_ = get_amount()
for k, v in amount_.items():
    print(len(k), v)
print(len(amount_.keys()))
grade()
client_data()
'''
#######################################################

#kupno wzzystkich spółek w różnej liczbie
#'''
client_data()
sell_all()
buy_all()
i = 0
while(True):
    i += 1
    data = get_amount()
    counter = 1
    guard = False
    sorted_data = sorted(data.items(), key = lambda item: item[1])
    for i in range(len(sorted_data)-1):
        cities = get_stock_exchanges()
        if(sorted_data[i][1] == sorted_data[i+1][1]):
            print(i)
            guard = True
            for j in range(0, len(cities)):
                if(sorted_data[i][0] in get_shares_list(cities[j])):
                    buy_amount(cities[j], sorted_data[i][0], int(counter))
                data = get_amount()
            counter += 1
            data = get_amount()
    if(guard == False):
        break
        #elif i == len(sorted_data - 1):
            #break

client_data()
grade()
#'''

########################################################











