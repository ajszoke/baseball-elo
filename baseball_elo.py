'''
###############################################################################
#                                                                             #
#                            Baseball Elo Tracker                             #
#                                                                             #
#   /u/LiveBeef's Baseball Elo tracker: track a baseball league's teams'      #
#   Elo ratings.                                                              #
#                                                                             #
#   Copyright (C) 2015 Andrew Szoke <ajszoke@ncsu.edu>                        #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU General Public License as published by      #
#   the Free Software Foundation, either version 3 of the License, or         #
#   (at your option) any later version.                                       #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU General Public License for more details.                              #
#                                                                             #
#   You should have received a copy of the GNU General Public License         #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################
'''

import sys
import collections
import textwrap

EloList = open('EloList.txt', 'r+')
ratings = eval(EloList.read())

# Initialize team list
teams = ["ARI","ATL","BAL","BOS","CHC","CWS","CIN","CLE","COL","DET",
"HOU","KC","LAA","LAD","MIA","MIL","MIN","NYM","NYY","OAK",
"PHI","PIT","SD","SEA","SF","STL","TB","TEX","TOR","WSH"]

# TODO implement commands
def main():
    ok=input("""\
Baseball Elo Tracker  Copyright (C) 2015  Andrew Szoke

This program comes with ABSOLUTELY NO WARRANTY; for details type 'show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type 'show c' for details.

Press 'enter' to accept these terms and continue or type EXIT and press
enter to exit the program. """).upper()
    if ok=="EXIT":
        sys.exit()
    mainOpt()

# Process to manually enter an Elo-affecting game.
def gameIn(k=4, hadv=25, again=0, at="None", ht="None",
           last_at="None", last_ht="None", undo=0):
    if again == 0:
        print(textwrap.fill("\nGames must be entered chronologically; do not\
 enter games out of order. Input 'X' to return to the main menu. Input 'UNDO'\
 to undo the last entered game."))
    while at.upper() not in teams:
        at = input("Enter away team abbreviation: ").upper()
        if   at == "X": mainOpt()
        elif at == "UNDO":
            if undo == 1:
                print(textwrap.fill("Error: only the last game entered may be\
 automatically undone. Return to the main menu and manually adjust teams'\
 ratings to undo previous games."))
                gameIn(again=1, undo=1)
            try:
                print("\n")
                reportEloChange(last_at, ratings[last_at][-1],
                                ratings[last_at][-2])
                reportEloChange(last_ht, ratings[last_ht][-1],
                                ratings[last_ht][-2])
                print("\n")

                ratings[last_at].pop()
                ratings[last_ht].pop()
            except KeyError:
                print(textwrap.fill("Error: No game to undo. Game history is\
 erased after returning to the main menu."))
                gameIn(again=1, undo=1)
        elif at not in teams:
            print("Team selection invalid, try again")
    while True:
        try:
            atr = int(input("                        Runs: "))
        except ValueError:
            print('Error: improper score.')
            continue
        break
    while ht not in teams:
        ht = input("Enter home team abbreviation: ").upper()
        if   ht == "X": mainOpt()
        elif ht == "UNDO":
            try:
                print("")
                reportEloChange(last_at, ratings[last_at][-1],
                                ratings[last_at][-2])
                reportEloChange(last_ht, ratings[last_ht][-1],
                                ratings[last_ht][-2])
                print("")

                ratings[last_at].pop()
                ratings[last_ht].pop()
            except KeyError:
                print(textwrap.fill("Error: No game to undo. Game history is\
 erased after returning to the main menu."))
                gameIn(again=1)
        if ht not in teams:
            print("Team selection invalid, try again")
        elif at == ht:
            print("Home team and away team cannot be the same;\
 cancelling entry")
            gameIn(k=k, again=1)
    while True:
        try:
            htr = int(input("                        Runs: "))
        except ValueError:
            print('Error: improper score.')
            continue
        break

    chgElo(ht, at, htr, atr, k, hadv)

    htelo_old = ratings[ht][-2]
    atelo_old = ratings[at][-2]
    htelo_new = ratings[ht][-1]
    atelo_new = ratings[at][-1]

    print("\n")
    reportEloChange(at, atelo_old, atelo_new)
    reportEloChange(ht, htelo_old, htelo_new)
    print("\n")

    gameIn(again=1, last_at=at, last_ht=ht, undo=0)

# Automated subroutine that adjusts two teams' Elo rating based on a game
# played between the two. Automatically writes to the Elo list.
def chgElo(ht, at, htr, atr, k=4, hadv=25):
    htelo_old = ratings[ht][-1]
    atelo_old = ratings[at][-1]

    if htr > atr:
        W = 1
    else:
        W = 0

    movI = abs(atr-htr)**(1/3)
    htelochg = k * movI * (W - expRes(htelo_old, atelo_old, hadv))
    W = 1 - W
    atelochg = k * movI * (W - (1-expRes(htelo_old, atelo_old, hadv)))

    htelo_new = htelo_old + htelochg
    atelo_new = atelo_old + atelochg

    ratings[ht].append(round(htelo_new, 6))
    ratings[at].append(round(atelo_new, 6))

    EloList.seek(0)
    EloList.write(str(ratings))
    EloList.truncate()

# Returns, as a decimal between 0 and 1, a team's expected probability of
# winning against another team or defined Elo value (1500 for an average team
# or "against the field"
def expRes(ht, at, hadv=0):
    return 1/(10**(-(ht + hadv - at)/400) + 1)

# Interactive subroutine that provides current Elo information for all teams or
# current Elo information and season max/min for user-specified teams.
def lookup():
    print(textwrap.fill("Enter team abbreviation, or enter 'ALL' to print all \
ELO ratings, or enter 'x' to return to the main menu:"), end="")
    team = input(" ").upper()
    if   team == "X": mainOpt()
    elif team == "ALL":
        while True:
            sort = input('Sort by name or rating? ').lower()
            if sort in ('n', 'na', 'nam', 'name'):
                for team in teams:
                    print(team.ljust(3), "{0:4.2f}".format(ratings[team][-1]))
                lookup()
            elif sort in ('r', 'ra', 'rat', 'rating', 'rate'):
                sortRates = sorted(ratings.items(),
                                   key=lambda team: team[-1][-1], reverse=True)
                for x in range(0, len(teams)):
                    print(sortRates[x][0].ljust(3),
                    "{0:4.2f}".format(sortRates[x][1][-1]))
                lookup()
            else:
                print('Error: invalid sort type. Type "name" or "rating".')
    elif team not in ratings:
        print("ERROR: Invalid team selection. Try again.")
        lookup()
    print('\n     ', team.ljust(3), 'ELO: {0:4.2f}'.format(ratings[team][-1]))
    print('          Max:', round(max(ratings[team]), 2),
          '(game ', teamMaxElo(team), ')')
    print('          Min:', round(min(ratings[team]), 2),
          '(game ', teamMinElo(team), ')\n')
    ed = input("Edit ELO rating? (y/n): ").lower()
    if ed in ('y', 'ye', 'yes'):
        old = ratings[team][-1]
        while True:
            try:
                print('New ELO rating for', team, ': ', end="")
                new = float(input())
            except ValueError:
                print('Error: improper rating.')
                continue
            break
        ratings[team][-1] = new
        print("")
        reportEloChange(team, old, new)
        print("")

    again = input("Look up/edit more teams? (y/n): ").lower()
    if again in ('y', 'ye', 'yes'): lookup()
    else: mainOpt()

# Provides win probabilities for any user-specified matchup at teams at their
# current skill levels. Returns percentage and American odds.
def prob():
    n = input("Neutral location? (y/n): ").lower()
    if n in ('y', 'ye', 'yes'): hadv = 0
    else: hadv = 25
    print("Enter 'AVG' to compare a team against a straw team with a 1500\
 rating")
    t1     = input("Enter team 1/home team abbreviation: ").upper()
    if t1 == "AVG":
        t1rate = 1500
    else:
        while True:
            gameKey1 = input(textwrap.fill("Enter 'C' to use the team's current\
 rating, 'B' to use their best rating this year, 'W' to use their worst\
 rating this year, or a number to use the team's rating after that game this\
 season. ")).upper()
            if   gameKey1 == "C":
                t1rate   = ratings[t1][-1]
                gameNum1 = len(ratings[t1]) - 1
            elif gameKey1 == "B":
                t1rate   = max(ratings[t1])
                gameNum1 = teamMaxElo(t1)
            elif gameKey1 == "W":
                t1rate   = min(ratings[t1])
                gameNum1 = teamMinElo(t1)
            elif gameKey1 + 1 < len(ratings[t1]):
                t1rate   = ratings[t1][gameKey1]
                gameNum1 = gameKey1
            else:
                print("Invalid entry; try again")
                continue
            break
    t2 = input("Enter team 2/away team abbreviation: ").upper()
    if t2 == "AVG":
        t2rate = 1500
    else:
        while True:
            gameKey2 = input(textwrap.fill("Enter 'C' to use the team's current\
 rating, 'B' to use their best rating this year, 'W' to use their worst\
 rating this year, or a number to use the team's rating after that game this\
 season.")).upper()
            if   gameKey2 == "C":
                t2rate   = ratings[t2][-1]
                gameNum2 = len(ratings[t2]) - 1
            elif gameKey2 == "B":
                t2rate   = max(ratings[t2])
                gameNum2 = teamMaxElo(t2)
            elif gameKey2 == "W":
                t2rate   = min(ratings[t2])
                gameNum2 = teamMinElo(t2)
            elif gameKey2 + 1 < len(ratings[t2]):
                t2rate   = ratings[t2][gameKey2]
            else:
                print("Invalid entry; try again")
                continue
            break
    t1prob = expRes(t1rate, t2rate, hadv)
    print('\n     ', t1.ljust(3), '( game', gameNum1,  ') win probability: ',
          round(100*t1prob, 2), '% (', probToAmOdds(t1prob), ')')
    print('     ', t2.ljust(3), '( game', gameNum2,  ') win probability: ',
          round(100*(1-t1prob), 2), '% (', probToAmOdds(1-t1prob), ')')
    again = input("Calculate more odds? (y/n): ").lower()
    if again in ('y', 'ye', 'yes'): prob()
    else: mainOpt()

# Given a team abbreviation, returns a string used in Reddit markdown to show
# the team's flair logo
def flairify(abr):
    if   abr == "ARI": return "[](/r/azdiamondbacks)"
    elif abr == "ATL": return "[](/r/Braves)"
    elif abr == "BAL": return "[](/r/Orioles)"
    elif abr == "BOS": return "[](/r/RedSox)"
    elif abr == "CHC": return "[](/r/Cubs)"
    elif abr == "CWS": return "[](/r/WhiteSox)"
    elif abr == "CIN": return "[](/r/Reds)"
    elif abr == "CLE": return "[](/r/WahoosTipi)"
    elif abr == "COL": return "[](/r/ColoradoRockies)"
    elif abr == "DET": return "[](/r/MotorCityKitties)"
    elif abr == "HOU": return "[](/r/Astros)"
    elif abr == "KC":  return "[](/r/KCRoyals)"
    elif abr == "LAA": return "[](/r/AngelsBaseball)"
    elif abr == "LAD": return "[](/r/Dodgers)"
    elif abr == "MIA": return "[](/r/letsgofish)"
    elif abr == "MIL": return "[](/r/Brewers)"
    elif abr == "MIN": return "[](/r/MinnesotaTwins)"
    elif abr == "NYM": return "[](/r/NewYorkMets)"
    elif abr == "NYY": return "[](/r/NYYankees)"
    elif abr == "OAK": return "[](/r/oaklandathletics)"
    elif abr == "PHI": return "[](/r/Phillies)"
    elif abr == "PIT": return "[](/r/Buccos)"
    elif abr == "SD":  return "[](/r/Padres)"
    elif abr == "SEA": return "[](/r/Mariners)"
    elif abr == "SF":  return "[](/r/SFGiants)"
    elif abr == "STL": return "[](/r/Cardinals)"
    elif abr == "TB":  return "[](/r/TampaBayRays)"
    elif abr == "TEX": return "[](/r/TexasRangers)"
    elif abr == "TOR": return "[](/r/TorontoBlueJays)"
    elif abr == "WSH": return "[](/r/Nationals)"

# Offseason options
def offOpt():
    goto = input("""\
Postseason/offseason menu:
    1. Normalize team ELO ratings
    2. Input postseason game
    3. Return to main menu
Enter a selection: """)
    goto = int(goto)
    print("")
    if goto == 1:
        sure = input(textwrap.fill("This option will OVERWRITE all saved games\
 for the season and initalize every team with a preseason rating halfway\
 between their current one and 1500. Are you sure this is what you want?\
 (y/n): ")).lower()
        if sure in ('y', 'ye', 'yes'): returnHalfwayToMean()
        else: offOpt()
    elif goto == 2: gameIn(k=6)
    elif goto == 3: mainOpt()
    else:
        print("SELECTION INVALID")
        offOpt()

# Clears every team's season history, replacing it with a single preseason
# rating halfway between their current rating and an average (1500) one.
def returnHalfwayToMean():
    print("")
    for team in teams:
        oldLast = ratings[team][-1]
        newFirst = (oldLast + 1500)/2
        ratings[team].clear()
        ratings[team].append(newFirst)
        reportEloChange(team, oldLast, newFirst)
    print("\nDone.")
    offOpt()

def progOpts():
    rectyn = input("Check score integrity? (y/n): ").lower()
    if rectyn in ('y', 'ye', 'yes'):
        sums = 0
        for team in teams:
            sums += ratings[team][-1]
        sums /= 30
        if (sums > 1499.99 and sums < 1500.01): print("Score integrity OK")
        else: print("Error: score average outside acceptable bounds")
    mainOpt()

# Aesthetic subroutine that takes a number and returns a "+" if positive, "–"
# if negative, or "±" if 0.
def plusOrMinus(num):
    if   (num > 0): return "+"
    elif (num < 0): return "–"
    else:           return "±"

# Subroutine which prints to the console a table in Markdown syntax a sorted
# ranking of teams' ratings, along with other stats for each team such as
# change since last rating, W-L info, etc.
# TODO best/worst points in season, Find the top 20 most: lopsided, evenly
# matched, strongest match.
# TODO fix DOS encoding issues
def report():
    lastReddit = open('lastReddit.txt', 'r+')
    oldSort    = eval(lastReddit.read())
    newSort    = sorted(ratings.items(),
                        key=lambda team: team[-1][-1], reverse=True)
    newReddit  = {}
    print("Rank | Team | Rating | Change | Instantaneous W-L\* | Expected W-L\
\**\n:---:|:---:|:---:|:---:|:---:|:---:")
    for x in range(0, len(teams)):
        team       = newSort[x][0]
        oldRank    = oldSort[team][0]
        newRank    = x+1
        absRankChg = abs(newRank-oldRank)
        oldElo     = oldSort[team][1]
        newElo     = ratings[team][-1]

        if   (newRank < oldRank): rankChg = "▲" + str(absRankChg)
        elif (newRank > oldRank): rankChg = "▼" + str(absRankChg)
        else:                     rankChg = "―"
        print("{0:2d} | {1} {2} | {3:4.2f} | "
              .format(x+1, flairify(team), team, newSort[x][1][-1]), end="")
        try:
            print(rankChg, end="")
        except UnicodeEncodeError:
            if(newRank < oldRank):
                print(" &uarr;" + str(absRankChg))
            elif(newRank > oldRank):
                print(" &uarr;" + str(absRankChg))
            else:
                print("-")
        print(" ({0}{1:1.2f}) |"
            .format(str(plusOrMinus(newElo-oldElo)),
                    abs(newElo-oldElo)), end=" ")
        teamRec = seasonWins(team)
        print("%(curW)s–%(curL)s | %(expW)s–%(expL)s" %
            {'curW': int(teamRec.curW), 'curL': int(teamRec.curL),
             'expW': int(teamRec.expW), 'expL': int(teamRec.expL)})
        newReddit[team] = [x+1, newElo]
    print("^\*How ^well ^a ^team ^is ^*currently* ^playing; ^that ^is, ^their\
 ^expected ^2015 ^record ^if ^the ^season ^started ^today")
    print("\n^\**Team's ^expected ^2015 ^record ^given ^their ^current ^record\
 ^and ^Elo ^rating")
    save = input("Save report as official? (y/n) ").lower()
    if save in ('y', 'ye', 'yes'):
        lastReddit.seek(0)
        lastReddit.write(str(newReddit))
        lastReddit.truncate()
        print("Report stored.")
    mainOpt()

# TODO? run a report for each region with combined Elo, rank, etc
def regionReport():
    pass

# TODO Attempts to resolve team-does-not-exist errors elsewhere in the program.
def badName(bad):
    pass

# Accepts a pre-sanitized team abbreviation and returns the number of wins that
# team has had over the season. Losses are calculated elsewhere by subtracting
# this number by the total number of games that team has played.
def countTeamWins(team):
    wins  = 0
    games = len(ratings[team])-1
    if games == 0: return 0
    for game in range(1,games):
        if ratings[team][game] > ratings[team][game - 1]: wins += 1
    return wins

# Accepts a team abbreviation and returns the game resulting in the team's
# highest Elo rating of the season.
def teamMaxElo(team):
    maxElo = max(ratings[team])
    if ratings[team].count(maxElo) > 1: return "multiple"
    else: return ratings[team].index(maxElo)

# Accepts a team abbreviation and returns the game resulting in the team's
# lowest Elo rating of the season.
def teamMinElo(team):
    minElo = min(ratings[team])
    if ratings[team].count(minElo) > 1: return "multiple"
    else: return ratings[team].index(minElo)

# Automated function that takes a pre-screened team abbreviation and returns a
# named tuple containing an extrapolated W-L record based on their current
# rating (that is, their expected record if the season started today) and their
# expected W-L record given their current rating and existing record.
def seasonWins(team):
    EloBaseWins   = 162*expRes(ratings[team][-1], 1500)
    EloBaseLosses = 162 - EloBaseWins
    curWins       = countTeamWins(team)
    expWins       = curWins +\
                   (162 - len(ratings[team])+1)*expRes(ratings[team][-1], 1500)
    expLosses     = 162 - expWins

    expRec        = collections.namedtuple('expRec', 'curW, curL, expW, expL')
    teamRec       = expRec(round(EloBaseWins), round(EloBaseLosses),
                           round(expWins), round(expLosses))
    return teamRec

# Accepts decimal odds of a team winning and prints a "moneyline", or American,
# representation of those odds
def probToAmOdds(dec):
    dec=100*dec
    if(dec>=50):
        line = -100*(dec/(100-dec))
        AmOdds = round(line,2)
    else:
        line = 100*(100-dec)/dec
        AmOdds = round(line,2)
    sign = plusOrMinus(AmOdds)
    return sign + str(abs(round(AmOdds)))

def mainOpt(goto=0):
    if(goto==0): goto = input("""\

Main menu:
    1. Enter regular season game results
    2. View/edit team ratings and season records
    3. Look up matchup win probability
    4. Calculate season record statistics and win-loss expectancy
    5. Run report
    6. Postseason/offseason options
    7. Program options
    8. Close the program
Enter a selection: """)
    goto = int(goto)
    print()
    if   goto == 1: gameIn()
    elif goto == 2: lookup()
    elif goto == 3: prob()
    elif goto == 4:
        team = input("Enter team abbreviation, or enter 'X'\
 to return to the main menu: ").upper()
        if team == "X": mainOpt()
        elif team not in teams:
            print("Team invalid")
            mainOpt(goto=4)
        else:
            teamRec = seasonWins(team)
            print("\n    ", team, "is CURRENTLY playing like a team with a(n)",
                  teamRec.curW, "-", teamRec.curL, "record")
            print("     and is EXPECTED to finish the season with a(n)",
                  teamRec.expW, "-", teamRec.expL, "record")
            mainOpt(goto=4)
    elif goto == 5: report()
    elif goto == 6: offOpt()
    elif goto == 7: progOpts()
    elif goto == 8:
        EloList.close()
        sys.exit()
    else:
        print("SELECTION INVALID")
        mainOpt()

def reportEloChange(team, old, new):
    print("     ", team.ljust(3),
          " ELO {0:4.2f}  ->  {1:4.2f}".format(old, new))

while(True):
    main()
