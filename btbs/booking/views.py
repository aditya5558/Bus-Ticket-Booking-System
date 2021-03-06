from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from .forms import UserForm
from .models import User,UserFeedback,Wallet,WalletTransaction,Bus,Booking
import datetime
from dateutil.parser import parse
import pandas as pd
import ast
from django.db.models import DateTimeField, ExpressionWrapper, F


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
			# print all_buses
			# bus_list = []
			# for bus in all_buses:
			# 	print bus['bus_type'],bus['source'],bus['destination']
			# 	bus_list.append([bus['bus_type'],bus['source'],bus['destination']])
			#return redirect('/booking/remove_bus/?all_buses=%s' % bus_list)
			return render(request,'booking/remove_bus.html',{'all_buses':all_buses})
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

		from_date = request.POST['date-from'].encode('utf-8')
		to_date = request.POST['date-to'].encode('utf-8')

		# f = datetime.strptime(from_date, '%m-%d-%Y')

		# print f,to_date

		daterange = pd.date_range(from_date,to_date)

		if from_date <= to_date:
			for d in daterange:
				# date = from_date + datetime.timedelta(n)
				Bus.objects.create(bus_op=user,date=d.strftime('%Y-%m-%d'),num_seats=50,bus_type=bus_type,price=price,source=source,destination=destination,time=time,journey_duration=journey_duration)
		else:
			message = 'Error! From date > To date'
			print message
			return redirect('/booking/add_bus/?error_message=%s' % message)

		# Bus.objects.create(bus_op=user,bus_type=bus_type,price=price,source=source,destination=destination,time=time,journey_duration=journey_duration)
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
		
		daterange = pd.date_range(lis[3],lis[3])
		print daterange

		m = Bus.objects.get(bus_type=lis[0],source=lis[1],destination=lis[2],date=daterange[0].strftime('%Y-%m-%d'))
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
		# username = request.user
		all_buses = Bus.objects.filter(bus_op=request.user).values()
		return render(request,'booking/remove_bus.html', {'all_buses':all_buses})

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
		w = Wallet.objects.get(user=request.user)
		return render(request,'booking/passenger.html', {'w':w})

@login_required
def add_money(request):

	if request.method == 'POST':
		
		username = request.POST['username']
		user = User.objects.get(username=username)
		money = request.POST['money']

		w = Wallet.objects.get(user=user)
		old = w.balance
		w.balance = w.balance + float(money)
		w.updated_at = datetime.datetime.now()
		w.save()

		wt = WalletTransaction.objects.create(wallet=w,type='credit',old_balance=old,new_balance=w.balance,trans_amt=float(money),timestamp=datetime.datetime.now())
		print wt
		# print w
		p = 'Money Added'
		# return render(request,'booking/wallet.html', {'p':p,'w':w})
		
		print p
		return redirect('/booking/passenger/?p=%s' % p)

	else:
		w = Wallet.objects.get(user=request.user)
		return render(request,'booking/wallet.html', {'w':w})

@login_required
def book_ticket(request):

	if request.method == 'POST':
		
		username = request.POST['username']
		user = User.objects.get(username=username)
		source = request.POST['source']
		destination = request.POST['destination']
		date = request.POST['date'].encode('utf-8')

		daterange = pd.date_range(date,date)


		buses = Bus.objects.filter(source=source,destination=destination,date=daterange[0].strftime('%Y-%m-%d'))
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
		
		print request.POST

		username = request.POST['username']
		balance = request.POST['balance']
		source = request.POST['source']
		destination = request.POST['destination']
		date = request.POST['date']
		

		user = User.objects.get(username=username)
		
		selection = request.POST['choice']
		num_seats = request.POST['num_seats']
		lis = selection.split("-")

		print source,destination,date
		
		daterange = pd.date_range(date,date)
		print lis[0]
		print lis[1]
		user_bus = User.objects.get(username=lis[1])
		m = Bus.objects.get(bus_type=lis[0],bus_op=user_bus,source=source,destination=destination,date=daterange[0].strftime('%Y-%m-%d'))

		print m.price,num_seats

		w = Wallet.objects.get(user=user)

		total_price = m.price*int(num_seats)

		if m:
			if w.balance >= total_price and m.num_seats - int(num_seats) > 0: 

				x = int(num_seats)
				s = ''
				while x > 0:
					s += str(m.num_seats)
					s += ','
					m.num_seats -= 1
					x -= 1

				obj = Booking.objects.create(user=user,bus=m,seat_numbers=s[0:-1],wallet_initial=w.balance,wallet_final=w.balance-total_price,total_price=total_price,timestamp=datetime.datetime.now(),num_tickets=num_seats,status='Success')
				message = 'Booking Success!!!'
				
				print obj.pk

				wt = WalletTransaction.objects.create(wallet=w,type='debit',old_balance=w.balance,new_balance=w.balance-total_price,trans_amt=total_price,timestamp=datetime.datetime.now())
				# m.num_seats = m.num_seats - int(num_seats)
				w.balance = w.balance - total_price
				w.save()
				wt.save()
				m.save()


				print message
				return redirect('/booking/passenger/?p=%s' % message)

			elif w.balance < total_price:
				message = "Not Enough Money! Please Add Money to wallet !"
				print message
				return redirect('/booking/wallet/?p=%s' % message)
			
			else:
				message = "Those many seats not available"
				print message
				return render(request,'booking/book_ticket.html', {'p':message,'date':date,'source':source,'destination':destination,'balance':balance})

		return render(request,'booking/book_ticket.html', {'date':date,'source':source,'destination':destination,'balance':balance})

	else:
		return render(request,'booking/book_ticket_1.html', {})

@login_required
def view_trips(request):


	user = request.user
	print user.username
		
	bookings = Booking.objects.filter(user=user)
	if bookings:
		return render(request,'booking/view_trips.html', {'bookings':bookings})
	else:
		message = "No Previous Trips"
		print message
		return redirect('/booking/passenger/?p=%s' % message)


@login_required
def feedback(request):

	if request.method == 'POST':
		
		username = request.POST['username']
		user = User.objects.get(username=username)
		choice = request.POST['choice']
		comment = request.POST['feedback']
		rating = request.POST['rating']
		# bookings = request.POST['bookings']
		print choice

		c = Booking.objects.get(pk=choice)
		print c
		
		# c = ast.literal_eval([choice])
		# print c[0]

		# c = choice.encode('utf-8')
		# print type(c)
		
		f = UserFeedback.objects.create(user=user,booking=c,comment=comment,rating=rating)
		print f
		
		
		message = 'Thank You for your Feedback!!!'
		print message

		return redirect('/booking/passenger/?p=%s' % message)
		# return render(request,'booking/feedback.html', {})

	else:



		user = request.user
		# print user.username
			
		bookings = Booking.objects.filter(user=user)

		if bookings:
			return render(request,'booking/feedback.html', {'bookings':bookings})
		else:
			message = "No Previous Trips for feedback"
			print message
			return redirect('/booking/passenger/?p=%s' % message)

@login_required
def view_feedback(request):


	user = request.user
	print user.username
		
	feedback = UserFeedback.objects.all()
	f1 = []
	for f in feedback:
		print f.booking.bus.bus_op
		if f.booking.bus.bus_op.username == user.username:
			f1.append(f)

	# feedback = Feedback.objects.filter(booking.bus.bus_op=user)
	if len(f1):
		return render(request,'booking/view_feedback.html', {'bookings':f1})
	else:
		message = "No Feedback"
		print message
		return redirect('/booking/bus_operator/?p=%s' % message)