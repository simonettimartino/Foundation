import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from antidote import inject

from generic_organization_service.services.verify_service import VerifyService
from generic_organization_service.services.connection_service import ConnectionService
from generic_organization_service.services.issue_service import IssueService


from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.db import connection
from django.http import HttpResponseRedirect
#from generic_organization_service.handlers.organization_handler_manager import OrganizationHandlerManager

import psycopg2


from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn
from algosdk import account, encoding
from algosdk.transaction import AssetConfigTxn
from algosdk.transaction import write_to_file

#from yourcompany.organization_handler import OrganizationHandler
from generic_organization_service.handlers.organization_handler_manager import OrganizationHandlerManager
from antidote import world
import json

logger = logging.getLogger(__name__)
pzier_token_id = "15104608"
astrazeneca_token_id = "15104588"
moderna_token_id = "15104604"
jej_token_id = "15104602" #johnson &johnson
vettore_id_token = [pzier_token_id, astrazeneca_token_id, moderna_token_id, jej_token_id]

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





#aggiungere le sessioni 
def generate_algorand_keypair(): #genera account algorand
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    straddress = str(address)
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
    strpassphrase = str(mnemonic.from_private_key(private_key))
    addrpiupass = straddress + " - " + strpassphrase
    return addrpiupass



def account_profile(request):
    #myaddrpiuacinfo = myAccInfo()
    #splitmyaddrpiuacinfo = myaddrpiuacinfo.split(" - ")

    #parte vera 
    requestUserID_connessione = request.GET.get('requid', '')
    #inizializzazione
    walletSplittato = ""
    algod_address = "http://192.168.1.67:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    #inizializzo connessione db
    hostname = '192.168.1.67'
    username = 'postgres'
    password = 'organization_db_password'
    database = 'generic_organization_db'
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

    cur = myConnection.cursor() #apro la connessione

    cur.execute("SELECT user_connection_id FROM generic_organization_service_request WHERE request_uid='"+str(requestUserID_connessione)+"' limit 1;") 
    user_connection_id = cur.fetchall()[0][0]
    
    cur.execute("SELECT data FROM generic_organization_service_userdata WHERE user_connection_id='"+str(user_connection_id)+"' limit 1;") 
    datiUtenteDalDB = cur.fetchall()[0][0]
    mailUtenteRicavata = datiUtenteDalDB['email']
    
    #generazione di un wallet algorand se non lo ha con noi
    cur.execute("SELECT count(*) FROM account WHERE mail='"+mailUtenteRicavata+"';") 
    verifica = cur.fetchall()[0][0]
    print('verifica: ',verifica)
    if verifica == 0:
        #aggiungo un wallet se non esiste alcuna mail nel db
        #inserisco la mail nel database
        resultWalletGenerato = generate_algorand_keypair()
        walletSplittato = resultWalletGenerato.split(" - ") #in 0 c'è il wallet generato, in 1 c'è la chiave privata
        cur.execute("INSERT INTO account(mail,wallet_algo,private_key) VALUES('"+mailUtenteRicavata+"','"+walletSplittato[0]+"','"+ walletSplittato[1]+"');" )
        myConnection.commit()
    #else: #seleziono i dati già presenti nel db
        #cur.execute("SELECT * FROM account WHERE mail='"+mailUtenteRicavata+"';")   
        #datiUtente = cur.fetchall()
        #print("dati utente ", datiUtente)

    cur.execute("SELECT * FROM account WHERE mail='"+mailUtenteRicavata+"' limit 1;")  #limit 1, non si sa mai...
    datiUtente_db = cur.fetchall()

    myConnection.close()#chiudo la connessione con il db


    #li recupero dal db perchè potrebbero essere già presenti al suo interno e non dovrei rigenerarli
    for riga in datiUtente_db:
        print("riga ",riga)
        mailDal_Db = riga[0]
        walletDal_db = riga[1]
        private_key_dalDb = riga[2]
       
    #recupero dati associati al wallet
  
    datiWalletOttenuti = recuperoDatiAccountAlgo(algod_client,walletDal_db)
    datiWalletOttenutiSplittati = datiWalletOttenuti.split(" - ")
    print("my_address ",walletDal_db)
    print("microAlgos ",datiWalletOttenutiSplittati[0])
    #passo da microalgo ad algo
    algoPosseduti = int(datiWalletOttenutiSplittati[0]) / 1000000
    

    algod_address = "http://192.168.1.67:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    #recupero quanti nft hanno i wallet
    j = 0
    amountToken = 0
    token_posseduti = []
    asset_id_vettore = []
    while j < len(vettore_id_token):
        amountToken = check_holdings(algod_client, vettore_id_token[j] , "FLSALBSJCHZCQ7P7V5KKDGYSPXIHWEIOWMSCARFJNMKMBBEMDE2KKOQ3AY")
        print("aaaaa ",amountToken)
        token_splittait = amountToken.split(" - ")
        token_posseduti.append(token_splittait[0])
        asset_id_vettore.append(token_splittait[1])#passo l'asset id
        j += 1



    return render(request,'account_profile.html',{"my_address":walletDal_db,"algo_posseduti":algoPosseduti, "amount_token_nft":token_posseduti,"asset_idvettore":asset_id_vettore})#non mostriamo la passphrase
    

    

def recuperoDatiAccountAlgo(algod_client, indirizzoWallet):
    #recupero quanti algorand ha
    
    account_info = algod_client.account_info(indirizzoWallet)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))
    microAlgo = str(account_info.get('amount'))
    
    datiWallet = microAlgo + " - "

    return datiWallet

#------------------------- visualizzazione token -------------------------
#metodo per la gestione dei token
def balance_formatter(amount, asset_id, algod_client):
    """
    Returns the formatted units for a given asset and amount. 
    """
    print("algoooo client ", algod_client)
    asset_info = algod_client.asset_info(asset_id)
    decimals = asset_info.get("decimals")
    unit = asset_info.get("unitname")
    formatted_amount = amount/10**decimals
    return "{} {}".format(formatted_amount, unit)

def check_holdings(algod_client, asset_id, address):
    amount = 0 
    asset_id_usato = ""

    """
    Checks the asset balance for the specific address and asset id.
    """
    account_info = algod_client.account_info(address)
    assets = account_info.get("assets")
    print("assets: ", assets)
    asset_holding = ""
    if assets:
        #asset_holdings = account_info["assets"]
        
        #asset_holding = asset_holdings['asset_id']
        indice = 0
        controllo = False
        print("lunghezza assets: ",len(assets))
        while controllo == False:
            if indice <= len(assets)-1:
                print("assets[indice][asset-id] =====  ", assets[indice]['asset-id'])
                print("asset_id =====  ", asset_id)
                if str(assets[indice]['asset-id']) == asset_id:
                    asset_holding = assets[indice]['asset-id']
                    controllo = True  
                    print("ema sono qui")

                    if not asset_holding:
                        print("Account {} must opt-in to Asset ID {}.".format(address, asset_id))
                    else:
                        amount = assets[indice]['amount']#asset_holding.get("amount")
                        asset_id_usato = asset_id
                        #print("Account {} has {}.".format(address, balance_formatter(amount,asset_id,algod_client)))
                        print("NFT posseduti: {} con asset id: {} ".format(amount, asset_holding))
                    
                else:
                    controllo = False
                    indice = indice + 1
            else:
                break
        
       
       
    else:
        print("Account {} must opt-in to Asset ID {}.".format(address, asset_id))


    return str(amount) + " - " + asset_id_usato




def home(request):
    #test inizio

    #fine test
    return render(request,'home.html')
    