class Movie(object):

    def __init__(self, id, title, year, rating, votes, genres):
        self._id = id
        self._title = title
        self._year = year
        self._rating = rating
        self._votes = votes
        self._genres = genres
        self._characters = []

    def __str__(self):
        # format title and genres
        title = self._title.ljust(70)
        genres = ", ".join(self._genres)

        # format character names
        characters = []
        for char in self._characters:
            characters.append(char.name())
        names = ", ".join(characters)

        return '%.3d\t%s\t%d\t%.1f\t%.7d\t%s\n\t%s' % \
            (self._id, title, self._year, self._rating, self._votes, genres, names)

    def title(self):
        return self._title

    def add_character(self, character):
        self._characters.append(character)
