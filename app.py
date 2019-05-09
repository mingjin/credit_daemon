# -*- coding: UTF-8 -*-

from flask import Flask
from flask_script import Manager
import spider

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def hello():
    return 'hello world'


@app.route('/login/<username>/<password>')
def login(username, password):
    print('request is coming, params:%s, %s' % (username, password))
    ret = {}

    #这边参数要转字符串格式，否则驱动在模拟键盘输入密码时会有问题
    ret = spider.login(str(username), str(password))
    return ret
    

if __name__ == '__main__':
    manager.run()

#End
