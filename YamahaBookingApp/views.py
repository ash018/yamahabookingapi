from django.shortcuts import render
from django.conf import settings
import django_filters
from rest_framework import viewsets, filters
#from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
import os
from rest_framework.response import Response
from datetime import datetime
from .models import *
from rest_framework.reverse import reverse
from .serializer import RegisteredStgSerializer, SMSMessageOTPSerializer
from rest_framework.renderers import JSONRenderer
from django.core.files.storage import FileSystemStorage
import json
import datetime
import requests
from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
from django.http import JsonResponse
from django.core import serializers
from time import sleep

from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
#from django.core import serializers
from django.core.serializers import serialize
from functools import reduce
from random import randint
from django.db import DatabaseError, transaction
import http.client, urllib.request, urllib.parse, urllib.error, base64
#import cognitive_face as CF
import pyodbc
#from kombu import Connection
from kombu import Connection, Exchange, Producer, Queue
from bson.json_util import dumps
import pymongo
from requests_oauthlib import OAuth1Session

from pymongo import MongoClient

def GetAzureEmotion(url):
    url = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age'
    headers = {'Content-Type': 'application/json','Ocp-Apim-Subscription-Key':'2c223b68e95840d48ad1e6d580332d6c'}
    r = requests.post(url, headers=headers, params={"url": "http://mis.digital:7779/PaySlip/Fair/2019-01-12-19-14-10-618_my_image.jpg"})
    print(r.text)



    # KEY = '2c223b68e95840d48ad1e6d580332d6c'  # Replace with a valid Subscription Key here.
    # CF.Key.set(KEY)
    #
    # BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age'  # Replace with your regional Base URL
    # CF.BaseUrl.set(BASE_URL)
    #
    # img_url = 'http://mis.digital:7779/PaySlip/Fair/2019-01-12-19-14-10-618_my_image.jpg'
    # result = CF.face.detect(img_url)
    # print(result)
    # headers = {
    #     # Request headers
    #     'Content-Type': 'application/json',
    #     'Ocp-Apim-Subscription-Key': '5e96252de9e340ed9225c2366d55a9ad',
    # }
    #
    # params = urllib.parse.urlencode({
    #     'returnFaceId': 'true',
    #     'returnFaceLandmarks': 'false',
    #     'returnFaceAttributes': '{string}',
    # })
    # try:
    #     conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    #     conn.request("POST", "/face/v1.0/detect?%s" % params, url, headers)
    #     response = conn.getresponse()
    #     data = response.read()
    #     print(data)
    #     conn.close()
    # except Exception as e:
    #     print(str(e))


# Create your views here.
class Location(viewsets.ModelViewSet):
    
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    # Endpoint to receive image from mobile app

    def create(self, request):
        # userId = request.POST.get('userId')
        # password = request.POST.get('password')
        # # userId = request.POST['userId']
        # #password = request.POST['password']
        # print ('userId ' + str(userId) + ' password ' + str(password))
        # checkUser = UserManager.objects.filter(UserId = userId, Password = password).values('UserId','UserName','RoleId').using('MotorConstructionEquipment')
        # print ('checkUser ---- > ' +str(len(checkUser)))

        # if len(checkUser) > 0 :
        #     data = json.dumps(list(checkUser))
        #     response = {'StatusCode': '200', 'StatusMessage': str(data)}
        #     return Response(response,content_type="application/json")
        # else:
        #     response = {'StatusCode': '203', 'StatusMessage': 'UserId/Password Error'}
        #     return Response(response,content_type="application/json")

        response = {'StatusCode': '200', 'StatusMessage': 'resend'}
        return Response(response,content_type="application/json")


    def list(self, request):
        queryset = District.objects.all().values('Id', 'DistrictName').using('YamahaBooking')
        data = json.dumps(list(queryset))

        response = {'StatusCode': '200', 'StatusMessage': str(data)}
        print(response)
        return Response(response,content_type="application/json")

class FormValidation(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer


    def create(self, request):
        response = {'StatusCode': '200', 'StatusMessage': 'resend'}
        return Response(response,content_type="application/json")

    def list(self, request):
        fieldName = request.GET['fieldName'].strip()
        print('filed - ' + fieldName)
        if str(fieldName) == 'Mobile':
            mobile = request.GET['mobile'].strip()
            print('mobile - ' + mobile)
            qmobileQuerySet = RegisteredUser.objects.filter(Mobile = str(mobile)).using('YamahaBooking')
            if len(list(qmobileQuerySet)) > 0:
                response = {'StatusCode': '200', 'StatusMessage': '0'}
                print(response)
                return Response(response,content_type="application/json")
            else :
                response = {'StatusCode': '200', 'StatusMessage': '1'}
                print(response)
                return Response(response, content_type="application/json")

        if str(fieldName) == 'Email':
            email = request.GET['email'].strip()
            print('email - ' + email)
            qmobileQuerySet = RegisteredUser.objects.filter(Email = str(email)).using('YamahaBooking')
            if len(list(qmobileQuerySet)) > 0:
                response = {'StatusCode': '200', 'StatusMessage': '0'}
                print(response)
                return Response(response,content_type="application/json")
            else :
                response = {'StatusCode': '200', 'StatusMessage': '1'}
                print(response)
                return Response(response, content_type="application/json")

        # queryset = District.objects.all().values('Id', 'DistrictName').using('YamahaBooking')
        # data = json.dumps(list(queryset))

        response = {'StatusCode': '200', 'StatusMessage': 'NotFound'}
        print(response)
        return Response(response,content_type="application/json")


class UserRegistration(viewsets.ModelViewSet):
    queryset = District.objects.all()
    #role_class = RegisteredStgSerializer
    sms_class = SMSMessageOTPSerializer

    def create(self, request):
        userName = request.POST.get('name')
        mobile = request.POST.get('mobile')
        district = request.POST.get('district')
        email = request.POST.get('email')
        remarks = request.POST.get('remarks')
        
        entryTime = datetime.datetime.now()
        Disct = District.objects.filter(pk=int(district)).using('YamahaBooking')[0]
        regUser = RegisteredUser(UserName=str(userName), Mobile=str(mobile), Email= str(email), IsUsed ='N', Status ='1', EntryDate=entryTime, Remark=remarks, DistrictId=Disct)
        regUser.save(using='YamahaBooking')

        otpm = random_with_N_digits(4)
        smsMessage = SMSMessage( OtpCode=str(otpm), Email= str(email), IsUsed ='N', EntryDate=entryTime)
        print(str(smsMessage))
        smsMessage.save(using='YamahaBooking')
        text = 'Please use this confirmation code for registration.' + str(otpm)
        SendSMS(mobile, text)
        #SendSMS('01920250777', text)
    
        response = {'StatusCode': '200', 'StatusMessage': 'success'}
        return Response(response,content_type="application/json")

class ForgetPassword(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def list(self, request):
        mobile = request.GET.get('mobile').strip()
        redObj = RegisteredUser.objects.filter(Mobile=str(mobile)).using('YamahaBooking')
        if len(list(redObj))>0:
            user = YamahaUser.objects.filter(RegsUserId=redObj[0]).values('UserId','Password').using('YamahaBooking')[0]

            text = 'UserId : ' + user['UserId']+" Passwors : " + user['Password']
            SendSMS(mobile, text)
            #SendSMS('01920250777', text)
            response = {'StatusCode': '200', 'StatusMessage': 'success'}
            return Response(response, content_type="application/json")
        else:
            response = {'StatusCode': '202', 'StatusMessage': 'Register Please. This System Can Not found your mobile Number.'}
            return Response(response, content_type="application/json")





class OTPCheck(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def create(self, request):
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        sms = SMSMessage.objects.filter(OtpCode=str(otp), Email=str(email), IsUsed='N').using('YamahaBooking')
        if len(list(sms)) > 0:
            SMSMessage.objects.filter(OtpCode=str(otp), Email=str(email), IsUsed='N').using('YamahaBooking').update(IsUsed='Y')
            response = {'StatusCode': '200', 'StatusMessage': 'success'}
            return Response(response, content_type="application/json")
        else :
            response = {'StatusCode': '202', 'StatusMessage': 'faile'}
            return Response(response, content_type="application/json")

class LoginCheck(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer
    def create(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        userCheck = YamahaUser.objects.filter(UserId=str(email), Password=str(password), Status = 'Y').using('YamahaBooking')
        print("userCheck " + str(userCheck ))

        if len(list(userCheck)) > 0:
            response = {'StatusCode': '200', 'StatusMessage': 'success'}
            return Response(response, content_type="application/json")
        else :
            RegisteredUser.objects.filter(Email=str(email), IsUsed='N').using('YamahaBooking').update(IsUsed='Y')
            regUser = RegisteredUser.objects.filter(Email=str(email)).values('UserName').using('YamahaBooking')
            rUser = RegisteredUser.objects.filter(Email=str(email)).all().using('YamahaBooking')
            YamahaUser(UserId=str(email), UserName=regUser[0]['UserName'], Password=str(password), IsAdmin='0', Status = 'Y', RegsUserId=rUser[0]).save(using='YamahaBooking')
            response = {'StatusCode': '200', 'StatusMessage': 'success'}
            return Response(response, content_type="application/json")

        response = {'StatusCode': '202', 'StatusMessage': 'fail'}
        return Response(response, content_type="application/json")

class DepositBank(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def list(self, request):
        #fieldName = request.GET['fieldName'].strip()
        print('All Deposite Bank Information - ')
        queryset = DepositBankInfo.objects.all().values('Id', 'BankAccountName', 'AccountNo', 'BranchName').using('YamahaBooking')
        data = json.dumps(list(queryset))

        response = {'StatusCode': '200', 'StatusMessage': str(data)}
        print(response)
        return Response(response, content_type="application/json")


class AllProductInfo(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def list(self, request):
        #fieldName = request.GET['fieldName'].strip()
        print('All Product Information - ')
        queryset = Product.objects.filter(Stock__gt=0, Status='1').values('Id', 'ProductName', 'ProductPrice', 'MinBookingPrice', 'ProductImage1').using('YamahaBooking')
        if len(list(queryset))> 0:
            data = json.dumps(list(queryset), cls=DjangoJSONEncoder)
            #data = json.dumps(list(queryset))
            response = {'StatusCode': '200', 'StatusMessage': str(data)}
            print(response)
            return Response(response, content_type="application/json")
        else :
            response = {'StatusCode': '202', 'StatusMessage': 'No Item For Sales'}
            print(response)
            return Response(response, content_type="application/json")

class BookingSave(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def create(self, request):
        UserName = request.POST.get('UserName')
        AccountName = request.POST.get('AccountName')
        AccountNo = request.POST.get('AccountNo')
        depositBakinfo = request.POST.get('DepositBankInfo')
        dealerPoint = request.POST.get('DealerPoint')
        BookingMoney = request.POST.get('BookingMoney')
        product = request.POST.get('Product')
        TermsCondition = request.POST.get('TermsCondition')
        Remarks = request.POST.get('Remarks')

        dt = str(datetime.datetime.now())
        _datetime = datetime.datetime.now()
        datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
        fs = FileSystemStorage(location=settings.MEDIA_URL)
        productImage1 = request.FILES['uploaded_file']

        PaySlipDoc = datetime_str + "-" + productImage1.name
        fs.save(datetime_str+"-"+productImage1.name, productImage1)
        user = YamahaUser.objects.filter(UserId = str(UserName)).using('YamahaBooking')[0]
        product = Product.objects.filter(pk=int(product)).using('YamahaBooking')[0]
        dealerLocation = DealerLocation.objects.filter(pk=int(dealerPoint)).using('YamahaBooking')[0]
        checkUserBooking = Booking.objects.filter(UserId=user, ProductId=product, BookingStatus='Pending').using('YamahaBooking')
        if len(list(checkUserBooking)) > 0:
            response = {'StatusCode': '203', 'StatusMessage': 'DB transaction Fail.'}
        else :
            sTime = datetime.datetime.now()
            depositBankBranch = DepositBankInfo.objects.filter(pk=int(depositBakinfo)).values('BranchName').using('YamahaBooking')[0]
            depositBank = DepositBankInfo.objects.filter(pk=int(depositBakinfo)).using('YamahaBooking')[0]

            try:
                with transaction.atomic():
                    booking = Booking(UserId=user, IsAgree='Y', ProductId=product, BookingStatus=str('Pending'), DepositAmount=Decimal(BookingMoney) ,TermsCondition=TermsCondition, Remarks=str(Remarks), EntryDate=sTime, DealerPoint=dealerLocation)
                    booking.save(using='YamahaBooking')
                    BookingPaySlip(BankAccountName=str(AccountName) , AccountNo=str(AccountNo), BranchName=depositBankBranch['BranchName'] ,DepositBank=depositBank , EntryDate=sTime, PaySlipDoc=str(PaySlipDoc), PayAmount=Decimal(BookingMoney), Booking=booking).save(using='YamahaBooking')
                    response = {'StatusCode': '200', 'StatusMessage': 'success'}
            except DatabaseError:
                response = {'StatusCode': '202', 'StatusMessage': 'DB transaction Fail.'}

        print(response)
        return Response(response, content_type="application/json")

class PiImageSave(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def create(self, request):
        dt = str(datetime.datetime.now())
        _datetime = datetime.datetime.now()
        datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
        fs = FileSystemStorage(location=settings.MEDIA_URL+'Fair/')
        productImage1 = request.FILES['uploaded_file']

        fs.save(datetime_str + "-" + productImage1.name, productImage1)
        #imageurl="http://mis.digital:7779/PaySlip/Fair/"+productImage1.name
        #GetAzureEmotion(productImage1)
        #imagename = datetime_str + "-" + productImage1.name
        # url = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age'
        # headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': '2c223b68e95840d48ad1e6d580332d6c'}
        # r = requests.post(url, headers=headers,
        #                   params={"url": "http://mis.digital:7779/PaySlip/Fair/2019-01-12-19-14-10-618_my_image.jpg"})
        # print(r.text)


        # sleep(5)
        # headers = {'Content-Type': 'application/octet-stream',
        #            'Ocp-Apim-Subscription-Key': '2c223b68e95840d48ad1e6d580332d6c'}
        # face_api_url = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age'
        #
        # data = open('D:\\pyspace\\YamahaBookingAPI\\PaySlip\\Fair\\'+imagename, 'rb')
        # r = requests.post(face_api_url, headers=headers, data=data)
        # print(r.text)
        response = {'StatusCode': '200', 'StatuasMessage': 'Success'}
        return Response(response, content_type="application/json")

    def list(self, request):

        query = RegisteredUser.objects.exclude(UserName = 'Minhaz').values('UserName','Mobile','UserName').using('YamahaBooking')
        #print("--Query Size--" + str(len(list(query))))
        #print("--Query--" + str(query))
        userList = LocTrackUserManager.objects.filter(Id__gte=15).values('UserName', 'Mobile').using('LocationTracker')

        #text = 'UserId : ' + user['UserId'] + " Passwors : " + user['Password']
        #SendSMS('01755676604', sms)
        for item in userList:
            #print('--'+str(item))
            sms = 'Dearest ' +str(item['UserName'])+', Download the app: http://dashboard.acigroup.info/GetData/aci-connect.apk in your android phone internet browser and then install it allowing the access of your location using your username(staff ID), password(staff ID). After successful installation and login, please restart your android phone.'
            #print('--' + sms)
            #SendSMS(str(item['Password']), sms)
            SendSMS(str(item['Mobile']), sms)


        # entryDate = datetime.datetime.now()
        # for item in query:
        #     sendSMSText = SendSMSText(Mobile=str(item['Mobile']),Name=str(item['UserName']), SmsText=sms,  EntryDate=entryDate)
        #     sendSMSText.save(using='YamahaBooking')
        #     SendSMS(str(item['Mobile']), sms)
        #     #SendSMSText(str(item['Mobile']), sms)

        response = {'StatusCode': '200', 'StatuasMessage': 'Success'}
        return Response(response, content_type="application/json")


class AccountDetail(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer
    def list(self, request):
        UserName = request.GET.get('UserName').strip()

        userDetail = YamahaUser.objects.filter(UserId=str(UserName)).values('UserId', 'UserName', 'Password', 'RegsUserId__Mobile', 'RegsUserId__Remark', 'RegsUserId__DistrictId__Id', 'RegsUserId__DistrictId__DistrictName').using('YamahaBooking')
        data = json.dumps(list(userDetail))
        print(data)
        response = {'StatusCode': '200', 'StatusMessage': data}
        return Response(response, content_type="application/json")


class AllBooking(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def list(self, request):
        UserName = request.GET.get('UserName').strip()
        user = YamahaUser.objects.filter(UserId=str(UserName)).using('YamahaBooking')[0]
        bookingList = Booking.objects.filter(UserId=user).values('Id', 'ProductId__ProductName', 'ProductId__ProductColor','BookingStatus', 'ProductId__ProductPrice', 'ProductId__MinBookingPrice', 'ProductId__ProductImage1', 'EntryDate', 'DealerPoint__DLRPoint').using('YamahaBooking')

        bookingList = bookingList.extra(select={'datestr': "to_char(EntryDate, 'YYYY-MM-DD HH24:MI:SS')"})
        adminList = list(bookingList)
        print("--------->"+str(user))
        adminTemp = []
        for item in adminList:
            item['EntryDate'] = str(item['EntryDate'].strftime('%Y-%m-%d %H:%M'))
            #item['ProductId__ProductPrice'] = str(item['ProductId__ProductPrice'])
            adminTemp.append(item)
        #data = json.dumps(list(adminTemp))
        data = json.dumps(list(adminTemp), cls=DjangoJSONEncoder)
        print(data)
        response = {'StatusCode': '200', 'StatusMessage': data}
        return Response(response, content_type="application/json")

class AllProductForMessage(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer
    def list(self, request):
        adminTemp = Product.objects.all().values('Id', 'ProductName', 'ProductColor').using('YamahaBooking')
        data = json.dumps(list(adminTemp), cls=DjangoJSONEncoder)
        print(data)
        response = {'StatusCode': '200', 'StatusMessage': data}
        return Response(response, content_type="application/json")

class BookingQueryCheck(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer
    def list(self,request):
        userName = request.GET.get('user').strip()
        product = request.GET.get('product').strip()
        bookingdate = request.GET.get('bookingdate').strip()
        prdct = Product.objects.filter(pk=int(product)).using('YamahaBooking')[0]
        user = YamahaUser.objects.filter(UserId=str(userName)).using('YamahaBooking')[0]

        sDate = datetime.datetime(int(bookingdate.split('-')[0]), int(bookingdate.split('-')[1]),int(bookingdate.split('-')[2]), 0, 0, 0, 000)
        eDate = datetime.datetime(int(bookingdate.split('-')[0]), int(bookingdate.split('-')[1]), int(bookingdate.split('-')[2]), 23, 59, 59, 000)
        print(userName + "  " + product + " " + bookingdate)
        bquery = Booking.objects.filter(UserId=user, ProductId=prdct, EntryDate__range=(sDate, eDate)).using('YamahaBooking')
        if len(list(bquery))> 0:
            response = {'StatusCode': '200', 'StatusMessage': 'OK'}
            print("response " + str(response))
            return Response(response, content_type="application/json")
        else :
            response = {'StatusCode': '200', 'StatusMessage': 'FAIL'}
            print("response " + str(response))
            return Response(response, content_type="application/json")


class MessageSave(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def create(self,request):
        userName = request.POST.get('user').strip()
        product = request.POST.get('Product').strip()
        bookingdate = request.POST.get('BookingDate').strip()
        messageDetails =  request.POST.get('BookingMessage').strip()

        print("messageDetails " + messageDetails + " bookingdate " + bookingdate + " product " + product)

        sDate = datetime.datetime(int(bookingdate.split('-')[0]), int(bookingdate.split('-')[1]),
                                  int(bookingdate.split('-')[2]), 0, 0, 0, 000)
        eDate = datetime.datetime(int(bookingdate.split('-')[0]), int(bookingdate.split('-')[1]),
                                  int(bookingdate.split('-')[2]), 23, 59, 59, 000)

        prdct = Product.objects.filter(pk=int(product)).using('YamahaBooking')[0]
        fromUser = YamahaUser.objects.filter(UserId=str(userName)).using('YamahaBooking')[0]
        toUser = YamahaUser.objects.filter(pk=1).using('YamahaBooking')[0]
        entryDate = datetime.datetime.now()
        bquery = Booking.objects.filter(UserId=fromUser, ProductId=prdct, EntryDate__range=(sDate, eDate)).using(
            'YamahaBooking')

        inbox = Inbox(From=fromUser, To=toUser, BookingId=bquery[0], EntryDate=entryDate)
        inbox.save(using='YamahaBooking')
        InboxDetail(Message=str(messageDetails), InboxId=inbox, EntryBy=fromUser, EntryDate=entryDate).save(using='YamahaBooking')

        response = {'StatusCode': '200', 'StatusMessage': 'OK'}
        print("response " + str(response))
        return Response(response, content_type="application/json")

class UserAccountUpdate(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def create(self, request):
        username = request.POST.get('username').strip()
        mobile = request.POST.get('mobile').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        changepassword = request.POST.get('changepassword').strip()
        district = request.POST.get('district').strip()
        remarks = request.POST.get('remarks').strip()
        Disct = District.objects.filter(pk=int(district)).using('YamahaBooking')[0]
        RegisteredUser.objects.filter(Email=str(email)).using('YamahaBooking').update(UserName=str(username),Mobile=str(mobile),Remark=str(remarks), DistrictId=Disct)
        if changepassword != '':
            password = changepassword

        YamahaUser.objects.filter(UserId=str(email)).using('YamahaBooking').update(UserName=str(username), Password=password)

        response = {'StatusCode': '200', 'StatusMessage': 'OK'}
        print("response " + str(response))
        return Response(response, content_type="application/json")

class BookingEdit(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer


    def list(self, request):
        bookingId = request.GET.get('bookingId')
        bookQuery = Booking.objects.filter(pk=int(bookingId)).values('ProductId__Id','DepositAmount', 'TermsCondition', 'Remarks', 'DealerPoint__Id').using('YamahaBooking')
        bookQ = Booking.objects.filter(pk=int(bookingId)).using('YamahaBooking')[0]
        bookDetailQue = BookingPaySlip.objects.filter(Booking=bookQ).values('BankAccountName', 'AccountNo', 'DepositBank__Id', 'PaySlipDoc', 'PayAmount').using('YamahaBooking')
        bookingData = json.dumps(list(bookQuery), cls=DjangoJSONEncoder)
        bookDetailData = json.dumps(list(bookDetailQue), cls=DjangoJSONEncoder)
        print("bookDetailData " + str(bookDetailData))
        response = {'StatusCode': '200', 'Booking': bookingData, 'BookingPaySlip': bookDetailData}
        print("response " + str(response))
        return Response(response, content_type="application/json")

class InboxInfoDetail(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer
    def list(self, request):
        userName = request.GET.get('userName')
        UserId = YamahaUser.objects.filter(UserId=str(userName)).using('YamahaBooking')[0]
        bookingList = Booking.objects.filter(UserId=UserId).using('YamahaBooking')
        inboxList = Inbox.objects.filter(BookingId__in=bookingList).using('YamahaBooking')
        queryInboxList = Inbox.objects.filter(BookingId__in=bookingList).order_by('-Id').values('Id','BookingId__ProductId__ProductName','BookingId__ProductId__ProductColor', 'BookingId__ProductId__ProductPrice','EntryDate','From__UserId','To__UserId').using('YamahaBooking')
        queryInboxList = queryInboxList.extra(select={'datestr': "to_char(EntryDate, 'YYYY-MM-DD HH24:MI:SS')"})
        myList = list(queryInboxList)

        queryInboxDetail = InboxDetail.objects.filter(InboxId__in = inboxList).values('Message','InboxId__Id',).using('YamahaBooking')
        inBoxDetalList = list(queryInboxDetail)
        temp = []
        for item in myList:
            item['EntryDate'] = str(item['EntryDate'].strftime('%Y-%m-%d %H:%M'))
            for ik in inBoxDetalList:
                if item['Id'] == ik['InboxId__Id']:
                    item['Message'] = ik['Message']

            temp.append(item)

        data = json.dumps(list(temp), cls=DjangoJSONEncoder)

        response = {'StatusCode': '200', 'Inbox': data}
        print("response " + str(response))
        return Response(response, content_type="application/json")

class BookingUpdate(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def create(self, request):
        BookingId = request.POST.get('BookingId')
        UserName = request.POST.get('UserName')
        AccountName = request.POST.get('AccountName')
        AccountNo = request.POST.get('AccountNo')
        depositBakinfo = request.POST.get('DepositBankInfo')
        BookingMoney = request.POST.get('BookingMoney')
        product = request.POST.get('Product')
        dealerPoint = request.POST.get('DealerPoint')
        Remarks = request.POST.get('Remarks')
        IsFile = request.POST.get('IsFile')
        dt = str(datetime.datetime.now())
        _datetime = datetime.datetime.now()
        productImage1 = ''
        if IsFile=='1':
            datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
            fs = FileSystemStorage(location=settings.MEDIA_URL)
            productImage1 = request.FILES['uploaded_file']

            PaySlipDoc = datetime_str + "-" + productImage1.name
            fs.save(datetime_str + "-" + productImage1.name, productImage1)



        product = Product.objects.filter(pk=int(product)).using('YamahaBooking')[0]
        sTime = datetime.datetime.now()

        dealPoint = DealerLocation.objects.filter(pk=int(dealerPoint)).using('YamahaBooking')[0]
        depositBankBranch = DepositBankInfo.objects.filter(pk=int(depositBakinfo)).values('BranchName').using('YamahaBooking')[0]
        depositBank = DepositBankInfo.objects.filter(pk=int(depositBakinfo)).using('YamahaBooking')[0]
        booking = Booking.objects.filter(pk=int(BookingId)).using('YamahaBooking')[0]
        Booking.objects.filter(pk = int(BookingId)).using('YamahaBooking').update(ProductId=product, DepositAmount=Decimal(BookingMoney), Remarks=Remarks, DealerPoint=dealPoint)

        if IsFile == '1':
            BookingPaySlip.objects.filter(Booking=booking).using('YamahaBooking').update(
                BankAccountName=str(AccountName), AccountNo=str(AccountNo),
                BranchName=depositBankBranch['BranchName'], DepositBank=depositBank, EntryDate=sTime,
                PaySlipDoc=str(PaySlipDoc), PayAmount=Decimal(BookingMoney))
        else:
            BookingPaySlip.objects.filter(Booking=booking).using('YamahaBooking').update(
                BankAccountName=str(AccountName), AccountNo=str(AccountNo),
                BranchName=depositBankBranch['BranchName'], DepositBank=depositBank, EntryDate=sTime, PayAmount=Decimal(BookingMoney))


        response = {'StatusCode': '200', 'StatusMessage': 'OK'}
        print("response " + str(response))
        return Response(response, content_type="application/json")

class DownloadPaySlip(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def list(self, request):
        bookingId = request.GET.get('BookingId').strip()
        UserName = request.GET.get('UserName').strip()

        yUser = YamahaUser.objects.filter(UserId=str(UserName)).using('YamahaBooking')
        if len(list(yUser)) > 0:
            book = Booking.objects.filter(Id = int(bookingId)).using('YamahaBooking')[0]
            bookQuery = Booking.objects.filter(Id=int(bookingId)).values('UserId__UserName',
                                                                         'UserId__RegsUserId__Mobile',
                                                                         'EntryDate', 'ProductId__ProductName',
                                                                         'ProductId__ProductPrice',
                                                                         'ProductId__ProductColor',
                                                                         'DepositAmount').using('YamahaBooking')
            bookQuery = bookQuery.extra(select={'datestr': "to_char(EntryDate, 'YYYY-MM-DD HH24:MI:SS')"})
            bookQueryList = list(bookQuery)
            tempBooking = []
            for item in bookQueryList:
                item['EntryDate'] = str(item['EntryDate'].strftime('%Y-%m-%d %H:%M'))
                tempBooking.append(item)

            bookingData = json.dumps(list(tempBooking), cls=DjangoJSONEncoder)

            deliveryQuery = DeliveryPoint.objects.filter(BookingId=book).values('DeliveryDate',
                                                                                'DealerLocation__DLRPoint',
                                                                                'DealerLocation__NameOfDealer',
                                                                                'DealerLocation__OwnerContactNo',
                                                                                'DealerLocation__FullLocation',
                                                                                'DealerLocation__DistrictId__DistrictName').using(
                'YamahaBooking')
            deliveryQuery = deliveryQuery.extra(select={'datestr': "to_char(DeliveryDate, 'YYYY-MM-DD HH24:MI:SS')"})
            deliveryQueryList = list(deliveryQuery)
            tempDelivery = []

            for item in deliveryQueryList:
                item['DeliveryDate'] = str(item['DeliveryDate'].strftime('%Y-%m-%d %H:%M'))
                tempDelivery.append(item)

            deliveryData = json.dumps(list(tempDelivery), cls=DjangoJSONEncoder)

            response = {'StatusCode': '200', 'booking': bookingData, 'delivery': deliveryData}
            print("response " + str(response))
            return Response(response, content_type="application/json")
        else:
            response = {'StatusCode': '401', 'booking':"FAIL"}
            print("response " + str(response))
            return Response(response, content_type="application/json")

class StocknRemainingdays(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def list(self, request):
        queryset = Product.objects.filter(Stock__gt=0, Status='1').values('Id', 'ProductName', 'LastBookingDate','Stock').using('YamahaBooking')
        if len(list(queryset)) > 0:
            deliveryQuery = queryset.extra(select={'datestr': "to_char(LastBookingDate, 'YYYY-MM-DD HH24:MI:SS')"})
            deliveryQueryList = list(deliveryQuery)
            tempDelivery = []
            #sTime = datetime.datetime.now() tempDelivery.append(item)
            today = datetime.datetime.today()
            _datetime = datetime.datetime.now()
            #d1 = today.strftime("%Y-%m-%d")
            for item in deliveryQueryList:
                item['LastBookingDate'] = str(item['LastBookingDate'].strftime('%Y-%m-%d %H:%M'))

                d2 = datetime.datetime.strptime(item['LastBookingDate'], "%Y-%m-%d %H:%M")
                diff = abs((d2 - today).days)
                item['RemainingDay'] = diff
                tempDelivery.append(item)

            data = json.dumps(list(tempDelivery), cls=DjangoJSONEncoder)
            # data = json.dumps(list(queryset))
            response = {'StatusCode': '200', 'StatusMessage': str(data)}
            print(response)
            return Response(response, content_type="application/json")
        else:
            response = {'StatusCode': '202', 'StatusMessage': 'No Item For Sales'}
            print(response)
            return Response(response, content_type="application/json")


class AllDealerLocation(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer
    def list(self, request):
        dealQuery = DealerLocation.objects.all().values('Id','DLRPoint','DistrictId__DistrictName').using(
                'YamahaBooking')
        data = json.dumps(list(dealQuery), cls=DjangoJSONEncoder)
        response = {'StatusCode': '200', 'StatusMessage': str(data)}
        print(response)
        return Response(response, content_type="application/json")

class NotificationControll(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer
    def list(self, request):
        userName = request.GET.get('UserName')
        user = YamahaUser.objects.filter(UserId=str(userName)).using('YamahaBooking')[0]
        bookQuery = Booking.objects.filter(UserId=user, BookingStatus='Pending').using('YamahaBooking')
        msg = ""
        if len(list(bookQuery)) > 0:
            msg = "0"
        else :
            msg = "1"
        #data = json.dumps(list(dealQuery), cls=DjangoJSONEncoder)
        response = {'StatusCode': '200', 'StatusMessage': msg}
        print(response)
        return Response(response, content_type="application/json")

class LocationTrackerLoginCheck(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def create(self, request):
        userId = request.POST.get('UserId')
        password = request.POST.get('Password')
        print('--->' + str(userId) + "---->"+password)

        checkUser = LocTrackUserManager.objects.filter(UserId=userId, Password=password, IsActive='Y').values('UserId', 'UserName').using('LocationTracker')
        print('checkUser ---- > ' + str(len(checkUser)))

        if len(checkUser) > 0:
            sTime = datetime.datetime.now()
            #LocTrackUserManager.objects.filter(UserId=userId, Password=password, IsActive='Y').using('LocationTracker').update(IsUsed='Y', EditDate=sTime)
            #data = json.dumps(list(checkUser))
            msg = "1"
            response = {'StatusCode': '200', 'StatusMessage': msg}
            print(response)
            print(response)
            return Response(response, content_type="application/json")
        else:
            msg = "2"
            response = {'StatusCode': '200', 'StatusMessage': msg}
            return Response(response, content_type="application/json")

        msg = "3"
        #data = json.dumps(list(dealQuery), cls=DjangoJSONEncoder)
        response = {'StatusCode': '200', 'StatusMessage': msg}
        print(response)
        return Response(response, content_type="application/json")

class UserPathByDate(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def list(self, request):
        userId = request.GET.get('UserId')
        srartDate = request.GET.get('StartDateTime')
        endDate = request.GET.get('EndDateTime')
        #print("===="+ str(userId))
        connection = pymongo.MongoClient('mongodb://admin:admin@192.168.101.175:27017')

        sDate = str(srartDate).split(" ")[0]
        sTime = str(srartDate).split(" ")[1]
        mStartDate = str(sDate).split("-")[0]+"/"+str(sDate).split("-")[1]+"/"+str(sDate).split("-")[2] +" "+ sTime

        eDate = str(endDate).split(" ")[0]
        eTime = str(endDate).split(" ")[1]
        mEndDate = str(eDate).split("-")[0] + "/" + str(eDate).split("-")[1] + "/" + str(eDate).split("-")[2] + " " + eTime

        database = connection['MisConnect']
        collection = database['TestMongo']

        #myquery = {"UserId":userId, "EntryTime":{"$gte": "2019-08-28 00:00:00.000","$lt":"2019-08-28 23:59:59.000"}, "Latitude":{"$gte": "0.0"}}
        myquery = {"UserId": userId, "Mobile": {"$gte": mStartDate, "$lt": mEndDate},
                   "Latitude": {"$gte": "0.0"}}
        #print("==SQL=="+str(myquery))
        cursor = collection.find(myquery,{"_id": 0,"UserId":1,"Mobile":1,"Latitude":1,"Longitude":1,"EntryTime":1}).sort('EntryTime',-1)

        #print(dumps(cursor))
        ms = dumps(cursor)
        #for document in cursor:
            #print(document)
        msg = "1"
        # data = json.dumps(list(dealQuery), cls=DjangoJSONEncoder)
        response = {'StatusCode': '200', 'StatusMessage': str(ms)}
        #print(response)
        return Response(response, content_type="application/json")


class RecoveryDataRecive(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def list(self, request):
        #RecoveryData = request.POST.get('RecoveryData')
        #print('--->' + str(RecoveryData))
        received_json_data = json.loads(request.POST['RecoveryData'])

        print('--received_json_data->' + str(received_json_data))
        print('--received_json_data->' + str(received_json_data))
        msg = "1"
        # data = json.dumps(list(dealQuery), cls=DjangoJSONEncoder)
        response = {'StatusCode': '200', 'StatusMessage': msg}
        print(response)
        return Response(response, content_type="application/json")

    def create(self, request):
        #recoverydata = request.POST.get('RecoveryData')
        #received_json_data = json.loads(request.POST['RecoveryData'])

        #print('--RecoveryData->' + str(request.data.get('RecoveryData')))
        #print('--ProjectionData->' + str(request.data.get('ProjectionData')))

        #json_array = json.load(request.data.get('RecoveryData'))
        json_array = json.loads(request.data.get('RecoveryData'))
        projection_array = json.loads(request.data.get('ProjectionData'))
        capture_array = json.loads(request.data.get('CaptureData'))
        release_array = json.loads(request.data.get('ReleaseData'))
        #print('---------Recovary----' + str(json_array))
        #print('---------Recovary----' + str(json_array))
        print('---------capture_array----' + str(capture_array))
        print('---------release_array----' + str(release_array))
        store_list = []

        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.100.25;DATABASE=MotorBrInvoiceMirror;UID=sa;PWD=dataport')
        cursor = cnxn.cursor()
        for item in json_array:
            stuffId = item['stuffId']
            mrn = item['mrn']
            customerCode = item['customerCode']
            created_at = item['created_at']+'.123'
            collectiondate = item['collectiondate']
            amount = item['amount']
            supportedby = item['supportedby']
            remarks = item['remarks']
            colorstatus = item['colorstatus']
            latitude = item['latitude']
            longitude = item['longitude']
            LogName = "COLLECTION_SYNC"
            query = ''
            query2 = "INSERT INTO HitLog(LogName,CustomerCode) VALUES('" + LogName + "'," + customerCode + ")"
            if str(collectiondate) == '':
                query = "INSERT  INTO CollMasterNew(Amount, CustomerCode, mrn, CreateDate, StuffId, SupportedBy, Remarks, ColorStatus, Latitude, Longitude) VALUES(" + str(
                    amount) + ", '" + customerCode + "', '" + str(
                    mrn) + "', '" + created_at + "', '" + stuffId + "','"+supportedby+"','"+remarks+"',"+colorstatus+","+latitude+","+longitude+")"
            else:
                query = "INSERT INTO CollMasterNew(Amount, CustomerCode, mrn, CollectionDate, CreateDate, StuffId, SupportedBy, Remarks, ColorStatus, Latitude, Longitude) VALUES(" + str(
                    amount) + ", '" + customerCode + "', '" + str(
                    mrn) + "', '" + collectiondate + "', '" + created_at + "', '" + stuffId + "','"+supportedby+"','"+remarks+"',"+colorstatus+","+latitude+","+longitude+")"

            #query = "INSERT  INTO CollMasterNew(Amount, CustomerCode, mrn, CollectionDate, CreateDate, StuffId) VALUES(" + str(amount) + ", '" + customerCode + "', '" + str(mrn) + "', '" + collectiondate + "', '" + created_at + "', '" + stuffId + "')"
            #print(query)
            cursor.execute(query)
            cursor.execute(query2)

        for item in projection_array:
            StaffID = item['staffid']
            ProjectionDate = item['projectiondate']
            CustomerMobile = item['customermobile']
            CustomerCode = item['customercode']
            CreateDate = item['created_at']
            ProjectionAmount = item['amount']
            LogName = "PROJECTION_SYNC"
            query = "INSERT  INTO ProjectionMaster(StaffID, CustomerCode, ProjectionAmount, ProjectionDate, CustomerMobile, CreateDate) VALUES('" + str(StaffID) + "', '" + CustomerCode + "', '" + ProjectionAmount + "', '" + ProjectionDate + "', '" + CustomerMobile + "', '" + CreateDate + "')"
            query2 = "INSERT INTO HitLog(LogName,CustomerCode) VALUES('" + LogName + "'," + customerCode + ")"
            # print(query)
            cursor.execute(query)
            cursor.execute(query2)

        for item in capture_array:
            staffID = item['staffid']
            customerCode = item['customercode']
            customerName = item['customername']
            captureDate = item['capturedate']
            captureLocation = item['capturelocation']
            capturetractormodel = item['capturetractormodel']
            captureother = item['captureother']
            LogName = "CAPTURE_SYNC"
            query2 = "INSERT INTO HitLog(LogName,CustomerCode) VALUES('" + LogName + "',"+customerCode+")"
            if captureother == '':
                captureother = ''

            query = "INSERT  INTO CaptureMaster(StaffID, CustomerCode, CustomerName, CaptureDate, CaptureLocation, CaptureTractorModel, CaptureOther) VALUES('" + str(
                staffID) + "', '" + customerCode + "', '" + customerName + "', '" + captureDate + "', '" + captureLocation + "', '" + capturetractormodel + "', '" + captureother + "')"
            # print(query)
            cursor.execute(query)
            cursor.execute(query2)

        for item in release_array:
            staffID = item['staffid']
            customerCode = item['customercode']
            customerName = item['customername']
            releaseDate = item['releasedate']
            amount = item['amount']
            LogName = "RELEASE_SYNC"
            query = "INSERT  INTO ReleaseMaster(StaffID, CustomerCode, CustomerName, ReleaseDate, Amount) VALUES('" + str(
                staffID) + "', '" + customerCode + "', '" + customerName + "', '" + releaseDate + "', '" + amount + "')"
            # print(query)
            query2 = "INSERT INTO HitLog(LogName,CustomerCode) VALUES('" + LogName + "'," + customerCode + ")"
            cursor.execute(query)
            cursor.execute(query2)

        cnxn.commit()
        cnxn.close()

        msg = "1"
        response = {'StatusCode': '200', 'StatusMessage': msg}
        print(response)
        return Response(response, content_type="application/json")

class MyAppCustomer(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def create(self, request):
        userId = request.POST.get('UserId')
        import re
        #print('--UserId--'+ str(userId))
        cnxn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=192.168.100.25;DATABASE=MotorBrInvoiceMirror;UID=sa;PWD=dataport')
        cursor = cnxn.cursor()
        today = datetime.datetime.today()
        mToday = re.split(" ", str(today))[0]

        fDate = re.split("-", str(mToday))[0]+'-'+re.split("-", str(mToday))[1]+'-'+'01'
        #fDate = '2019-10-01'

        #print('---' + fDate)

        sqlst = "SELECT aum.UserName, cas.Code, cas.CustomerName, ForMonth, '0' AS SyncStatus FROM AppUserManager aum INNER JOIN Territory TT ON aum.TerritoryCode = TT.TTYCode INNER JOIN CreditAnalysisStg cas ON cas.Territory LIKE TT.TTYName WHERE (cas.ForMonth = '"+fDate+"') AND aum.UserName = '"+str(userId)+"'"

        print('--'+str(sqlst))

        cursor.execute(sqlst)
        results = cursor.fetchall()
        tempDelivery = []
        # sTime = datetime.datetime.now() tempDelivery.append(item)
        item = {}
        for row in results:
            item = {}

            item['userName'] = row[0]
            item['code'] = row[1]
            item['customerName'] = row[2]
            item['forMonth'] = row[3]
            item['syncStatus'] = row[4]
            #item['syncDate'] = row[5]
            tempDelivery.append(item)
            #print('--'+str(userName)+'--'+str(code)+'--'+str(customerName)+'--'+str(forMonth)+'--'+str(syncStatus)+'--'+str(syncDate))

        data = json.dumps(list(tempDelivery), cls=DjangoJSONEncoder)
        msg = ''
        response = {'StatusCode': '200', 'StatusMessage': str(data)}
        print(response)
        return Response(response, content_type="application/json")

class Myrabbitmq(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def create(self, request):
        userId = request.POST.get('userId')
        doctorType = request.POST.get('doctorType')
        doctorCode = request.POST.get('doctorCode')
        institution = request.POST.get('institution')
        productCode = request.POST.get('productCode')
        prescriptionDate = request.POST.get('prescriptionDate')
        mobileNo = request.POST.get('mobileNo')
        IMEI = request.POST.get('IMEI')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        competitorBrandCode = request.POST.get('competitorBrandCode')

        image = request.FILES.get('prescription_image')
        #image = request.FILES.get('image')
        _datetime = datetime.datetime.now()
        datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S-%f")

        fs = FileSystemStorage(location=settings.MEDIA_URL + 'UploadedMedia/')
        iName = str.replace(image.name,':','-')
        iName = str.replace(iName,' ','-')
        print('----'+iName)
        #fs.save(datetime_str + "-" + image.name, image)
        fs.save(datetime_str + "-" + iName, image)

        print('UserId->'+str(userId) + "doctorType->"+str(doctorType) + "->"+ str(doctorCode) + "->"+str(institution)+"->"+ str(productCode)+"->"+str(latitude))

        data = {"userId": str(userId), "doctorType": str(doctorType), "doctorCode": str(doctorCode), "institution": str(institution),
                "productCode": str(productCode), "prescriptionDate": str(prescriptionDate), "mobileNo": str(mobileNo), "IMEI": str(IMEI),
                "latitude": str(latitude), "longitude": str(longitude), "competitorBrandCode": str(competitorBrandCode),"imgname":str(datetime_str + "-" + image.name)}

        json_data = json.dumps(data)



        rabbit_url = 'amqp://admin:admin@192.168.101.175:5672/'

        conn = Connection(rabbit_url)

        channel = conn.channel()

        exchange = Exchange('test', type = 'direct')

        producer = Producer(exchange=exchange, channel=channel, routing_key='BOB')

        queue = Queue(name='rximage', exchange = exchange, routing_key ='BOB')
        queue.maybe_bind(conn)
        queue.declare()

        producer.publish(str(json_data))

        response = {'StatusCode': '200', 'StatusMessage': 'OK'}
        return Response(response, content_type="application/json")

class MayaDataProvider(viewsets.ModelViewSet):
    queryset = District.objects.all()
    role_class = RegisteredStgSerializer

    def list(self, request):
        #RecoveryData = request.POST.get('RecoveryData')
        #print('--->' + str(RecoveryData))
        #received_json_data = json.loads(request.POST['RecoveryData'])

        twitter = OAuth1Session('1cb615ef0b50b640324bb7e614551f7b',
                                client_secret='edf2e5500bd06bdcf0a48182236917af',
                                resource_owner_key='bfddd465b6ea96755e5b170c7dc5adec',
                                resource_owner_secret='d4b2655c7355faa644dd9dcf20948b57')
        url = 'http://staging.banglameds.com.bd/api/rest/productlist?name=napa&page='
        r = twitter.get(url)
        print("====="+str(r.content))
        msg = "1"
        # data = json.dumps(list(dealQuery), cls=DjangoJSONEncoder)
        response = {'StatusCode': '200', 'StatusMessage': msg}
        print(response)
        return Response(response, content_type="application/json")



def SendSMS(number, text):
    data = {'smstext': text,
            'number': number}
    r = requests.post(url='http://192.168.100.8/fifaabecab/Authenticate/sendSMS', data=data)
    return

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
