from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter


class EncuentroRouter(BaseRouter):
    route_name = 'tacos'
    valid_verbs = ['subscribe']

    def get_subscription_channels(self, **kwargs):
        return ['notification']

route_handler.register(EncuentroRouter)
