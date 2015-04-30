-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- players table
CREATE TABLE players (id serial, name text);

-- match_data table
CREATE TABLE match_data (id serial, player1 integer, player2 integer, winner integer);

