from room import Room
from player import Player
from world import World
from stack import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

direction_ops = { "n": "s", "e": "w", "s": "n", "w": "e"}

## bfs mod

s = Stack()
s.push([player.current_room])
visited = set()

traversal_graph = {}
traversal_graph[player.current_room.id] = {}


while len(s.stack) > 0:
    path = s.pop()
    curr_room = path[-1]

    if curr_room not in visited:
        visited.add(curr_room)
        traversal_graph[curr_room.id] = dict.fromkeys(
            cur_room.get_exits(), None)

        for direction in curr_room.get_exits():

            traversal_graph[curr_room.id][direction] = curr_room.get_room_in_direction(
                direction).id
            s.push(
                path + [curr_room.get_room_in_direction(direction)])

def dft_recursive(starting_room, visited=[], direction=None):

    if starting_room not in visited:
        visited.append(starting_room)
        traversal_path.append(direction)

        for next_room in traversal_graph[starting_room]:
            dft_recursive(traversal_graph[starting_room]
                          [next_room], visited, next_room)

        if len(visited) >= len(room_graph):
            return

        if direction in direction_ops.keys():
            traversal_path.append(direction_ops[direction])


dft_recursive(0)

traversal_path = traversal_path[1:]  # removes None

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
