from django.apps import AppConfig


class MessagesConfig(AppConfig):
    name = 'messages'
    label = 'mymessages'  # <-- this is the important line - change it to anything other than the default,
    # which is the module name ('messages' in this case)
