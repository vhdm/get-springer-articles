import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
def get_springer_articles(query, max_results=5):
    # ساخت URL جستجو در Springer
    data=[]
    counter=1
    for page in range(1,50):
      try:
        url = f"https://link.springer.com/search?query={query}&date=custom&dateFrom=2022&dateTo=2024&sortBy=relevance&page={page}"
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('a', class_='app-card-open__link')
            for i, article in enumerate(articles):
                title = article.find('span').text.strip() if article.find('span').text.strip() else 'عنوان موجود نیست'
                temp_url= article['href'] if article['href']  else None
                if temp_url is None:
                  continue
                if not temp_url.startswith("http"):
                  temp_url= "https://link.springer.com" + article['href'] if article['href']  else None
                url = temp_url

                date=""
                abstract=""
                print(f"{counter}/{max_results}",url)
                if counter > max_results:
                  return data
                # دریافت صفحه مقاله برای استخراج چکیده
                if url:
                  try:
                    article_response = requests.get(url)
                    time.sleep(2)
                    if article_response.status_code == 200:
                      article_soup = BeautifulSoup(article_response.content, 'html.parser')
                      abstract_tag = article_soup.find('div', id='Abs1-content')
                      date = article_soup.find('time')['datetime']
                      abstract = abstract_tag.text.strip() if abstract_tag else 'چکیده موجود نیست'
                      counter+=1
                    else:
                      abstract = 'چکیده موجود نیست'
                  except Exception as e:
                    print(e)
                    print("wait...")
                    time.sleep(10)
                else:
                    abstract = 'چکیده موجود نیست'

                print(f"Title: {title}")
                print(f"Date: {date}")
                print(f"Abstract: {abstract}")
                print('-' * 100)
                data.append({
                    'title':title,
                    'url':url,
                    'date':date,
                    'abstract':abstract,
                })
        else:
            print("مشکلی در اتصال به Springer وجود دارد.")
      except:
        return data

# جستجو با کلمه کلیدی
data=get_springer_articles("cyber threat intelligence", max_results=200)
df= pd.DataFrame(data)
df.to_csv('cyber-threat-intelligence.csv')


data=get_springer_articles("CTI", max_results=200)
df= pd.DataFrame(data)
df.to_csv('cti.csv')
