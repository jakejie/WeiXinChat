# -*-coding:utf-8-*-
import sys
import itchat  # 这是一个用于微信回复的库
import requests

reload(sys)
sys.setdefaultencoding('utf8')

KEY = '******'  # 


# 向api发送请求
def get_response(msg):
    api_url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'pth-robot',
    }
    try:
        r = requests.post(api_url, data=data).json()
        # print r
        return r.get('text')
    except:
        return u'我不知道你说的是啥，这是自动回复的！'


# 处理私聊消息  注册方法
@itchat.msg_register(itchat.content.TEXT)
def to_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    default_reply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    # print reply
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    return '>|' + reply or default_reply


# 处理群聊消息
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        reply = get_response(msg['Text'])
        itchat.send(u'@%s\u2005| %s' % (msg['ActualNickName'], reply), msg['FromUserName'])
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复


# 处理多媒体类消息 包括图片、录音、文件、视频
@itchat.msg_register([itchat.content.PICTURE, itchat.content.RECORDING,
                      itchat.content.ATTACHMENT, itchat.content.VIDEO])
def download_files(msg):
    # msg['Text']是一个文件下载函数
    # 传入文件名，将文件下载下来
    msg['Text'](msg['FileName'])
    reply = u'你发的都是什么，信号不好听不到。给我打字好啦！'
    # 把下载好的文件再发回给发送者
    # return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
    # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], reply), msg['FromUserName'])
    itchat.send(u'@%s\u2005| %s' % (msg['ActualNickName'], reply), msg['FromUserName'])


# # 处理好友添加请求
@itchat.msg_register(itchat.add_friend)
def add_friend(msg):
    # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.add_friend(**msg['Text'])
    # 加完好友后，给好友打个招呼
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


if __name__ == '__main__':
    # 为了让修改程序不用多次扫码,使用热启动
    itchat.auto_login(hotReload=True)
    itchat.run()
