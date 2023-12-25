from datetime import datetime
from urllib.parse import quote
import requests
from lxml import html
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#通用的方法，主要是需要伪装头，cookie的规律找起来也很麻烦
#获取雪球的实时消息就是通过找cookie实现
# 发送HTTP请求并获取页面内容
def crawl_usual():
    url = "https://www.msn.cn/zh-cn/community/channel/vid-yigrey3aqwvu8msgcwqkicf3gvj43va4rtcwf4wgrgici2gi2eps"
    response = requests.get(url)
    print(response.text)
    # 使用lxml解析页面内容
    tree = html.fromstring(response.text)

    # 使用XPath表达式提取指定元素的文本内容
    xpath_expression = "/html/body/div[1]/div/div/fluent-design-system-provider/div/div[4]/div/div/div/div[2]/div[3]/div/div/fluent-design-system-provider/msft-feed-layout[1]//msft-article-card[1]/msft-article/text()"
    result = tree.xpath(xpath_expression)
    print(result)

#通过数据接口，一般可以从官方的开发api文档中找
def hot_search_api(num):
    url = 'https://weibo.com/ajax/side/hotSearch'
    response = requests.get(url)
    if response.status_code != 200:
        print('获取微博热搜榜失败')
        return
    data= response.json()['data']
    print(datetime.now().strftime('微博热搜榜 20%y年%m月%d日 %H:%M'))
    print(f"置顶:{data['hotgov']['word'].strip('#')}")
    for i, rs in enumerate(data['realtime'][:num], 1):
        title = rs['word']
        try:
            label = rs['label_name']
            if label in ['新', '爆', '沸']:
                label = label
            else:
                label = ''
        except:
            label = ''
        print(f"{i}. {title} {label} 链接：https://s.weibo.com/weibo?q={quote(title)}&Refer=top")
        # print(f"{i}. {title} {label}")


#搭配selenium，模拟浏览
def hot_search_selenium():
    # 配置浏览器选项
    opts = Options()
    mobile_emulation = {"deviceMetrics": {"width": 375, "height": 677, "pixelRatio": 2.0},
                        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/116.0.0.0"}
    opts.add_experimental_option("mobileEmulation", mobile_emulation)
    opts.add_argument('--headless')  # 启用无头模式
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')

    # 运行远程Chrome 浏览器
    #driver = webdriver.Remote(command_executor='http://ip:4444/wd/hub', options=opts)


    # 创建浏览器
    driver = webdriver.Chrome(options=opts)
    driver.set_window_size(375, 750)  # 窗口大小
    name = datetime.now().strftime('20%y年%m月%日%H时%M分')
    # 导航到要截图的页面
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    driver.get(url)

    # 截取整个页面
    print("正在运行，请稍后……")
    time.sleep(10)
    driver.get_screenshot_as_file(f'screenshot/{name}.png')
    # 关闭浏览器
    driver.quit()
    print("运行完毕，请于文件夹中查看")




if __name__ == '__main__':
    num = 20 #获取热搜的数量
    #hot_search_api(num)
    #hot_search_selenium()
    crawl_usual()
