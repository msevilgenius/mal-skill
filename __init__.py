from mycroft import MycroftSkill, intent_file_handler, intent_handler
from jikanpy import Jikan

USERNAME_SETTING_KEY = 'username'

class Mal(MycroftSkill):
    def __init__(self):
        super().__init__(self)

    def initialize(self):
        self.jikan = Jikan()
        self.mal_username = self.settings.get(USERNAME_SETTING_KEY)

    def on_settings_changed(self):
        self.mal_username = self.settings.get(USERNAME_SETTING_KEY, False)
    

    @intent_handler('next.episode.intent')
    def handle_next_episode_intent(self, message):

        if not self.mal_username:
            self.speak_dialog('username.not.set')
            return

        show = message.data.get('show')

        if show is not None:
            animelist_watching = self.jikan.user(username=self.mal_username, request='animelist', argument='watching')
            
            for anime in animelist_watching['anime']:
                self.log.debug(str.format("checking show id {}. title: '{}'", anime['mal_id'], anime['title']))
                if anime['title'].lower().startswith(show):
                    self.speak_dialog('next.episode', {'show': anime['title'], 'ep_next': anime['watched_episodes'] + 1, 'ep_total': anime['total_episodes']})
            
            self.speak_dialog('unknown.show', {'show': show})
        else:
            self.speak_dialog('show.entity.none')


    # @intent_handler()
    # def handle_plan_to_watch_intent(self, message):
    #     animelist_ptw = self.jikan.user(username=self.mal_username, request='animelist', argument='ptw')
    #     self.log.info('plan to watch intent')
    #     self.speak_dialog(message)

    # def converse(self, utterances, lang):
    #     if utterances and self.voc_match(utterances[0], 'understood'):
    #         self.speak_dialog('great')
    #         return True
    #     else:
    #         return False

    def stop(self):
        pass
    
    # def shutdown(self):
    #     self.cancel_scheduled_event('my_event')
    #     self.stop_my_subprocess()


def create_skill():
    return Mal()

