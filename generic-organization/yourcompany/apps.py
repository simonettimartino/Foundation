import os
from django.apps import AppConfig
from antidote import world

from generic_organization_service.handlers.organization_handler_manager import OrganizationHandlerManager
from generic_organization.settings import LOGGING


class MyAppConfig(AppConfig):
    name = "yourcompany"

    def ready(self):
        # FIXME change the import with your organization folder --> fatto       
        from yourcompany.organization_handler import OrganizationHandler
        handler_manager = world.get(OrganizationHandlerManager)
        handler_manager.add_organization_handler("yourcompany", OrganizationHandler())

        logger_conf = {
            'handlers': ['console'],
            'level': os.getenv('SEVERITY_LOG_LEVEL', 'INFO'),
            'propagate': False,
        }
        LOGGING['loggers']['yourcompany'] = logger_conf
