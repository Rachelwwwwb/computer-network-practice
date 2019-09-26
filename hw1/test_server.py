#!/usr/bin/env python3
# coding = utf-8
 
import os
import sys
import socket
 
 
# 登录判断
def do_login(s, user, name, addr):
    if (name in user) or name == '管理员':
        s.sendto('用户名已存在'.encode(), addr)
        return
    else:
        s.sendto('OK'.encode(), addr)
        # 通知其他人欢迎进去聊天室
 
        msg = '\n欢迎 %s 进入聊天室' % name
        for i in user:
            s.sendto(msg.encode(), user[i])
        # 插入用户
        user[name] = addr
 
 
def do_chat(s, user, name, text):
    msg = '\n%s 说 %s\n' % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])
 
 
# 退出聊天室
def do_quit(s, user, name):
    msg = name + '退出聊天室'
    for i in user:
        if i == name:
            s.sendto(b'EXIT', user[i])
        else:
            s.sendto(msg.encode(), user[i])
    del user[name]
 
 
# 接收客户端请求
def do_parent(s):
    # 存储结构({'zhangsan':(127.0.0.1,9999)})
    user = {}
    while True:
        msg, addr = s.recvfrom(1024)
        msgList = msg.decode().split(' ')
        # 区分请求类型
        if msgList[0] == 'L':  # L为请求登录
            do_login(s, user, msgList[1], addr)
        elif msgList[0] == 'C':
            do_chat(s, user, msgList[1], ' '.join(msgList[2:]))
        elif msgList[0] == 'Q':
            do_quit(s, user, msgList[1])
 
 
# 创建网络,进程,调用功能函数
def main():
    # server address
    ADDR = ('0.0.0.0', 9999)
 
    # 创建数据报套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(ADDR)
 
    # 创建一个单独的进程处理管理员喊话功能
    pid = os.fork()
    if pid < 0:
        sys.exit('创建进程失败')
    elif pid is not 0:
        do_parent(s)
 
 
if __name__== "__main__":
    main()