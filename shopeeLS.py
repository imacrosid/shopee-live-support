import requests
import time
import json
import os
import io
import qrcode
import random
from datetime import datetime

devART = '''
███████╗██╗  ██╗ ██████╗ ██████╗ ███████╗███████╗    ██╗     ██╗██╗   ██╗███████╗
██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔════╝██╔════╝    ██║     ██║██║   ██║██╔════╝
███████╗███████║██║   ██║██████╔╝█████╗  █████╗      ██║     ██║██║   ██║█████╗  
╚════██║██╔══██║██║   ██║██╔═══╝ ██╔══╝  ██╔══╝      ██║     ██║╚██╗ ██╔╝██╔══╝  
███████║██║  ██║╚██████╔╝██║     ███████╗███████╗    ███████╗██║ ╚████╔╝ ███████╗
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚══════╝    ╚══════╝╚═╝  ╚═══╝  ╚══════╝
                                             Support v1 | Made with 💚 BANG LAEY'''

def clear_console():
    os.system('cls')

def getcookie():
    try:
        with open('cookieShopee.txt', 'r') as file:
            cookie = file.read()
            
            if not cookie:
                print("\nFILE COOKIES KOSONG, GUNAKAN FITUR 1 DAHULU.")
                time.sleep(5)
                return None
            return cookie
    
    except FileNotFoundError:
        print("\nFILE COOKIES TIDAK DITEMUKAN, GUNAKAN FITUR 1 DAHULU.")
        time.sleep(5)

cookie = getcookie()
cookies = {'SPC_ST': f'{cookie}',}

headers = {
        "authority": "shopee.co.id",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        "client-info": "platform=9",
        'X-Shopee-Language': 'id',
        'X-Requested-With': 'XMLHttpRequest',
        }

# LOGIN
def getQrLogin():
    qrLogin = requests.get('https://shopee.co.id/api/v2/authentication/gen_qrcode', headers=headers)
    if qrLogin.status_code == 200:
        result = qrLogin.json()
        qrcode_id = result["data"]["qrcode_id"]
        if qrcode_id:
            login_link = f"https://shopee.co.id/universal-link/qrcode-login?id={qrcode_id}"
            
            # CREATE QR LOGIN
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=1,
                )
            qr.add_data(login_link)
            qr.make(fit=True)
            f = io.StringIO()
            qr.print_ascii(out=f)
            f.seek(0)
            print(f.read())
            return qrcode_id
        else:
            print("[!] Failed get new QR.")
    else:
        print("[!] Failed create QR login.")

def checkQrStatus(qrcode_id):
    cookies = {
    '__LOCALE__null': 'ID',
    }
    params = {
        "qrcode_id": qrcode_id,
    }
    response = requests.get(
        "https://shopee.co.id/api/v2/authentication/qrcode_status",
        params=params,
        cookies=cookies,
        headers=headers,
    )
    if response.status_code == 200:
        result = response.json()
        statusQR = result["data"]["status"]
        if statusQR == 'NEW':
            print(f"[{statusQR}] SCAN THIS QR WITH YOUR SHOPEE APP", end='\r')
        elif statusQR == 'SCANNED':
            print("                                       ", end='\r')
            print(f"[{statusQR}] CONFIRM IN YOUR APP!", end='\r')
        elif statusQR == 'CONFIRMED':
            print("                              ", end='\r')
            tokenQR = result["data"]["qrcode_token"]
            getCookiesLogin(tokenQR)
            exit()
        elif statusQR == 'EXPIRED':
            print("                                        ", end='\r')
            print(f"QR {statusQR}!\n")
            exit()
        else:
            print("                              ", end='\r')
            print(statusQR)
    else:
        print("[!] Failed checking status QR")
        exit()

def getCookiesLogin(tokenQR):
    postData = {
        "qrcode_token": tokenQR,
        "device_sz_fingerprint": "OazXiPqlUgm158nr1h09yA==|0/eMoV7m/rlUHbgxsRgRC/n0vyOe6XzhDMa2PcnZPv3ecioRaJQg2W7ur5GfhoDDEeuMz2az7GGj/8Y=|Pu2hbrwoH+45rDNC|08|3",
        "client_identifier": {
            "security_device_fingerprint": "OazXiPqlUgm158nr1h09yA==|0/eMoV7m/rlUHbgxsRgRC/n0vyOe6XzhDMa2PcnZPv3ecioRaJQg2W7ur5GfhoDDEeuMz2az7GGj/8Y=|Pu2hbrwoH+45rDNC|08|3",
        },
    }
    url = "https://shopee.co.id/api/v2/authentication/qrcode_login"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    login_response = requests.post(url, json=postData, headers=headers)
    result = login_response.headers.get('Set-Cookie', '').split(', ')
    
    all_cookies = {}
    
    for cookie_value in result:
        cookie_parts = cookie_value.split('; ')
        if cookie_parts:
            cookie_name, cookie_data = cookie_parts[0].split('=', 1)
            all_cookies[cookie_name] = cookie_data

    # spc_ec_cookie = all_cookies.get('SPC_EC', '')
    spc_st_cookie = all_cookies.get('SPC_ST', '')
    with open('cookieShopee.txt', 'w') as file:
        file.write(spc_st_cookie)
        print("Success saved cookie account.\n")

#  AUTO PUSH/SHOW VOUCHER LIVE
def cekVoucherLive(sessionLive):
    params = {
        "scene": "0",
    }

    response = requests.get(
        f"https://live.shopee.co.id/webapi/v1/session/{sessionLive}/voucher",
        params=params,
        cookies=cookies,
        headers=headers,
    )

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print("Failed Get List Voucher.")
        exit()
        return None

def showVoucherLive(sessionLive, id_voucher, code_voucher, signature, data_voucher):
    json_data = {
        "session_id": sessionLive,
        "identifier": {
            "promotion_id": id_voucher,
            "voucher_code": code_voucher,
            "signature": signature,
        },
        "voucher": data_voucher,
    }

    response = requests.post(
        f"https://live.shopee.co.id/webapi/v1/session/{sessionLive}/voucher/show",
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    
    if response.status_code == 200:
        sekarang = datetime.now().strftime("%H:%M:%S")
        result = response.json()
        statusPush = result["err_msg"]
        return statusPush
    else:
        print("Gagal menampilkan voucher.")

def pushVoucherLive():
    while True:
        clear_console()
        print("Auto Push/Show Vouchers Live\n")
        voucherShopee = cekVoucherLive(sessionLive) # Check Available Vouchers Live Stream
        for shopee_vouchers in voucherShopee["data"]["shopee_vouchers"]:
            data_voucher = json.dumps({"extra_voucher": json.dumps(shopee_vouchers)})
            id_voucher = shopee_vouchers["promotion_id"]
            code_voucher = shopee_vouchers["voucher_code"]
            signature = shopee_vouchers["signature"]

            statusPush = showVoucherLive(sessionLive, id_voucher, code_voucher, signature, data_voucher)
            sekarang = datetime.now().strftime("%H:%M:%S")
            if statusPush == 'Berhasil':
                print(f"Voucher {code_voucher} | SUCCESS | {sekarang}")
            else:
                print(f"Voucher {code_voucher} | FAILED ({statusPush}) | {sekarang}")
            time.sleep(35)

#  AUTO PIN RANDOM PRODUCT
def getDataProductList(sessionLive):
    headers = {
        "authority": "live.shopee.co.id",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "client-info": "platform=9",
    }
    params = {
    'visible': 'true',
    'offset': '0',
    'limit': '100',
    }
    response = requests.get(
    f'https://live.shopee.co.id/webapi/v1/session/{sessionLive}/host/items',
    params=params,
    cookies=cookies,
    headers=headers,
    )
    if response.status_code == 200:
        result = response.json()
        totalProduct = result["data"]["total_count"]
        randomProduct = random.randint(0, totalProduct)
        dataProduk = result["data"]["items"][randomProduct]
        namaProduk = dataProduk["name"]
        idProduk = dataProduk["id"]
        productDataFull = json.dumps(dataProduk)
        return productDataFull, namaProduk, idProduk

def pinProduct(sessionLive, productDataFull):
    headers = {
        "authority": "live.shopee.co.id",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "client-info": "platform=9",
    }
    json_data = {
        'item': productDataFull,
    }
    response = requests.post(
    f'https://live.shopee.co.id/webapi/v1/session/{sessionLive}/show',
    cookies=cookies,
    headers=headers,
    json=json_data,
    )
    if response.status_code == 200:
        result = response.json()
        statusPin = result["err_msg"]
        return statusPin

def pinProductDetails():
    delayChangeProduct = 60
    while True:
        clear_console()
        print("Auto Pin Random Product from Etalase\n")
        productDataFull, namaProduk, idProduk = getDataProductList(sessionLive)
        statusPin = pinProduct(sessionLive, productDataFull)
        sekarang = datetime.now().strftime("%H:%M:%S")
        print(f"[{sekarang}] {statusPin} | {namaProduk}")
        time.sleep(delayChangeProduct)

# ANOTHER
def donate():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qris = '00020101021126570011ID.DANA.WWW011893600915303639259902090363925990303UMI51440014ID.CO.QRIS.WWW0215ID10200298090080303UMI5204594553033605802ID5909LAE STORE6015Kota Pekan Baru610528256626960650011ID.DANA.WWW0146https://qr.dana.id/v1/28101205202003074254897763043358'
    qr.add_data(qris)
    qr.make(fit=True)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())
    print("DONASI VIA QR UNTUK SEGALA JENIS PEMBAYARAN, MAKASIH BANG.\n")
            
            
if __name__ == "__main__":
    clear_console()
    print(devART)
    print("1. Login Account")
    print("2. Auto Push Voucher")
    print("3. Auto Pin Random Produk")
    print("4. Mass Detele Etalase (under development)")
    print("5. Another More (under development)")
    print("\n0. DONASI")
    pilihYa = input(f"\nVote ? ")
    if pilihYa == '1':
        qrcode_id = getQrLogin()
        while True:
            checkQrStatus(qrcode_id)
            time.sleep(1)
    elif pilihYa == '2':
        sessionLive = input(f"\nSession Live Example: https://live.shopee.co.id/pc/live?session=55029522\nInput Sesi (5502xxxx): ")
        pushVoucherLive()
    elif pilihYa == '3':
        sessionLive = input(f"\nSession Live Example: https://live.shopee.co.id/pc/live?session=55029522\nInput Sesi (5502xxxx): ")
        pinProductDetails()
    elif pilihYa == '0':
        donate()
    else:
        print("\nPilihan tidak tersedia!\n")
        exit()