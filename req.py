import requests as rq
import json
import pandas as pd
from time import sleep
########################################### post request headers + pyload #################################

def request_spider():
    api_headers = {
        'content-type': 'application/json',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    null=None

    api_url = 'https://axieinfinity.com/graphql-server-v2/graphql'

    api_pyload = {"operationName":"GetAxieBriefList","query":"query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\naxies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n  total\n  results {\n    ...AxieBrief\n    __typename\n  }\n  __typename\n}\n      }\n\n      fragment AxieBrief on Axie {\nid\nname\nstage\nclass\nbreedCount\nimage\ntitle\ngenes\nbattleInfo {\n  banned\n  __typename\n}\nauction {\n  currentPrice\n  currentPriceUSD\n  __typename\n}\nstats {\n  ...AxieStats\n  __typename\n}\nparts {\n  id\n  name\n  class\n  type\n  specialGenes\n  __typename\n}\n__typename\n      }\n    \n      fragment AxieStats on AxieStats {\n       hp\n       speed\n       skill\n       morale\n__typename\n      }",
    "variables":
        {
        "auctionType":"Sale",
        "criteria":{
            "classes":[],  #this one
            "parts":[],
            "hp":null,
            "speed":null,
            "skill":null,
            "morale":null,
            "breedCount":[0,0],
            "pureness":[6],
            "numMystic":[],
            "title":null,
            "region":null,
            "stages":[3,4]
                    },
        "from":0,  #this one
        "size": 100, #this one
        "sort":"PriceAsc",
        "owner":null
        }
    }

    ##########

    #### get all the data
    data = {}
    item_idx = -1
    req_results_size = 1
    total_axies_size = 0
    results = []
    req_data = {}

    r1 = rq.post(url=api_url,headers=api_headers,data=json.dumps(api_pyload)).json()
    total_axies_size = r1["data"]["axies"]["total"]
    print()
    while req_results_size != 0:
        r = rq.post(url=api_url,headers=api_headers,data=json.dumps(api_pyload))
        if(not r.ok):
            print("request failed :",r.status_code)
        else:
            req_data = r.json()
            try:
                req_results_size = len(req_data["data"]["axies"]["results"])
                results += req_data["data"]["axies"]["results"]
                api_pyload["variables"]["from"] += 100
            except:
                print("-----  exception  ------ ")
                api_pyload["variables"]["from"] -= 100
            print("scrapped results   :  ",(len(results)))
            if(total_axies_size != 0):
                print("Scraping ------------------> ",int((len(results)/total_axies_size)*100)," %")
    #save data 

    #in dict
    for res in results:
        id = res["id"]
        price = res["auction"]["currentPriceUSD"] 
        # save in pandas 
        item_idx += 1
        data[item_idx] = [id,price]

    #from dict to csv
    df = pd.DataFrame().from_dict(data,orient='index',columns=['id','price'])
    df.to_csv("prices.csv",index=False)