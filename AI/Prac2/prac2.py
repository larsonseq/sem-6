last_cleaned_room = 0


def check_tile(current_tile, dirty_tiles):
    global last_cleaned_room
    print(f"Checking Tile {current_tile}")
    if (dirty_tiles[current_tile - 1] == '1'):
        print(f"Tile {current_tile} is Dirty")
        clean(current_tile, dirty_tiles)
    else:
        print(f"Tile {current_tile} is clean")
        if last_cleaned_room == 1 and current_tile == 2:
            return
        if last_cleaned_room == 2 and current_tile == 1:
            return
        last_cleaned_room = current_tile
        move((2 if current_tile == 1 else 1), dirty_tiles)


def move(current_tile, dirty_tiles):
    global last_cleaned_room 
    print(f"Moving to tile {current_tile}") 
    check_tile(current_tile, dirty_tiles) 


def clean(current_tile, dirty_tiles):
    global last_cleaned_room
    print(f"Cleaning Tile {current_tile}")
    dirty_tiles[current_tile - 1] = '0' 
    last_cleaned_room = current_tile
    if current_tile == 1:
        move(2, dirty_tiles)
    else:
        move(1, dirty_tiles)


def main():
    print("Enter Current tile of Cleaner: \n1 -> Left\t2 -> Right\n")
    current_tile = int(input())
    print("Enter Dirty Tiles:\n0 0: Both Clean \t1 1: Both Dirty \t1 0: Left Dirty \t0 1: Right Dirty")
    dirty_tiles = list(input().split(' '))

    check_tile(current_tile, dirty_tiles)

    print("\n..........Terminating Program.............")


if __name__ == "__main__":
    main()
