"""
Module operating_system. This module contains the Core Python OS functions and classes. Probably the most complex file in the system.
"""
import random, time, traceback, requests
try:
    from Applications.bagels import Bagels
    from Applications.event_viewer import EventViewer
    from Applications.hangman import Hangman
    from Applications.jokes import Jokes
    from Applications.notepad import Notepad
    from Applications.scout_rpg import ScoutRpg
    from Applications.sonar import Sonar
    from Applications.speed_up_or_slow_down import SpeedUpOrSlowDown
    from Applications.system_info import SystemInfo
    from Applications.task_manager import TaskManager
    from Applications.tictactoe import Tictactoe
    from Applications.user_settings import UserSettings
    from System import Loading
    from System import system_recovery
    from System.User import *
    from System.reset import Reset
except ImportError as e:
    Bagels = EventViewer = Hangman = Jokes = Notepad = ScoutRpg = Sonar = SpeedUpOrSlowDown = SystemInfo = TaskManager = \
        Tictactoe = UserSettings = system_recovery = Reset = None
    # If any file is missing, code will come here.
    # UPDATE Change whenever the token changes!
    token = "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"
    for sys_file in ("Loading.py", "operating_system.py", "reset.py", "system_recovery.py", "User.py"):
        try:
            file = open("System/" + sys_file, 'x', encoding='utf-8')
            download = requests.get("https://raw.githubusercontent.com/Cerberus1470/Sentiens-Anguis/Tejas/System/{}".format(sys_file),
                                    headers={'accept': 'application/vnd.github.v3.raw', 'authorization': 'token {}'.format(token)})
            file.write(download.content.decode())
            file.close()
        except (FileExistsError, FileNotFoundError):
            pass
    from System import Loading
    Loading.returning("The system is missing files. It will now re-download them from GitHub. Please wait.", 4)
    Loading.progress_bar("Downloading Files", 5)
    Loading.returning("The system has finished downloading/updating files and will now reboot", 5)

dirty = []


# noinspection PyBroadException
def boot():
    """
    Method boot(). This method regulates the boot process of the Core OS. It is responsible for allowing one-line startup.
    :return: 0 if no crashes occur. Code 1-4 if an error occurs.
    """
    global dirty
    running = True
    start = time.time()
    dirty = []
    cerberus = OperatingSystem()
    while running:
        try:
            # Initialization reads all files and data from disk and loads it into memory.
            Loading.log("System Startup.")
            if cerberus.error:
                Loading.returning("Entering Recovery...", 1)
                system_recovery.SystemRecovery.boot(cerberus.error)
                Loading.returning("Saving changes and booting...", 3)
                print('\n\n\n\n\n')
            cerberus.reload()
            # Logic to run setup

            # Logic for restarting.
            if cerberus.startup() == 4:
                Loading.returning("Restarting system...", 2)
                Loading.returning("Booting...", 2)
            else:
                running = False
                return "Code 0. Execution successful."
        # Screen for fatal errors. Catches all exceptions and prints the stacktrace. Allows for a reboot.
        except Exception as f:
            for j in range(20):
                print("\n")
            Loading.log("{} encountered a fatal error. Reboot is required. Stacktrace: {}".format(cerberus.name, f))
            if input('!!! {} encountered a fatal error. Reboot is required. !!! \nWhat failed: {}\n\nStacktrace: \n{}'.format(
                    cerberus.name, str(traceback.format_exc()).split('\n')[len(traceback.format_exc().split('\n'))-4].split('"')[1], str(traceback.format_exc())) + '\nType "REBOOT" to reboot.') == "REBOOT":
                pass
            else:
                print("Goodbye")
                return "Code {}. A system error has occurred.".format(','.join([i for i in cerberus.error]))
        Loading.log("System Shutdown. {} seconds have elapsed.".format(str(time.time() - start)))


# noinspection PyTypeChecker
class OperatingSystem:
    """
    Class Operating System. Houses all the core functions aside from boot.
    """

    def __init__(self):
        # User list, name, and versions. All inherent settings.
        self.users = []
        self.name = "Cerberus"
        self.error = []
        self.recently_deleted_users = []
        self.utilities = ["User Settings", "System Info\t", "Notepad\t\t", "SpeedSlow\t", "\t\t\t", "\t\t\t"]
        self.games = ["Bagels\t", "Tictactoe", "Hangman ", "Sonar", "Joke Teller", "ScoutRPG"]
        self.admin = ["Reset\t\t", "Event Viewer\t", "Task Manager", "\t\t", "\t\t", "\t\t"]
        self.versions = {"Main": 5.6, "Bagels": 4.5, "Event Viewer": 1.1, "Hangman": 3.5, "Joke Teller": 1.4, "Notepad": 3.4, "ScoutRPG": 1.2,
                         "Sonar": 2.1, "SpeedUpOrSlowDown": 1.2, "Sudoku": 1.0, "System Info": 1.6, "System Recovery": 1.3, "Tictactoe": 5.7,
                         "User Settings": 2.9}
        self.path = "Users\\{}"
        self.current_user = User()
        Loading.log("Boot complete.")
        return

    def __repr__(self):
        # Representation of this class.
        return "< This is an OperatingSystem class named " + self.name + "\n Users: " + str(len(self.users)) + "\n Current User: " + \
               self.current_user.username + "\n Current Password is hidden. >"

    # noinspection PyUnreachableCode
    def reload(self):
        """
        This method reloads the OS variables from the disk. Very useful in a restart because one does not have to close the
        python shell.
        :return:
        """
        global dirty
        self.error = []
        new_users = []
        for subdir, dirs, files in os.walk("Users"):
            if len(dirs) == 0 and len(files) == 0:
                self.setup()
                return
            if "info.usr" in files:
                user_file = list(open("{}\\info.usr".format(subdir), 'r'))
                info = Loading.caesar_decrypt(user_file[0]).split('\t\t')
                programs = Loading.caesar_decrypt(user_file[1]).split('\t\t')
                length = len([files for files in os.walk("Applications")][0][2])
                if len(info) == 5 and (len(programs) == length or len(programs) == length - 2):
                    try:
                        new_users.append(globals()[info[0]](info[1], info[2], info[3] == "True", [j.split('\t') for j in programs]))
                    except (AttributeError, IndexError):
                        self.error.append(system_recovery.CorruptedFileSystem([subdir, info, programs]))
                else:
                    self.error.append(system_recovery.CorruptedFileSystem([subdir, info, programs]))
        if new_users or self.error:
            # Setting the current user object.
            admin_present = False
            self.users = new_users
            for j in self.users:
                if j.current:
                    self.current_user = j
                if j.elevated:
                    admin_present = True
            if self.current_user.username == "Default" and self.current_user.password == "Default" and self.current_user.__class__.__name__ == "User":
                self.error.append(system_recovery.NoCurrentUser())
            if not admin_present:
                self.error.append(system_recovery.NoAdministrator())
            if self.error:
                if len(self.error) == 1:
                    raise Exception(self.error[0].__repr__() + " Please reboot the system.")
                else:
                    raise Exception("Multiple fatal errors occurred. Please reboot the system.")
        else:
            self.setup()
            return

    def startup(self):
        """
        This method regulates the startup and login of the OS. Allows to shut down and switch users.
        :return: Shutdown values returned from operating_system().
        """
        # The main startup and login screen, housed within a while loop to keep the user here unless specific circumstances are met.
        while True:
            print("\nHello! I am {}.".format(self.name))
            if self.current_user.username != 'Guest':
                # Separate while loop for users. Guest users head down.
                incorrect_pwd = 0
                while True:
                    if incorrect_pwd >= 3:
                        Loading.returning("You have incorrectly entered the password 3 times. The computer will now restart.", 5)
                        return 4
                    print("\nCurrent user: " + self.current_user.username + ". Type \"switch\" to switch users or \"power\" to shut down the system.")
                    # Ask for password
                    pwd = input("Enter password.\n")
                    if pwd == self.current_user.password:
                        Loading.returning("Welcome!", 1)
                        # Move to the system screen.
                        os_rv = self.operating_system()
                        Loading.log("Code {} returned. Executing task.".format(os_rv))
                        # Logic for returning from the OS screen.
                        if os_rv == 1:
                            print("\n" * 10)
                            print("The System is sleeping. Press [ENTER] or [return] to wake.")
                            input()
                            break
                        elif os_rv == 'regular':
                            pass
                        else:
                            return os_rv
                    elif pwd == 'switch':
                        # Switch users!
                        UserSettings.switch_user(self)
                        break
                    elif pwd in ('shutdown', 'power'):
                        # Shutting down...
                        shutdown = self.shutdown()
                        if shutdown == 1:
                            print("\n" * 10)
                            Loading.log("System asleep.")
                            print("The System is sleeping. Press [ENTER] or [return] to wake.")
                            input()
                            break
                        else:
                            return shutdown
                    elif pwd == 'debugexit':
                        # Carryover from original code :)
                        Loading.log("Returned code debug.")
                        return
                    else:
                        print("Sorry, that's the wrong password. Try again.")
                        incorrect_pwd += 1
                        pass
            else:
                while True:
                    # The guest account, housed in its own while loop. The only way to exit is to use debugexit, or when the user shuts down.
                    print("WARNING: The Guest account will boot into the main screen, but any user settings or games will have no effect. \nThis includes usernames, passwords, game progress, saved notes, etc.")
                    print("All games will say that the file or path is not found, this is normal. The Guest User doesn't have a user folder.\nPress [ENTER] or [return] to login.")
                    if input() == 'debugexit':
                        return
                    Loading.log("Guest user logged in")
                    self.operating_system()
                    return 3

    def operating_system(self):
        """
        Method operating_system(). The home screen and hub for almost every command in the OS.
        :return:
        """
        # The main OS window. Contains the list of apps and choices. Stored in a while loop to keep them inside.
        Loading.log(self.current_user.username + " logged in.")
        print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
        while True:
            # Main while loop for applications.
            if self.current_user.elevated:
                print("\nAPPLICATIONS\nUTILITIES\t\t\tGAMES\t\t\tADMIN")
                for j in range(len(self.games)):
                    print(self.utilities[j] + '\t\t' + self.games[j] + '\t\t' + self.admin[j])
            else:
                print("\nAPPLICATIONS\nUTILITIES\t\t\tGAMES")
                for j in range(len(self.games)):
                    print(self.utilities[j] + '\t\t' + self.games[j])
            print("\nLock Computer\tPower")
            choice = input().lower()
            # This logs what app the user opened, but the number codes still work.
            Loading.log(self.current_user.username + " opened " + choice)
            choices_list = {Jokes: ('jokes', 'joke', '1', 'joke teller'), Notepad: ('notepad', 'notes', 'note', '2')
                            , SpeedUpOrSlowDown: ('speedslow', 'speed up', 'slow down', 'speed up or slow down')
                            , Bagels: ('bagels', 'bagels', '3'), Tictactoe: ('tictactoe', 'tic-tac-toe', 'ttt', '4')
                            , Hangman: ('hangman', '5'), Sonar: ('sonar', '6'), ScoutRpg: ("scout rpg", "scout", "rpg", "scout_rpg", "scoutrpg")
                            , UserSettings: ('user settings', 'usersettings', '8'), SystemInfo: ('system info', 'sys info', '9')
                            , TaskManager: ('task manager', '7'), EventViewer: ('event viewer', 'events'), Reset: ('reset', '10')}
            if choice in ('exit', 'lock computer', 'lock', '11'):
                Loading.log(self.current_user.username + " logged out.")
                print("Computer has been locked.")
                return 'regular'
            elif choice in ('shutdown', '12', 'power'):
                Loading.log(self.current_user.username + " logged out and shutdown.")
                return self.shutdown()
            elif choice in ('debugexit', 'debug'):
                return 'regular'
            for j in choices_list:
                if choice in choices_list[j]:
                    self.current_user.saved_state[j] = True
                    if list(choices_list.keys()).index(j) >= len(choices_list) - 3:
                        if self.current_user.elevated:
                            if j.boot(self) == 4:
                                return 4
                    else:
                        if j.category == "games":
                            if j.boot(self.path.format(self.current_user.username)) == 'regular':
                                print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
                                return 'regular'
                        elif j.category == "utilities":
                            if j.boot(self) == 'regular':
                                print("Hello! I am {}, running POCS v{}".format(self.name, self.versions["Main"]))
                                return 'regular'
                    break
            else:
                Loading.returning("Please choose from the list of applications.", 1)

    def shutdown(self):
        """
        Method shutdown(). Handles sleeping, hibernating, shutting down, and restarting properly and modifies user files accordingly.
        :return:
        """
        Loading.log("Preparing to shut down...")
        # The shutdown method. Saves everything to disk and rides return statements all the way back to the main file. Exits safely after that.
        if self.current_user.username == 'Guest':
            Loading.returning("The guest user cannot save progress. The system will shutdown.", 3)
            return 3
        while True:
            # While loop to choose what type of shutdown to do.
            print("Choose an option.")
            print("1. Sleep\n2. Hibernate\n3. Shutdown\n4. Restart\nType \"info\" for details.")
            shutdown_choice = input().lower()
            if shutdown_choice == "info":
                # Show info
                print("1. Sleep\nSleep does not close the python shell. It logs out the current user and saves the session to RAM. Forcibly closing "
                      "the shell will result in lost data.\n2. Hibernate\nHibernate saves the current session to disk and exits the python shell. "
                      "The python shell is closed and all data is saved.\n3. Shutdown\nShutdown saves only users and notes to disk. All other data "
                      "is erased and all apps are quit.\n4. Restart\nRestart shuts down the computer, saving only users and notes to disk, and opens "
                      "the program again.")
                input()
                pass
            elif shutdown_choice in ("sleep", "1"):
                # Return sleep code.
                Loading.log("The system is now asleep.")
                print("Sleeping...")
                return 1
            elif shutdown_choice in ("hibernate", "2", 'shutdown', '3', 'restart', '4'):
                # Logic for hibernate vs shutdown vs restart.
                hibernate = False
                shutdown = False
                if shutdown_choice in ('hibernate', '2'):
                    print("Hibernating...")
                    hibernate = True
                elif shutdown_choice in ('shutdown', '3', 'restart', '4'):
                    # Logic for shutdown vs restart. Very simple.
                    if shutdown_choice in ('shutdown', '3'):
                        shutdown_choice = 'shutdown'
                        shutdown = True
                        print("Shutting down...")
                    else:
                        shutdown_choice = 'restart'
                        print("Restarting...")
                    # Check if any programs are running
                    program_count = 0
                    for i in self.users:
                        for j in i.saved_state:
                            if i.current:
                                if self.current_user.saved_state[j]:
                                    program_count += 1
                            elif i.saved_state[j]:
                                i.saved_state[j] = False
                    if program_count > 0:
                        print("Waiting for {} programs to close.".format(program_count))
                        for i in self.current_user.saved_state:
                            if self.current_user.saved_state[i]:
                                self.current_user.saved_state[i] = False
                                Loading.returning("Closing {}.".format(str(i.__name__)), 2)
                        if shutdown_choice in ('shutdown', '3'):
                            print("Shutting down...")
                        else:
                            print("Restarting...")
                        Loading.log("All apps closed.")
                    else:
                        print("No apps are open.")
                for i in self.users:
                    # Running Programs!
                    i.saved_state = '\t\t'.join(["{}\t{}".format(j.__name__, k) for (j, k) in i.saved_state.items()]) + '\t\t\n'
                # Now write each user's info to their respective info files.
                for i in self.users:
                    # Open their file, write encrypted data and close the file.
                    Loading.log("Updating user files...")
                    user_file = open(self.path.format(i.username) + "\\info.usr", 'w')
                    user_file.write(Loading.caesar_encrypt(i.__class__.__name__ + '\t\t' + i.username + '\t\t' + i.password + "\t\t" + str(i.current) + '\t\t\n'))
                    user_file.write(Loading.caesar_encrypt(i.saved_state))
                    user_file.close()
                # Finishing with some print statements.
                Loading.log("Shutdown complete.")
                if hibernate:
                    input('Hibernation complete. Open "{}.py" to restart the system.'.format(self.name))
                    return 2
                elif shutdown:
                    input('Shutdown complete. Open "{}.py" to restart the system.'.format(self.name))
                    return 3
                else:
                    return 4
            else:
                print("Please choose from the list of choices.")

    def setup(self):
        """
        Method setup(). This method sets the system up with the correct files. Soon to be overhauled to download files from GitHub.
        :return:
        """
        # The setup method. Conveniently sets up the system to run on its first boot, and whenever there is no data. Modifies the dictionary with a new user.
        Loading.log("The system has entered SETUP.")
        try:
            os.mkdir("Users")
        except FileExistsError:
            pass
        print("SETUP: Since this is the first time you're running this OS, you have entered the setup.")
        # Ask the user if they want to make a user or not.
        print("Would you like to create a new user, or login as guest?")
        user_or_guest = input()
        if user_or_guest.lower() in ('new user', 'new', 'user', 'yes'):
            # New user it is!
            setup_user = input("Name your user:\n")
            print("New User added. Enter a password or press [ENTER] or [return] to use the default password.")
            while True:
                # The while loop handles the password creation. Can only escape under certain circumstances.
                setup_pwd = input()
                if setup_pwd:
                    # If the user entered a password:
                    print("Password set. Enter it again to confirm it.")
                    if setup_pwd == input():
                        break
                    else:
                        # Handle password matching. Loops back to ensure the user typed the correct passwords.
                        print("The passwords you entered didn't match. Type the same password twice.")
                else:
                    # If the user did not enter a password.
                    setup_pwd = "python123"
                    Loading.returning('Default password set. The password is "python123".', 2)
                    break
            # User entered password correctly twice.
            self.current_user = Administrator(setup_user, setup_pwd)
            Loading.returning("Password set successfully.", 2)
            Loading.returning("One last thing!", 1)
            recovery_pwd = ''.join(str(random.choice(Loading.alphabet)) for _ in range(1000)) + '\t\t' + input("Please enter a recovery password.") + '\t\t' + ''.join(str(random.choice(Loading.alphabet)) for _ in range(1000))
            recovery_file = open("System\\recovery.info", 'w')
            recovery_file.write(Loading.caesar_encrypt(recovery_pwd))
            recovery_file.close()
            self.users.append(self.current_user)
            os.mkdir(self.path.format(self.current_user.username))
            user_file = open(self.path.format(self.current_user.username) + "\\info.usr", 'w')
            user_file.write(Loading.caesar_encrypt(self.current_user.__class__.__name__ + '\t\t' + self.current_user.username + '\t\t' + self.current_user.password + "\t\t" + str(self.current_user.current) + '\t\t\n\n'))
            user_file.close()
            Loading.returning("Entering startup in 3 seconds.", 3)
        else:
            # If the user did not specify whether they wanted a new user.
            self.current_user = Administrator("Guest", "")
            self.users.append(self.current_user)
            Loading.returning("Guest user added. There is no password. Entering startup in 3 seconds.", 3)
            os.rmdir("Users")
        Loading.log("SETUP is complete. Entering startup.")
        return
