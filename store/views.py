from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse 
import json

from . import models

from .models import * 

import pandas as pd

def store(request):
	print(request.user)
	logout = 0
	if request.user.is_authenticated:
		logout = 1
		customer = request.user.id
		print(customer)
		name = request.user.username
		customer = Customer.objects.get_or_create(id = customer,  defaults={'name': name, 'user_id': customer})
		customer_id = request.user.id
		customer = Customer.objects.get(id = customer_id)
		
		print(customer_id)
		# customer.username = "divyan"
		# customer.name = "divyan"
		# customer.email = "fernando@gmail.com"
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']


	products = Product.objects.all()
	#recommendations = ["Divyan", "Sona", "Neethu"]
	try:
		rec = request.session['recommend']
	except:
		request.session['recommend'] = ["","",""]
		rec = ["","",""]
	context = {'products':products, 'cartItems': cartItems, 'recommendations': rec}
	if(logout == 0):
		return render(request, 'store/store.html', context)
	else:
		context['logout'] = logout
		return render(request, 'store/store.html', context)

def cart(request):

	logout = 0
	if request.user.is_authenticated:
		logout = 1
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']
	rec = request.session['recommend']
	context = {'items':items, 'order':order, 'cartItems': cartItems, "recommendations": rec}
	#return render(request, 'store/cart.html', context)
	if(logout == 0):
		return render(request, 'store/cart.html', context)
	else:
		context['logout'] = logout
		return render(request, 'store/cart.html', context)

def checkout(request):
	
	logout = 0
	if request.user.is_authenticated:
		logout = 1
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']
	rec = request.session['recommend']
	context = {'items':items, 'order':order,'cartItems': cartItems, "recommendations": rec}
	#return render(request, 'store/checkout.html', context)
	if(logout == 0):
		return render(request, 'store/checkout.html', context)
	else:
		context['logout'] = logout
		return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)



	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		print("Reached add")
		orderItem.quantity = (orderItem.quantity + 1)
		inp = str(product)

		df=pd.read_csv('finaldataframe.csv')
		df.drop(columns = 'Unnamed: 0', axis = 1, inplace= True)
		df = df[df['antecedents'] == inp] 
		df = df.sort_values('confidence', ascending=False).reset_index(drop = True)
		out = df[:3]['consequents'].tolist()
		while(len(out)<3):
			out.append("")
		request.session['recommend'] = out

	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
		out = []
		request.session['recommend'] = out

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def chart(request):
	return render(request, "store/chart.html")
	#return HttpResponse("<h1><b><center>ADMIN PAGE</center></b></h1>")

def placeorder(request):
	return render(request, "store/placeorder.html")
