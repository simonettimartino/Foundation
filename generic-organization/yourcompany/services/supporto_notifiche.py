from generic_organization_service.handlers.organization_abstract_handler import OrganizationAbstractHandler
from antidote import world
from generic_organization_service.services.notification_service import NotificationService
from generic_organization_service.interfaces.responses.generic_response import VerifyResult
from generic_organization_service.services.verify_service import VerifyService
from generic_organization_service.entity import request_entity, user_entity
from generic_organization_service.utils.description_handler import DescriptionHandler, DescriptionMessagesCodes
from generic_organization_service.handlers.organization_handler_manager import OrganizationHandlerManager
from antidote import register, inject

@register(singleton=True)
class SupportoNotifiche:
    @inject
    def __init__(self, notification_service: NotificationService, description_handler: DescriptionHandler, handler_manager: OrganizationHandlerManager):
        self.notification_service = notification_service
        self.description_handler = description_handler
        self.handler_manager = handler_manager
    
    def handle_confirm_verify(self, request_uid: str, connection_id: str, presentation_id: str, request_data: dict()):
        user_connection = user_entity.get_user_connection(connection_id= connection_id)

        notification_service: NotificationService = world.get(NotificationService)
        descriptions = self.description_handler.get_descriptions(
                    DescriptionMessagesCodes.VERIFY_EXECUTED_SUCCESSFULLY)
        print("notification_service: ",notification_service)
        if (notification_service):
            print("------------ USER CONNECTION: ", user_connection)
            print("------------ CONNECTION ID: ",presentation_id)
            self.notification_service.send_verify_response(user_connection, presentation_id, descriptions, VerifyResult.OK)


