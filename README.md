# Natural Language Processing Independent Work

This is a semester-long project that focuses on analyzing women's role in films over time using NLP and topic-modelling algorithms. The data used in this project comes from the [Cornell Movie-Dialogs Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html).

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

This stage of my project reads through the cleaned up data and sorts the movie lines by character's gender and year movie was released. All female lines are written to the `fem` folder and male lines are written to the `male` folder, each in files titled by year (.e.g `1975.txt`).

The program prints the number of characters of each gender (male, female, unknown) and the number of lines and words spoken by each.

All data is written to `2_parsed_data`.

## 
