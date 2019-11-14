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
        genres = ', '.join(self._genres)

        # format character names
        characters = []
        for char in self._characters:
            characters.append(char.name())
        names = ', '.join(characters)

        return '%.3d\t%s\t%d\t%.1f\t%7.d\t%s\n\t%s' % \
            (self._id, title, self._year, self._rating, self._votes, genres, names)

    def title(self):
        return self._title

    def year(self):
        return self._year

    def add_character(self, character):
        self._characters.append(character)

    def characters(self):
        return self._characters

#-------------------------------------------------------------------------------

class Character(object):

    def __init__(self, id, name, movie, gender, pos):
        self._id = id
        self._name = name
        self._movie = movie
        self._gender = gender
        self._pos = pos
        self._lines = []
        self._word_count = 0

    def __str__(self):
        # format name and movies
        name = self._name.ljust(35)
        movie = self._movie.title().ljust(70)

        return '%.4d\t%s\t%s\t%s\t%d' % \
            (self._id, name, movie, self._gender, self._pos)

    def name(self):
        return self._name

    def gender(self):
        return self._gender

    def is_fem(self):
        return self._gender == 'f'

    def is_male(self):
        return self._gender == 'm'

    def is_unknown(self):
        return self._gender == '?'

    def add_line(self, line):
        self._lines.append(line)
        self._word_count += len(line.rsplit(' '))

    def line_count(self):
        return len(self._lines)

    def lines(self):
        return ' '.join(self._lines)

    def word_count(self):
        return self._word_count

    def print_lines(self):
        for line in self._lines:
            print('%s: %s' % (self._name, line))
