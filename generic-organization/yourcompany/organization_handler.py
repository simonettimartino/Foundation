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


import psycopg2
from config import config


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
            mail = request_data['revealed_attributes']['email']
            #inserimento mail nella tabella
            
            sql = "INSERT INTO account(mail) VALUES(%s) RETURNING mail_gen;"
            conn = None
            vendor_id = None
            try:
                # read database configuration
                params = config()
                # connect to the PostgreSQL database
                conn = psycopg2.connect(**params)
                # create a new cursor
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (mail,))
                # get the generated id back
                mail_gen = cur.fetchone()[0]
                # commit the changes to the database
                conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

            return mail_gen



           
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

