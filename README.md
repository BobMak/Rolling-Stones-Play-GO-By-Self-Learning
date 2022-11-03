Using Sphero robots to play Go.

## goboard

go game engine implementation of the interface from [alpha-zero-general](https://github.com/suragnair/alpha-zero-general).
current features:
* play go against a random agent
* send mqtt commands about stone placement to pathfinding

### Setup

`conda create --name rlpg --file env.txt`

### Play against a random agent

`python src/playgo.py`

### Test
 
`python -m unittest test/GoGameTests.py`

## pathfinding

A* pathfinding for the expanded go grid. The logical grid is expanded to include a
unit of space between all robots for simpler pathfinding.
Features:
* A* pathfinding for putting new stones on the board, and removing stones from the board


### Using Repositories

[alpha-zero-general](https://github.com/suragnair/alpha-zero-general)   
[sphero_formation (0ac14aad3)](https://github.com/mkrizmancic/sphero_formation)
[sphero_ros](github.com:mmwise/sphero_ros)