from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render


class Queue:
    def __init__(self):
        self.queue = {'change_oil': [], 'inflate_tires': [], 'diagnostic': []}
        self.times = {'change_oil': 2, 'inflate_tires': 5, 'diagnostic': 30}
        self.last_ticket = 'nothing'
        self.number = 1

    def add(self, service):
        time = self.get_time(service)
        self.queue[service].append(self.number)
        self.number += 1
        return self.number - 1, time

    def get_time(self, service):
        time = 0
        match service:
            case 'change_oil': priorities = ['change_oil']
            case 'inflate_tires': priorities = ['change_oil', 'inflate_tires']
            case _: priorities = ['change_oil', 'inflate_tires', 'diagnostic']
        for serv in priorities:
            time += len(self.queue[serv]) * self.times[serv]
        return time

    def next(self):
        if self.queue['change_oil']:
            self.last_ticket = self.queue['change_oil'][0]
            del self.queue['change_oil'][0]
        elif self.queue['inflate_tires']:
            self.last_ticket = self.queue['inflate_tires'][0]
            del self.queue['inflate_tires'][0]
        elif self.queue['diagnostic']:
            self.last_ticket = self.queue['diagnostic'][0]
            del self.queue['diagnostic'][0]
        else:
            self.last_ticket = 'nothing'


queue = Queue()


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')


class GetTicketView(View):
    def get(self, request, *args, **kwargs):
        number, time = queue.add(args[0])
        return render(request, 'tickets/ticket.html', context={'service': args[0], 'number': number, 'time': time})


class OperatorMenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/operator_menu.html', context=queue.queue)

    def post(self, request, *args, **kwargs):
        queue.next()
        return render(request, 'tickets/operator_menu.html', context=queue.queue)


class NextTicketView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next_ticket.html', context={'next_ticket': queue.last_ticket})