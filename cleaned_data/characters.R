characters1 <- read.table("1_movie_characters_metadata_clean.txt", sep = "\t")
characters2 <- read.table("2_movie_characters_metadata_gendered_title.txt", sep = "\t")

names(characters1) <- c("id", "name", "movie.id", "title", "gender", "position")
names(characters2) <- c("id", "name", "movie.id", "title", "gender", "position")

table(characters1$V5)
table(characters2$V5)

characters2$given.name <- findGivenNames(characters2$name)

#------------

movies <- read.table("1_movie_titles_metadata_clean.txt", sep = "\t")
names(movies) <- c("id", "title", "year", "rating", "votes", "genres")


frequency(movies$year)
