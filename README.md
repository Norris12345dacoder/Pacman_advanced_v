# Pacman

This is an advanced version of the famous Pacman game.

This is also a process of me learning Pygame.

Here I'm going to introduce how the game's played and a bit of its inner workings

## Structure

- A maze map and its food based on a text file
- A 16 x 16 grid map
- A 592 x 592 map
- Player (Pacman)
- Ghosts (Red and Purple)

## Text file to map

- | means an apple (later description)
- A star means a wall

It allows users to make their own map.

## Sprites

Pacman (user-controlled)

Red Ghost (follows and chases Pacman)

Purple Ghost (teleports to Pacman)

## Levels

- Level 1: one ghost (red only)
- Level 2: two ghost (red and purple)
- Level 3: two ghost but faster

## Controls

W, A, S, D --> up, left, down, right

## Win and Lose

- Win: Get a total of 250 points

- Lose: Be touched by a ghost

## How to get points?

By eating food

- apple: 2 points
- pellets: 1 point

## What to install to run the game

- Python 3.10+

- Pygame

```bash
pip install -r requirements.txt
```

## To run the game

```bash
python pacman_chasing.py
```

## File description

- pacman_chasing.py: the game's main file
- map2.txt: the map
- pacman.png, wall.png, red_ball.jpg, food.png, ghost.png, ghost(2).jpg: The Pacman, the wall grid, the apple, the pellet, the red ghost, the purple ghost respectively

## My progress

This is a project I made while learning Pygame.
Hope this game is enjoyable to others to play.
I'm proud of the progress I made in my journey in game design.

## AI Implementation

Disclaimer: This project is 100% made by me, completely on my own. However, I did ask AI for advice for specific numbers, such as color scale (styling), sizes of the start and end menus, fonts etc..
Generated the .gitgore file, if that counts.

## Future possible improvements

- Add a feature that connects an AI to generate a new map everytime
- Add special effects when eating or when ghost teleports
- Make better UI and graphics with Godot.
- Save high scores for individual users.
- Add lives so that players won't instantly die.

# Conclusion

This is a really fun game I made, I had a lot of fun making it and hopefully everyone can enjoy it too.
This project has broaden my horizons on game design with Pygame and explored possibilities of further improvements.
