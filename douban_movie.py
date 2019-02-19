'''
豆瓣电影纪录片爬虫,该网站的电影列表在ajax请求中，请求类型为GET。
网站地址：https://movie.douban.com/tag/#/
tags参数为电影形式
genres参数为类型（喜剧、动作、爱情...）
'''
import json
from requests_html import HTMLSession
from tqdm import tqdm  # 进度条包
from urllib.parse import urlencode

base_url = 'https://movie.douban.com/j/new_search_subjects?'
tags = '电影'
genres = '动画'


def get_page(url):
    '''
    获取链接和发送请求
    :param url:需要获取的链接
    :return:Ajax内容
    '''
    session = HTMLSession()
    try:
        r = session.get(url)
        if r.status_code == 200:
            results = r.html.html
            return results
        return None
    except Exception as e:
        print('请求失败', str(e))
        return None


def parse_page(results):
    '''
    解析Ajax内容，提取需要的东西
    :param results:Ajax内容
    :return:生成的豆瓣电影结果
    '''
    if results:
        results = json.loads(results)
        for index, result in enumerate(results.get('data')):
            douban = {}
            douban['directors'] = ''.join(result.get('directors'))
            douban['id'] = result.get('id')
            douban['rate'] = result.get('rate')
            douban['detail_url'] = result.get('url')
            douban['title'] = result.get('title')
            douban['casts'] = ''.join(result.get('casts'))
            yield douban
    else:
        print('没有结果')
        return None
        

def save_data(douban):
    '''
    存储结果为JSON文件
    :param douban:豆瓣结果生成器
    :return:
    '''
    with open('douban.json', 'a+', encoding='utf-8') as f:
        f.write(
            json.dumps(list(douban), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    for start in tqdm(range(0, 101, 20)):
        params = {
            'sort': 'U',
            'range': '0,10',
            'tags': tags,
            'genres': genres,
            'start': start
        }
        # 拼接链接
        url = base_url + urlencode(params)
        results = get_page(url)
        douban = parse_page(results)
        save_data(douban)
