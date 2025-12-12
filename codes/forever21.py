import re
import os
import math
import json
import requests
from sys import platform
from datetime import date
from bs4 import BeautifulSoup

def fetch_json_folder_path(**kwargs):
    if platform == 'win32':
        json_folder_path = os.path.join(os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop'), kwargs.get('folder'))
    else:
        json_folder_path = os.path.join(os.path.join(os.path.join(
            os.path.expanduser('~')), 'Desktop'), kwargs.get('folder'))

    if not os.path.exists(json_folder_path):
        os.mkdir(json_folder_path)
    today = date.today()
    current_date_folder=os.path.join(json_folder_path,today.strftime('%d-%m-%y'))
    if not os.path.exists(current_date_folder):
       os.mkdir(current_date_folder)
   
    return current_date_folder

def create_json(**kwargs):
    output_lst=kwargs.get("output_list")
    folder_path=kwargs.get("folder_path")
    my_json_dict = {}
    my_json_dict['businessName'] = "Forever 21"
    my_json_dict['businessId'] = '62aac296b98eca1b487c6cec'
    my_json_dict['classification'] = "622f7c43223ea99def05b462"
    my_json_dict['classificationTitle'] = "Regular"
    my_json_dict["data"] = output_lst

    with open((os.path.join(folder_path,'forever21.json')), "w", encoding='utf-8') as file:
            json.dump(my_json_dict, file, ensure_ascii=False, indent=4)
    return my_json_dict

def calculate_offer(actual_price,offer_price):
    offer = round(100-((float(offer_price)*100)/float(actual_price)),1)
    return math.ceil(offer) if offer>0 and offer<1 else round(offer) if int(str(offer)[-1])>5 else math.floor(offer)

def fetch_response(**kwargs):
   
    response = requests.get(kwargs.get("url"),
                            params=kwargs.get("params"),
                            headers=kwargs.get("headers"))
    print(response)
    return response.text

def fetch_data(**kwargs):
    categories = kwargs.get("categories")
    headers=kwargs.get("headers")
    product_link_dict={}
    name_list=[]

    for category in categories:
            xoolit_subcategory=category["xoolit_subcategory"]
            xoolit_category = category["xoolit_category"]
            subcategory_url = category["subcategory_url"]
            priority_value=category["priority"]  
            params = {
                    'filter.p.m.custom.shop_by_department': subcategory_url,
                    'page': '1',
                }
            response = requests.get('https://www.forever21.com/collections/f21-shop-all-sale-1',
                                    params = params,
                                    headers=headers
                        ) 
            print("resp",response, subcategory_url)
            data=response.text
            soup = BeautifulSoup(data, 'html.parser')        
            dealcount= int(soup.select_one('p.collection-toolbar__products-count').text.split()[0])
            print("count",dealcount)

            if dealcount > 48:
                pagination = dealcount//48
            else:
                pagination = 1
            print("Pagination_Items",pagination)

            for page_no in range(1, pagination+1):
                params["page"] =  str(page_no)
                response = requests.get(
                                    'https://www.forever21.com/collections/f21-shop-all-sale-1',
                                    params=params,
                                    headers=headers,
                                )
                print(response)
                soup_ = BeautifulSoup(response.text, 'lxml')
                soup = soup_.body
                product_grids = soup.find_all("product-card",{"class":"product-card"})
                print("grid",len(product_grids))

                for product_div in product_grids:
                    if product_div.select_one('.price-list sale-price')==None:
                        continue
                    name=product_div.select_one('a.product-title')
                    if  name and name.text not in name_list:
                        name_list.append(name.text)
                        product_url="https://www.forever21.com"+product_div.find("a").get("href")
                        # print(product_url)
                        product_link_dict[product_url] =[xoolit_category,xoolit_subcategory,subcategory_url,priority_value]
                print(len(product_link_dict),"Links extracted")
    return product_link_dict


def fetch_detail_page(**kwargs) :
    
    product_link_dict=kwargs.get("product_link_dict")
    folder_path=kwargs.get("folder_path")
    headers=kwargs.get("headers")
    output_list=[] 
    
    for url,values in product_link_dict.items():
        response=requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        product_info_dict={}
        offername_selector=soup.select_one("h1")
        actual_price_selector=soup.select_one("compare-at-price.h5")
        offer_price_selector=soup.select_one("sale-price.h4")
        image_selector=soup.select_one(".is-initial img")
        description_selector=soup.select_one("section.d_wrapper:nth-of-type(1) div")
        
        if offername_selector and actual_price_selector and offer_price_selector :
            offerName=offername_selector.text.title().strip().replace("\n"," ").replace("\t"," ")
            product_info_dict["offerName"]=offerName
            actual_price = float(re.sub(r"[^Z0-9,^Z.]", "", actual_price_selector.text).replace(",",""))
            offer_price = float(re.sub(r"[^Z0-9,^Z.]", "", offer_price_selector.text).replace(",",""))
            product_info_dict['actualPrice']=actual_price
            product_info_dict["offerPrice"]=offer_price
            offer =calculate_offer(actual_price,offer_price)
            product_info_dict["offer"]=offer
            product_info_dict["isPercentageOff"]=True 
            product_info_dict["offerImageUrl"]= "https:" + image_selector.get("src")
            if description_selector:
                product_info_dict["description"]=description_selector.text.strip().replace("\n"," ").replace("\t"," ")
            else:
                product_info_dict["description"]=""
            product_info_dict["priority"] = values[-1]
            product_info_dict["offerSource"]=url
            product_info_dict["gender"]=""            
            try:
                rating_value = soup.select_one(".total_reviews").text
                rating_data = rating_value.split()
                product_info_dict["rating"]=float(rating_data[0].replace("(","").replace(")",""))
                product_info_dict["ratedBy"]=int(rating_data[1]) 
            except:
                product_info_dict["rating"]=""
                product_info_dict["ratedBy"]="" 
            product_info_dict['category'] =  [values[0]]
            product_info_dict["subCategory"]=values[1]
            product_info_dict["priority"]=values[-1]
            product_info_dict["tags"]=[values[1],values[2]]
            product_info_dict["specification"] = [

                    ]
            if offer>0 and offer<100:
                output_list.append(product_info_dict)
                print(len(output_list), "data scrapped")
                json_data =create_json(output_list=output_list,folder_path=folder_path)
    
    return json_data
    
def main():
    folder_path=fetch_json_folder_path(folder="Json_files")
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.forever21.com/collections/womens-sale',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'localization=US; cart_currency=USD; _shopify_y=28f59910-493e-4743-a036-f01db208fbf9; _tracking_consent=3.AMPS_INBR_f_f_pBL0gReESdWelrypdLDbSg; _orig_referrer=https%3A%2F%2Fwww.google.com%2F; _landing_page=%2F%3Fsrsltid%3DAfmBOopTq6nMRG2ZOMq4abDxwAGIfoNXZaY-GqW-Hf4I_YRgRk_vAAf_; _shopify_essential=:AZft8V-KAAEAS615nYlXtSWCHfDqIh_c0ufWHtYCWnNUi5wMM1rilIOGU1owmM5x37mIc10tgWy3uRaVxS2iSV5VBkj7:; _ga=GA1.1.1448083840.1752043709; shopify_pay_redirect=pending; _fbp=fb.1.1752043709492.603037185205807787; _shopify_s=12c85d80-9757-4fb0-b6fb-7b747e4a6510; _ga_7SPK77HF2V=GS2.1.s1752043709$o1$g1$t1752045148$j58$l0$h0; __kla_id=eyJjaWQiOiJPVEF4WmpOak9XWXRNbVUxTkMwMFpESmtMV0k1Tm1RdFptUmpaR1U0T0RFeE4yWTIiLCIkcmVmZXJyZXIiOnsidHMiOjE3NTIwNDM3MDksInZhbHVlIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJmaXJzdF9wYWdlIjoiaHR0cHM6Ly93d3cuZm9yZXZlcjIxLmNvbS8/c3JzbHRpZD1BZm1CT29wVHE2bk1SRzJaT01xNGFiRHh3QUdJZm9OWFphWS1HcVctSGY0SV9ZUmdSa192QUFmXyJ9LCIkbGFzdF9yZWZlcnJlciI6eyJ0cyI6MTc1MjA0NTE0OSwidmFsdWUiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsImZpcnN0X3BhZ2UiOiJodHRwczovL3d3dy5mb3JldmVyMjEuY29tLz9zcnNsdGlkPUFmbUJPb3BUcTZuTVJHMlpPTXE0YWJEeHdBR0lmb05YWmFZLUdxVy1IZjRJX1lSZ1JrX3ZBQWZfIn19; _ga_L1T9QR4S4K=GS2.1.s1752043709$o1$g1$t1752045153$j53$l0$h0; keep_alive=eyJ2IjoyLCJ0cyI6MTc1MjA0NTE1MzY2MiwiZW52Ijp7IndkIjowLCJ1YSI6MSwiY3YiOjEsImJyIjoxfSwiYmh2Ijp7Im1hIjo2LCJjYSI6NTAsImthIjowLCJzYSI6OCwidGEiOjAsImtiYSI6MCwidCI6NSwibm0iOjEsIm1zIjowLjI1LCJtaiI6MC43NiwibXNwIjowLjQxLCJ2YyI6MCwiY3AiOjAsInJjIjowLCJraiI6MCwia2kiOjAsInNzIjoyLjg0LCJzaiI6My44Mywic3NtIjoxLCJzcCI6MSwidHMiOjAsInRqIjowLCJ0cCI6MCwidHNtIjowfSwic2VzIjp7InAiOjMsInMiOjE3NTIwNDM3MDg3ODIsImQiOjE0Mjd9fQ%3D%3D',
}
    categories= [
    {
        "subcategory_url": "Women's",
        "xoolit_subcategory": "Womens",
        "priority": 1,
        "xoolit_category": {
            "_id": "6062d4f24ce0bc001321fa27",
            "categoryName": "Apparel & Clothing"
        }
    },
     {
        "subcategory_url": "Shoes",
        "xoolit_subcategory": "Footwear and Accessories",
        "priority": 1,
        "xoolit_category": {
            "_id": "6062d4f24ce0bc001321fa27",
            "categoryName": "Apparel & Clothing"
        }
    },
    {
        "subcategory_url": "Plus",
        "xoolit_subcategory": "Plus Sizes",
        "priority": 1,
        "xoolit_category": {
            "_id": "6062d4f24ce0bc001321fa27",
            "categoryName": "Apparel & Clothing"
        }
    },
    {
        "subcategory_url": "Men's",
        "xoolit_subcategory": "Mens",
        "priority": 1,
        "xoolit_category": {
            "_id": "6062d4f24ce0bc001321fa27",
            "categoryName": "Apparel & Clothing"
        }
    },
    {
        "subcategory_url": "Kids",
        "xoolit_subcategory": "Kids Clothing",
        "priority": 1,
        "xoolit_category": {
            "_id": "6062d5774ce0bc001321fa2b",
            "categoryName": "Babies & Kids"
        }
    }

    ]
    product_link_dict = fetch_data(headers=headers,categories=categories)
    my_json_dict=fetch_detail_page(
        product_link_dict=product_link_dict,
        folder_path=folder_path,
        headers=headers
        

    )
    
if __name__ == "__main__":
    main()