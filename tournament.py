#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():

    # Delete all matches from table
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM match_data")
    db.commit()
    db.close()

def deletePlayers():

    # Delete all players from table
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE FROM players")
    db.commit()
    db.close()

def countPlayers():

    # Return the number of players in the players table
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM players")
    result = cur.fetchone()
    db.close()
    return result[0]

def registerPlayer(name):

    # Add provided player to the players table
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO players (name) VALUES (%s)", [name])
    db.commit()
    db.close()

def playerStandings():
        
    # Get list of players with their name, wins and total matches
    db = connect()
    cur = db.cursor()
    cur.execute("SELECT id, name, (SELECT COUNT(*) FROM match_data WHERE winner=players.id) as wins, (SELECT COUNT(*) FROM match_data WHERE player1=players.id OR player2=players.id) as matches FROM players ORDER BY wins DESC")
    player_standings = cur.fetchall()
    db.close()
    return player_standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    # Add match results to match_data table, indicating who played and who won
    db = connect()
    cur = db.cursor()
    cur.execute("INSERT INTO match_data (player1, player2, winner) VALUES(%s,%s,%s)", [winner, loser, winner])
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    pairing_data = []

    # Get players and their standings
    standings = playerStandings()

    # Spin through standings data
    for player_standing in standings:

        # Add player's id and name to pairing_data
        # - pairing_data will include up to two players (4 items in tuple)
        pairing_data.extend((player_standing[0], player_standing[1]))

        # Do we have enough data in the tuple (2 players, id and name for each)?  Add to main pairings list and reset temp pairings_data list
        if len(pairing_data) == 4:
            pairings.append(pairing_data)
            pairing_data = []

    return pairings
