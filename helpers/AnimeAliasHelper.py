import re
from jikanpy import Jikan

class AnimeAliasHelper():
    def __init__(self):
        super().__init__(self)
        self.jikan = Jikan()
    
    def name_matches_anime(self, name, anime_id):
        anime = self.jikan.anime(anime_id) # could cache this locally?
        titles = [anime['title'], anime['title_english'], anime['title_japanese']]
        titles.append(anime['title_synonyms'])
        # strip punctuation and whitespace
        titles_norm = [re.sub(r'([^\w]|_)', '', t.lower()) for t in titles]
        name_norm = re.sub(r'([^\w]|_)', '', name.lower())
        
        return any(title.startswith(name_norm) for title in titles_norm)