from django.urls import path
from . import views


urlpatterns=[

	path('',views.indexPage,name='indexPage'),
	path('register',views.registerPage,name='registerPage'),
	path('login',views.loginPage,name='loginPage'),
	path('tender/<int:tender_id>', views.displayTender, name='tender_display'),
	path('tender/<int:tender_id>/finalize', views.finalize, name='finalize'),
	path('tender/<int:tender_id>/finalize/confirm/<int:bid_id>', views.confirm, name='confirm'),
	path('tenders', views.tenders, name='tenders'),
	
	path('logout', views.logout, name='logout'),
	path('contactus', views.contactus, name='contactus'),
	path('account', views.account, name='account'),
	path('block', views.block, name='block'),
	#path('transaction', views.transaction, name='transaction'),
	#path('<tender_id>/checkout', views.checkout, name='checkout'),
	path('<tender_id>/add', views.addbid, name='addbid'),
	path('<tender_id>/bid_submitted', views.submit_bid, name='submit_bid'),
	#path('form_test', views.form_test, name='form_test'),
	path('confirm', views.confirm, name='confirm'),
	path('user_bids', views.user_bids, name='user_bids'),
	path('user_bids/delete/<bid_id>', views.delete_bid, name='delete_bid'),
	path('search/', views.search, name='param'),
	path('success/', views.success, name='success'),
	path('elements/', views.elements, name='elements'),


]