from mycroft import MycroftSkill, intent_file_handler


class Mal(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('mal.intent')
    def handle_mal(self, message):
        self.speak_dialog('mal')


def create_skill():
    return Mal()

