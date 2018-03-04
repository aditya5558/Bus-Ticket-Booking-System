from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from .forms import UserForm
from .models import User,UserFeedback,Wallet,WalletTransaction,Bus,Booking
import datetime
# Create your views here.
def index(request):
	logout(request)
	return render(request,'booking/index.html')


def register(request):
    registered = False
    error_message = ''
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            
            if request.POST['acc_type'] == 'Passenger':
            	user.is_passenger = True
            else:
            	user.is_bus_operator = True
            user.save()

            #Wallet.objects.create(user=user,balance=0.00)

            registered = True
            # return render(request, 'booking/passenger_login.html',{})

        else:
            print user_form.errors

    else:
        logout(request)
        user_form = UserForm()
        return render(request,
            'booking/passenger_register.html',
            {},
            )

    print registered

    if registered == True:
    	error_message = "Registered Successfully!"
    	return render(request,
            'booking/passenger_register.html',
            {'error_message':error_message},
            )

    # if registered == True:
    #     return render(request, 'booking/passenger_login.html',{})

    #print "hi"
    return render(request,
            'booking/passenger_register.html',
            {'error_message':'Username already exists!'},
            )


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            # if user.is_active:
                login(request, user)
                request.session['data'] = user.username

                if user.is_passenger == True and user.is_bus_operator == False:
                    #return render(request,'booking/passenger.html', {'user': user, })
                	return redirect('/booking/passenger/')
                else:
                    if user.is_passenger == False and user.is_bus_operator == True:
                        #return render(request,'booking/bus_operator.html', {'user': user, })
                    	return redirect('/booking/bus_operator/')
                    else:
                        user.is_active = False
                        print "hi"
                        user.save()
                        return HttpResponse("Sorry. Your account is disabled.")


            # else:
            # 	print "hello"
            #     return HttpResponse("Sorry. Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            error_message = "Invalid Credentials. Please try again"
            return render(request,'booking/passenger_login.html',{ 'error_message':error_message, })

    else:
        logout(request)
        return render(request,'booking/passenger_login.html', {})

@login_required
def bus_operator_home(request):

	if request.method == 'POST':
		
		username = request.POST['username']
		user = User.objects.get(username=username)
		action = request.POST['choice']
		print "hi",username

		if action == 'Add Bus':
			print "ch"
			return redirect('/booking/add_bus/')
		elif action == 'Remove Bus':
			all_buses = Bus.objects.filter(bus_op=user).values()
			print all_buses
			bus_list = []
			for bus in all_buses:
				print bus['bus_type'],bus['source'],bus['destination']
				bus_list.append([bus['bus_type'],bus['source'],bus['destination']])
			return redirect('/booking/remove_bus/?all_buses=%s' % bus_list)
			#return render(request,'booking/remove_bus.html',{'all_buses':all_buses})
		else:
			return render(request,'booking/bus_operator.html', {})

	else:
		return render(request,'booking/bus_operator.html', {})


@login_required
def add_bus(request):

	if request.method == 'POST':
		username = request.POST['username']
		user = User.objects.get(username=username)
		bus_type = request.POST['bus_type']
		journey_duration = request.POST['duration']
		source = request.POST['source']
		destination = request.POST['destination']
		price = request.POST['price']
		time = request.POST['time']

		Bus.objects.create(bus_op=user,bus_type=bus_type,price=price,source=source,destination=destination,time=time,journey_duration=journey_duration)
		message = 'Bus Successfully Added'
		print message
		return redirect('/booking/bus_operator/?p=%s' % message)
	
	else:
		return render(request,'booking/add_bus.html', {})

@login_required
def remove_bus(request):

	if request.method == 'POST':
		username = request.POST['username']
		user = User.objects.get(username=username)
		
		bus = request.POST['choice']
		lis = bus.split("-")
		m = Bus.objects.get(bus_type=lis[0],source=lis[1],destination=lis[2])
		if m:
			m.delete()
			message = 'Bus Successfully removed'
			print message			
		else:
			message = 'Error'
			print message	
		return redirect('/booking/bus_operator/?p=%s' % message)

	else:
		# for bus in request.GET['bus_list']:
		# 	print bus[0]
		return render(request,'booking/remove_bus.html', {})

@login_required
def passenger_home(request):

	if request.method == 'POST':
		
		username = request.POST['username']
		user = User.objects.get(username=username)
		action = request.POST['choice']

		if action == 'Book Ticket':
			return redirect('/booking/book_ticket/')
		elif action == 'View Previous Trips':
			return redirect('/booking/view_trips/')
		elif action == 'Add Money to Wallet':
			return redirect('/booking/wallet/')
		elif action == 'Give Feedback':
			return redirect('/booking/feedback/')
		else:
			return render(request,'booking/passenger.html', {})

	else:
		return render(request,'booking/passenger.html', {})

@login_required
def add_money(request):

	if request.method == 'POST':
		
		username = request.POST['username']
		user = User.objects.get(username=username)
		money = request.POST['money']

		w = Wallet.objects.get(user=user)
		w.balance = w.balance + float(money)
		w.updated_at = datetime.datetime.now()
		w.save()
		print w
		p = 'Money Added'
		return render(request,'booking/wallet.html', {'p':p})

	else:
		return render(request,'booking/wallet.html', {})

@login_required
def book_ticket(request):

	if request.method == 'POST':
		
		username = request.POST['username']
		user = User.objects.get(username=username)
		source = request.POST['source']
		destination = request.POST['destination']
		date = request.POST['date']

		buses = Bus.objects.filter(source=source,destination=destination)
		print buses
		w = Wallet.objects.get(user=user)
		money = w.balance

		if not buses:
			p = "Sorry! No buses available"
			return render(request,'booking/book_ticket.html', {'p':p})

		return render(request,'booking/book_ticket_1.html', {'all_buses':buses,'date':date,'source':source,'destination':destination,'balance':money})

	else:
		return render(request,'booking/book_ticket.html', {})

@login_required
def book_ticket_1(request):

	if request.method == 'POST':
		
		username = request.POST['username']
		balance = request.POST['balance']
		source = request.POST['source']
		destination = request.POST['destination']
		date = request.POST['date']
		user = User.objects.get(username=username)
		selection = request.POST['choice']
		num_seats = request.POST['num_seats']
		lis = selection.split("-")
		m = Bus.objects.get(bus_type=lis[0],bus_op=lis[1])

		w = Wallet.objects.get(user=user)
		total_price = m.price*num_seats

		if m:
			if w.balance >= total_price: 

				obj = Booking.objects.create(user=user,bus=m,wallet_initial=w.balance,wallet_final=w.balance-total_price,total_price=total_price,timestamp=datetime.datetime.now(),num_tickets=num_seats,status='Success')
				message = 'Booking Success!!!'
				print message
				return redirect('/booking/bus_operator/?p=%s' % message)
			else:
				redirect('/booking/add_money/')
		return render(request,'booking/book_ticket_1.html', {'date':date,'source':source,'destination':destination,'balance':money})

	else:
		return render(request,'booking/book_ticket_1.html', {})