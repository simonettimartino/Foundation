from generic_organization_service.handlers.organization_abstract_handler import OrganizationAbstractHandler
from antidote import world
from generic_organization_service.services.notification_service import NotificationService
from generic_organization_service.interfaces.responses.generic_response import VerifyResult
from generic_organization_service.services.verify_service import VerifyService
from generic_organization_service.entity import request_entity, user_entity

import logging

logger = logging.getLogger(__name__)

# FIXME implement all methods


class OrganizationHandler(OrganizationAbstractHandler):
    def handle_confirm_verify(self, request_uid: str, connection_id: str, presentation_id, request_data: dict()):
        logger.info('------------------------------ Connessione effettuata ------------------------------ ')
        ##chiamare metodo response (notificatio_service)
        #notificationService = NotificationService()
        #notificationService.send_verify_response(self, connection_id, presentation_id,VerifyResult.KO)
        #oggService: VerifyService = world.get(VerifyService)
        #if(oggService):
        #verify_request = request_entity.get_verify_request_by_request_uid(request_uid)
        #proof_service_action = verify_request.proof_service_action
        #if(proof_service_action.action.name == ActionName):

        notification_service = NotificationService()
        user_connection = user_entity.get_user_connection(connection_id= connection_id)
        notification_service.send_verify_response(user_connection, presentation_id, "errore descrizione", VerifyResult.KO)

        pass

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

