# Power-4---Contest
Implementation of an artificial intelligence for a Power 4 in Python as part of a competition where every student would would let their AI compete against each other.


This project being a PvP (two players) zero sum game, we used a Minimax algorithm as a base for our AI. We used the Minimax.
Ofcourse, in order to optimize the Minimax, we incorporated a beta alpha pruning in order to intelligently cut the nodes at the right places in order to improve the speed of the AI. Since the size of the grid makes it impossible to compute all the possibilities, alpha beta is performed by simulating all the parts to a certain depth from a given node. This depth, varying between 4 and 6 depending on the progress of the game, was determined in order to respect the balance between efficiency and action time.

In order to improve the performance of this AI (in terms of reflection), we added two heuristics, both complementary.
The first one is an evaluation of the grid at a given state. This evaluation gives more weight to a square than to another one, this weight being defined by the number of potential victories that this square implies. Let's take an example:
![puissance 4 1](https://user-images.githubusercontent.com/59508102/153102921-9efdff01-5b25-4cab-805a-95c38dc8fb60.jpg)

In the case opposite, the played square can be involved in 3 victories: one on the line, one on the column and one on the upward diagonal. This square is therefore worth 3 points.

In this second case, the played square can be involved in 7 victories: 1 on the diagonal, 1 on the column and 4 on the line. This square is therefore worth 7 points.

![puissance 4 2](https://user-images.githubusercontent.com/59508102/153102994-4979f17f-0cff-4dec-ba3e-67395140aa20.jpg)

The principle of this heuristic is to go through the grid by returning the evaluation comprising the sum of the values of the squares played by a player minus the sum of the values of the squares played by his opponent.

The second heuristic works in the same way as the first one (evaluation of the grid) but this time by looking at the number of chips aligned by a player allowing to win. A coefficient is applied to give a value of :
- 1 point per alignment of two chips that can lead to a victory
- 3 points for each alignment of 3 chips that can lead to a victory
- 1000 points for every 4 tokens that lead to a victory
As with the first heuristic, the evaluation is done by summing the player's points and subtracting the opponent's points.
On the other hand, this heuristic being very time consuming for a depth exceeding 5, we decided not to apply it on the whole board, but only on the rows, columns and diagonals (ascending and descending) associated to the last two moves played (the player's and the opponent's). This considerably reduces the speed of execution and only slightly decreases the efficiency of the AI because the "heat of the action" is often around the last chips played.
For your information, using this method reduced the average execution time from 50-60 sec to 10-15 sec in depth 6 and from 30-35 sec to 3-8 sec in depth 5.

Translated with www.DeepL.com/Translator (free version)
