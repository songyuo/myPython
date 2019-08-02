import os
import pickle
import shutil
import time
from io import StringIO, BytesIO
import json
from importlib import import_module
from multiprocessing.pool import Pool
import shelve


def fun1():
    out = [os.path.abspath(x) for x in os.listdir() if os.path.splitext(x)[1] == '.py']
    print(out)


def fun2():
    print(os.name)
    print(os.environ.get("Path"))


def fun3():
    root = os.path.abspath('.')
    path = os.path.join(root, "123")
    # os.mkdir(path)
    # time.sleep(5)
    os.rmdir(path)


def fun4():
    shutil.copyfile("./IOTest.py", "./copytest.py")


def fun5():
    f = StringIO()
    f.write("我")
    f.write("哈")
    f.write("哈")
    print(f.getvalue())


def fun6():
    f = StringIO("我哈哈哈\n我呵呵呵")
    print([line.strip() for line in f.readlines()])
    print(f.read())   # 第二次不输出


def fun7():
    f = BytesIO()
    f.write("站站".encode("gbk"))
    f.write("最骚".encode("gbk"))
    print(f.getvalue())
    print(f.getvalue().decode("gbk"))


def fun8():
    f = BytesIO("站站最骚".encode("gbk"))
    print(f.getvalue().decode("gbk"))
    print(f.read())
    print(f.read().decode("gbk"), flush=True)  # 第二次不输出


def fun9():
    """  用pickle进行序列化 """
    d = {"name": "张三", "age": 20, "sex": "男"}
    f = open("dump.pkl", "wb")
    pickle.dump(d, f)
    f.close()
    f = open("dump.pkl", "rb")
    dd = pickle.load(f)
    f.close()
    print(dd)


def fun10():
    """  用json序列化 注意打开文件不需要b """
    d = {"name": "张三", "age": 20, "sex": "男"}
    print(json.dumps(d, ensure_ascii=False, indent=''), type(json.dumps(d)))
    dd = '{"name": "张三", "age": 20, "sex": "男"}'
    print(json.loads(dd).get("age"))
    with open('dump.json', 'w') as f:
        json.dump(d, f)
    with open("dump.json", 'r') as f:
        print(json.load(f))


def fun11():
    """  json序列化自定义数据类型 """
    """  代码有问题，先搁置 """
    pool = Pool(processes=4)
    with open("pool_json.json", "w") as f:
        json.dump(pool, f, ensure_ascii=False, default=obj2dic)
        pool2 = json.load(f, object_hook=dic2obj)
    print(pool, pool2)


def obj2dic(obj):
    """  代码有问题，先搁置 """
    d = {'__class__': obj.__class__.__name__, '__module__': obj.__module__}
    d.update(obj.__dict__)
    return d


def dic2obj(d):
    """  代码有问题，先搁置  """
    module_name = import_module(d.pop('__module__'))
    class_name = d.pop('__name__')
    class_ = getattr(module_name, class_name)
    args = dict([(key, value) for key, value in d.items()])
    return class_(**args)


class Student:
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex


def fun12():
    """  shelve的使用  """
    tom = Student('tom', 18, 'male')
    marry = Student('marry', 20, "female")
    with shelve.open("student.db", flag='c', protocol=3) as f:
        f['tom'] = tom
        f['marry'] = marry
    with shelve.open('student.db', flag='c', protocol=3) as f:
        a = f['tom']
        print(a.name, a.age, a.sex)
        print(f['marry'])


if __name__ == "__main__":
    fun12()
    """  讲解序列化的网址 https://www.cnblogs.com/yyds/p/6563608.html  """
