import requests
import json


def get_kfc(url, cname):
    """
    循环获取链接
    :param url:初始url
    :param cname：城市的名字
    :return:
    """
    page = 1
    while True:
        data = {
               'cname': cname,
               'pid': '',
               'pageIndex': page,
               'pageSize': '10'
                }
        response = requests.post(url, data=data)
        result = response.json()
        if result.get('Table1', ''):
            items = result.get('Table1')[0]
            save_kfc_data(items, cname)
            page += 1
        elif result.get('Table')[0]['rowcount'] == 0:
            print('该城市没有肯德基店铺')
            break
        else:
            break


def save_kfc_data(items, cname):
    """
    处理和储存数据
    :param items:Table1中的数据
    :param cname:城市名
    :return:
    """
    store_name = items['storeName'] + "餐厅"
    address = items['addressDetail']
    pro = items['pro']
    detail = {
        "餐厅名字": store_name,
        "地点": address,
        "礼品卡": pro
    }

    # 存储为TEXT文件
    with open(cname + '.text', 'a+', encoding='utf-8') as f:
        f.write(str(detail))


if __name__ == '__main__':
    cname = input('请输入城市名：')
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
    get_kfc(url, cname)
