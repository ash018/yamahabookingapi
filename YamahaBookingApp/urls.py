from rest_framework import routers
from .views import  RecoveryDataRecive, Location, FormValidation, UserRegistration, OTPCheck, LoginCheck, DepositBank, AllProductInfo, BookingSave, AccountDetail, AllBooking, AllProductForMessage, BookingQueryCheck, MessageSave, UserAccountUpdate, BookingEdit, InboxInfoDetail, BookingUpdate, DownloadPaySlip, ForgetPassword, StocknRemainingdays, AllDealerLocation, NotificationControll, PiImageSave, MyAppCustomer, LocationTrackerLoginCheck, Myrabbitmq, UserPathByDate, MayaDataProvider
from .models import District

from django.conf.urls import url, include

router = routers.DefaultRouter()
#router.register(r'ImageExtractAPI', ImageViewSet) , BaseAPICallURL ,BaseUrlConfig
#router.register(r'registration', Registration)
router.register(r'alldistrict', Location)
router.register(r'fromvalidator', FormValidation)
router.register(r'registerusersave', UserRegistration)
router.register(r'otpcheck', OTPCheck)
router.register(r'logincheck', LoginCheck)
router.register(r'depositbankinfo', DepositBank)
router.register(r'availableproduct', AllProductInfo)
router.register(r'allproduct', AllProductForMessage)
router.register(r'savenewbooking', BookingSave)
router.register(r'accountdetial', AccountDetail)
router.register(r'allbooking', AllBooking)
router.register(r'checkBooking', BookingQueryCheck)
router.register(r'messagesave', MessageSave)
router.register(r'useraccountupdate', UserAccountUpdate)
router.register(r'editbooking', BookingEdit)
router.register(r'inboxdetail', InboxInfoDetail)
router.register(r'updatebooking', BookingUpdate)
router.register(r'downloadpayslip', DownloadPaySlip)
router.register(r'forgetPassword', ForgetPassword)
router.register(r'stocknremainingday', StocknRemainingdays)
router.register(r'alldealerlocation', AllDealerLocation)
router.register(r'notificationcontroll', NotificationControll)

router.register(r'savenewpiimage', PiImageSave)
router.register(r'recoverydatarecive', RecoveryDataRecive)
router.register(r'myappcustomer', MyAppCustomer)
router.register(r'mayadataprovider', MayaDataProvider)

router.register(r'myrabbitmq', Myrabbitmq)

router.register(r'locationtrackerlogincheck', LocationTrackerLoginCheck)
router.register(r'userpathbydate', UserPathByDate)




# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]