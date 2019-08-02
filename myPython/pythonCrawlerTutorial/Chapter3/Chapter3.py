import socket
import urllib.request
import urllib.parse
import urllib.error
from urllib.request import HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm, build_opener, ProxyHandler
import http.cookiejar
"""  3.1  urllib库的使用  """

# 3.1.1 发起请求

def fun1():
    """  urlopen的使用，使用urlopen可以发送简单的请求 """
    response = urllib.request.urlopen("https://www.baidu.com")
    print(response.read().decode('utf-8'))
    print(type(response), response.__module__, response.__class__)
    print(response.status)
    print(response.getheaders())
    print(response.getheader('Server'))


def fun2():
    """  urlopen的data参数  """
    data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf-8')
    response = urllib.request.urlopen(url="http://www.httpbin.org/post", data=data)
    print(response.read().decode('utf-8'))


def fun3():
    """  urlopen的timeout参数  """
    try:
        response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout): # reason属性貌似是URLError特意设置的，并非所有的异常都有
            print(e.reason)
            print('Time Out')


def fun4():
    """   Requests类的使用，可以配合urlopen发起更为复杂的请求，如设置请求头，请求方法等  """
    url = "http://httpbin.org/post"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Host': 'httpbin.org'
    }
    dict = {
        'name': 'Germey'
    }
    data = bytes(urllib.parse.urlencode(dict), encoding='utf8')
    req = urllib.request.Request(url=url, headers=headers, data=data, method='POST')
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))


def fun5():
    """   利用HTTPBasicAuthHANDLER发起需要验证密码的请求  """
    username = 'username'
    password = 'password'
    url = 'blah'
    p = HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None,uri=url, user=username, passwd=password)
    auth_handler = HTTPBasicAuthHandler(p)
    opener = build_opener(auth_handler)
    opener.open(url)


def fun6():
    """   添加代理  """
    proxy_handler = ProxyHandler({
        'http': 'http://127.0.0.1:9743',
        'https': 'https://127.0.0.1:9743'
    })
    opener = build_opener(proxy_handler)
    try:
        response = opener.open("https://www.baidu.com")
        print(response.read().decode('utf8'))
    except urllib.error.URLError as e:
        print(e.reason)


def fun7():
    """  Cookies """
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = build_opener(handler)
    opener.open('http://www.baidu.com')
    for item in cookie:
        print(item.name + '=' + item.value)


def fun8():
    """   利用文件保存或读取cookies  """

    # 保存
    file_name = '3_cookies.txt'
    cookie = http.cookiejar.LWPCookieJar(file_name)  # 也可以用MozillaCookieJar类实例化，二者的规格不同
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = build_opener(handler)
    opener.open('http://www.baidu.com')
    # save()的第一个参数意为cookies即使要被抛弃也要保存，第二个参数意为即使过期也要保存
    cookie.save(ignore_discard=True, ignore_expires=True)

    # 读取
    cookie2 = http.cookiejar.LWPCookieJar(file_name)
    cookie2.load(ignore_expires=True, ignore_discard=True)
    handler2 = urllib.request.HTTPCookieProcessor(cookie2)
    opener2 = build_opener(handler2)
    response = opener2.open('http://www.baidu.com')
    print(response.read().decode('utf8'))


# 3.1.2 处理异常

def fun9():
    """
    URLError  其属性reason可以描述错误的原因
    HTTPError URLError的子类，有属性code、headers、reason
    可以先捕获子类，再捕获父类
    reason不仅可以返回字符串，有时还会返回对象，见fun3
    """
    try:
        urllib.request.urlopen('https://cuiqingcai.com/index.htm')
    except urllib.error.HTTPError as e:
        print(e.reason, e.code, e.headers, sep='\n')
    except urllib.error.URLError as e:
        print(e.reason)
    else:
        print('Request Successfully')

#  3.1.3 解析连接

def fun10():
    """   urlparse：用于解析链接  """
    # 标准的链接格式：scheme://netloc/path;params?query#fragment
    result = urllib.parse.urlparse("http://www.baidu.com/index.html;user?id=5#comment")
    print(result)
    # 当url没有指明协议时，用scheme参数作为补充，否则以url为准
    result = urllib.parse.urlparse("www.baidu.com/index.html;user?id=5#comment", scheme="https")
    print(result)
    result = urllib.parse.urlparse("http://www.baidu.com/index.html;user?id=5#comment", scheme='https')
    print(result)
    # allow_fragments为True时，fragment会被附加到别的参数中去
    result = urllib.parse.urlparse("http://www.baidu.com/index.html;user?id=5#comment", allow_fragments=False)
    print(result)
    result = urllib.parse.urlparse("http://www.baidu.com/index.html#comment", allow_fragments=False)
    print(result)
    # ParseResult对象可以通过索引和属性名获得相应的值
    print(result.scheme, result[0], result.netloc, result[1], sep='\n')
    """  urlunparse：相反用途，必须提供六个参数  """
    data = ['http', 'www.baidu.com', 'index.html', 'user', 'id=5&uid=6', 'comment']
    print(urllib.parse.urlunparse(data))


def fun11():
    """   urlsplit：同urlparse，只是把params合并到了path中  """
    result = urllib.parse.urlsplit("http://www.baidu.com/index.html;user?id=4#comment")
    print(result)
    print(result.scheme, result[0], sep='\n')
    """  urlunsplit：相反作用  """
    data = ['http', 'www.baidu.com', 'index.html;user', 'id=5', 'comment']
    print(urllib.parse.urlunsplit(data))


def fun12():
    """
     urljoin: 用base_url给新的url作参数补充，矛盾时以新url为主
     只能补充scheme、netloc、path三种参数
    """
    from urllib.parse import urljoin
    print(urljoin('http://baidu.com', 'FAQ.html'))
    print(urljoin('http://www.baidu.com', 'http://cuiqingcai.com/FAQ.html'))
    print(urljoin('http://www.baidu.com/about.html', 'http://cuiqingcai.com/FAQ.html?question=2'))
    print(urljoin('http://www.baidu.com?wb=abc', 'http://cuiqingcai.com/index.php'))
    print(urljoin('http://www.baidu.com', '?category=2#commment'))
    print(urljoin('www.baidu.com', '?category=2#comment'))
    print(urljoin('www.baidu.com#comment', '?category=2'))


def fun13():
    """   urlencode使用， 用于拼接查询参数, 后两个函数用于反拼接  """
    from urllib.parse import urlencode, parse_qs, parse_qsl
    params = {
        'a': 123,
        'b': 456
    }
    s = urlencode(params)
    print(s)
    # 字典形式反拼接
    print(parse_qs(s))
    # 元组形式反拼接
    print(parse_qsl(s))


def fun14():
    """   避免中文乱码问题，将中文字符转为URL编码模式  """
    from urllib.parse import quote, unquote
    ch = "中文"
    by = quote('中文')
    ch2 = unquote(by)
    print(ch, by, ch2, sep='\n')

# 3.1.4 分析Robot协议
def fun15():
    pass


"""  3.2  requests库的使用  """


def fun():
    pass


fun14()