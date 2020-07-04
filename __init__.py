from mycroft import MycroftSkill, intent_file_handler, intent_handler
from jikanpy import Jikan


class Mal(MycroftSkill):
    def __init__(self):
        super().__init__(self)

    def initialize(self):
        self.jikan = Jikan()
        self.mal_username = self.settings.get('username')

    def on_settings_changed(self):
        self.mal_username = self.settings.get('username', False)
        # self.trigger_time_display(show_time)

    @intent_file_handler('mal.intent')
    def handle_mal(self, message):
        self.speak_dialog('mal')

    @intent_handler('next.episode.intent')
    def handle_next_episode_intent(self, message):
        self.log.info('next episode intent')

        if not self.mal_username:
            self.log.info('mal username not set')
            self.speak_dialog('I don\'t know your mal username')
            return

        show = message.data.get('show')
        if show is not None:
            animelist_watching = self.jikan.user(username=self.mal_username, request='animelist', argument='watching')
            reply = format("I couldn't find any info for {}", show)
            for anime in animelist_watching['anime']:
                if anime['title'].startswith(show):
                   reply =  format("The next episode is {} of {}", anime['watched_episodes'] + 1, anime['total_episodes'])
            self.speak_dialog(reply)
        else:
            self.speak_dialog('I didn\'t catch the name of the show')


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

