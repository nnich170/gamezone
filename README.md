# gamezone

1. Project Title: Game Zone
2. Project Issues or Problems to be solved: Game lovers may sometimes facing issues in downloading several games at once. The goal of "Game Zone" is to provide an engaging and interactive platform where users can play multiple games from a single application. Currently, the application offers 3 types of game: Car Racing, Snake, and Ping Pong. 

3. Current Progress:

     - Problem Analysis: Identify users needs and requirements for a smooth game selection and playing experience.
     - Design: For the GUI layout, there are 3 buttons for game selection. Each game has separate scripts and funtions.
     - Implementation: Developing an all-in-one gaming application using Pygame, and Python (Tkinter).
     - Testing: I bring this game to my friends for testing, ensuring a smooth gaming experience and avoiding debugs.
     - Deployment: Finalizing the application for distribution.



4. Project Funtions:
    + Main Page: There are 3 buttons available for choosing such as: Snake Game, Ping Pong Game, and Car Racing Game. The player will be asked to select/click on one button among these 3 buttons. When the using click on any game, it will directly link game to the game platform. 

    + Snake Game: If user chooses Snake Game, he/she will see the instructions before proceeding. Player needs to use arrow keys to move the positions of the snake. The snake needs to eat the chicken piece to increase its length. One chicken piece equals to one point. The highest score will be stored using SQLite3. 
    + Ping Pong Game: If user chooses Ping Pong Game, he/she will see the instructions before proceeding. Player needs to use the Up/Down arrow keys to move the position of their Ping Pong racket. The player can set the name before playing. During the game, player will stand for the blue team, and he/she have to against the red team, which was played automatically by the computer system. If one fails to catch the ball, the enemy will get one point. The highest score will be stored using SQLite3. 
    + Car Racing game: If user chooses Car Racing Game, he/she will see the instructions before proceeding. Player needs to use the Left/Right arrow keys to move the position of the red car. The rule is to not let the red car hit the yellow cars. 

5. Expected numbers of pages: 
    1. Main Page
    2. Snake Game 
    3. Ping Pong Game
    6. Car Racing Game

6. Database Applied: The application uses SQLite3 to store the database. It is lightweight and embedded directly into the application, making it ideal for managing game-related data locally.
