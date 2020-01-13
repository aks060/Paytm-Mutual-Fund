#!/usr/bin/python3
import os
import json
import requests
import sqlite3

con=sqlite3.connect('database.db')
cur=con.cursor()
s=requests.session()
s.cookies['x-user-agent']='{"platform":"web","app_version":"2.0.0"}'
s.cookies['x-sso-token']='<Your SSO Token from cookie>'
head={
	'x-request-id': '<Get it FROM header Parameter>',
'x-user-id': '<GET it FROM header Parameter> '
}

res=s.get('https://paytmmoney.com/api/user/portfolio/mf', headers=head)
js=json.loads(res.content.decode())
mf=js['data']['schemeView']['results']
#os.system('echo "'+mf+'">mf.json')
print(json.dumps(mf))
for i in mf:
	dat=cur.execute('SELECT checkpoint, days FROM mf WHERE mfid="'+i['investmentDetails']['isin']+'"').fetchall()
	if dat==[]:
		#print('no checkpoint allocated. Please set checkpoint')
		if i['portfolioSipDetails']['sipStatus']!='':
			while 1:
				print('It\'s look you are investing SIP: ')
				p=int(input('Enter amount you spending each month: '))
				tt=int(input('Time in month of investing: '))
				r=float(input('Rate per year: '))
				calc=(int(tt)*int(tt+1))/2
				profit=((p*r*calc)/(100*12))
				total=profit+(p*tt)
				print('Total Profit: '+str(profit))
				print('Total money you will get: '+str(total))
				yn=input('Agree? (y/n): ')
				if(yn=='y' or yn=='Y'):
					break;
		chkpt=float(input('no checkpoint allocated. Please set checkpoint for '+i['investmentDetails']['isinName']))
		os.popen('notify-send -t 100000 "no checkpoint allocated. Please set checkpoint for '+i['investmentDetails']['isinName']+'"')
		if cur.execute('INSERT INTO mf (mfid, mfname, invested, checkpoint) VALUES("'+i['investmentDetails']['isin']+'", "'+i['investmentDetails']['isinName']+'", '+str(i['investmentDetails']['totalInvestedAmount'])+', '+str(chkpt)+')'):
			print('Data inserted')
		else:
			print('Sorry Not inserted')
		con.commit()
	else:
		chkpt=float(dat[0][0])
		reset=int(i['investmentDetails']['createdDate'])
		if dat[0][1]!=None:
			reset=int(dat[0][1])
		days=int((int(i['investmentDetails']['updatedDate'])-reset)/(1000*60*60*24))
		if float(dat[0][0])<=float(i['investmentDetails']['totalReturns']):
			os.popen('notify-send -t 100000 "'+i['investmentDetails']['isinName']+' crossed the checkpoint" "Invested: '+str(i['investmentDetails']['totalInvestedAmount'])+'\nCurrent Value: '+str(i['investmentDetails']['totalCurrentValue'])+'\nCheckpoint: '+str(chkpt)+'\nReturns: '+str(i['investmentDetails']['totalReturns'])+'\nDays spend: '+str(days+1)+'"')
		else:
			os.popen('notify-send -t 30000 "'+i['investmentDetails']['isinName']+'" "Invested: '+str(i['investmentDetails']['totalInvestedAmount'])+'\nCurrent Value: '+str(i['investmentDetails']['totalCurrentValue'])+'\nCheckpoint: '+str(chkpt)+'\nReturns: '+str(i['investmentDetails']['totalReturns'])+'\nDays spend: '+str(days+1)+'"')
