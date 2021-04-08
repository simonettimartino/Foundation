import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from antidote import inject

from generic_organization_service.services.verify_service import VerifyService
from generic_organization_service.services.connection_service import ConnectionService
from generic_organization_service.services.issue_service import IssueService

#from yourcompany.organization_handler import OrganizationHandler

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.db import connection
from django.http import HttpResponseRedirect

import psycopg2


from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn
from algosdk import account, encoding



logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(["GET"])
@permission_classes(())
@inject
def start_verify(request, proof_business_code, service_name, verify_service: VerifyService, *args, **kwargs):
    logger.info("start_verify for business_code: %s and service_name: %s", proof_business_code, service_name)
    allow_multiple_read = request.GET.get("allow_multiple_read", "false")

    request.data['proof_business_code'] = proof_business_code
    request.data['service'] = service_name
    request.data['restrictions'] = {}
    request.data['allow_multiple_read'] = True if (allow_multiple_read == "True" or allow_multiple_read == "true") \
        else False
    return verify_service.start_verify(request.data)

@csrf_exempt
@api_view(["GET"])
@permission_classes(())
@inject
def start_connection(request, organization_business_code, connection_service: ConnectionService, *args, **kwargs):
    logger.info("start_connection for organization_business_code: %s", organization_business_code)
    allow_multiple_read = request.GET.get("allow_multiple_read", "false")
    request.data['organization_business_code'] = organization_business_code
    request.data['allow_multiple_read'] = True if (allow_multiple_read == "True" or allow_multiple_read == "true") \
        else False
    return connection_service.start_connection(request.data)


@csrf_exempt
@api_view(["GET"])
@permission_classes(())
@inject
def start_verify_with_widget(request, proof_business_code, service_name, verify_service: VerifyService, *args, **kwargs):
    logger.info("start_verify for business_code: %s and service_name: %s", proof_business_code, service_name)
    allow_multiple_read = request.GET.get("allow_multiple_read", "false")

    request.data['proof_business_code'] = proof_business_code
    request.data['service'] = service_name
    request.data['restrictions'] = {}
    request.data['allow_multiple_read'] = True if (allow_multiple_read == "True" or allow_multiple_read == "true") \
        else False

    return verify_service.start_verify_with_widget(request.data)


@csrf_exempt
@api_view(["POST"])
@inject
@permission_classes(())
def confirm_verify(request, verify_service: VerifyService, *args, **kwargs):
    logger.info("confirm_verify")
    return verify_service.confirm_verify(request.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes(())
@inject
def connection_notify(request, connection_service: ConnectionService, *args, **kwargs):
    logger.info("connection_notify")
    return connection_service.connection_notify(request.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes(())
@inject
def confirm_issue(request, issue_service: IssueService, *args, **kwargs):
    logger.info("confirm_issue")
    return issue_service.confirm_issue(request.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes(())
@inject
def discard_credential(request, issue_service: IssueService, *args, **kwargs):
    logger.info("discard_credential")
    return issue_service.discard_credential(request.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes(())
@inject
def discard_proof(request, verify_service: VerifyService, *args, **kwargs):
    logger.info("discard_credential")
    return verify_service.discard_proof(request.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes(())
@inject
def values_for_credential(request, issue_service: IssueService, *args, **kwargs):
    logger.info("discard_credential")
    return issue_service.values_for_credential(request.data)



def main(request):
    #return HttpResponse('about')
    return render(request,'main.html')


def error(request):
    return HttpResponse('about')
    return render(request,'error.html')

def generic_error(request):
    return HttpResponse('about')
    return render(request,'generic_error.html')





def home(request):
    #addrpiupass = generate_algorand_keypair()
    #myaddrpiuacinfo = myAccInfo()
    #splitaddrpiupass = addrpiupass.split(" - ")
    #splitmyaddrpiuacinfo = myaddrpiuacinfo.split(" - ")
    return render(request,'home.html')
    
#aggiungere le sessioni     
def generate_algorand_keypair(): #genera account algorand
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    straddress = str(address)
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
    strpassphrase = str(mnemonic.from_private_key(private_key))
    addrpiupass = straddress + " - " + strpassphrase
    return addrpiupass


def myAccInfo():
    #192.168.1.67
    algod_address = "http://192.168.1.67:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    passphrase = "sample oven shop vacuum ribbon multiply skull grain buddy eagle razor trash average fury alley pioneer garbage panda lecture road tattoo inflict core above joke"

    private_key = mnemonic.to_private_key(passphrase)
    my_address = mnemonic.to_public_key(passphrase)
    print("My address: {}".format(my_address))
    strmy_address = str(my_address)
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))
    straccount_info = str(account_info.get('amount'))
    myaddrpiuacinfo = strmy_address + " - " + straccount_info
    return myaddrpiuacinfo


def account_profile(request):
    myaddrpiuacinfo = myAccInfo()
    splitmyaddrpiuacinfo = myaddrpiuacinfo.split(" - ")

    emailUtente = OrganizationHandler.getMailUtente()
    print("pony: ",emailUtente)
    #walletGenerato =

    return render(request,'account_profile.html',{"my_address":splitmyaddrpiuacinfo[0],"microAlgos":splitmyaddrpiuacinfo[1]})
    

    



    
