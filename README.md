This is the repository for the game 'Blufpoker' for the course Logical Aspects of Multi-Agent Systems.
Website at https://boscy.github.io/Blufpoker/


<img src="https://i.pinimg.com/originals/f5/95/f6/f595f6e121085652d5118eaf3a20e8e1.jpg" class="img-responsive" alt=""> </div>


**Analyzing Blufpoker using Epistemic Logic**

Ivar Mak (S2506580)   Oscar de Vries (S2713748)   Joost Warmerdam (S2591367)

# 1    Introduction

Blufpokeris  a  dice  game  which  contains  several  interesting  aspects  with  regards  to  knowledge,beliefs and bluffing.  In this project, we aim to implement (a simplified version of) the game in aprogramming environment, as well as simulating different players and their respective strategies.This will be done using Epistemic Logic combined with a Multi Agent System that models playingbehaviour for three players.  We aim to implement different playing styles,  which will be furtherexplained  in  Section  2.   Furthermore,  we  aim  to  define  and  compose  an  epistemic  model  of  theknowledge for at least one player.  This model will contain the possible worlds which can be reachedfrom the in game situation and will be used for the decision making process of the player.  Theaspect of bluffing (false public announcements) comes into play when a player throws a bad turn.But before we address this, we will describe the rules of the game.

## 1.1    Game Description

The game is played using three dice, which together depict a number in the hundreds.  The highestranking die translates to the hundred, the second to the ten, and the lowest ranking die translatesto the single digit.  So in a situation where a 5, 3, and 2 are rolled the corresponding number is 532.The exception are the ”pokers” which are triplets (i.e.  111, 222, 333, etc).  These are the highestpossible throws, 111 is higher than 665, and 666 is poker 6 and the highest possible score.  Table 1 describes all possible combinations, ranked descending from highest to lowest.  Players take turnsthrowing the dice, which are concealed under a cup (i.e.  other players do not see the player’s dice).The aim of the game is to throw a number that is higher that the number that was passed on bythe previous player.  Each dice can be thrown once in order to try to reach a higher number.  Whenthe player completes his turn,  he needs to publicly announce the number that he reached whichneeds to be higher than the number that was passed on to him (unless he is starting the round, inthis case any number suffices).  Obviously, there is a possibility that he did not reach a number thatis high enough.  In this case the player needs to bluff, by saying a number that he did not throw.Since the dice are concealed, he can say whatever number he deems suitable, and pass on the diceto the next player.  It is up to this player to determine whether his adversary is telling the truth.If he believes the truth was told, it is his turn to throw the dice and reach a higher number yetagain.  In the case he does not believe the previous player, he can call the bluff and lift the cup.  Ifthe number that was announced is actually on the table player 2 loses the round, if the number isnot there; player 1 loses the round.  Note that not all dice have to be thrown in order for a playerto pass the dice, a player can stop and announce his number after each throw.  Furthermore thenumber of rounds to be played is variable, with a player obtaining one penalty point for each roundlost, and the game ending when a specific number of points is reached.  Therefore there will alwaysbe one loser and multiple winners.  The number of penalty points chosen to finish can resemble aword such as ”HORSE”, receiving a letter for each loss.

<img src="images/PossibleWorlds.png" class="img-responsive" alt=""> </div>

## 1.2    Simplifications

The original game consist of multiple aspects that will heavily complicate the composition of themodel and therefore the decision making process.  This is why we will apply several simplificationsto make the game more manageable.

-•When a player is not bluffing, he will announce the exact number he reached with the dice. *In  the  original  game,  the  player  can  choose  whichever  number  he  wants  (even  ’impossible’numbers such as 500) as long as his throw is higher than this.•The ”golden triangle” is not the highest throw.In  the  original  game,  the  combination  321  yields  a  ”golden  triangle”  which  is  the  highestpossible throw, beating 666.*
-•All players play to win. *In  the  original  game,  players  can  decide  to  adjust  their  announcements  in  order  complicatespecific  other  player’s  turns,  trying  to  make  them  lose.   In  our  version  the  player  is  onlyconcerned with himself not losing.*
-•The player will never pass the dice without throwing. *In the original game, a player has a third option besides throwing the dice or calling a bluff.Which is announcing a higher number, while not having thrown the dice, and passing them tothe next player.  This does not add to the knowledge base of the player, which is why we willnot implement this part.*

## 1.3    Outline

We aim to build an algorithm that simulates the game, in which agents play according to differentstrategies.   These  strategies  will  include  superficial  strategies,  but  also  a  more  complex  strategybased on the knowledge that is obtained.  Given this approach,  we aim to address the followingquestion:  How does an agent with a knowledge based strategy perform versus more naive, superfi-cial strategies?In the following section we will describe formally how we aim to construct our knowledge base,and how we base our decision making process on this.  Furthermore, we will describe how the naiveplayers achieve their decision making.  In the Results section, we will describe which results we willgather and how we will utilize these in order to draw conclusions.  Depending on the progress of the project, we will try to implement extensions with regards to the baseline version of our game,as well as the model and decision making.  The directions for these extensions are described in theSection Possible Extensions.

# 2    Methods

The Blufpoker simulation made in Python to model the game and the epistemic knowledge modelwill be used to create a strategy for the knowledge-based agent.

## 2.1    Simulation

A simulation of Blufpoker is made to quantify the performance of the knowledge-based agent.  Inthis  simulation,  the  rules  described  in  section  1.1  are  implemented  in  a  setup  for  a  three-playergame of Blufpoker.  This means there are three agents that play against each other, each with theirown strategy.  One of these agents will use the knowledge-base for its decision making (Section 2.2).The simulation will perform the game in a step-wise manner and assign penalty letters accordingly.Once,  an  agent  has  reached  the  maximum  number  of  penalty  points,  that  player  has  lost.   Thesimulation will record, which player has lost as well as data about the playstyle of the knowledge-based agent.  Relevant data about the knowledge-based agent are the number of bluffs in one game,the ratio of bluff-calls per game.The strategies of the other ’naive’ agents will differ in three manners:  (1) deciding which dicethey roll, (2) deciding whether they will bluff, and (3) deciding whether the previous player bluffed.These  strategies  are  not  implemented  yet  but  will  be  used  to  create  results  about  how  well  theknowledge-based agent performs against these different strategies.

### 2.1.1    Naive Strategies

An  overview  of  the  strategies  of  the  naive  agents  that  will  be  used  in  the  games  against  theknowledge-based agent is given:

1.  Which dice will the agent throw?
-•Random
-•Throw the lowest die
-•Throw any die that is lower than 6

2.  When will the agent bluff?
-•Always be truthful, if possible.
-•Always tell a number x above the previous value

3.  When has the previous agent bluffed?
-•Random
-•Always believe it
-•Always call the bluff

## 2.2    Knowledge-based agent

One of the agents in the simulation will play according to a more sophisticated strategy, involving knowledge and probabilities in the game.  We will now go over the 3 phases in the gamethat involve decision making and explain how the knowledge-based agent will apply its strategy.This will be based on a regular turn (i.e.  not a first turn of the game).

### 2.2.1    Phase 1: Believing or calling a bluff 
First of all, the agent has to make the decision whether it believes the previous players bet or callsit a bluff.  This will be done by looking at the number of possible worlds in which the previousplayer is bluffing.  If the percentage of these worlds (in which the bet is not true) is bigger than athreshold, the model will call a bluff and the cup will be lifted.If the previous player is not believed to be bluffing, the agent believes the bet and goes into thethrowing dice phase.

### 2.2.2    Phase 2: Throwing dice
The model has to decide which dice to throw (and which not to throw) in order to get a highervalue than the previous bet.  It does so by calculating the percentage of possible worlds for whichthis is the case.  From this it can be calculated which dice are best to throw first and whether itsbest to throw another die.  Note that in contrast to the possible worlds in phase 1,  the possibleworlds here represent theexpectedpossible worlds given a certain action, namely that of throwinga particular die.After the player is happy with the dice its rolled, or can not roll any more dice, we go into thebidding phase.

### 2.2.3    Phase 3: Bidding
For the bidding phase there are two options.  Either the agent can bid truthfully to what its value is,or it could bluff and bid a value higher than its cup.  Explaining the truthful bid is self-explanatory,it’s simply stating the value the agent has under its cup.Bluffing is one of the hardest steps to implement, since it usually involves higher order knowledge.For bluffing the agent could make use of (a combination of) the following strategies:Always bet slightly higher than the previous bet.  This could be a random number higher thanthe value of the previous bet, but different every time it is applied.Determine  which  bluffs  are  most  believable,  according  to  previous  players  turns.   This  couldinvolve some memory, for example when player 1 throws (6,5,1), then player 2 throws one dice andcalls (6,5,3) and player 3 throws one dice and calls (6,5,4).  At this point, both player 1 and player 2can know with large certainty that player 3 was speaking the truth.  For player 1, it is the case thathe knows that player 2 has a high belief of what is approximately on the table.  If player 1 decidesto throw just one dice (E.G the ’4’), then he knows that player 2 holds the states (6,5,5) (6,6,4)and (6,6,5) for possible as higher values than the previous bet.  However, since players rationallytend to throw their lowest dice first, the option (6,6,4) could be less viable than the other options.Hence, if player 1 has not thrown enough for the bet to be on the table, he could throw again tomake the bet, or bluff on either (6,5,5) or (6,6,5)


# 3    Results

The results we will gather are focused whether we will be able to efficiently construct a model andits accuracy.  We will evaluate the decision making process based on this model by measuring theperformance of our logic based agent compared to the other agents.  Firstly we will measure this bylooking at the ratio between won and lost games.  Secondly, by looking at the amount of bluffs thatare successfully called by our logical agent, drawing conclusions about in what way the knowledgein this model aids to making the correct decision.

# 4    Possible Extensions

If time allows for it, we have thought of several directions to take in order to extend our projectand/or it’s implementation.•We want to evaluate different settings with regards to the strategies against which the logicalplayer has to compete, and look at the way its performance changes.
-•When  possible,  we  would  like  to  add  more  players  using  a  logical  model  for  their  decisionmaking process.
-•We would like to add feedback prompts describing the decision making process of the logicalagent, much like the thought process of a human player.
-•More aesthetically, we would like to add visualizations of the dice and or the cup.
