# -*- coding: UTF-8 -*- 
from bs4 import BeautifulSoup
import sys,requests, json,re,string,sqlite3,time,datetime
#2018-08-06 13:57:56 by sixer

reload(sys) 
sys.setdefaultencoding('utf8') #设置编码，解决中文乱码

def GetNowTime():

    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def getMeterData(xm,xh):
	url='http://dag.ccnu.edu.cn/daqxcx.jsp?wbtreeid=1082&flag=1&xm='+xm+'&xh='+xh
	
	query = {'xm':xm,'xh':xh}
	
	data=json.dumps(query)
	headers={'content-type':'application/json','Connection':'close'}
	timeout=60
	
	response = requests.post(url,data=data,headers=headers,timeout=timeout)

	if response.status_code == 200:
		result=response.text

	bs = BeautifulSoup(result, "html.parser")
	daqx = bs.find('span', id='qyqx').get_text()
	dadw = bs.find('span', id='DWname').get_text()
	jdsj = bs.find('span', id='jdtime').get_text()
	ems = bs.find('span', id='jyh').get_text()

	
	cx.execute("replace into ccnuda (xm,xh,daqx,dadw,jdsj,ems) values ('"+xm+"','"+xh+"','"+daqx+"','"+dadw+"','"+jdsj+"','"+ems+"')")
	cx.commit()
	

print GetNowTime()

f = open("ccnuers.txt","r")
cx = sqlite3.connect("ccnumeter.db")
cu=cx.cursor()
for m in f:
	meter_list=m.strip().split(":")
	print meter_list[0]+','+meter_list[1]
	try:
		getMeterData(meter_list[0],meter_list[1])
	except requests.exceptions.Timeout:
  		print "服务器没有响应，获取（"+meter_list[0]+"）电量超时！"
	time.sleep(2)
cu.close()
cx.close()