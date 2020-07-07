import re
import time
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from jikanpy import Jikan


USERNAME_SETTING_KEY = 'username'

class Mal(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.mal_username = self.settings.get(USERNAME_SETTING_KEY)
        self.jikan = CachedJikan(self.mal_username)
        self.alias_helper = AnimeAliasHelper(self.jikan)

    def on_settings_changed(self):
        self.mal_username = self.settings.get(USERNAME_SETTING_KEY, False)
    

    @intent_handler('next.episode.intent')
    def handle_next_episode_intent(self, message):

        if not self.mal_username:
            self.speak_dialog('username.not.set')
            return

        requested_anime = message.data.get('show')

        if requested_anime is not None:
            animelist_watching = self.jikan.animelist_watching()
            
            for anime in animelist_watching['anime']:
                self.log.debug(str.format("checking show id {}. title: '{}'", anime['mal_id'], anime['title']))
                if self.alias_helper.name_matches_anime(requested_anime, anime['mal_id']):
                    self.speak_dialog('next.episode', {'show': anime['title'], 'ep_next': anime['watched_episodes'] + 1, 'ep_total': anime['total_episodes']})
            
            self.speak_dialog('unknown.show', {'show': requested_anime})
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


class AnimeAliasHelper():
    def __init__(self, cached_jikan):
        self.jikan = cached_jikan
    
    def name_matches_anime(self, name, anime_id):
        anime = self.jikan.anime(anime_id)
        titles = [anime['title'], anime['title_english'], anime['title_japanese']]
        titles.extend(anime['title_synonyms'])
        # strip punctuation and whitespace
        titles_norm = [re.sub(r'([^\w]|_)', '', t.lower()) for t in titles]
        name_norm = re.sub(r'([^\w]|_)', '', name.lower())
        
        return any(title.startswith(name_norm) for title in titles_norm)

class CachedJikan():
    def __init__(self, username):
        self._jikan = Jikan()
        self._last_request_time = time.time()
        self._REQUEST_DELAY = 2
        self._mal_username = username
        self._animelist_watching = None
        self._animelist_watching_time = None
        self._animes = dict()

    def _request_wait_time(self):
        return max(0, (self._last_request_time +self._REQUEST_DELAY) - time.time())

    
    def _delay_request(self, request_func):
        time.sleep(self._request_wait_time())
        result = request_func()
        self._last_request_time = time.time()
        return result


    
    def animelist_watching(self):
        if self._animelist_watching is None or time.time() - self._animelist_watching_time > 5 * 60:
            def do_request():
                return self._jikan.user(username=self._mal_username, request='animelist', argument='watching')
            self._animelist_watching = self._delay_request(do_request)
        return self._animelist_watching


    def anime(self, anime_id):
        if anime_id not in self._animes:
            try:
                def do_request():
                    return self._jikan.anime(anime_id)
                anime = self._delay_request(do_request)
                self._animes[anime_id] = anime
            except:
                # todo: log line here
                return None
        return self._animes[anime_id]