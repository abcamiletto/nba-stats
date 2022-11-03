# NBA Scraper Package

This package is used to scrape NBA data from [Basketball Reference](https://www.basketball-reference.com/).

# Use of code

Seasons, if represented by a single number, end in the explicited year (ex. 2020 --> 2019-20).

Files with information about a season are represented with the string yyyy-yy

All data is saved to the data/ directory, in the right subfolder. Subfolders are named in const.py.

### To Do List

- [x] Fix scraping functions
- [x] Refactor scraping functions
- [ ] Scrape also the info per game (not only per season)
- [ ] Create an Info dataclass to store results of seasson stats and per game stats
- [ ] Find a smart way to store draft info of a player