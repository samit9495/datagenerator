import json
import random
from django.http import HttpResponse
import csv
from django.shortcuts import render
from faker import Faker
from jinja2 import Environment, FileSystemLoader
from .models import category
from django.db.utils import IntegrityError
from collections import OrderedDict
# import pandas as pd
import pandas


def create_category(request):
    choices = ["Number", "Alphabetic", "Alphanumeric", "Special Sequence"]

    if request.method == "POST":
        if request.POST.get("submit") == "form1":
            print(request.POST)
            return render(request, "generator/creation.html",
                          context={"form": "form2", "category": request.POST.get("category")})

        if request.POST.get("submit") == "form2":
            print(request.POST)
            if request.POST.get("category") == "Alphanumeric":
                x = ""
                for i in range(int(request.POST.get("length"))):
                    x += random.choice(["#", "?"])
            if request.POST.get("category") == "Number":
                x = "#" * int(request.POST.get("length"))
            if request.POST.get("category") == "Alphabetic":
                x = "?" * int(request.POST.get("length"))
            try:
                category.objects.get_or_create(Name=request.POST.get("name"),
                                               length=request.POST.get("length") if request.POST.get("length") else len(
                                                   request.POST.get("sequence")),
                                               sequence=request.POST.get("sequence") if request.POST.get("sequence") else x,
                                               case=request.POST.get("case", ""),
                                               type=request.POST.get("category"))
                return render(request, "generator/creation.html",
                              context={"form": "save", "category": request.POST.get("category"),
                                       "status": "Category Saved Successfully"})
            except IntegrityError:
                exist_cat = category.objects.get(
                                               length=request.POST.get("length") if request.POST.get("length") else len(
                                                   request.POST.get("sequence")),
                                               sequence=request.POST.get("sequence") if request.POST.get(
                                                   "sequence") else x,
                                               case=request.POST.get("case", ""),
                                               type=request.POST.get("category"))
                return render(request, "generator/creation.html",
                              context={"form": "save", "category": request.POST.get("category"),
                                       "status": f"Same Category already exists with name: {exist_cat.Name}"})
    return render(request, "generator/creation.html", context={"choices": choices, "form": "form1", })


def download_csv(request):
    df = pandas.DataFrame.from_dict(request.session["csvdata"])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{filename}.csv"'.format(filename='data')
    writer = csv.writer(response)
    writer.writerow([column for column in df.columns])
    writer.writerows(df.values.tolist())
    return response

download_csv.short_description = "Download selected as csv"


def save_category(request):

    return render(request, "generator/save_category.html", context={})


def homepage(request):
    if request.method == "POST":
        print("@@@@@@@",request.POST)
        if request.POST.get("Download"):
            csvdata = download_csv(request)
            return HttpResponse(csvdata, content_type='text/csv')
        faker = Faker('en_IN')
        final = {}
        mappings = {"Name": faker.name, "First Name": faker.first_name, "Last Name": faker.last_name,
                    "Email": faker.email, "Address": faker.address, "Phone Number": faker.phone_number,
                    "Integer": faker.random_int, "Word": faker.word, "Random Profile": faker.profile,
                    "Aadhar": faker.numerify, "Male Profile": faker.profile, "Female Profile": faker.profile,
                    "bothify": faker.bothify}

        params = {"Aadhar": ["#### #### ####", ], "Male Profile": [None, "M"], "Female Profile": [None, "M"]}
        for ctg in request.POST.getlist('category'):
            print("ctg",ctg)
            data = []

            if params.get(ctg):
                for i in range(int(request.POST.get("count"))):
                    data.append(mappings[ctg](*params[ctg]))
            elif ctg in request.session["ct"]:
                for i in range(int(request.POST.get("count"))):
                    sq = category.objects.get(Name=request.POST.get("category"))
                    print(sq.sequence)

                    val = mappings["bothify"](sq.sequence)
                    if sq.case == "Upper":
                        val = val.upper()
                    if sq.case == "Lower":
                        val = val.lower()
                    data.append(val)
            else:
                for i in range(int(request.POST.get("count"))):
                    data.append(mappings[ctg]())
            final[ctg] = data
        print(final)
        print(type(final))
        request.session["csvdata"] = final
        ff = []
        for i in range(len(data)):
            t = []
            for k in final.keys():
                t.append(final[k][i])
            ff.append(t)
        return render(request, "generator/approved.html", {"final": ff, "keys": final.keys(), "name": request.POST.get("category")})

    ct = category.objects.all()
    ct = [x.Name for x in ct]
    request.session["ct"] = ct
    choices = ["Name", "First Name", "Last Name", "Email", "Aadhar", "Address", "Phone Number", "Integer", "Word",
               "Random Profile", "Male Profile", "Female Profile"]
    choices.extend(ct)
    return render(request, "generator/home.html", {"choices": choices})


def get_aadhar(faker):
    return faker.numerify("#### #### ####")


def data_generator(request):
    faker = Faker()
    name = faker.name()
    #
    # print(f'First name: {faker.first_name()}')
    # print(f'Last name: {faker.last_name()}')
    #
    #
    # print(f'Male name: {faker.name_male()}')
    # print(f'Female name: {faker.name_female()}')
    #
    # for _ in range(6):
    #     print(faker.job())
    #
    # get_loacle_data()
    # get_currency()
    # get_words()
    # get_xmldata()
    # get_profiles()
    get_numbers()
    get_data_and_time()
    get_hash_and_uuid()
    get_internet_data()
    get_loacle_data()
    get_more_dates()
    return render(request, "generator/home.html")


def get_loacle_data():
    faker = Faker('en_IN')

    for i in range(3):
        name = faker.name()
        address = faker.address()
        phone = faker.phone_number()

        print(f'{name}, {address}, {phone}')


def get_currency():
    faker = Faker()

    print(f'currency: {faker.currency()}')
    print(f'currency name: {faker.currency_name()}')
    print(f'currency code: {faker.currency_code()}')



def get_words():
    faker = Faker()

    print(f'a word: {faker.word()}')
    print(f'six words: {faker.words(6)}')

    words = ['forest', 'blue', 'cloud', 'sky', 'wood', 'falcon']

    print(f'customized unique words: {faker.words(3, True, words)}')


def get_profiles():
    faker = Faker()

    profile1 = faker.simple_profile()
    print(profile1)

    print('--------------------------')

    profile2 = faker.simple_profile('M')
    print(profile2)

    print('--------------------------')

    profile3 = faker.profile(sex='F')
    print(profile3)


def get_numbers():
    faker = Faker()

    print(f'Random int: {faker.random_int()}')
    print(f'Random int: {faker.random_int(0, 100)}')
    print(f'Random digit: {faker.random_digit()}')


def get_hash_and_uuid():
    faker = Faker()
    print(f'md5: {faker.md5()}')
    print(f'sha1: {faker.sha1()}')
    print(f'sha256: {faker.sha256()}')
    print(f'uuid4: {faker.uuid4()}')


def get_internet_data():
    faker = Faker()

    print(f'Email: {faker.email()}')
    print(f'Safe email: {faker.safe_email()}')
    print(f'Free email: {faker.free_email()}')
    print(f'Company email: {faker.company_email()}')

    print('------------------------------------')

    print(f'Host name: {faker.hostname()}')
    print(f'Domain name: {faker.domain_name()}')
    print(f'Domain word: {faker.domain_word()}')
    print(f'TLD: {faker.tld()}')

    print('------------------------------------')

    print(f'IPv4: {faker.ipv4()}')
    print(f'IPv6: {faker.ipv6()}')
    print(f'MAC address: {faker.mac_address()}')

    print('------------------------------------')

    print(f'Slug: {faker.slug()}')
    print(f'Image URL: {faker.image_url()}')


def get_data_and_time():
    faker = Faker()
    print(f'Date of birth: {faker.date_of_birth()}')
    print(f'Century: {faker.century()}')
    print(f'Year: {faker.year()}')
    print(f'Month: {faker.month()}')
    print(f'Month name: {faker.month_name()}')
    print(f'Day of week: {faker.day_of_week()}')
    print(f'Day of month: {faker.day_of_month()}')
    print(f'Time zone: {faker.timezone()}')
    print(f'AM/PM: {faker.am_pm()}')


def get_more_dates():
    faker = Faker()

    print(f'Datetime this century: {faker.date_time_this_century()}')
    print(f'Datetime this decade: {faker.date_time_this_decade()}')
    print(f'Datetime this year: {faker.date_time_this_year()}')
    print(f'Datetime this month: {faker.date_time_this_month()}')

    print('-------------------------')

    print(f'Date this century: {faker.date_this_century()}')
    print(f'Date this decade: {faker.date_this_decade()}')
    print(f'Date this year: {faker.date_this_year()}')
    print(f'Date this month: {faker.date_this_month()}')

    print('-------------------------')

    TOTAL_SECONDS = 60 * 60 * 24 * 2  # two days

    series = faker.time_series(start_date='-12d', end_date='now', precision=TOTAL_SECONDS)

    for val in series:
        print(val[0])


def get_xmldata():
    class User:

        def __init__(self, first_name, last_name, occupation):
            self.first_name = first_name
            self.last_name = last_name
            self.occupation = occupation

    faker = Faker()
    users = []

    for _ in range(10):
        first_name = faker.first_name()
        last_name = faker.last_name()
        occupation = faker.job()

        user = User(first_name, last_name, occupation)

        users.append(user)

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('users.xml.j2')
    output = template.render(users=users)
    print("###########", output)
    print(output, file=open('users.xml', 'w'))
