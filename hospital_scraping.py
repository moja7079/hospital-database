import requests
from bs4 import BeautifulSoup

def main():
    #setting---------------------
    URL = "https://www.iryou.teikyouseido.mhlw.go.jp/znk-web/juminkanja/S2400/initialize?sc=01-03-5-05002,01-03-5-05003,01-03-5-05004,01-03-5-05992&st=01-2&sjk=3&jc=MC-02&cp=%E6%9D%B1%E4%BA%AC%E9%83%BD%E5%8D%83%E4%BB%A3%E7%94%B0%E5%8C%BA_35.6940309_139.7537719_00_A"

    #setting---------------------
    urls=get_hospital_urls(URL)
    # print(f'url:\n{urls}')

    for url in urls:
        hospital_informations=get_hospital_informations(url)
        # print(f"{hospital_informations}")

        print("-" * 30)
        print(f"URL: {hospital_informations['url']}")
        print(f"病院名: {hospital_informations['病院名']}")
        print(f"院内処方: {hospital_informations['院内処方']}")
        print(f"院外処方: {hospital_informations['院外処方']}")



    return 


def get_hospital_urls(url):
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        hospital_informations=soup.find_all('h3', class_="name")    
        base_url="https://www.iryou.teikyouseido.mhlw.go.jp"

        hospital_urls=[
        base_url + hospital_information.find('a').get('href')
        for hospital_information in hospital_informations
        ]
    except:
         print(f"erorr: get_hospital_urls")

    return hospital_urls

def get_hospital_informations(url):
        try:
            response = requests.get(url)
            
            soup = BeautifulSoup(response.content, 'html.parser')

            #院外処方、院外処方関する情報
            service_div = soup.find('div', attrs={'aria-labelledby': 'service'})
            # 属性を持たない<label>タグのみを抽出
            no_attribute_labels = [label for label in service_div.find_all('label') if not label.attrs]
            # テキストを抽出し、不要な空白を除去
            hospital_prescription_in_or_out = [x.get_text().strip() for x in no_attribute_labels if x.get_text(strip=True)]

            h1_tag=soup.find('h1' ,class_='pageTitle')
            hospital_name = h1_tag.find(string=True, recursive=False).strip()
            
            
            # 結果を辞書として返す
            return {
                'url': url,
                'status': 'success',
                '病院名': hospital_name,
                '院内処方': hospital_prescription_in_or_out[0],
                '院外処方': hospital_prescription_in_or_out[1]
            }

        except requests.RequestException as e:
            return {'url': url, 'status': 'error', 'message': f"リクエストエラー: {e}"}


if __name__ == "__main__":
    main()