import csv
# 단어 csv 파일 넣어주시면 됩니다.:)
f = open('word_1.csv','r',encoding = 'utf-8-sig')
rdr = csv.reader(f)

words = []
syan = []
for line in rdr:
    words.append(line)
f.close()


print(words[14])
aa= words[:500]
print(len(aa))


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import multiprocessing #import Pool
import re
import time

# 구글 버전에 맞는 드라이브 설치하셔서 경로 넣어주세요. 
driver = webdriver.Chrome('/Users/kangyujin/Downloads/chromedriver 2')
driver.implicitly_wait(5)

# # count = 0
# #결과물 파일 이름 지정해주세요
# savef = open('word_output_1.csv','w', encoding ='utf-8',newline = '')
# wr = csv.writer(savef, delimiter = ',')
    
word_data = []


def get_links():

# url 접근
    data = []
    
    for word in aa:
        try:
            driver.get('https://ko.dict.naver.com/#/main')
            driver.find_element_by_name('query').send_keys(word)# csv로 받은 값 사용
            driver.find_element_by_xpath('//*[@id="searchArea"]/div/button').click()
            driver.implicitly_wait(5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            title = driver.find_element_by_xpath('//*[@id="searchPage_entry"]/div/div[1]/div/a')
            data.append([title.get_attribute('href'),word])
            #url = soup.select('#searchPage_entry > div > div:nth-child(1) > div > a')
            #print(url)
            #driver.find_element_by_xpath('//*[@id="searchPage_entry"]/div/div[1]/div/a').click()
#             driver.implicitly_wait(5)

#             for u in url:
#                 data.append(u.get('href'))

        except:# 검색했을 때 단어가 나오는 경우
            try:
                driver.get('https://ko.dict.naver.com/#/main')
                driver.find_element_by_name('query').send_keys(word)# csv로 받은 값 사용
                driver.find_element_by_xpath('//*[@id="searchArea"]/div/button').click()
                driver.implicitly_wait(5)
                data.append([str(driver.current_url),word])
            except:
                print(word)
                print("문제생김")
                
                    
    #print(data)
        
    return data 

def get_content(link):
     # 유의어, 반의어 추출
    sym = []# 유의어 없는 경우 이전 값 들어갈 수 있으니 초기화
    anto = []# 반의어 없는 경우 이전 값 들어갈 수 있으니 초기화
    s = []
    a = []
    
    abs_link = link[0]
    driver.get(abs_link)
    driver.implicitly_wait(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        if soup.select("#_id_section_thesaurus") != []:
            s = driver.find_elements_by_css_selector('div.slides > div > div > div.synonym')
            a = driver.find_elements_by_css_selector('div.slides > div > div > div.antonym')
    except:
        print("유의어 반의어 찾기 실패")



    #print(s[0].text,a[0].text)
   

    # 유의어, 반의어 추출한 s,a에서 텍스트만 뽑아내는 작업
    if s != []:
        sym = ((s[0].text).strip('\n').split('\n새창\n'))
        sym[0] = sym[0].split('\n')[1]
        sym[-1] = sym[-1].split('새창')[0]

    if a != []:
        anto = ((a[0].text).strip('\n').split('새창\n'))
        anto[0] = anto[0].split('\n')[1]
        anto[-1] = anto[-1].split('새창')[0]

    #print(sym, anto)
    
    
    # 유의어 중 다의어 숫자 붙은 것 제거
    temp = []
    for i in sym:
        i = i.strip('\n')
        data = re.findall('[0-9]',i) # 숫자 있다면 들어감
        if data != []:
            for j in range (len(data)):
                i = i[0:-1]
        temp.append(i)
        
    #,로 하나의 str으로 합치기
    synonym = ""
    for t in temp:
        synonym += t+";"
    synonym = synonym[:-1]
    
    #반의어 중 다의어 숫자 붙은 것 제거
    temp = []
    for i in anto:
        i = i.strip('\n')
        data = re.findall('[0-9]',i) # 숫자 있다면 들어감
        if data != []:
            for j in range (len(data)):
                i = i[0:-1]
        temp.append(i)
        
    #,로 하나의 str으로 합치기
    antonym = ""
    for t in temp:
        antonym += t+";"
    antonym = antonym[:-1]

    print(synonym, antonym)
    temp = []
    temp.append(link[1][0])
    temp.append(str(synonym))
    temp.append(str(antonym))
    
    word_data.append(temp)
    #wr.writerow([str(link[1]),temp,])
    # 출력
    #wr.writerow([word,syan])
    
    time.sleep(0.01)
    return
  
if __name__ == '__main__':
    
    manager = multiprocessing.Manager()
    word_data = manager.list()
    jobs = []
    data = get_links()
    #pool = Pool(processes = 4)
    #pool.map(get_content, get_links())
    for i in data:
        p = multiprocessing.Process(target = get_content, args = (i,))   
        jobs.append(p)
        p.start()
        for j in jobs:
            j.join()
            
    for proc in jobs:
        proc.join()
    
    print(word_data)
    
    #결과물 파일 이름 지정해주세요
    

savef = open('word_output_1.csv','w', encoding ='utf-8',newline = '')
wr = csv.writer(savef, delimiter = ',')

print(word_data[0])
wr.writerow(['단어', '유의어', '반의어'])

for i in word_data:
    wr.writerow([i[0],i[1],i[2]])
    
savef.close()
