import os
import json
import requests
import time
import mail

api_url = "https://api.ethermine.org"
class reminder:

    # 输入钱包地址
    def set_address(self):
        if os.path.exists("address.txt"):
            with open("address.txt", "r") as f:
                self.address = f.read()
        else:
            print("address.txt 没有找到. 初始化用户信息")
            self.address = input("钱包地址:")
            with open("address.txt", "w") as f:
                f.write(self.address)
        return self.address
    # 得到api接口url
    def get_workers_statistics_url(self):
        self.url = api_url+'/miner/'+self.address+'/workers'
        return self.url
    # get请求
    def get_workers_statistics(self):
        proxies = {'https': 'http://127.0.0.1:7890',
    'http': 'http://127.0.0.1:7890'}
        res = requests.get(self.url,proxies=proxies)
        return json.loads(res.content)
    def send_mail(self,receive,title,text):
        sender,token = mail.set_mail_sender()
        mail.mail(sender,token,receive,title,text)
    # 得到上次的数据
    def get_last_res(self):
        if os.path.exists("last.txt"):
            with open("last.txt", "r") as f:
                last = f.read()
                return json.loads(last)
        else:
            self.send_mail("liuzunxiong@qq.com", "初次运行","监控矿机开始运行")
            return None
    # 保存现在的数据
    def save_res(self,res):
        with open("last.txt", "w") as f:
            if type(res) == dict:
                res = json.dumps(res)
            f.write(res)

    def compare(self,res,last_res):
        data = res["data"];
        last_data = last_res["data"]
        flag = False
        info = ""
        j = 0
        for i in range(0,len(data)-1):
            ctime = data[i]["time"]-data[i]["lastSeen"]
            if data[i]["worker"]!=last_data[i+j]["worker"]:
                flag = True
                info += '\n'+last_data[i+j]["worker"]
                j += 1
            if ctime>1200:
                flag = True
                info += "\n矿机："+data[i]["worker"]+" "+time.strftime("%M分钟%S秒",time.localtime(ctime))+"未检测到上线"
        if flag:
            print(self.send_mail("liuzunxiong@qq.com", "矿机掉线",info))
        else:
            print("未出现矿机掉线")



if __name__ == '__main__':
    r = reminder()
    r.set_address()
    r.get_workers_statistics_url()
    res = r.get_workers_statistics()
    last_res = r.get_last_res()
    r.save_res(res)
    if last_res!=None:
        r.compare(res,last_res)




