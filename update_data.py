import urllib.request
import json
import random

# 台灣證券交易所 Open API (每日收盤行情)
url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
req = urllib.request.Request(url)

print("🚀 啟動高盛級爬蟲：正在連接台灣證券交易所...")

try:
    with urllib.request.urlopen(req) as response:
        twse_data = json.loads(response.read().decode('utf-8'))
        
    # 我們的高潛力觀察清單 (您可以隨時在這裡新增代碼)
    target_stocks =['2330', '2317', '2408', '3017', '2888', '3450']
    output_data =[]

    for stock in twse_data:
        if stock['Code'] in target_stocks:
            # 取得真實收盤價
            real_price = float(stock['ClosingPrice'])
            
            # --- 量化因子模組 ---
            # 實戰中，這裡會去爬取法人的買賣超與營收數據。
            # 為了讓您先跑通自動化流程，我們這裡先用模擬演算法給予波動分數
            fundamental_score = random.randint(70, 95) 
            chip_score = random.randint(60, 95)
            technical_score = random.randint(60, 95)

            output_data.append({
                "id": stock['Code'],
                "name": stock['Name'],
                "price": real_price,
                "fundamental": fundamental_score,
                "chip": chip_score,
                "technical": technical_score
            })
            print(f"✅ 成功抓取: {stock['Name']} (收盤價: {real_price})")

    # 將算好的數據存成 JSON 檔案，準備餵給前端網頁
    with open('stocks_data.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
        
    print("🎯 所有數據已成功更新並打包為 stocks_data.json！")

except Exception as e:
    print(f"❌ 爬蟲執行失敗: {e}")
