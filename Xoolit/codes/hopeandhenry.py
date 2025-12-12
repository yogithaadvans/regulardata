import requests
import json
from datetime import date
from bs4 import BeautifulSoup
import time
import pytz
import re
import os
import math
UTC = pytz.utc
timeZ_Kl = pytz.timezone('Asia/Kolkata')

def calculate_offer(actual_price,offer_price):
    offer = round(100-((float(offer_price)*100)/float(actual_price)),1)
    return math.ceil(offer) if offer>0 and offer<1 else round(offer) if int(str(offer)[-1])>5 else math.floor(offer)

def folder_modification():
    desktop_path = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop')
    json_folder_path = os.path.join(desktop_path, "Json_files")
    if not os.path.exists(json_folder_path):
        os.mkdir(json_folder_path)
    today = date.today()
    cureent_date_folder=os.path.join(json_folder_path,today.strftime('%d-%m-%y'))
    #try to create a folder which be named as today date inside of output folder...............
    if not os.path.exists(cureent_date_folder):
       os.mkdir(cureent_date_folder)
    raw_data_folder_path = os.path.join(cureent_date_folder, "raw_data")
    if not os.path.exists(raw_data_folder_path):
        os.mkdir(raw_data_folder_path)
    return cureent_date_folder,raw_data_folder_path


category_mapping = [
    {
        "category_id" : "647659946350",
        "product_type" : "Shirts",
        "xoolit_subcategory": "Mens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "647659946350",
        "product_type" : "Outerwear",
        "xoolit_subcategory": "Mens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "647659946350",
        "product_type" : "Shorts",
        "xoolit_subcategory": "Mens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "647659946350",
        "product_type" : "Sweaters",
        "xoolit_subcategory": "Mens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "301254049953",
        "product_type" : "Dresses",
        "xoolit_subcategory": "Womens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "301254049953",
        "product_type" : "Outerwear",
        "xoolit_subcategory": "Womens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "301254049953",
        "product_type" : "Rompers",
        "xoolit_subcategory": "Womens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "301254049953",
        "product_type" : "Skirts",
        "xoolit_subcategory": "Womens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "301254049953",
        "product_type" : "Jumpsuits",
        "xoolit_subcategory": "Womens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "301254049953",
        "product_type" : "Pants",
        "xoolit_subcategory": "Womens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "301254049953",
        "product_type" : "Shirts",
        "xoolit_subcategory": "Womens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "category_id" : "301254049953",
        "product_type" : "Sweaters",
        "xoolit_subcategory": "Womens",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    }
  ]

def fetch_api_data(raw_data):
    data_list = []
    name_list = []

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://hopeandhenry.com',
        'priority': 'u=1, i',
        'referer': 'https://hopeandhenry.com/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }
    
    current_date_folder,raw_data_folder_path=folder_modification()
    for category in category_mapping:
        params = {
        'shop': 'zack-perlman.myshopify.com',
        'page': '1',
        'limit': '24',
        'pg': 'collection_page',
        'build_filter_tree': 'true',
        'collection_scope': category.get("category_id"),
        'currency_rate': '1.0',
        'currency': 'USD',
        'country': 'US',
        'pf_pt_product_type[]': category.get("product_type"),
    }
        response = requests.get('https://services.mybcapps.com/bc-sf-filter/filter', headers=headers, params=params)
        print(response)
        data = response.json()
        total_count = data.get("total_product", 0)
        print("Pagination:", total_count, "Category:", category.get("product_type"))

        pagination = max(1, total_count // 24)

        for page_size in range(1,pagination+1):
            params["page"] = page_size
            response = requests.get('https://services.mybcapps.com/bc-sf-filter/filter', headers=headers, params=params)
            print(response)
            page_data = response.json()

            products=page_data.get("products", [])
            raw_data+=products
            create_raw_data_json(raw_data,raw_data_folder_path)

            for item in products:
                actual_price = item.get("compare_at_price_max_usd")
                offer_price = item.get("price_max")
                print(actual_price,offer_price)
                if not actual_price:
                    continue
                offer = calculate_offer(actual_price,offer_price)
                
                offer_name = item["title"]
                if offer > 0 and offer != 100 and offer_name not in name_list:
                    name_list.append(offer_name)
                    data_list.append({
                        "offerName": offer_name,
                        "offerSource": "https://hopeandhenry.com/products/" + item.get("handle"),
                        "actualPrice": actual_price,
                        "offerPrice": offer_price,
                        "offer": offer,
                        "isPercentageOff": True,
                        "priority": category.get("priority"),
                        "offerImageUrl": item.get("images_info")[0].get("src"),
                        "tags": [category.get("xoolit_subcategory"),category.get("product_type")],
                        "description": item.get("body_html"),
                        "rating": "",
                        "ratedBy": "",
                        "category": [category.get("xoolit_category")],
                        "subCategory": category.get("xoolit_subcategory")
                    })

                    print(len(data_list),"data scrapped")            
                    my_json_dict=create_json(data_list,current_date_folder)
            
        time.sleep(3)
def create_raw_data_json(raw_data,raw_data_folder_path):
    with open((os.path.join(raw_data_folder_path,'hopeandhenry_raw_data-.json')), "w", encoding='utf-8') as file:
        json.dump(raw_data, file, ensure_ascii=False, indent=4)
           

def create_json(data_list,current_date_folder):
    my_json_dict={}
    my_json_dict['businessName'] = "Hope & Henry"
    my_json_dict['businessId'] = '62ab0acd753f059ed01fad8a'
    my_json_dict['classification'] = "622f7c43223ea99def05b462"
    my_json_dict['classificationTitle'] = "Regular"
    my_json_dict["data"]=data_list  
    with open((os.path.join(current_date_folder,'hopeandhenry.json')), "w", encoding='utf-8') as file:
        json.dump(my_json_dict, file, ensure_ascii=False, indent=4)
    
    return my_json_dict


def main():
    raw_data=[]
    fetch_api_data(raw_data)

if __name__ == "__main__":
    main()

