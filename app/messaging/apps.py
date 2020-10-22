from django.apps import AppConfig


class MessagingConfig(AppConfig):
    name = 'messaging'
    
    def ready(self):
        import messaging.signals
        from actstream import registry
        registry.register(self.get_model('Message'))
        registry.register(self.get_model('Blacklist'))