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
        "id": "outlet > outlet-women",
        "xoolit_subcategory": "Footwear and Accessories",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "id": "outlet > outlet-men",
        "xoolit_subcategory": "Footwear and Accessories",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d4f24ce0bc001321fa27',
                "categoryName": "Apparel & Clothing"
                }
    },
    {
        "id": "outlet > outlet-kids",
        "xoolit_subcategory": "Kids Footwear",
        "priority": 1,
        "xoolit_category":{
                "_id": '6062d5774ce0bc001321fa2b',
                "categoryName": "Babies & Kids"
                }
    }
  ]

def fetch_api_data(raw_data):
    data_list = []
    name_list = []
    
    headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.crocs.com',
    'Referer': 'https://www.crocs.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'content-type': 'text/plain',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
    
    current_date_folder,raw_data_folder_path=folder_modification()
    for category in category_mapping:
        
        data = {"requests":[{"indexName":"production_crocs_us__products__default","analytics":True,"attributesToRetrieve":["name","url","image","altImage","gender","master","brand","ratingPercent","ratingCount","pricing","snipes","color","colorVariations","colorDefaults","refinementJibbitz","flatCategories","gender"],"clickAnalytics":True,"facets":["gender","jibbitable","lifestyle","pricing.price","refinementColor","refinementOccasion","refinementSizes"],"filters":"categoryIDs:\'{0}\'","highlightPostTag":"__/ais-highlight__","highlightPreTag":"__ais-highlight__","hitsPerPage":36,"maxValuesPerFacet":100,"page":0,"query":"","userToken":"anonymous-9bcec287-d3d0-468f-a0fe-b0c0080df2ef"}]}
        data["requests"][0]["filters"]= data["requests"][0].get("filters").format(category.get("id"),0)
        print(data)
        response = requests.post(
            'https://jrq5ug04de-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(5.29.0)%3B%20Lite%20(5.29.0)%3B%20Browser%3B%20instantsearch.js%20(4.79.0)%3B%20react%20(17.0.2)%3B%20react-instantsearch%20(7.16.0)%3B%20react-instantsearch-core%20(7.16.0)%3B%20JS%20Helper%20(3.26.0)&x-algolia-api-key=cbc84872f615adcc4d79c3b194e49c86&x-algolia-application-id=JRQ5UG04DE',
            headers=headers,
            json=data
        )
        print(response)
        data = response.json()
        count  = data.get("results")[0].get("nbPages")

        pegination = count
        print("pegination: ",pegination,"deal_count : ",count,"category",category.get("subcategory"))
        for page_no in range(0,pegination+1):
            data = {"requests":[{"indexName":"production_crocs_us__products__default","analytics":True,"attributesToRetrieve":["name","url","image","altImage","gender","master","brand","ratingPercent","ratingCount","pricing","snipes","color","colorVariations","colorDefaults","refinementJibbitz","flatCategories","gender"],"clickAnalytics":True,"facets":["gender","jibbitable","lifestyle","pricing.price","refinementColor","refinementOccasion","refinementSizes"],"filters":"categoryIDs:\'{0}\'","highlightPostTag":"__/ais-highlight__","highlightPreTag":"__ais-highlight__","hitsPerPage":36,"maxValuesPerFacet":100,"page":page_no,"query":"","userToken":"anonymous-9bcec287-d3d0-468f-a0fe-b0c0080df2ef"}]}
            data["requests"][0]["filters"]= data["requests"][0].get("filters").format(category.get("id"))

            response = requests.post(
                'https://jrq5ug04de-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(5.29.0)%3B%20Lite%20(5.29.0)%3B%20Browser%3B%20instantsearch.js%20(4.79.0)%3B%20react%20(17.0.2)%3B%20react-instantsearch%20(7.16.0)%3B%20react-instantsearch-core%20(7.16.0)%3B%20JS%20Helper%20(3.26.0)&x-algolia-api-key=cbc84872f615adcc4d79c3b194e49c86&x-algolia-application-id=JRQ5UG04DE',
                headers=headers,
                json=data,
            )
            data = response.json()

            product=data["results"][0]["hits"]
            raw_data+=product
            create_raw_data_json(raw_data,raw_data_folder_path)

            for item in product:
                
                if item==None or item.get("image") ==None or item.get("pricing").get("regularPrice")==None or item.get("pricing").get("salePriceLow")==None:
                    continue
                actual_price_str = item.get("pricing").get("regularPrice")
                actual_price = float(actual_price_str.replace("$",""))
                offer_price = item.get("pricing").get("price")
                print(actual_price,offer_price)
                if actual_price == None or offer_price ==None:
                    continue
                offer = calculate_offer(actual_price,offer_price)
                
                offer_name = item["name"]
                if actual_price > offer_price and offer>0 and  offer!=100 and offer_name not in name_list:
                    name_list.append(offer_name) 
                    product_info_dict = {}
                    product_info_dict["offerName"]=offer_name
                    product_info_dict["offerSource"]="https://www.crocs.com"+item["url"]
                    product_info_dict['actualPrice']=actual_price
                    product_info_dict["offerPrice"]=offer_price
                    product_info_dict["offer"] = offer
                    product_info_dict["isPercentageOff"] = True
                    product_info_dict["offerImageUrl"]=item.get("image")
                    product_info_dict["tags"] = [category.get("xoolit_subcategory")]

                    product_info_dict["description"]=""

                    product_info_dict["rating"] = ""
                    product_info_dict['ratedBy'] = ""
                    product_info_dict["gender"]=""
                    product_info_dict['category'] =[category.get("xoolit_category")]
                    product_info_dict['subCategory']=category.get("xoolit_subcategory")

                    data_list.append(product_info_dict)
                    print(len(data_list),"data scrapped")            
                    my_json_dict=create_json(data_list,current_date_folder)
        
        time.sleep(3)
def create_raw_data_json(raw_data,raw_data_folder_path):
    with open((os.path.join(raw_data_folder_path,'Crocs_raw_data-.json')), "w", encoding='utf-8') as file:
        json.dump(raw_data, file, ensure_ascii=False, indent=4)
           

def create_json(data_list,current_date_folder):
    my_json_dict={}
    my_json_dict['businessName'] = "Crocs"
    my_json_dict['businessId'] = '62aad32a753f059ed01fac9c'
    my_json_dict['classification'] = '622f7c43223ea99def05b462'
    my_json_dict['classificationTitle'] = 'Regular'
    my_json_dict["data"]=data_list  
    with open((os.path.join(current_date_folder,'Crocs.json')), "w", encoding='utf-8') as file:
        json.dump(my_json_dict, file, ensure_ascii=False, indent=4)
    
    return my_json_dict


def main():
    raw_data=[]
    fetch_api_data(raw_data)

if __name__ == "__main__":
    main()

