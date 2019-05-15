from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Persons, Bills, Payments, BillsToPayments, PaymentsStatus



# Auxiliar functions.

personsDict = dict()

def updatePersonsDict():
    persons = Persons.objects.all()
    for person in persons:
        personsDict[person.id] = person.name



# Views.

def index(request):
    return  HttpResponse("Hello, world. You're at the pools index")

def person(request, person_id):
    updatePersonsDict()
    data = dict()
    for key, value in personsDict.items():
        if key == person_id:
            person = dict()
            person["id"] = str(key)
            person["name"] = str(value)
            data[key] = person
    return JsonResponse(data)

def person_name(request, person_id):
    updatePersonsDict()
    output = ""
    for key, value in personsDict.items():
        if key == person_id:
            output += "Name: " + value + " "
    return HttpResponse(output)


# USE THIS TO FIND FIELD NAMES
#
# output = ""
# for f in Payments._meta.get_fields():
#     output += f.name + " "