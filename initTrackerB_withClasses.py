from termcolor import colored, cprint
import time
import os

# TABLE OF CONTENTS:
# SECTION I. CLASS ->
#   a. defines Character class
#       - constructor builds attributes
#       - operations functions manipulate class data
#       - setters/getter for class information
# SECTION II. MENUS ->
#   a. Main menu
#       -Begin Round
#       - Search
#       - Edit
#       - Print Active Lists
#       - Exit Program
#   b. Battle menu
#       - Miss
#       - Hit
#       - Heal
#       - Move
#       - Use Skill
# SECTION III. OPERATIONAL FUNCTIONS ->
#   a. combo_sort()
#   b. sortele()
#   c. one_round()
#   d. are_dead()
# SECTION IV. DRIVER ->
#   a. auto-fill()
#   b. manual_fill()
#   c. char_setup()
#   d. sys_driver()
#
# The program is instantiate through sys_driver().


# ========================================================================================================================== #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#                                                   SECTION I.  CLASS                                                        #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ========================================================================================================================== #
# This is the main class that frames both NPC and PC.
# ____________________________________________________________________________________________________________________________
# -------------------------------------------------------- START CHARACTER CLASS _____________________________________________
class Character:
    # Constructor to initalize data inside each class
    def __init__(self, name, init, hp, dead):
        # Name of the character, how searches are referenced - string
        self.name = name
        # Initiative stat - integer
        self.init = init
        # HPs - int
        self.hp = hp
        # Is the character below 0 HP?
        # dead is defaulted to false - boolean
        self.isdead = dead
        # damage the character inflicted - int
        self.damagedone = 0
        # damge the character received - int
        self.damagetaken = 0
        # healing delivered by character - int
        self.healdone = 0
        # healing received by character - int
        self.healtaken = 0
        # Flag to remember who has gone, default false - bool
        self.hasgone = False
        # A character's max hit points - int
        self.maxhp = hp
        # When a character delivers a killing blow, the name is 
        # documented - string array
        self.kb = []
        # How many attack a character can make each round - int
        self.numOfAttacks = 0

    # A function which in called when a character takes damage.
    # It's paramenter is amount of damage - int
    def takedamage(self, amt):
        temp = self.hp
        self.hp = self.hp - amt
        print("The HP has changed from", temp, " to ", self.hp, " by taking damage: ", amt)

    # A function that prints out to the screen a character's base statistics
    def printplayer(self):
        cprint(self.name.upper(), 'yellow')
        print("Initiative:", colored(self.init, 'green'), colored("|", 'grey'), "Hit Points:", colored(self.hp, 'magenta'))
        cprint("_________________________________", 'grey')

    # Function to print a character's name
    def printname(self):
        cprint(self.name.upper(), 'yellow')

    # A Function to print all of the character's statistics
    def fullprint(self):
        cprint(self.name.upper(), 'yellow')
        print("Initiative:", colored(self.init, 'green'), colored("|", 'grey'),
              "Hit Points:", colored(self.hp, 'magenta'),  colored("|", 'grey'),
              "Damage Done:", colored(self.damagedone, "blue"), colored("|", 'grey'),
              "Damage Taken:", colored(self.damagetaken, "cyan"),  colored("|", 'grey'),
              "Healing Received:", colored(self.healtaken, "red"), colored("|", 'grey'),
              "Healing Dealt:", colored(self.healdone, "yellow"), colored("|", 'grey'),
              "Max HP:", colored(self.maxhp, "green"), colored("|", 'grey'),
              "Killing Blows:", colored(self.kb, "magenta"), colored("|", 'grey'),
              "Number of attacks:", colored(self.numOfAttacks, "blue"))
        cprint("_________________________________", 'grey')


    # Below are the setter and getter functions of the class Character.  They allow access to the class and a way to change it.  
    # ---------------------------- Class Setters/Getters _____________________________

    def setinit(self, num):
        self.init = num

    def getinit(self):
        return self.init

    def setname(self, name):
        self.name = name

    def getname(self):
        return self.name

    def sethp(self, hp):
        self.hp = hp
        self.maxhp = self.hp

    def gethp(self):
        return self.hp

    def setdead(self):
        self.isdead = False

    def getdead(self):
        return self.isdead

    def died(self):
        self.isdead = True

    def dodmg(self, dmg):
        dmg = int(dmg)
        self.damagedone = self.damagedone + dmg

    def returndodmg(self):
        return self.damagedone

    def takedmg(self, dmg):
        dmg = int(dmg)
        self.damagetaken = self.damagetaken + dmg
        self.hp = self.hp - dmg

    def returntakedmg(self):
        return self.damagetaken

    def doheal(self, heal):
        heal = int(heal)
        self.healdone = self.healdone + heal

    def returndoheal(self):
        return self.healdone

    def takeheal(self, heal):
        heal = int(heal)
        self.healtaken = self.healtaken + heal
        self.hp = self.hp + heal
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def returntakeheal(self):
        return self.healdone

    def addattacknum(self):
        self.numOfAttacks += 1

    def addkb(self, whowaskilled):
        self.kb.append(whowaskilled)
# __________________________________________________________ End Character Class--------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------





# ========================================================================================================================== #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#                                                   SECTION II.  MENUS                                                       #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ========================================================================================================================== #

# There are two menus: main and battle.
# Main allows navigation and use of utilities when outside of a round.
# Battle offers use utilities to input and store round data.
# Now that we have a class prototype with all the data we need, we make some by populating each class individually,
# and then setting them in a group.  That requires some functionality: below are functions that will host the ui and gaming logic.
# Beyond that, we have the Driver section where we instantiate the classes, join the arrays,
# and perform operations on the data as represented by the input.

# ___________________________________________________________________________________________________________________________
# ------------------------------------------------ START MAIN MENU __________________________________________________________

# This function supplies us with the main menu of the program.  It will initiate a round or allow access to the database
# NOTE: pa = player array, ma = monster/mob array, ia = initiative array, file = file to write data to
def menu(pa, ma, ia, file):
    # Base case for deciding when everyone has gone or died.
    quitround = False
    # While quitround is false (or, consider, everyone is not finished is true)
    while not quitround:

        # Print the menu
        print('\n\n',
              colored("----- MAIN MENU --------------------------------------------------------------------", 'red',
                      'on_grey'), '\n',
              colored("------------------------------------------------------------------------------------", 'grey'),
              "\n\n", colored('1', 'yellow'), "- Play ", colored('| ', 'grey'),
              colored('2', 'yellow'), " - Search  ", colored('| ', 'grey'),
              colored('3', 'yellow'), " - Edit ", colored('| ', 'grey'),
              colored('4', 'yellow'), " - Print Active List ", colored('| ', 'grey'),
              colored('5', 'yellow'), " - Exit \n\n",
              colored("--------------------------------------------------------------------", 'grey'),
              colored("iniTrack", 'red', 'on_grey'),
              colored("------\n", 'grey'),
              colored("------------------------------------------------------------------------------------", 'red',
                      'on_grey'), '\n\n')

        # Record the user input
        select = input("Please make your selection:\n")

        # ----------------------------------------- IF SELECT = 1 CONTINUE TO ROUND _________________________
        if select == '1':
            print("You selected one.  We will run a round.")
            print("Let's set our initiatives. As the name prints, put in their initiative.")

            # Cycle through both player list and mob list, then create new initiative list
            for p in pa:
                print("Name: ", p.getname())
                editInit = input("Set this initiative to: \n")
                editInit = int(editInit)
                p.setinit(editInit)

            for m in ma:
                print("Name: ", m.getname())
                editInit = input("Set this initiative to: \n")
                editInit = int(editInit)
                m.setinit(editInit)

            init = combo_sort(pa, ma)



            # Run the one_round() function
            one_round(pa, ma, init, file)

        # ----------------------------------------- IF SELECT = 2 SEARCH _____________________________
        elif select == '2':
            # When donesearching boolean is set to true, we return to the main menu
            donesearching = False
            while not donesearching:
                print(
                    colored("\n\n------", 'blue'), colored("Search", 'blue', 'on_grey'),
                    colored("--------------------------------------------------------------------", 'blue'), "\n\n",
                    colored('1', 'yellow'), "- By name ", colored('| ', 'grey'),
                    colored('2', 'yellow'), " - By lowest HPs ", colored('| ', 'grey'),
                    colored('3', 'yellow'), " - By initiative ", colored('| ', 'grey'),
                    colored('x', 'yellow'), " - Return to Main \n\n",
                    colored("---------------------------------------------------------------------------------", 'grey',
                            'on_blue'), "\n\n")
                search = input("Type the appropriate letter to search: \n")

                # -------------- TO-DO ___________________
                # 1. Error handle search items
                #   a. does name exist?
                #       - yes: return name
                #       - no: return error message

                # Search priorities
                if search == '1':
                    searchname = input("What is the name you wish to search? \n")
                    for p in pa:
                        if p.getname() == searchname:
                            p.fullprint()
                elif search == '2':
                    print("The player with the lowest hitpoints:\n\n ")
                    lowhp = 1000
                    holder = ""
                    for p in ia:
                        if p.gethp() <= lowhp:
                            lowhp = p.gethp()
                            holder = p.getname()
                    for p in ia:
                        if p.getname() == holder:
                            p.fullprint()

                    print("Search for lowest hitpoints.")
                elif search == '3':
                    highinit = 0
                    holder = ""
                    for i in ia:
                        if not i.getdead():
                            if i.getinit() > highinit:
                                highinit = i.getinit()
                                holder = i.getname()

                    for i in ia:
                        if i.getname() == holder:
                            i.fullprint()

                    print("Search by Initiative.")
                elif search == 'x':
                    donesearching = True
                else:
                    print("I don't understand your selection.  Please try again: ")

        # ----------------------------------- IF SELECT = 3 EDIT ______________________________
        elif select == '3':

            doneediting = False
            while not doneediting:
                print("\n\n",
                      colored("------", 'green'), colored("Edit", 'green', 'on_grey'),
                      colored(
                          "-----------------------------------------------------------------------------------------------------------",
                          'green'), "\n\n",
                      colored('1', 'yellow'), "- Player Names ", colored('| ', 'grey'),
                      colored('2', 'yellow'), " - Mob Names", colored('| ', 'grey'),
                      colored('3', 'yellow'), " - Initiative list ", colored('| ', 'grey'),
                      colored('4', 'yellow'), " - Player HPs", colored('| ', 'grey'),
                      colored('5', 'yellow'), " - Mob HPs ", colored('| ', 'grey'),
                      colored('x', 'yellow'), " - Return to Main \n\n", colored(
                        "-----------------------------------------------------------------------------------------------------------------------",
                        'grey', 'on_green'), "\n\n")
                printer = input("Make your selections: \n")
                if printer == '1':
                    selectname = input("Please select a Player to edit by typing their name: \n")
                    replacename = input("What would you like to replace the name with? \n")
                    check = 0
                    for p in pa:
                        if p.getname() == selectname:
                            p.setname(replacename)
                            p.printplayer()
                            print("Your change has been committed.")
                            check += 1
                    if check == 0:
                        print("We could not find the name you were looking for")
                elif printer == '2':
                    check = 0
                    selectname = input("Please select a Mob to edit by typing their name: \n")
                    replacename = input("What would you like to replace the name with? \n")
                    for m in ma:
                        if m.getname() == selectname:
                            m.setname(replacename)
                            m.printplayer()
                            print("Your change has been committed.")
                    if check == 0:
                        print("We could not find the name you were looking for")

                elif printer == '3':
                    selectname = input("Please select a character to edit by typing their name: \n")
                    replaceinit = input("What would you like to change the initiation to? \n")
                    # replaceinit = int(replaceinit)
                    check = 0
                    for c in ia:
                        if c.getname() == selectname:
                            c.setinit(replaceinit)
                            c.printplayer()
                            check += 1
                    if check == 0:
                        print("We could not find the name you were looking for")

                elif printer == '4':
                    check = 0
                    selectname = input("Please select a Player to edit by typing their hp: \n")
                    replacehp = input("How many hit points to be reassigned?\n")
                    for p in pa:
                        if p.getname() == selectname:
                            p.sethp(replacehp)
                            p.printplayer()
                            print("Your change has been committed.")
                    if check == 0:
                        print("We could not find the name you were looking for")
                elif printer == '5':
                    check = 0
                    selectname = input("Please select a Mob to edit by typing their name: \n")
                    replacehp = input("What would you like to replace their hps to? \n")
                    for m in ma:
                        if m.getname() == selectname:
                            m.sethp(replacehp)
                            m.printplayer()
                            print("Your change has been committed.")
                            check += 1
                    if check == 0:
                        print("We could not find the name you were looking for")
                elif printer == 'x':
                    doneediting = True
                else:
                    print("I don't understand your selection.  Please try again. ")

        # ------------------------------- IF SELECT = 4 PRINT ___________________________________
        elif select == '4':

            doneprinting = False
            while not doneprinting:
                print("\n\n",
                      colored("------", 'magenta'), colored("Print", "magenta", "on_grey"),
                      colored(
                          "-------------------------------------------------------------------------------------------\n\n",
                          'magenta'),
                      colored('1', 'yellow'), "- Print Initiative list ", colored('| ', 'grey'),
                      colored('2', 'yellow'), " - Print Players' list ", colored('| ', 'grey'),
                      colored('3', 'yellow'), " - Print Mobs' list ", colored('| ', 'grey'),
                      colored('x', 'yellow'), " - Return to Main \n\n",
                      colored(
                          "--------------------------------------------------------------------------------------------------------",
                          'grey', 'on_magenta'),
                      "\n\n")
                printer = input("Make your selections: ")
                # Print by intiative lists
                if printer == '1':
                    print("Printing Initiative List...")
                    for i in ia:
                        i.fullprint()
                # Print by player's list
                elif printer == '2':
                    print("Printing Players' List...")
                    for p in pa:
                        p.printplayer()
                # Print by mobs' list
                elif printer == '3':
                    print("Printing Mobs' List...")
                    for m in ma:
                        m.printplayer()
                # Exit Print
                elif printer == 'x':
                    doneprinting = True
                else:
                    print("I don't understand your selection.  Please try again. ")

        # ---------------------------------IF SELECT = 5 EXIT _________________________________
        elif select == '5':
            print("Goodbye.")
            quitround = True


        else:
            print("I'm not sure what you are requesting.  Please re-enter your selection.")
# _________________________________________________ END MAIN MENU -----------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------



# ___________________________________________________________________________________________________________________________
# ----------------------------------------------- START BATTLE MENU _________________________________________________________
# Truncated turn options
# A menu prints options based on what the character did on their turn
def battle_menu(ilist, att_name, plist, mlist, file):

    # Print the menu and get user input
    att = input("0 - Missed Attack | 1 - Hit | 2 - Heal | 3 - Movement | 4 - Use a skill | p - Print Initiative List \n")
    # Set loop trigger; tripped = exit value, true when you want to exit
    tripped = False
    # Loop until you want to exit
    while not tripped:
        # ----------------------------- IF ATTACK = 0 MISS ATTACK
        if att == '0':
            print(att_name, "missed!")
            # Write to file
            file.write(att_name + " misses!\n")
            for x in ilist:
                if x.getname() == att_name:
                    # Updates the number of attack the Character has attempted
                    x.addattacknum()


            tripped = True
        # ----------------------------- IF ATTACK = 1 HIT ATTACK
        elif att == '1':
            hitnum = input("How many people were hit? 1 - One hit, 2 - Multiple hits, 0 - reset\n")
            hitnumint = int(hitnum)

            if hitnum == '1':
                dmgtarget = input("Who were you attacking? \n")
                dmg = input("how much damage was done on the sole recipient?\n  ")

                for x in ilist:
                    if x.getname() == dmgtarget:
                        x.takedmg(dmg)
                        file.write(att_name + " hits " + dmgtarget + " for " + dmg + "!\n")
                        if x.gethp() < 0:
                            x.died()
                            print(dmgtarget + " has died.")
                            file.write(dmgtarget + " has died.\n")
                            #x.fullprint()
                    if x.getname() == att_name:
                        x.dodmg(dmg)
                        x.addattacknum()
                        # x.fullprint()
            elif hitnumint >= 2:

                for y in range(hitnumint):
                    dmgtarget = input("Who is being attacked? \n")
                    dmg = input("how much damage was done? \n ")
                    for z in ilist:
                        if z.getname() == dmgtarget:
                            z.takedmg(dmg)
                            file.write(att_name + " hits " + dmgtarget + " for " + dmg + "!\n")
                            if z.gethp() < 0:
                                z.died()
                                print(dmgtarget + " has died.")
                                file.write(dmgtarget + " has died.\n")
                                for a in ilist:
                                    if a.getname() == att_name:
                                        a.addkb(dmgtarget)
                                #z.fullprint()
                        if z.getname() == att_name:
                            z.dodmg(dmg)
                            z.addattacknum()
                            #z.fullprint()
            elif hitnum == '0':
                att = input("0 - Missed Attack | 1 - Hit | 2 - Heal | 3 - Movement | 4 - Use a skill | 5 - Print Character list\n")

            tripped = True

        # -----------------------------IF ATTACK = 2 HEAL
        elif att == '2':
            # print(att_name, "healed someone!")
            more_heals = True
            while more_heals:
                healtarget = input("Who did they heal?\n")
                healamt = input("How much healing did they do?\n ")
                for x in ilist:
                    if x.getname() == healtarget:
                        x.takeheal(healamt)
                        x.fullprint()
                    if x.getname() == att_name:
                        x.doheal(healamt)
                        x.fullprint()


                end_loop = False
                while not end_loop:
                    more = input("Did anyone else get healed?  1 - yes, 2- no\n")
                    if more == "2":
                        more_heals = False
                        end_loop = True
                    elif more == '1':
                        file.write(att_name + " has healed " + healtarget + " for " + healamt + ".\n")
                        end_loop = True
                    else:
                        print("You missed keyed the response. \n ")

            tripped = True
        # ----------------------------- IF ATTACK = 3 MOVEMENT
        elif att == '3':
            print(att_name, "moved!")
            print("Write to file (movement).")
            tripped = True
        # ----------------------------- IF ATTACK = 4 Skill
        elif att == '4':
            print(att_name, "used a skill!")
            skill = input("What did they do? \n")
            print("Write to file (skill).")
            tripped = True
        elif att == '5':
            cycle = len(ilist)
            for x in range(cycle):
                ilist[x].fullprint()
        # ----------------------------- IF ATTACK = p PRINT
        elif att == "p":
            print("Printing Initiative List...")
            for i in ilist:
                i.fullprint()
            print("0 - Missed Attack | 1 - Hit | 2 - Heal | 3 - Movement | 4 - Use a skill | 5 - Print Character list\n")
            att = input("What would you like to do now? \n")

       # ----------------------------- TYPO ERROR CALL
        else:
            print("You typed a wrong response.")
# ________________________________________________ END BATTLE MENU ----------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------





# ========================================================================================================================== #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#                                          SECTION III.  OPERATIONAL FUNCTIONS                                               #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# ========================================================================================================================== #

# This function takes the player and monster array and returns
# a combined array of both groups; it's sorted by highest initiative
# NOTE: Right now, the monster and player arrays are created in the driver
def combo_sort(players, mobs):

    # create returned array
    temp = []

    # Loops the number of elements in player array
    for s in players:
        # Append each character in the players' array to temp
        temp.append(s)

    # Do the same for mobs' array
    for t in mobs:
        temp.append(t)

    # Now that we have a single array with both groups (NPC and PC) we can sort it by initiative.
    temp.sort(key=sortele, reverse=True)

    # Return the sorted array
    return temp


# A helper function to sort the initiatives in combo_sort()
def sortele(val):
    return val.getinit()


# Defines a function to logically track a round on game play
# arguments => plist = players array, mlist = mobs array, ilist = initiative array, file = write_to.txt
def one_round(plist, mlist, ilist, file):
    # Get the size of the initiative list
    size = len(ilist)
    # Loop through the size if ilist times and check if both groups have characters still alive
    for x in range(size):
        # Test both player and mob lists and see if anyone is alive
        if are_dead(plist) or are_dead(mlist):
            # If every monster is dead
            if are_dead(mlist):
                print("The rest of the initiative round has been cancelled.  All enemy mobs have been taken care of.\n")
            # If every PC is dead
            else:
                print("The rest of the initiative round has been cancelled.  Unfortunately, your entire group has died.\n")
        # If there are still group members alive by the character whose turn it is is dead
        elif ilist[x].getdead():
            print(colored("Skipping", 'red'), ilist[x].getname(), colored("because they are dead.", 'red'), "\n")
        # Else there are living characters for both PC and mobs so the round continues
        else:
            input("Press ENTER to continue... \n")
            print("Next up............")
            ilist[x].printname()
            # Timer between initiatives, currently just a simple 2 second snooze
            # Original designs was for the sleep timer to be 45 secs, instantiation comment out below
            time.sleep(2)
            print("The clock begins now.  You have 30 seconds to decide a course of action.\n")
            #sleep_timer(ilist)
            # After the timer, the character has taken his turn and battle_menu() is called to document it
            battle_menu(ilist, ilist[x].getname(), plist, mlist, file)

# This will print a message to count down the timer
# def sleep_timer(arr):
#     print()

# Function that takes an array (mob or player) and returns a boolean
# True means the group is dead, False means someone lives
def are_dead(arr):
    # initialize tracker which keep up with all the dead PC/NPC in list
    tracker = 0
    # Open list
    for c in arr:
        # Test if the element in list is true or false (dead or alive)
        # print(p, "Inside areDead()")
        if c.getdead():
            # If dead, increment tracker
            tracker += 1
    # Test if the entire group is dead
    # If tracker (num of dead) is same and list, then group is dead
    if tracker == len(arr):
        # print(tracker, "From if at the end....  Everyone is dead...")
        return True
    # If they aren't the same, then someone is still alive
    else:
        return False



# DRIVER SECTION

def auto_fill(mlist, plist, f):
    # Select number of players and mobs
    numPlayers = 7
    numMobs = 2

    # Instantiate a class for each player and mob
    # p1 = Character("Michael", 0, 34, False)
    p2 = Character("Burns", 0, 32, False)
    p3 = Character("Teddy", 0, 31, False)
    p4 = Character("Matt", 0, 25, False)
    p5 = Character("Tommy", 0, 35, False)
    p6 = Character("Phil", 0, 27, False)
    p7 = Character("Fri", 0, 24, False)
    p8 = Character("Nathan", 0, 29, False)

    # Push the instantiated player classes into player array
    # pArr.append(p1)
    plist.append(p2)
    plist.append(p3)
    plist.append(p4)
    plist.append(p5)
    plist.append(p6)
    plist.append(p7)
    plist.append(p8)

    # Do the same to mobs
    m1 = Character("boar", 0, 42, False)
    m2 = Character("rhino", 0, 45, False)

    mlist.append(m1)
    mlist.append(m2)

    # Call combo sort of combine the player and mob array into a single sorted intiative array
    cArr = combo_sort(plist, mlist)

    # Call the menu to start the program
    # menu(pArr, mArr, cArr, f)

   # # When done, close the file
   #  f.close()

def manual_fill(mlist, plist, f):
    group_size = input("Let's start with the player character groups.  How many are there?")
    group_size = int(group_size)
    for x in range(group_size):
        char_name = input("What is the name of player?\n")
        char_max_hp = input("What is their max hit points?\n")
        char_max_hp = int(char_max_hp)
        char = Character(char_name, 0, char_max_hp, False)
        plist.append(char)

    mob_group = input("And onto the Mob and Monster list.  How many this encounter?\n")
    mob_group = int(mob_group)
    for y in range(mob_group):
        mob_name = input("What do you want to call this mob?\n")
        mob_max_hps = input("What is mob's max hit points?\n")
        mob_max_hps = int(mob_max_hps)
        mob = Character(mob_name, 0, mob_max_hps, False)
        mlist.append(mob)


def char_setup(request, mlist, plist, f):
    if request == 'n':
        auto_fill(mlist, plist, f)
    elif request == 'N':
        auto_fill(mlist, plist, f)
    elif request == 'y':
        manual_fill(mlist, plist, f)
        for p in plist:
            p.fullprint()
    elif request == 'Y':
        manual_fill(mlist, plist, f)
    else:
        print("I could not understand what you typed. something like '", request, "'")
        try_again = input("Please try again or type 'exit' to leave the system.\n")
        if try_again == 'exit':
            print("Goodbye.")
            return
        else:
            char_setup(try_again, mlist, plist, f)

    # Call combo sort of combine the player and mob array into a single sorted intiative array
    clist = combo_sort(plist, mlist)
    menu(plist, mlist, clist, f)




def sys_driver():
    # Open document for writing
    f = open("battle.txt", "w")

    # Inititialize player and mob arrays to null
    pArr = []
    mArr = []

    request = input("Type 'y' if you wish to create your own character lists,\nOr type 'n' to use the preset lists.\n")
    print("This is the pwd: ", request)

    char_setup(request, mArr, pArr, f)

    f.close()


sys_driver()
