-- Q1 Retrieve the list of countries that have won a world cup.
select distinct(Winner) from worldcup_history;

-- Q2 Retrieve the list of country names that have won a world cup and the number of  world cups each has won in descending order. 
select Winner, count(*) as cups  from worldcup_history
group by Winner
order by cups desc;

-- Q3 List the Capital of the countries in increasing order of country population for countries that have population more than 100 million.
select Capital from country
where population > 100 -- here 100 is 100 millions
order by population asc;

-- Q4 List the Name of the stadium which has hosted a match where the number of goals scored by a single team was greater   than 4. 
select distinct(stadium) from match_results
where (score1 > 4) or (score2 > 4);

-- Q5 List the names of all the cities which have the name of the Stadium starting with “Estadio”. 
select distinct(city)from match_results
where Stadium like "Estadio%";

-- Q6 List all stadiums and the number of matches hosted by each stadium. 
select stadium, count(*) as s from match_results
group by stadium
order by s desc;

-- Q7 List the First Name, Last Name and Date of Birth of Players whose heights is greater than 198 cms. 
select Fname, Lname, BirthDate from players
where height > 198;

-- --------------------------------------------------- BONUS QUESTION ---------------------------------------------------- --

-- Q8 List the Stadium Names and the Teams (Team1 and Team2) that played Matches between 20-Jun-2014 and 24-Jun-2014
select stadium, team1, team2 from match_results
where match_date between '2014-06-20' and '2014-06-24';


-- Q9 List the Fname, Lname, Position and No of Goals scored by the Captain of a team  who has more than 2 Yellow cards or 1 Red card.
select p.Fname,  p.Lname, p.Position, g.goals, P.PID
from players as p join player_assists_goals as g on p.PID = G.PID
join player_cards as c on p.PID = c.PID
where (isCaptain = 'TRUE') AND (no_of_yellow_cards > 2 OR no_of_red_cards = 1)
order by g.goals desc;
