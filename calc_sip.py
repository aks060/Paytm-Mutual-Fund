#!/usr/bin/python3
import os
import json
import requests
import datetime
import time
from collections import defaultdict
import sys

s=requests.session()
s.cookies['x-user-agent']='{"platform":"web","app_version":"2.0.0"}'
s.cookies['x-sso-token']='<Enter SSO Token From Browser Cookie>'
head={
	'x-request-id': '<Get it from header of Request to Paytm Money>',
'x-user-id': '<Get it from header of Request to Paytm Money>'
}

rd=input('Enter ID of MF: ')
res=s.get('https://paytmmoney.com/api/mf/isin/'+rd+'/chart', headers=head)
js=json.loads(res.content.decode())
mf=js['data']
print('data for: '+mf['name'])
gt=time.time()-31643326
#os.system('echo "'+mf+'">mf.json')
dic=defaultdict(int)
#print(dic)
mi=sys.maxsize
ind=0
for i in mf['navs']:
	if ((int)(i['date'])/1000)<gt:
		continue;
	date=datetime.datetime.fromtimestamp((int)(i['date'])/1000).strftime('%-d')
	dic[date]=dic[date]+(int)(i['value'])/12
#print(dic)
for i in range(1, 29):
	if mi > dic[str(i)]:
		mi=dic[str(i)]
		ind=str(i)
	print(str(i)+': '+str(dic[str(i)])+"\n")

print('min on: '+str(ind)+' with value '+str(mi))
