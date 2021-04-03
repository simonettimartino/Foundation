from generic_organization_service.handlers.organization_abstract_handler import OrganizationAbstractHandler
from antidote import world
from generic_organization_service.services.notification_service import NotificationService
from generic_organization_service.interfaces.responses.generic_response import VerifyResult
from generic_organization_service.services.verify_service import VerifyService
from generic_organization_service.entity import request_entity, user_entity
from antidote import register, inject

@register(singleton=True)
class SupportoNotifiche:
    @inject
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service
    
    def handle_confirm_verify(self, request_uid: str, connection_id: str, presentation_id: str, request_data: dict()):
        user_connection = user_entity.get_user_connection(connection_id= connection_id)

        notification_service: NotificationService = world.get(NotificationService)
        print("aaaaaaaaaaaaaaa: ",notification_service)
        if (notification_service):
            print("------------ USER CONNECTION: ", user_connection)
            print("------------ CONNECTION ID: ",presentation_id)
            notification_service.send_verify_response(user_connection, presentation_id, "errore descrizione", VerifyResult.KO)


