import sys

from player import Player


if len(sys.argv) != 3:
    print("Usage: python3.10 solve.py <start word> <end word>")
    sys.exit(1)

player = Player()
player.play(sys.argv[1].lower(), sys.argv[2].lower())
