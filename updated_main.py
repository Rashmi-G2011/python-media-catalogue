from typing import List, Optional


class MediaError(Exception):
    """Custom exception for media-related errors."""

    def __init__(self, message: str, obj=None):
        super().__init__(message)
        self.obj = obj

    def __str__(self) -> str:
        return f"{self.args[0]}"


class Movie:
    """Represents a movie."""

    MIN_YEAR = 1895

    def __init__(
        self,
        title: str,
        year: int,
        director: str,
        duration: int
    ) -> None:

        self.title = self.validate_title(title)
        self.year = self.validate_year(year)
        self.director = self.validate_director(director)
        self.duration = self.validate_duration(duration)

    @staticmethod
    def validate_title(title: str) -> str:
        """Validate movie title."""

        title = title.strip()

        if not title:
            raise ValueError("Title cannot be empty.")

        return title

    @classmethod
    def validate_year(cls, year: int) -> int:
        """Validate release year."""

        if year < cls.MIN_YEAR:
            raise ValueError(
                f"Invalid year ({year}). Year must be {cls.MIN_YEAR} or later."
            )

        return year

    @staticmethod
    def validate_director(director: str) -> str:
        """Validate director name."""

        director = director.strip()

        if not director:
            raise ValueError("Director name cannot be empty.")

        return director

    @staticmethod
    def validate_duration(duration: int) -> int:
        """Validate movie duration."""

        if duration <= 0:
            raise ValueError(
                f"Invalid duration ({duration}). Duration must be greater than 0."
            )

        return duration

    def __str__(self) -> str:
        return (
            f"{self.title} ({self.year}) | "
            f"{self.duration} min | "
            f"Director: {self.director}"
        )


class TVSeries(Movie):
    """Represents a TV Series."""

    def __init__(
        self,
        title: str,
        year: int,
        director: str,
        duration: int,
        seasons: int,
        total_episodes: int
    ) -> None:

        super().__init__(title, year, director, duration)

        self.seasons = self.validate_seasons(seasons)
        self.total_episodes = self.validate_total_episodes(total_episodes)

    @staticmethod
    def validate_seasons(seasons: int) -> int:
        """Validate number of seasons."""

        if seasons < 1:
            raise ValueError(
                f"Invalid seasons ({seasons}). Must be at least 1."
            )

        return seasons

    @staticmethod
    def validate_total_episodes(total_episodes: int) -> int:
        """Validate total episodes."""

        if total_episodes < 1:
            raise ValueError(
                f"Invalid episode count ({total_episodes}). Must be at least 1."
            )

        return total_episodes

    def __str__(self) -> str:
        return (
            f"{self.title} ({self.year}) | "
            f"{self.seasons} Seasons | "
            f"{self.total_episodes} Episodes | "
            f"{self.duration} min/episode | "
            f"Director: {self.director}"
            )
class MediaCatalogue:
    """Stores and manages movies and TV series."""

    def __init__(self) -> None:
        self.items: List[Movie] = []

    def add(self, media_item: Movie) -> None:
        """Add a movie or TV series to the catalogue."""

        if not isinstance(media_item, Movie):
            raise MediaError(
                f"Cannot add object of type '{type(media_item).__name__}'. "
                "Only Movie or TVSeries objects are allowed.",
                media_item,
            )

        # Prevent duplicate titles
        if self.search(media_item.title) is not None:
            raise MediaError(
                f"'{media_item.title}' already exists in the catalogue.",
                media_item,
            )

        self.items.append(media_item)

    def search(self, title: str) -> Optional[Movie]:
        """Search for a media item by title."""

        title = title.strip().lower()

        for item in self.items:
            if item.title.lower() == title:
                return item

        return None

    def remove(self, title: str) -> bool:
        """Remove a media item by title."""

        media = self.search(title)

        if media is None:
            return False

        self.items.remove(media)
        return True

    def get_movies(self) -> List[Movie]:
        """Return only movies."""

        return [item for item in self.items if type(item) is Movie]

    def get_tv_series(self) -> List[TVSeries]:
        """Return only TV series."""

        return [item for item in self.items if isinstance(item, TVSeries)]

    def total_items(self) -> int:
        """Return total number of media items."""

        return len(self.items)

    def total_movies(self) -> int:
        """Return total number of movies."""

        return len(self.get_movies())

    def total_tv_series(self) -> int:
        """Return total number of TV series."""

        return len(self.get_tv_series())

    def display_statistics(self) -> None:
        """Display catalogue statistics."""

        print("\n===== Catalogue Statistics =====")
        print(f"Total Items     : {self.total_items()}")
        print(f"Movies          : {self.total_movies()}")
        print(f"TV Series       : {self.total_tv_series()}")

    def __str__(self) -> str:
        """Return a formatted catalogue."""

        if not self.items:
            return "Media Catalogue is empty."

        result = "\n========== MEDIA CATALOGUE ==========\n"

        movies = self.get_movies()
        series = self.get_tv_series()

        if movies:
            result += "\n----- MOVIES -----\n"
            for index, movie in enumerate(movies, start=1):
                result += f"{index}. {movie}\n"

        if series:
            result += "\n----- TV SERIES -----\n"
            for index, tv in enumerate(series, start=1):
                result += f"{index}. {tv}\n"

        return result
    def get_non_empty_string(prompt: str) -> str:
    """Get a non-empty string from the user."""

    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Input cannot be empty. Please try again.\n")


    def get_positive_integer(prompt: str) -> int:
        """Get a positive integer from the user."""

        while True:
            try:
                value = int(input(prompt))

                if value <= 0:
                    print("Please enter a positive integer.\n")
                    continue

                return value

            except ValueError:
                print("Invalid input. Please enter a valid integer.\n")


    def add_movie(catalogue: MediaCatalogue) -> None:
        """Add a movie."""

        try:
            print("\n----- Add Movie -----")

            title = get_non_empty_string("Title: ")
            year = get_positive_integer("Release Year: ")
            director = get_non_empty_string("Director: ")
            duration = get_positive_integer("Duration (minutes): ")

            movie = Movie(title, year, director, duration)
            catalogue.add(movie)

            print("\nMovie added successfully!")

        except (ValueError, MediaError) as error:
            print(f"\nError: {error}")


    def add_tv_series(catalogue: MediaCatalogue) -> None:
        """Add a TV series."""

        try:
            print("\n----- Add TV Series -----")

            title = get_non_empty_string("Title: ")
            year = get_positive_integer("Release Year: ")
            director = get_non_empty_string("Director: ")
            duration = get_positive_integer("Average Episode Duration (minutes): ")
            seasons = get_positive_integer("Number of Seasons: ")
            episodes = get_positive_integer("Total Episodes: ")

            series = TVSeries(
                title,
                year,
                director,
                duration,
                seasons,
                episodes
            )

            catalogue.add(series)

            print("\nTV Series added successfully!")

        except (ValueError, MediaError) as error:
            print(f"\nError: {error}")

    def search_media(catalogue: MediaCatalogue) -> None:
        """Search for a media item."""

        title = get_non_empty_string("\nEnter title to search: ")

        media = catalogue.search(title)

        if media:
            print("\nMedia Found:")
            print(media)
        else:
            print("\nNo media found with that title.")


    def remove_media(catalogue: MediaCatalogue) -> None:
        """Remove a media item."""

        title = get_non_empty_string("\nEnter title to remove: ")

        if catalogue.remove(title):
            print("\nMedia removed successfully!")
        else:
            print("\nMedia not found.")


    def display_menu() -> None:
        """Display the menu."""

        print("\n========== MEDIA CATALOGUE ==========")
        print("1. Add Movie")
        print("2. Add TV Series")
        print("3. Display Catalogue")
        print("4. Search Media")
        print("5. Remove Media")
        print("6. Display Statistics")
        print("7. Exit")


    def main() -> None:
        """Main program."""

        catalogue = MediaCatalogue()

        while True:
            display_menu()

            try:
                choice = int(input("\nEnter your choice: "))

                if choice == 1:
                    add_movie(catalogue)

                elif choice == 2:
                     add_tv_series(catalogue)

                elif choice == 3:
                     print(catalogue)

                elif choice == 4:
                    search_media(catalogue)

                elif choice == 5:
                    remove_media(catalogue)
 
                elif choice == 6:
                    catalogue.display_statistics()

                elif choice == 7:
                    print("\nThank you for using Media Catalogue!")
                    break

                else:
                    print("\nPlease choose a number between 1 and 7.")

            except ValueError:
                print("\nInvalid input. Please enter a valid menu option.")


if __name__ == "__main__":
    main()
