# This is an experimental operating system running on Python. Features include password protection, joke-teller,
# notePad, task manager, two games, information on the system, and the ability to change user settings! IT DOES
# INCLUDE TWO PYTHON GAMES FROM EARLIER IN THE COURSE (Bagels and TicTacToe)
import random
from System import operating_system
from Applications.scout_rpg import ScoutRPG
from System import Loading

# thread = Loading.LoadingClass(0)
# thread.thred()

# Loading.modify_user("Tejas", 7, "running")
# Loading.display_user("Tejas")
# print(Loading.caesar_encrypt_hex("Hello"))
# print(Loading.caesar_encrypt_hex(random.choices(Loading.alphabet, k=20)))
scout_rpg = ScoutRPG.boot('Users\\Tejas')

one = operating_system.boot()
