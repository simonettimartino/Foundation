from generic_organization_service.handlers.organization_abstract_handler import OrganizationAbstractHandler
from antidote import world
from generic_organization_service.services.notification_service import NotificationService
from generic_organization_service.interfaces.responses.generic_response import VerifyResult
from generic_organization_service.services.verify_service import VerifyService
from generic_organization_service.entity import request_entity, user_entity
from yourcompany.services.supporto_notifiche import SupportoNotifiche
from generic_organization_service.utils.description_handler import DescriptionHandler, DescriptionMessagesCodes
from generic_organization_service.handlers.organization_handler_manager import OrganizationHandlerManager
from antidote import inject
import logging
import pprint
import json
from generic_organization_service.views import generate_algorand_keypair



import psycopg2



logger = logging.getLogger(__name__)

# FIXME implement all methods


class OrganizationHandler(OrganizationAbstractHandler):



    def handle_confirm_verify(self, request_uid: str, connection_id: str, presentation_id, request_data: dict()):
        logger.info('------------------------------ Connessione effettuata ------------------------------ ')


        oggService: SupportoNotifiche = world.get(SupportoNotifiche)
    
        if(oggService): #se tutto va bene
            oggService.handle_confirm_verify(request_uid, connection_id, presentation_id, request_data)
            #inserisco la mail nel database
            #dati = json.load(request_data)
            print("=======================",request_data['revealed_attributes']['email'])
            mailInviata = request_data['revealed_attributes']['email']
            
           
            #inserimento mail nella tabella
            ''' 
            hostname = '192.168.1.67'
            username = 'postgres'
            password = 'organization_db_password'
            database = 'generic_organization_db'
            myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            
            #query
            cur = myConnection.cursor()
            
            cur.execute("SELECT count(*) FROM account WHERE mail='"+mailInviata+"';") 
            verifica = cur.fetchall()[0][0]
            print('verifica: ',verifica)
            if verifica == 0:
                #aggiungo un wallet se non esiste alcuna mail nel db
                #inserisco la mail nel database
                resultWalletGenerato = generate_algorand_keypair()
                splitaddrpiupass = resultWalletGenerato.split(" - ") #in 0 c'è il wallet generato
                #non gli diamo la passphrase
                cur.execute("INSERT INTO account(mail,algo_wallet) VALUES('"+mailInviata+"','"+splitaddrpiupass[0]+"');" )
                myConnection.commit()
            else: #seleziono i dati già presenti nel db
                cur.execute("SELECT * FROM account WHERE mail='"+mailInviata+"';")   
                datiUtente = cur.fetchall()
                print("dati utente ", datiUtente)

            myConnection.close()'''

           
    def handle_connection_notify(self, request_uid: str, connection_id: str, request_data: dict()):
        pass

    def handle_confirm_issue(self, request_uid: str, connection_id: str, request_data: dict()):
        pass
    def handle_discard_credential(self, request_uid: str, connection_id: str, request_data: dict()):
        pass

    def handle_discard_proof(self, request_uid: str, connection_id: str, request_data: dict()):
        pass

    def handle_values_for_credential(self, request_uid: str, connection_id: str, request_data: dict()) -> list:
        pass
    
    def handle_async_event(self, event_type: str, request_data: dict):
        pass

