# Pac-Man Description
Here is the Group A8's course project of CSCI3100: Software Engineering, Spring 2023, CUHK. 

We are building our own version of the classic Pac-Man game in Python! We plan to keep the classic mode of Pac-Man and add more exciting elements like powerful items, fun modes, and AI agent. Follow us to know more!

This project currently is a Python-based implementation of the classic Pac-Man game with three modes: classical, multiplayer, and AI. The project uses pygame as the main library for graphics and sound.

The classical mode is the original Pac-Man game logic, where the player controls Pac-Man to eat dots and avoid ghosts in a maze. The multiplayer mode is a two-player version of Pac-Man game logic, where two player controls weo Pac-Mans. The AI mode is a single-player version of Pac-Man game logic, where the player cannot play and both Pac-Man and the ghost controlled by AI.

# Requirements and How to Run

To run this project, you need to have Python 3， pygame， and tkinter installed on your system. You can install pygame and tkinter using pip:

`pip install pygame`

`pip install tkinter`

To run the project, you need to clone this repository and navigate to the root directory. Then you can execute the following command:

`python login_data.py`

This will launch the game window, where you can choose a mode and start playing.

# How to play

* To start the game, use your mouse to click on the main menu options.

* To control Pac-Man, use the arrow keys or the W, A, S, D keys on your keyboard. You can move Pac-Man up, down, left or right to eat the dots and avoid the ghosts.

* In multi-player mode, you can control two Pac-Men with different sets of keys. The arrow keys control one Pac-Man and the W, A, S, D keys control the other Pac-Man. You can cooperate or compete with each other to get a higher score.

Have fun playing Pac-Man!

# Guidance for creating the local database for user's local host

Steps for setting up sql and pymysql:

   1. Install the sql client. 

   Interface according to the mysql.png in the document

   2. Modify login_data.py the code section and set the host to the name and password of the client on your computer to complete the link

   3. Use the connect method to connect to our database. For example, 

   `db = pymysql.connect(host="localhost", user="root", password="password", database="test", charset="utf8")`

   4. Then get the cursor by(this is for fetch your data in the database)

   `cursor = db.cursor()`

   5. Then follow the basic mysql syntax, call the cursor.execute() method to run mysql commands with pymysql. For example,
   This is optional because our program code is completed settings, you can reset it according to your preference.

   `cursor.execute("CREATE TABLE IF NOT EXISTS proj_db(\
      name VARCHAR(100) NOT NULL,\
      password VARCHAR(100) NOT NULL,\
      score int,\
      PRIMARY KEY (name)\
   )")`


# Group Members and Contribution

This project is developed by GroupA8, which consists of the following members:

|  Name  |  SID  |  Contribution  |
|--------|-------|----------------|
| BAI Yuan | 1155157073 | responsible for the sound, animation, and design mazes for different difficulty levels, including the sound effects and background music for different game situations, the animation effects for Pac-Man, fruit’s appearance, etc. |
| BAO Wenrui | 1155157220 | responsible for the homepage design and functionality, including the main menu, instructions, and exit options. |
| LI Jianqiang | 1155157143 | responsible for the basic gameplay logic and implementation, including the Pac-Man and ghost movement, dot and power pellet effect, fruit and bonus point effect, and collision detection. |
| YUE Haoyuan | 1155157271 | responsible for the AI player feature, including the AI algorithm for Pac-Man and ghost behavior. |
| ZHANG Juyuan | 1155160257 | responsible for the database and user management system, including the user registration, login, logout, profile management, and leaderboard functions. |

# Progress
Phase 1: High-Level Design Document    (DONE)

Phase 2a: DFD Specification Document    (DONE)

Phase 2b: GitHub Repository Creation    (DONE)

Phase 3: UML Specification and UI Design Document    (DONE)

Phase 4: Project Demo    (DONE)

Phase 5a: Testing Document    (DUE at 5/6)

Phase 5b: Final code    (DUE at 5/6)

# Acknowledge and References
We would like to thank our CSCI3100 Teaching Staffs for their guidance and support throughout this project. We would also like to thank the following resources that we used or referenced in this project:

Pygame: a cross-platform library for making multimedia applications like games using Python. https://www.pygame.org/

Pac-Man Sounds: Our sound effects are taken from various free music libraries. In addition, 8bit music mainly comes from NetEase Cloud Music.
