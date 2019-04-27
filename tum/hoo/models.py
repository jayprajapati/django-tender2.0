from django.db import models
import datetime
from django import forms

# Create your models here.

class users(models.Model):
	email=models.EmailField(unique=True,default="")
	firstname=models.CharField(max_length=20)
	lastname=models.CharField(max_length=20)
	password=models.CharField(max_length=20)
	
	is_verifed=models.BooleanField(default=False)
	org_name=models.CharField(max_length=20,default="")
	noti=models.IntegerField(default=-1)

	def __str__(self):
		return self.firstname + " " + self.lastname + " [" + str(self.id) + "] "


class document(models.Model):
	name=models.CharField(max_length=50)
	document_description=models.TextField()
	file=models.FileField(upload_to='uploads/%Y/%m/%d/')

class tender(models.Model):

	def pkgen():
		import random	
		pk=random.randint(100000000000,999999999999)
		return pk
	category_choice=(
		('G','GOODS'),
		('S','SERVICES'),
		('W','WORKS'),
	)
	product_category_choice=(
		('1','Civil Works'),
		('2','Advertisement Services'),
		('3','Computer Works'),
		('4','Electrical Works'),
		('5','Food'),
		)
	tenderID=models.CharField(primary_key=True,default=pkgen,max_length=25)
	title=models.CharField(max_length=100,default="None")
	organization_chain=models.CharField(max_length=100)
	category = models.CharField(max_length=1, choices=category_choice,default=False)
	product_category = models.CharField(max_length=1, choices=product_category_choice,default=False)
	
	emd_amount=models.PositiveIntegerField()
	emd_patable_to=models.TextField()
	published_date=models.DateTimeField(default=datetime.datetime.now,blank=True)
	bid_end_date=models.DateTimeField()
	documents=models.ManyToManyField(document)
	details=models.TextField()
	is_display=models.BooleanField(default=True)
	is_open=models.BooleanField(default=False)
	is_passed=models.BooleanField(default=False)

	def __str__(self):
		return self.tenderID + " | " + self.organization_chain 

	def __repr__(self):
	    return str(self.__dict__)
	    
class likes(models.Model):
	from_user=models.CharField(max_length=20)
	tenderID=models.CharField(max_length=25)
	is_liked=models.BooleanField(default=True)



class topping(models.Model):
	name=models.CharField(max_length=20)

class pizza(models.Model):
	name=models.CharField(max_length=20)
	toppings=models.ManyToManyField(topping)


class tran(models.Model):
	def pkgen():
		import random	
		s="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		s=list(s)
		key=[]
		for i in range(15):
			key.append(s[random.randint(0,len(s)-1)])
		key="".join(key)
		#pk=random.randint(100000000000,999999999999)
		return key
	def get_ts():
		import time
		return time.time()
	def dump_json(self):
		import json
		data={
		'transID':self.transID,
		'to_userID':self.to_userID,
		'bid_id':self.bid_id,
		'tenderID':self.tenderID,
		'timestamp':self.timestamp,
		'amount':self.amount,
		}
		#data= json.dumps(data)
		return data
		
	transID=models.CharField(default=pkgen,max_length=16)
	to_userID=models.CharField(max_length=20)
	bid_id=models.IntegerField()
	tenderID=models.CharField(max_length=50)
	amount=models.IntegerField()
	timestamp=models.CharField(max_length=30,default=get_ts)

class bids(models.Model):
	from_userID=models.IntegerField(default=0)
	tenderID=models.CharField(max_length=30,default=0)
	firstname=models.CharField(max_length=25)
	lastname=models.CharField(max_length=25)
	org_name=models.CharField(max_length=25)
	email=models.CharField(max_length=25)
	fileupload=models.FileField(default=False,upload_to='uploads/%Y/%m/%d/%H/%S' )
	amount=models.IntegerField()
	detail=models.TextField(default="None")
	
	def __str__(self):
		return str(self.tenderID) + " - from :" + str(self.from_userID) 
	


class bs(forms.Form):
	firstname=forms.CharField(label='First name', max_length=100)
	lastname=forms.CharField(label='Last name', max_length=100)
	org_name=forms.CharField(label='organization-chain name', max_length=100)
	email=forms.EmailField(label='Email Address')
	amount=forms.IntegerField(label='Bid Amount')
	fileupload=forms.FileField(label='Upload Documents')
	detail=forms.CharField(label='Enter Details Here',max_length=200, widget=forms.TextInput({}),help_text='This information can helps you to increase your chances')


class notifications(models.Model):
	to_userID=models.IntegerField()
	notification=models.CharField(max_length=100,default="None")
	pushed=models.IntegerField(default=0)

