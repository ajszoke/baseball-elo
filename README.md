# Baseball-Elo
/u/Livebeef's baseball team Elo tracker

 This program is designed to keep track of [Elo ratings](http://en.wikipedia.org/wiki/Elo_rating_system) of teams within a normal-rules baseball league. Elo ratings are designed to reduce all information about a team's matchups into a single number: 1500 is average, lower is worse, higher is stronger.
 
 Nate Silver's (FiveThirtyEight blog) methodology for Elo adjustments is copied exactly in this program. [This](http://fivethirtyeight.com/datalab/introducing-nfl-elo-ratings/) is his explanation of the Elo rating system in general in the context of American football, and [this](http://www.baseballprospectus.com/article.php?articleid=5247) is his exact methodology for application to baseball. This program's functionality follows his methodology exactly with the exception of the handling of the offseason (below).
 
 From the Elo rating we can pull a good amount of useful information: we can see how many games a team with a given Elo rating could expect to win against another team (with probabilities), we can easily stack and order teams by their ratings to derive a numerically-produced ranking, and we can compare teams across eras by comparing their Elo ratings to determine who would be objectively "better" in their own era. Support for the first of these possibilities is provided in the program.
 
 The program is currently designed for the MLB for the purpose of producing biweekly-ish reports in /r/baseball. The program needs to be included with some EloList.txt dict within the same directory which contains team abbreviations as keys and an array of their Elo values throughout the season as each value. These arrays must be manually initialized with some starting Elo value. For the MLB, I use the average projected record for each team previded by PECOTA and BaseRuns to back-generate a starting Elo rating for each team. This back-generation is done mathematically and separate from the program using the formula:

> 1/(10**(-x/400) + 1) = W/G
 
 where x is the rating to be solved for, W is the team's projected wins, and G is the season length in games. A method for postseason rating adjustment is provided within "Postseason options" within the program where, during the offseason after a season, all teams' ratings are returned halfway to 1500. This is not preferred to options based on preseason projections but may be the only option available in some smaller leagues.
 
 This program is adaptable for leagues other than the MLB. To adapt the program, replace each team abbreviation in the `teams` array at the top with an appropriate abbreviation for each team in your league. Then create an EloList.txt file whose contents are simply a dict with each team's abbreviation as the keys and a 1-item array containing their starting Elo rating as the keys' values.
 
 This program is released under the GNU Public License v3. More information may be found within the license.txt file within this repository.
