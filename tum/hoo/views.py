from django.shortcuts import render,HttpResponseRedirect,reverse,HttpResponse,redirect
from django.http import Http404
from .models import *
from django.utils import timezone
# Create your views here.
from django.core.files.storage import FileSystemStorage


def indexPage(request):
	return render(request,'hoo/index.html')

def registerPage(request):
	if request.method=='GET':
		return render(request,'hoo/register.html')
	elif request.method=='POST':
		try:
			firstname=request.POST['Firstname']
			lastname=request.POST['Lastname']
			email=request.POST['Email']
			password=request.POST['password']
			cpassword=request.POST['cpassword']
			orgname=request.POST['orgname']
			user= users.objects.filter(email=email)
			if user:
				message='The email is already exists'
				return render(request,'hoo/register.html',{'message':message})
			else:
				if password==cpassword:
					newuser=users.objects.create(email=email,firstname=firstname,lastname=lastname,password=password,org_name=orgname)
					return HttpResponseRedirect(reverse('loginPage'))
				else:
					message='Password and Confirm password doesnt match!'
					return render(request,'hoo/register.html',{'message':message})
		except users.DoesNotExist:
			message='email alredy exists!'
			return render(request,'hoo/register.html',{'message':message})



def loginPage(request):
	if request.method=='GET':
		return render(request,'hoo/login.html')
	elif request.method=='POST':
		email=request.POST['email']
		password=request.POST['password']

		if email=="admin" and password=="mfadmin":
			request.session['email'] = "admin"
			request.session['firstname'] = "admin"
			request.session['lastname'] = "saheb"
			request.session['id'] = "-2158"
			request.session['is_admin'] = 1
			request.session['notifications'] = -1
			return HttpResponseRedirect(reverse('tenders'))

		if email=="" or password=="":
			message = "Please fill email and password correct!"
			return render(request,"hoo/login.html",{'message':message})
		
		user=users.objects.filter(email=email).first()

		if user:
			if user.password==password:
				request.session['email'] = user.email
				request.session['firstname'] = user.firstname
				request.session['lastname'] = user.lastname
				request.session['id'] = user.id
				request.session['is_admin'] = 0
				if user.noti == -1 :
					request.session['notifications'] = "No notifications!"
				else:
					ye=notifications.objects.filter(id=user.noti,pushed=0).first()
					request.session['notifications']= ye.notification


				return HttpResponseRedirect(reverse('tenders'))
			else:
			    message = "Your password is incorrect or user doesn't exist"
			    return render(request,"hoo/login.html",{'message':message})
		else:
			message="users doesnt exists!"
			return render(request,'hoo/login.html',{'message':message})



def displayTender(request,tender_id):
	
	my_tender=tender.objects.get(tenderID=tender_id)
	docs=my_tender.documents.all()
	diff=my_tender.bid_end_date - timezone.now()
	if diff.days>0:
		diff=str(diff.days) + " DAYS LEFT!"
	elif diff.days>=0 and diff.days<=0:
		diff= " LAST HOURS STARTED!"
	else:
		diff= "DEADLINE PASSED"
	
	all_bids=bids.objects.filter(tenderID=tender_id)
	all_users=[]
	avg_bid=0
	for bid in all_bids:
		my_user=users.objects.filter(id=bid.from_userID)
		all_users.append(my_user)
		avg_bid=avg_bid+bid.amount

	avg_bid=avg_bid/len(all_bids)
	avg_bid=int(avg_bid)
	

	is_bidded=False
	if 'id' in request.session and 'email' in request.session:

		if bids.objects.filter(tenderID=tender_id,from_userID=request.session['id']).exists():
			is_bidded=True
	is_passed=False
	winner=None
	
	if 'id' in request.session and 'email' in request.session:
	
	
		if tran.objects.filter(tenderID=tender_id).exists():
			is_passed=True
			winner=tran.objects.filter(tenderID=tender_id).first()
			winner=bids.objects.filter(id=winner.bid_id).first()
	
			

		
	is_admin=0
	if 'id' in request.session and 'email' in request.session:
		if request.session['is_admin']==1:
			is_admin=1


	

	context={
		'message':tender_id,
		'data':my_tender,
		'docs': docs,
		'diff' : diff,
		'all_bids' : all_bids,
		'all_users' : all_users,
		'is_bidded': is_bidded,
		'avg_bid' : avg_bid,
		'is_admin':is_admin,
		'is_passed' : is_passed,
		'winner' : winner,
		
	}
	
	return render(request,'hoo/tender.html',context)


def tenders(request):
	all_tender=tender.objects.all()
	admin=0
	if 'id' in request.session and 'email' in request.session:
		if str(request.session['email'])=="admin":
			admin=1



	return render(request,'hoo/all_tender.html',{'all_tender':all_tender,'admin':admin})


def logout(request):
	try:
	    del request.session['email']
	    del request.session['id']
	    del request.session['firstname']
	    del request.session['lastname']
	    return redirect('indexPage')
	except:
		return redirect('indexPage')


def account(request):
	if request.method=='GET':
		if request.session['id']:
			email=request.session['email']
			user=users.objects.filter(email=email).first()
			if user:
				context={
				'user': user
				}
				return render(request,'hoo/account.html',context)
			else:
				return render(request,'hoo/login.html')				


			return render(request,'hoo/account.html')
		else:	
			return render(request,'hoo/account.html')


def contactus(request):
	return render(request,'hoo/contact.html')

def block(request):
	
	tr=tran.objects.all()
	yes={}
	j=1
	for i in tr:
		yes.update({str(j):i.dump_json()})
		j=j+1

	
	import json
	new = json.dumps(yes)
	extra={
		'ex': new,
	}
	#return render(request,'hoo/block.html',{'data':data,'extra':extra})
	return HttpResponse(new,content_type="application/json")




def addbid(request,tender_id):
	if request.method=="GET":

		t=tender.objects.filter(tenderID=tender_id).first()
		form = bs()
		data={
		'tender_id' : tender_id,
			'titleq' : t.title ,
			'obj' : t,
			'form': form,
		}
		return render(request,"hoo/checkout.html",data)

	

        

def submit_bid(request,tender_id):
	if request.method=="POST":
		form = bs(request.POST, request.FILES)
		try:
			if form.is_valid():
				firstname=form.cleaned_data['firstname']
				lastname=form.cleaned_data['lastname']
				org_name=form.cleaned_data['org_name']
				email=form.cleaned_data['email']
				amount=form.cleaned_data['amount']
				fileupload=form.cleaned_data['fileupload']
				detail=form.cleaned_data['detail']
				msg={
				'firstname':firstname,
				'lastname':lastname,
				'org_name':org_name,
				'email':email,
				'amount':amount,
				'fileupload':fileupload,
				'detail':detail
				}
				obj=bids.objects.create(firstname=firstname,lastname=lastname,org_name=org_name,email=email,amount=amount,fileupload=fileupload,from_userID=request.session['id'],tenderID=tender_id,detail=detail)
				
				return render(request, 'hoo/confirm_bid.html')
			else:
				context={'msg': "no mf",
				'tender_id' : tender_id ,
				'form' : form}
				return render(request, 'hoo/checkout.html',context)
	
		except Exception as e:
		    
		    context={'msg': e.message }
		    return render(request, 'hoo/confirm_bid.html',context)

		else:
			return render(request, 'hoo/confirm_bid12345.html')
	else:
		return render(request, 'hoo/confirm_bid.html11')



def confirm(request):
	context={
	'success' : 'yes',
	}
	return render(request,"hoo/confirm_bid.html",context)


def user_bids(request):
	if 'id' in request.session and 'email' in request.session:
		single=True
		my_bids=bids.objects.filter(from_userID=request.session['id'])
		if len(my_bids)==0:
			single=False
		else:
			single=True
		return render(request,"hoo/my_bids.html",{'single' : single,'my_bids' :my_bids})
	else:
		return redirect('loginPage')


def delete_bid(request,bid_id):
	if 'id' in request.session and 'email' in request.session:
	
		my_bids=bids.objects.filter(id=bid_id).first()
	
		if my_bids.from_userID==request.session['id']:
			#bids.objects.filter(id=bid_id,from_userID=request.session['id'])
			my_bids.delete()


			
		return redirect('user_bids')
	else:
		return redirect('logout')


def finalize(request,tender_id):
	if 'id' in request.session and 'email' in request.session:
		if request.session['is_admin']==1:
			pairs={}
			all_bids=bids.objects.filter(tenderID=tender_id)

			for i in all_bids:
				
				pairs.update({i.id:i.amount})
			tender.objects.filter(tenderID=tender_id).update(is_passed=True)	
			key_min = min(pairs.keys(), key=(lambda k: pairs[k]))

			bid=bids.objects.filter(id=key_min).first()
			context={
				'key_min':key_min,
				'bid':bid,
			}
			return render(request,"hoo/finalize.html",context)
		else:
			return redirect('logout')
	else:			
		return redirect('logout')

def confirm(request,tender_id,bid_id):
	if 'id' in request.session and 'email' in request.session:
		if request.session['is_admin']==1:
			bid=bids.objects.filter(id=bid_id).first()
			yes=tran.objects.create(to_userID=bid.from_userID,bid_id=bid.id,tenderID=tender_id,amount=bid.amount)
			notice=notifications.objects.create(to_userID=bid.from_userID,notification="Congratualtions!!, You Bid is Selected!")
			users.objects.filter(id=bid.from_userID).update(noti=notice.id)
			return redirect('success')
		else:
			return redirect('logout')
	else:			
		return redirect('logout')

def success(request):
	return render(request,"hoo/confirm_bid.html")
def search(request):
	import json
	param=request.GET['search_input']
	data=[]
	result=0
	ob=tender.objects.all()
	
	for i in ob:
		counter=0
		yes=i.__repr__().lower()
		
		if param in yes:
			counter=counter+1
			x=i.__repr__()
			y=json.dumps(x)
			data.append(i)
			result=result+1
	if not data:
		data.append("Search Not Found!")

	context={
		'data' : data,
		'result' : result,
		'param' : param,
	}
	return render(request,"hoo/search.html",context)
	#return HttpResponse("Parameter is " + str(data)  ) 


def elements(request):
	return render(request,"hoo/elements1.html")