from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from datetime import datetime

from .models import *

# Create your views here.

today = datetime.today().strftime('%Y-%m-%d')


def index(request):
    Halls = Hall.objects.all()
    status = {}

    for Hall in Halls:
        if Hall.reservation_set.filter(date=today):
            status[Hall.id] = 'Busy'
        else:
            status[Hall.id] = 'Free'
    ctx = {
        'Halls': Halls,
        'status': status,
    }
    return render(request, 'Book/index.html', ctx)


def Hall(request, id):
    Hall = Hall.objects.get(pk=int(id))
    if Hall:
        reservations = Hall.reservation_set.filter(date__gte=today).order_by('date')
        Halls = Hall.objects.all()
        if Hall.projector == True:
            projector = "Yes"
        else:
            projector = "No"
        ctx = {
            "Hall": Hall,
            "projector": projector,
            "reservations": reservations,
            "Halls": Halls,
        }
    else:
        ctx = {
            "Hall": 'Hall Not Available',
            "projector": 'NA',
            "reservations": 'NA',
            "Halls": 'NA',
        }
    return render(request, 'Book/Hall.html', ctx)


class NewHallView(View):

    def get(self, request):
        return render(request, 'Book/new_Hall.html')

    def post(self, request):
        try:
            name = request.POST.get("name")
            capacity = request.POST.get("capacity")
            projector = request.POST.get("projector")
            proj = True if projector == "True" else False

            Hall.objects.create(name=name, capacity=capacity, projector=proj)
            return redirect("/")

        except Exception as e:
            message = "Incorrect Data: {}".format(e)
            ctx = {
                "message": message,
            }
            return render(request, 'Book/new_Hall.html', ctx)


class ModifyView(View):

    def get(self, request, id):
        Hall = Hall.objects.get(pk=id)
        ctx = {
            "Hall": Hall,
        }
        return render(request, 'Book/modify.html', ctx)

    def post(self, request, id):
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = True if request.POST.get('projector') else False
        Hall = Hall.objects.get(pk=id)
        try:
            Hall.name = name
            Hall.capacity = capacity
            Hall.projector = projector
            Hall.save()
            return redirect("/")
        except Exception as e:
            message = "Incorrect Data: {}".format(e)
            ctx = {
                "message": message,
                "Hall": Hall,
            }
            return render(request, 'Book/modify.html', ctx)


class DeleteView(View):

    def get(self, request, id):
        Hall = Hall.objects.get(pk=id)
        ctx = {
            "Hall": Hall,
        }
        return render(request, 'Book/delete.html', ctx)

    def post(self, request, id):
        action = request.POST.get("submit")

        if action == "Yes":
            Hall = Hall.objects.get(pk=id)
            Hall.delete()
        return redirect("/")


class ReservationView(View):

    def get(self, request, id):
        Hall = Hall.objects.get(pk=id)
        reservations = Hall.reservation_set.filter(date__gte=today).order_by('date')
        ctx = {
            "Hall": Hall,
            "reservations": reservations,
        }
        return render(request, 'Book/reservation.html', ctx)

    def post(self, request, id):
        Hall = Hall.objects.get(pk=id)
        reservations = Hall.reservation_set.filter(date__gte=today).order_by('date')
        try:
            date = request.POST.get("date")
            comment = request.POST.get("comment")
            message = ""

            if Hall.reservation_set.filter(date=date):
                message = "This Hall is already occupied for that day"
            elif date < today:
                message = "The chosen data can not be in the past"

            if (message == "This Hall is already occupied for that day"
                or message == "The chosen data can not be in the past"):
                ctx = {
                    "Hall": Hall,
                    "reservations": reservations,
                    "message": message,
                }
                return render(request, 'Book/reservation.html', ctx)

            reservation = Reservation.objects.create(date=date, comment=comment)
            reservation.Hall.add(Hall)

        except Exception as e:
            message = "Incorrect Data: {}".format(e)
            ctx = {
                "message": message,
                "Hall": Hall,
                "reservations": reservations,
            }
            return render(request, 'Book/reservation.html', ctx)

        if Hall.projector == True:
            projector = "TAK"
        else:
            projector = "NIE"
        message = """Dziękujemy! Zarezerwowałeś salę: 
                     {} w dniu: {}""".format(Hall.name, date)
        ctx = {
            "Hall": Hall,
            "projector": projector,
            "reservations": reservations,
            "message": message,
        }
        return render(request, 'Book/Hall.html', ctx)


class SearchView(View):

    def get(self, request):
        Hall = request.GET.get("Hall")
        capacity = request.GET.get("capacity")
        date = request.GET.get("date")
        projector = True if request.GET.get('projector') else False

        result1 = Hall.objects.exclude(reservation__date=date)

        if Hall == "":
            result2 = result1
        else:
            result2 = result1.filter(name__icontains=Hall)

        if capacity != "":
            result3 = result2.filter(capacity__gte=int(capacity))
        else:
            result3 = result2

        if projector:
            result4 = result3.filter(projector=projector)
        else:
            result4 = result3

        ctx = {
            "results": result4,
            "date": date,
        }
        return render(request, 'Book/search.html', ctx)





