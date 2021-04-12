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
import http.client
from algosdk.future.transaction import AssetTransferTxn, AssetFreezeTxn
from datetime import date


logger = logging.getLogger(__name__)

#inizializzazione variabili
pzier_token_id = "15104608"
astrazeneca_token_id = "15104588"
moderna_token_id = "15104604"
jej_token_id = "15104602" #johnson &johnson
vettore_id_token = [pzier_token_id, astrazeneca_token_id, moderna_token_id, jej_token_id]


algod_address = "http://192.168.1.67:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

token_issue_credential = "JNNb5EMJpPhubxRJ8RtHDK:3:CL:201960:Token Vaccinazione"

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
def generate_algorand_keypair(algod_client): #genera account algorand
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    straddress = str(address)
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
    strpassphrase = str(mnemonic.from_private_key(private_key))
    addrpiupass = straddress + " - " + strpassphrase

    # ----------------------- INVIATO 0,2 ALGO all'account appena creato -----------------------

    # passphrase dell'ACCOUNT BANCA
    passphrase = "mercy swift guilt crunch board favorite tail grow explain family rookie math depth cram fly apple duty steel hurry foot liquid dream custom able axis"

    private_key = mnemonic.to_private_key(passphrase)
    my_address = mnemonic.to_public_key(passphrase)
    #print("My address: {}".format(my_address))

    account_info = algod_client.account_info(my_address)
    #print("Account balance: {} microAlgos".format(account_info.get('amount')))

    account_che_riceve = address #address è l'indirizzo del wallet appena creato
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000
    receiver = account_che_riceve  # questo va gestito con una variabile
    note = "Hello World".encode()
    # vanno spediti 0,2 algo --> il minimo per poter fare l'opt-in
    unsigned_txn = PaymentTxn(my_address, params, receiver, 201000, None, note)

    #signe transaction
    signed_txn = unsigned_txn.sign(mnemonic.to_private_key(passphrase))

    #submit transaction
    txid = algod_client.send_transaction(signed_txn)

    return addrpiupass



def account_profile(request):
    #myaddrpiuacinfo = myAccInfo()
    #splitmyaddrpiuacinfo = myaddrpiuacinfo.split(" - ")

    #parte vera 
    requestUserID_connessione = request.GET.get('requid', '')
    #inizializzazione
    walletSplittato = ""
    #algod_address = "http://192.168.1.67:4001"
    #algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    #algod_client = algod.AlgodClient(algod_token, algod_address)

    #inizializzo connessione db
    hostname = '192.168.1.67'
    username = 'postgres'
    password = 'organization_db_password'
    database = 'generic_organization_db'
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

    cur = myConnection.cursor() #apro la connessione

    cur.execute("SELECT id FROM generic_organization_service_request WHERE request_uid='"+str(requestUserID_connessione)+"' limit 1;") 
    user_connection_id = cur.fetchall()[0][0]
    
    cur.execute("SELECT data FROM generic_organization_service_userdata WHERE request_id='"+str(user_connection_id)+"' limit 1;") 
    datiUtenteDalDB = cur.fetchall()[0][0]
    print("datiUtenteDalDB ",datiUtenteDalDB)
    try:
        cflUtenteRicavata = datiUtenteDalDB['personIdentifierNumber']
    except:
        return render(request,'error.html')
    #generazione di un wallet algorand se non lo ha con noi
    cur.execute("SELECT count(*) FROM account WHERE codice_fiscale='"+cflUtenteRicavata+"';") 
    verifica = cur.fetchall()[0][0]
    print('verifica: ',verifica)
    if verifica == 0:
        #aggiungo un wallet se non esiste alcuna mail nel db
        #inserisco la mail nel database
        resultWalletGenerato = generate_algorand_keypair(algod_client)
        walletSplittato = resultWalletGenerato.split(" - ") #in 0 c'è il wallet generato, in 1 c'è la chiave privata
        cur.execute("INSERT INTO account(codice_fiscale,wallet_algo,private_key) VALUES('"+cflUtenteRicavata+"','"+walletSplittato[0]+"','"+ walletSplittato[1]+"');" )
        myConnection.commit()
    #else: #seleziono i dati già presenti nel db
        #cur.execute("SELECT * FROM account WHERE mail='"+cflUtenteRicavata+"';")   
        #datiUtente = cur.fetchall()
        #print("dati utente ", datiUtente)

    cur.execute("SELECT * FROM account WHERE codice_fiscale='"+cflUtenteRicavata+"' limit 1;")  #limit 1, non si sa mai...
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
    

   
    #recupero quanti nft hanno i wallet
    j = 0
    amountToken = 0
    token_posseduti = []
    asset_id_vettore = []
    vettore_nomi = []
    vettore_url = []
    while j < len(vettore_id_token):
        #preparo amount token e asset id
        amountToken = check_holdings(algod_client, vettore_id_token[j] , walletDal_db)
        print("aaaaa ",amountToken)
        token_splittait = amountToken.split(" - ")
        token_posseduti.append(token_splittait[0])
        #asset_id_vettore.append(token_splittait[1])#passo l'asset id
        #recupero nome vaccino e url
        risultatoDati = print_created_asset(algod_client, walletDal_db, vettore_id_token[j])
        risultatoDatisplittati = risultatoDati.split(" - ")
        vettore_nomi.append(risultatoDatisplittati[0])
        vettore_url.append(str(risultatoDatisplittati[1]))
        asset_id_vettore.append(str(risultatoDatisplittati[2]))
        j += 1


    return render(request,'account_profile.html',{"my_address":walletDal_db,"algo_posseduti":algoPosseduti, "amount_token_nft":token_posseduti,"asset_idvettore":asset_id_vettore,"nome_token_vettore":vettore_nomi,"url_token_vettore":vettore_url})#non mostriamo la passphrase
    

    

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
    asset_holding = ""
    if assets:
        #asset_holdings = account_info["assets"]
        
        #asset_holding = asset_holdings['asset_id']
        indice = 0
        controllo = False
        print("lunghezza assets: ",len(assets))
        while controllo == False:
            if indice <= len(assets)-1:
                if str(assets[indice]['asset-id']) == asset_id:
                    asset_holding = assets[indice]['asset-id']
                    controllo = True  

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


# ------------ recupero url e txid algorand ------------
def print_created_asset(algod_client, account, assetid):    
 
    nomeVaccino = ""
    url = ""
    account_info = algod_client.account_info(account)
    idx = 0
    wallet_creatore_dell_asset = ""
    asset_id_recuperato = ""
    print("account_info ",account_info)
   
    for my_account_info in account_info['assets']:
        wallet_creatore_dell_asset = account_info['assets'][idx]['creator'] #trovo il wallet del creatore
        #print("wallet_creatore_dell_asset ",wallet_creatore_dell_asset)
       
    if len(account_info['assets']) == 0: #se non è vuoto 
        wallet_creatore_dell_asset = "FLSALBSJCHZCQ7P7V5KKDGYSPXIHWEIOWMSCARFJNMKMBBEMDE2KKOQ3AY"

    #uso l'account di un creatore che conosco sicuramente (è una cosa temporanea)
    account_info_creatore = algod_client.account_info(wallet_creatore_dell_asset)
    print("account_info_creatore ",account_info_creatore)

    idx = 0
    for scorri_account_info_creatore in account_info_creatore['created-assets']: #non va
        scrutinized_asset = account_info_creatore['created-assets'][idx]
        print("scrutinized_asset ",scrutinized_asset)
        #print("scrutinized_asset ", scrutinized_asset)
        idx = idx + 1      
        #print("scrutinized_asset[index] ", scrutinized_asset['index']) 
        #print("assetid ", assetid)
        if (str(scrutinized_asset['index']) == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(scorri_account_info_creatore['params'], indent=4))
            nomeVaccino = scorri_account_info_creatore['params']['unit-name']
            url = scorri_account_info_creatore['params']['url']
            asset_id_recuperato = scrutinized_asset['index']
            break
        
    print("================")
    print(nomeVaccino , url)
    return nomeVaccino + " - " + url + " - " + str(asset_id_recuperato)


# --------------- optin -> richiesta di un token vaccino
def optin(request, algod_client, asset_id, account_richiedente):
  
    hostname = '192.168.1.67'
    username = 'postgres'
    password = 'organization_db_password'
    database = 'generic_organization_db'
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

    cur = myConnection.cursor() #apro la connessione
    cur.execute("SELECT private_key FROM account WHERE wallet_algo='"+account_richiedente+"' limit 1;")  #limit 1, non si sa mai...
    passphrase = cur.fetchall()[0][0]

    myConnection.close()#chiudo la connessione con il db

    private_key_utente = mnemonic.to_private_key(passphrase)
    print("private_key_utente ",private_key_utente)

    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True

    account_info = algod_client.account_info(account_richiedente)
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1    
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            break

    if not holding:

        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=account_richiedente,
            sp=params,
            receiver=account_richiedente,
            amt=0,
            index=int(asset_id))
       
        stxn = txn.sign(private_key_utente)
        txid = algod_client.send_transaction(stxn)

        
       





def home(request):
    return render(request,'home.html')
    

def search_account(request):
    searched_wallet = request.GET.get('search_wallet', '')
    hostname = '192.168.1.67'
    username = 'postgres'
    password = 'organization_db_password'
    database = 'generic_organization_db'
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = myConnection.cursor() #apro la connessione
    if(searched_wallet==""):
        cur.execute("SELECT codice_fiscale FROM account;")  
        codice_fiscale_recuperato = cur.fetchall()
        cur.execute("SELECT wallet_algo FROM account;")  
        wallet_recuperato = cur.fetchall()
    else:
        cur.execute("SELECT codice_fiscale FROM account WHERE wallet_algo='"+searched_wallet+"';")  
        codice_fiscale_recuperato = cur.fetchall()
        cur.execute("SELECT wallet_algo FROM account WHERE wallet_algo='"+searched_wallet+"';")  
        wallet_recuperato = cur.fetchall()

        myConnection.close()#chiudo la connessione con il db

    return render(request,'search_account.html',{"codice_fiscale":codice_fiscale_recuperato,"wallet_utente":wallet_recuperato})
    


def richiesta_token(request):
    get_asset_it_fromURL = request.GET.get('asset_id', '')
    wallet_id = request.GET.get('wallet_id', '')
    tipoRichiesta = request.GET.get('optin', '')
    requid = request.GET.get('requid', '')
    link_algo_explorer = "https://testnet.algoexplorer.io/address/"+wallet_id
    if(tipoRichiesta == "True"): #in questo caso la richiesta richiede di fare un optin
        optin(request, algod_client, get_asset_it_fromURL, wallet_id)
        conferma_risultato = "True"
    else: #in questo caso l'utente richiede di inviare al wallet Dizme un determinato token
        amountToken2 = check_holdings(algod_client, get_asset_it_fromURL , wallet_id)
        print("Possiedi questo quantitativo di token: ",amountToken2)
        token_splittati_nft = amountToken2.split(" - ")
        if(int(token_splittati_nft[0]) >= 1): #se ci sono due token, posso inviarli al waller
            print("====================================================================================")
            print(" ==================== PREPARO L'INVIO DELLE CREDENZIALI (TOKEN) ====================") 
            hostname = '192.168.1.67'
            username = 'postgres'
            password = 'organization_db_password'
            database = 'generic_organization_db'
            myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

            cur = myConnection.cursor() #apro la connessione
            cur.execute("SELECT user_connection_id FROM generic_organization_service_request WHERE request_uid='"+requid+"' limit 1;")  #limit 1, non si sa mai...
            id_small = cur.fetchall()
            id_small = str(id_small).replace(',', '')
            id_small = str(id_small).replace(')', '')
            id_small = str(id_small).replace('(', '')
            id_small = str(id_small).replace('[', '')
            id_small = str(id_small).replace(']', '')
            cur.execute("SELECT connection_id FROM generic_organization_service_userconnection WHERE id='"+str(id_small)+"' limit 1;")  #limit 1, non si sa mai...
            user_connection_id = cur.fetchall()

            user_connection_id = str(user_connection_id).replace(',', '')
            user_connection_id = str(user_connection_id).replace(')', '')
            user_connection_id = str(user_connection_id).replace('(', '')
            user_connection_id = str(user_connection_id).replace("'", "")


            print("trovato ",user_connection_id)

            myConnection.close()#chiudo la connessione con il db


            conn = http.client.HTTPSConnection("demo-agent-cl.dizme.io")

            #payload = "{\"request_uid\":\"\",\"connection_id\":\"f54e8952-0203-4147-a631-7c83894690a6\",\"credential_def_id\":\"JNNb5EMJpPhubxRJ8RtHDK:3:CL:201960:Token Vaccinazione\",\"credential_values\":[{\"name\":\"data\",\"mime_type\":\"string\",\"value\":\"prova\"},{\"name\":\"transactionID\",\"mime_type\":\"string\",\"value\":'{get_asset_it_fromURL}'}],\"comment\":\"Hai ricevuto il token da te richiesto.\"}"
            #payload = "{\"request_uid\":\"\",\"connection_id\":\"f54e8952-0203-4147-a631-7c83894690a6\",\"credential_def_id\":\"JNNb5EMJpPhubxRJ8RtHDK:3:CL:201960:Token Vaccinazione\",\"credential_values\":[{\"name\":\"data\",\"mime_type\":\"string\",\"value\":\"prova\"},{\"name\":\"transactionID\",\"mime_type\":\"string\",\"value\":\"id_di_prova_01\"}],\"comment\":\"Hai ricevuto il token da te richiesto.\"}"
            print(str(user_connection_id))
            user_connection_id = str(user_connection_id).replace('[', '')
            user_connection_id = str(user_connection_id).replace(']', '')
            today = date.today()
            #print("Today's date:", today)       
            payload = {
                        #"request_uid": "",
                        "connection_id": user_connection_id,
                        "credential_def_id": token_issue_credential,
                        "credential_values": [
                            {
                            "name": "data",
                            "mime_type": "text/plain",
                            "value": str(today)
                            },
                            {
                            "name": "transactionID",
                            "mime_type": "text/plain",
                            "value": link_algo_explorer
                            }

                        ],
                        "comment": "Hai ricevuto il token da te richiesto. Copia ed incolla il link ricevuto per verificare il tuo wallet."
                        }

            payload_json = json.dumps(payload)

            headers = {
                'accept': "application/json",
                'x-auth-token': "JESjtNprnHMKrbtKkCakrrfodKTGZQrn",
                'x-dizme-agent-id': "Your Company",
                'content-type': "application/json"
                }

            conn.request("POST", "/api/v1/credential/offer", payload_json, headers)

            res = conn.getresponse()
            data = res.read()

            print(data.decode("utf-8"))
            conferma_risultato = "True"
        else:
            conferma_risultato = "False"
    return render(request, 'richiesta_token.html',{"result_richiesta": conferma_risultato})