from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time,random
import pandas as pd
import numpy as np




web = 0
for web in range(0,5):
    
    webs = "browser{}".format(web)

    webs = webdriver.Chrome()
    
    webs.get("https://www.google.com")
    
    inputElements = "inputElement{}".format(web)
    inputElements = webs.find_element_by_name("q")
            
    inputElements.send_keys("交通部觀光局觀光統計資料庫")
    
    inputElements.submit()

    
    try:
        WebDriverWait(webs, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "r")))
    
        page1_resultss = webs.find_elements_by_class_name("r")
        time.sleep(random.randint(1,3))

        
        page1_resultss[0].click()
        time.sleep(random.randint(1,3))

        
        page2_resultss = webs.find_elements_by_class_name("col")
        time.sleep(random.randint(1,3))

        
        page2_resultss[12].click()
        time.sleep(random.randint(1,3))

        
        page3_resultss = webs.find_elements_by_xpath("//a[@class='nav-link']")
        time.sleep(random.randint(1,3))

        
        page3_resultss[0].click()
        time.sleep(random.randint(1,3))
      
    
    
##    ''' 選取起始年月 '''
    
        time.sleep(random.randint(1,3))
        Years = "Year{}".format(web)
        Years = Select(webs.find_element_by_xpath("//select[@formcontrolname='startYear']"))
        Years.select_by_value('2: 98')
        Months= "Month{}".format(web)
        Months = Select(webs.find_element_by_xpath("//select[@formcontrolname='startMonth']"))
        Months.select_by_value('1: 1')
    
    ##    ''' 選取地點 '''
        time.sleep(random.randint(1,3))
        if web == 0:            
            labels0 = webs.find_elements_by_tag_name("label") #找到所有 label
            labels0[4].click() #北部地區
            labels0[32].click() #北部地區全部遊憩區
        elif web == 1:
            labels1 = webs.find_elements_by_tag_name("label")
            labels1[12].click() #中部地區
            labels1[32].click() #中部地區全部遊憩區
        elif web == 2:
            labels2 = webs.find_elements_by_tag_name("label")
        
            labels2[18].click() #南部地區
            labels2[20].click()
            labels2 = webs.find_elements_by_tag_name("label")
            labels2[32].click() #南部地區全部遊憩區
            labels2[101].click()
        elif web == 3:
            labels3 = webs.find_elements_by_tag_name("label")
            labels3[24].click() #東部地區
            labels3[32].click() #東部地區全部遊憩區
        elif web == 4:
            labels4 = webs.find_elements_by_tag_name("label")
            labels4[27].click() #離島地區
            labels4[32].click() #離島地區全部遊憩區
#    
###   ''' 把找到的地點編碼 '''
##    print(labels)
##    i = 0
##    for item in labels:
##        print(i,item.text)
##        i += 1
#
        time.sleep(random.randint(1,3))
##   ''' 送出選取表單 '''

        webs.find_element_by_xpath("//div//button[@class='btn btn-danger']").click()
##    抓取表格資料   
        time.sleep(5)
        datass = pd.read_html(webs.page_source)[0]
        df=np.array(datass)

    
        datas_columnss = ['縣市','Location','遊憩據點','Scenic Spot']
        for i in range(98,109):
            for j in range(1,13):
#                if i == 108 and j == 11: #取值到 2019/11
#                    break
                times ="{}年{}月".format(i,j) 
                datas_columnss.append(times)
        datas_columnss.append("小計")

        time.sleep(random.randint(1,3))
    #    print(datas_columns)
        
        df = pd.DataFrame(df,columns=datas_columnss)
        datas = 'amusement_park{}.csv'.format(web+1)
#        print(datas)
        df.to_csv( datas , index = False)
        webs.quit()

    
      
    except TimeoutException:
        print('等待逾時!')
