# Natural Language Processing Independent Work

This is a semester-long project that focuses on analyzing women's role in films over time using NLP and topic-modelling algorithms. The data used in this project comes from the [Cornell Movie-Dialogs Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html). The project cultimated in a paper where the findings of the project were analyzed: [Evaluating Women’s Roles in Movies with Topic Modeling](https://drive.google.com/file/d/1dV3GBINZ4i8i2df-jmNQloxk-rXfFyuv/view?usp=sharing).

All programs can be found in the `scripts` folder.

## Cleaned Data

This stage of my project cleans up the data. I used data from `movie_characters_metadata.txt`, `movie_lines.txt`, and `movie_titles_metadata.txt`. I also further gender characters using gendered titles (e.g. "Ms.", "Mr.", "Sir", Father", "Mother", etc.) and the [Genderize.io](https://genderize.io/) API.

All data is written to `1_cleaned_data`.

#### `cleaner.py`

Command-line argument options: `characters` `movies` `titles`<br>
For `movie_characters_metadata.txt`, the program converts gender to lowercase and replaces position "0" with "?". For `movie_lines.txt`, it removes the original field separator ("+++$+++") and replaces it with tabs. For `movie_titles_metadata.txt`, it removes "/I" from the years and removes the quotes and brackets from the genres field.

#### `title_genderizer.py`

This program sorts characters by gender based on titles and other gendered words in their credited character names.
- Female: "female", "woman", "girl", "mrs.", "ms.", "miss", "wife", "mom", "mother", "sister"
- Male: "male", "man", "boy", "guy", "mr.", "husband", "dad", "father", "brother"

#### `genderize`

This program uses the Genderize.io API to sort the remaining ungendered characters based on their credited character names. It is set so that only results with a probability greater than 60% are accepted.

## Parsed Data

This stage of my project reads through the cleaned up data and sorts the movie lines into folders by character's gender and year the movie was released and into files by movie title.

All data is written to `2_parsed_data`.

#### `helper.py`

This program contains the function `clear_dir`, which creates the year directories in the `fem` and `male` folders or clears them of files if they already exist.

#### `parser.py`

This program reads in all the cleaned movies, characters, and lines data and sorts movie lines. All lines are sorted into folders by year and written to either the `fem` or `male` folders depending on the gender of the character who spoke the line. Each of the files in the gender/year folders are titled by movie title.

The program also prints to standard output the number of characters of each gender (male, female, unknown) and the number of lines and words spoken by each gender.

## Preprocessed Data

This stage of my project reads in all the data and preprocesses the text using [spaCy](https://spacy.io/).

## Evaluation

Used [topic-interpretabiity](https://github.com/jhlau/topic_interpretability) by [jhlau](https://github.com/jhlau) to analyze the consistency and interpretability of results from topic modelling.
