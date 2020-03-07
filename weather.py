def cal_namelength(row):
    if pd.notnull(row[0]):
        row['月份'] = j
        row['年份'] = i-1911
    else:
        row['月份'] = 0
        row['年份'] = 0 
    return row
            



from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time,random
import pandas as pd
import numpy as np

browser = webdriver.Chrome()

browser.get("https://www.google.com")

inputElement = browser.find_element_by_name("q")

inputElement.send_keys("交通部中央氣象局每月氣象")

inputElement.submit()



try:
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "r")))
    
    page1_results = browser.find_elements_by_class_name("LC20lb")
#    print(page1_results)
    page1_results[0].click()
#
##    ''' 選取起始年月 '''
    time.sleep(random.randint(1,3))
    
    for i in range(2009,2020):
        Year = Select(browser.find_element_by_xpath("//select[@name='year']"))

        Year.select_by_value(str(i))
        
        
        for j in range(1,13):
            Month = Select(browser.find_element_by_xpath("//select[@name='month']"))

            Month.select_by_value(str(j))
            
#           ### 抓取表格資料 ###
            time.sleep(random.randint(1,3))                    # 需要等待網頁載入資料
            datas = pd.read_html(browser.page_source)[0]
            df2=np.array(datas)
#            print(type(df2))
            df2[df2 == 'T'] = 0             # 替換 numpy 裡的特定值
            df2[df2 == 'V'] = 0             # 替換 numpy 裡的特定值

            
#           ### 原本想用 for迴圈替代資料內 T值 ###
#            print(df2[:,4])                #找出陣列中需要清洗的資料欄位
#           def replace_T(data):
#           
#           for item in data: 
#           if item == 'T':
#               item = item.replace('T','0')
#               data1.append()
#               return data            
#            data1 = replace_T(df2[:,4])
#            print(data1) 
#           ###### 原本想用 startswith 去除 / 以後的東西 ########                   
            
#           ### ###      
#            y=[]
#            for item in x:
#               if  
#                z = item[:4]                  # 直接取 str第一個到第四個值(單字or符號or數值)
##                n = item.index("/")        
##                z = item.startswith(item,0,n)  # endswith first arg must be str or a tuple of str, not int
#                y.append(z)
#            print(y)
#           #######################################
        
            datas_columns = ['測站','月氣溫平均','月氣溫最高','月氣溫最低','雨量(毫米)','最大十分鐘風',\
                             '最大瞬間風','月濕度平均','月濕度最小','氣壓(百帕)','降水日數(天)','日照時數(小時)']
        
            df = pd.DataFrame(df2,columns=datas_columns)
            
            df['月份'] = 0                    # 先透過這種方式新增好欄位做準備，下面執行效能會好很多
            df['年份'] = 0  
            df = df.apply(cal_namelength, axis=1) # 記得: 1.要把新的df指派給原本的df才會成功更新。 2. axis要設定為1，才會以row為單位跑回圈。

            time3 = "{}year{}month.csv".format(i-1911,j)  
            df.to_csv(time3 , index = False)

    


        
except TimeoutException:
    print('等待逾時!')