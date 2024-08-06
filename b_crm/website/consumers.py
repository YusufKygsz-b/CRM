import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info('WebSocket connection established')
        await self.channel_layer.group_add(
            'notifications',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        logger.info('WebSocket connection closed')
        await self.channel_layer.group_discard(
            'notifications',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        verb = data.get('verb', None)
        logger.info(f'Received verb: {verb}')
        if verb is None:
            logger.error('Verb key is missing in received data')
            return
        await self.channel_layer.group_send(
            'notifications',
            {
                'type': 'send_notification',
                'verb': verb
            }
        )

    async def send_notification(self, event):
        verb = event.get('verb', None)
        logger.info(f'Sending verb: {verb}')
        if verb is None:
            logger.error('Verb key is missing in event data')
            return
        await self.send(text_data=json.dumps({
            'verb': verb
        }))
