import urllib.request
import json
import random

output_data = {}

# ==========================================
# 引擎 1：抓取【上市】股票 (TWSE)
# ==========================================
print("🚀 啟動引擎 1：抓取上市股票...")
twse_success = False
try:
    url_twse = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
    req_twse = urllib.request.Request(url_twse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req_twse, timeout=10) as response:
        twse_data = json.loads(response.read().decode('utf-8'))
        for stock in twse_data:
            code = stock.get('Code', '')
            if len(code) <= 6:
                price_str = stock.get('ClosingPrice', '').replace(',', '')
                try:
                    price = float(price_str) if price_str else 0.0
                    if price > 0:
                        output_data[code] = {
                            "name": stock.get('Name', ''), "price": price,
                            "fundamental": random.randint(50, 95), "chip": random.randint(40, 95), "technical": random.randint(40, 95)
                        }
                except ValueError:
                    continue
    # 檢查名單裡有沒有台積電，確認真的成功抓到上市資料
    if '2330' in output_data:
        twse_success = True
        print("✅ 上市股票抓取成功！")
except Exception as e:
    print(f"⚠️ 上市 API 連線失敗: {e}")

# ==========================================
# 引擎 2：抓取【上櫃】股票 (TPEx)
# ==========================================
print("🚀 啟動引擎 2：抓取上櫃股票...")
tpex_success = False
try:
    url_tpex = "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_quotes"
    req_tpex = urllib.request.Request(url_tpex, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req_tpex, timeout=10) as response:
        tpex_data = json.loads(response.read().decode('utf-8'))
        for stock in tpex_data:
            code = stock.get('SecuritiesCompanyCode', '')
            if len(code) <= 6:
                price_str = stock.get('Close', '').replace(',', '')
                try:
                    price = float(price_str) if price_str else 0.0
                    if price > 0:
                        output_data[code] = {
                            "name": stock.get('CompanyName', ''), "price": price,
                            "fundamental": random.randint(50, 95), "chip": random.randint(40, 95), "technical": random.randint(40, 95)
                        }
                except ValueError:
                    continue
    # 檢查名單裡有沒有元太，確認真的成功抓到上櫃資料
    if '8069' in output_data:
        tpex_success = True
        print("✅ 上櫃股票抓取成功！")
except Exception as e:
    print(f"⚠️ 上櫃 API 連線失敗: {e}")

# ==========================================
# 獨立防呆：分別注入備援資料
# ==========================================
if not twse_success:
    print("🔄 啟動防護網：注入【上市】備援資料...")
    twse_fallback = {
        '2330': {'name': '台積電(備援)', 'price': 2250}, '2317': {'name': '鴻海(備援)', 'price': 230},
        '2454': {'name': '聯發科(備援)', 'price': 1200}, '2382': {'name': '廣達(備援)', 'price': 320},
        '3017': {'name': '奇鋐(備援)', 'price': 850}, '3450': {'name': '聯鈞(備援)', 'price': 215},
        '2603': {'name': '長榮(備援)', 'price': 180}, '2303': {'name': '聯電(備援)', 'price': 55}
    }
    for code, info in twse_fallback.items():
        output_data[code] = {"name": info['name'], "price": info['price'], "fundamental": random.randint(70, 95), "chip": random.randint(60, 95), "technical": random.randint(60, 95)}

if not tpex_success:
    print("🔄 啟動防護網：注入【上櫃】備援資料...")
    tpex_fallback = {
        '8069': {'name': '元太(備援)', 'price': 250}, '3293': {'name': '鈊象(備援)', 'price': 1050},
        '3105': {'name': '穩懋(備援)', 'price': 150}, '6223': {'name': '旺矽(備援)', 'price': 350}
    }
    for code, info in tpex_fallback.items():
        output_data[code] = {"name": info['name'], "price": info['price'], "fundamental": random.randint(70, 95), "chip": random.randint(60, 95), "technical": random.randint(60, 95)}

with open('stocks_data.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)
    
print(f"🎯 總計打包 {len(output_data)} 檔股票資料完成！")
