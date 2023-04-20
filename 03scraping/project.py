import re
import requests
from bs4 import BeautifulSoup

def create_soup(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def print_news(index, title, link):
    print("{}. {}".format(index+1, title))
    print("  (링크 : {})".format(link))

def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    # 흐림, 어제보다 OO˚ 높아요
    cast = soup.find("p", attrs={"class":"summary"}).get_text().replace("  ", " / ")
    # 현재 OO℃  (최저 OO˚ / 최고 OO˚)
    curr_temp = soup.find("div", attrs={"class":"temperature_text"}).get_text().replace("현재 온도", "").strip() # 현재 온도
    min_temp = soup.find("span", attrs={"class":"lowest"}).get_text().replace("최저기온", "") # 최저 온도
    max_temp = soup.find("span", attrs={"class":"highest"}).get_text().replace("최고기온", "") # 최고 온도
    # 오전 강수확률 OO% / 오후 강수확률 OO%
    morning_rain_rate = soup.find_all("span", attrs={"class":"weather_inner"})[0].find("span", attrs={"class":"weather_left"}).get_text().strip().replace("오전", "") # 오전 강수확률
    afternoon_rain_rate = soup.find_all("span", attrs={"class":"weather_inner"})[1].find("span", attrs={"class":"weather_left"}).get_text().strip().replace("오후", "") # 오전 강수확률
    # 미세먼지 OO㎍/㎥좋음
    # 초미세먼지 OO㎍/㎥좋음
    dust = soup.find("ul", attrs={"class":"today_chart_list"})
    pm10 = dust.find_all("li")[0].get_text().strip() # 미세먼지
    pm25 = dust.find_all("li")[1].get_text().strip() # 초미세먼지

    # 출력
    print(cast)
    print("현재 {} (최저 {} / 최고 {})".format(curr_temp, min_temp, max_temp))
    print("오전 강수확률{} / 오후 강수확률{}".format(morning_rain_rate, afternoon_rain_rate))
    print(pm10)
    print(pm25)
    print()

def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://media.naver.com/press/214/ranking?type=popular"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"press_ranking_list"}).find_all("li", limit=3) # 가져올 숫자 한정
    for index, news in enumerate(news_list):
        title = news.find("strong", attrs={"class":"list_title"}).get_text()
        link = news.find("a")["href"]
        print_news(index, title, link)
    print()

def scrape_it_news():
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li", limit=3)
    for index, news in enumerate(news_list):
        a_idx = 0
        img = news.find("img")
        if img:
            a_idx = 1 # img 태그가 있으면 1번 idx의 a 태그 정보를 사용 (아니면 0번)
        a_tag = news.find_all("a")[a_idx]
        title = a_tag.get_text().strip()
        link = a_tag["href"]
        print_news(index, title, link)
    print()

def scrape_english():
    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english#;"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})
    print("(영어 지문)")
    for sentence in sentences[len(sentences)//2:]: # 8문장이 있다고 가정할 때, idx 4~7까지 잘라서 가져옴
        print(sentence.get_text().strip())
    print()
    print("(한글 지문)")
    for sentence in sentences[:len(sentences)//2]: # 8문장이 있다고 가정할 때, idx 0~3까지 잘라서 가져옴
        print(sentence.get_text().strip())
    print()


if __name__ == "__main__":
    scrape_weather() # 오늘의 날씨 정보 가져오기
    scrape_headline_news() # 헤드라인 뉴스 정보 가져오기
    scrape_it_news() # it 뉴스 정보 가져오기
    scrape_english() # 오늘의 영어 회화 가져오기
