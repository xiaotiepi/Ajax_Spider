import requests
import csv


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
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                result = response.json()
                if result.get('Table1', ''):
                    items = result.get('Table1')
                    for index, item in enumerate(items):
                        process_save_data(item, cname)
                    page += 1
                elif result.get('Table')[0]['rowcount'] == 0:
                    print('该城市没有肯德基店铺')
                    break
                else:
                    break
        except requests.ConnectionError as e:
            print('连接失败', e.args)
            break


def process_save_data(item, cname):
    """
    处理和存储数据
    :param items:Table1中的数据
    :param cname:城市名
    :return:
    """
    detail = {}
    detail['store_name'] = item.get('storeName') + '餐厅'
    detail['address'] = item.get('addressDetail')
    detail['pro'] = item.get('pro')
    # 写入CSV文件
    writer.writerow(detail, cname)


if __name__ == '__main__':
    cname = input('请输入城市名：')
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'

    with open(cname + '.csv', 'w') as csvfile:
        fieldnames = ['store_name', 'address', 'pro']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        get_kfc(url, cname)
    