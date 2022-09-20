from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, sys, os, os.path, csv, datetime



print('程式開始')



print('3b. 打開瀏覽器')
driver = webdriver.Chrome( r"./chromedriver" )



print('3c. 設定瀏覽器參數')
driver.implicitly_wait(5)                    # 如果瀏覽器頁面載入後，find_element_by_css_selector() 指定的元素未立刻出現，最多等待5秒，超時則視為錯誤。
driver.set_page_load_timeout(60)             # 如果瀏覽器最多等待頁面載入60秒，超時則視為錯誤。



while True:

    print('前往頁面')
    driver.get( 'https://bet.hkjc.com/football/odds/odds_had.aspx?lang=ch' )


    print('等待頁面載入完成')
    time.sleep(2)


    print('獲取賠率表資料')
    cell_elements = driver.find_elements_by_css_selector('[class*="couponTable"] [class*="couponRow"] > div')


    # 由於表格內每行有9格, 而 cell_elements 變數是一個 List, 裡面順序裝所有的格
    # 第1行格 index 為 0-8, 第2行格 index 為 9-17, 第3行格 index 為 18-26, 如此類推...
    # 我們用 range(0, len(cell_elements), 9) 函數, start, stop, step 分別為 0, cell_elements length, 9, 以產生這些以9為倍數的 indices
    # 變數 i 會是 0, 9, 18, 27 ...
    # cell_elements[ i : i+9 ] 則是每行的9個格, [0: 8], [9: 17], [18: 26] ...
    data = []
    for i in range(0, len(cell_elements), 9):       # start, stop, step 分別為 0, cell_elements length, 9. i = 0, 9, 18, 27...
        cells = cell_elements[ i : i+9 ]                 # start, stop 分別為 i, i+9
        now = str(datetime.datetime.now())[ 0 : 19 ]    # 取得此刻的採集時間
        row = [ now ]                                       # 建立一個 row List, 首個元素為採集時間 now
        for cell in cells:
            row.append( cell.text.strip() )           # 把每格文字資料裝到 row List 內
        data.append( row )                              # 把 List 裝到 data List 內
        


    print("儲存資料到檔案")
    with open(r"result_had_odds.csv", "at", newline="", encoding="utf-8-sig") as f:

        # 以CSV格式寫入，定義CSV列順序
        writer = csv.writer(f)

        # 檢查檔案長度，如果檔案是空的，則寫入CSV列定義
        if f.tell() <= 0:
            writer.writerow(["採集時間", "球賽編號", "旗徽", "對賽隊伍", "場地", "預定截止投注時間", "即場投注", "主隊賠率", "和賠率", "客隊賠率"])

        for row in data:
            # 寫入資料, 把 now 變數放到List內, 再
            writer.writerow(row)
            
            # 把資料印出屏幕方便觀察程式運行, 如不需要可移除
            print(','.join(row))
            

    print("檔案寫入完成")
        
        
    print('\n程式將於60秒後再度擷取 ...')
    time.sleep(30)







