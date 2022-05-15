# -*- encoding: utf-8 -*-
'''
@Time            : 2022-05-10
@Author          : Snake8859
@Version         : 1.0
@Description     : 核酸检测点爬虫
'''
import os
import logging
import time
import csv
import json
import traceback
import requests
from datetime import datetime
from coordinate_transform import convert_MCT_2_BD09
from coordTransform_utils import bd09_to_wgs84

city = 'bj'

logging.basicConfig(
        format='%(asctime)s %(pathname)s - %(levelname)s: %(message)s',
        filename=os.path.join(
            "{0}_{1}_{2}.log".format(city, os.path.basename(__file__),
                                 datetime.now().strftime('%Y-%m-%d'))),
        filemode='a',
        level=logging.INFO)

# 头信息
headers = {
    "Accept":  'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "Accept-Encoding":  'gzip, deflate, br',
    "Accept-Language":  'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    "Cache-Control":  'max-age=0',
    "Connection":  'keep-alive',
    "Cookie": '__yjs_duid=1_f5d67b1aba20fe79ec96ca3cf15e96921626613981137; BIDUPSID=EA6AB4A3DADF4F66A736AB5905D88AE9; PSTM=1640696774; BAIDUID_BFESS=BAE860FEFD27EDA61B6CDA32C927DE87:FG=1; BDUSS=NNTlpIbUVPZDNld3ZQVTg2MVBXV0l-eHhFZHNXNjJ5aVRHTWxoekx2Y3E0SXhpRVFBQUFBJCQAAAAAAAAAAAEAAAAvCGw22Ly4pcmH08~LuQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACpTZWIqU2Vibn; BDUSS_BFESS=NNTlpIbUVPZDNld3ZQVTg2MVBXV0l-eHhFZHNXNjJ5aVRHTWxoekx2Y3E0SXhpRVFBQUFBJCQAAAAAAAAAAAEAAAAvCGw22Ly4pcmH08~LuQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACpTZWIqU2Vibn; RT="z=1&dm=baidu.com&si=jdnof49rwn&ss=l2ypxbwj&sl=3&tt=sj&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=3bz&ul=4at&hd=4b8"; ugcid=1-8246279dde9cb808-1652153833%7C2576663746; BAIDUID=1E90AC37AD37589990DE7C3364854D6D:FG=1; H_PS_PSSID=36429_31660_36422_36165_34584_35978_36055_35802_36346_26350_36315; BA_HECTOR=2l04a4ahak808521rq1h7kaou0q; MCITY=-131%3A; ab_sr=1.0.1_OTBjOTBhNzg5Y2M1ZDhlNDFmZDJlZDRjY2E2M2M3YmZhOGM4ZTA5OTgwZTRkZGU4NmRhZDVhNWQ4MmZjZDVlOGJkMTZmMzBiMGIwMzI1YmIzZjNjZTlhMWMxZGJjZDhhYTc1NTIwZjdiZGExYTZhODNjYThkMWYyNTY5YzY3MTIxM2YwNDIzMTVkZGQxYzE3ZjA5MWRiNjk4M2RjMWZkNA==',
    "Host": 'ugc.map.baidu.com',
    "Sec-Fetch-Dest": 'document',
    "Sec-Fetch-Mode": 'navigate',
    "Sec-Fetch-Site": 'none',
    "Sec-Fetch-User": '?1',
    "Upgrade-Insecure-Requests": '1',
    "User-Agent": '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    "sec-ch-ua-mobile": '?0',
    "sec-ch-ua-platform": '"Windows"'
}

# 模板URL
url = 'https://ugc.map.baidu.com/cube/nucdetect/areaInfo?poi_uid='

def get_hs_poi_info(out_file, metadata_file):
    """获取核酸检测点POI信息
    Args:
        out_file (str): 输出文件
        metadata_file (str): 输入元数据文件
    """
    # 追加模式，便于边爬取边写入
    with open(out_file, 'a', newline='', encoding='UTF-8') as o:
        o_csv = csv.writer(o)
        o_csv.writerow(['uid', 'poi_name', 'poi_address', 'poi_lon', 'poi_lat', 'city_id'])
        with open(metadata_file, 'r') as f:
            hs_metadata = json.loads(f.read())
            print(len(hs_metadata['result']['poi_list'])) # POI个数
            for item in hs_metadata['result']['poi_list']:
                print(item)
                poi_url = url + item['uid'] # 检测点id
                # print(poi_url)
                try:
                    resp = requests.get(poi_url, headers= headers)
                    if(resp.status_code == 200):
                        print(resp.text, type(resp.text))
                        result_text = resp.text
                        result = json.loads(resp.text)['result']
                        print(result)
                        # ! 坐标转换
                        # MCT TO BD09
                        mct_lon, mct_lat = result['point'].split(',')
                        bd09_lon, bd09_lat = convert_MCT_2_BD09(float(mct_lon), float(mct_lat))
                        # BO09 TO WGS84
                        # print(bd09_lon, bd09_lat)
                        wgs84_lon, wgs84_lat = bd09_to_wgs84(bd09_lon, bd09_lat)
                        # print(wgs84_lon, wgs84_lat)
                        o_csv.writerow([item['uid'], result['poi_name'], result['address'], wgs84_lon, wgs84_lat, item['city_id']])
                        logging.info('{0} ... success'.format(item['uid']))
                except Exception as e0:
                    traceback.print_exc()
                    logging.error('{0} ... fail'.format(item['uid']))
                    # time.sleep(10) # 睡眠10s再爬
                finally:
                    # break
                    pass
    
    return out_file

if __name__ == "__main__":
    out_file = './{0}_hs_pois1.csv'.format(city)
    metadata_file = './{0}_hs_metadata1.json'.format(city)
    out_csv = get_hs_poi_info(out_file, metadata_file)