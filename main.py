'''
Main module
'''
import time
import blessed
import game

term = blessed.Terminal()

def read_conversation(filename, hero_first):
    '''
    This function reads conversations from files and returns the list of formated thesis
    '''
    conversation_list, counter = [], 0
    with open('./conversations/'+filename, 'r') as conv_file:
        for line in conv_file:
            line = line.strip()
            speaker = 'Me: ' if counter%2!=int(hero_first) else filename[:-4].capitalize() + ': '
            conversation_list.append(speaker + line)
            counter += 1

    return conversation_list


def main_game():
    '''
    Main function that organises the flow of the game
    '''
    print_intro_screen()

    reception = game.Location('Reception')
    reception.set_description('Sheptytsky Center reception on the first floor next to entrance.\
With monitors, termometer and guards')

    basement = game.Location('Basement')
    basement.set_description('Sheptytsky Center Underground Basement with lots of tables,\
chairs, desks and sofas to study')

    it_space = game.Location('IT Space')
    it_space.set_description('Basement in Academic Corps with tables and comfortable chairs')

    trapezna = game.Location('Trapezna')
    trapezna.set_description('Place to eat. Large room with tables')

    striysky_park_south = game.Location('Stryiskyi Park South Side Entrance')
    striysky_park_south.set_description('Dark park. Nobody knows what a mistery and dangerous\
creatures hides inside')

    railway_station = game.Location('Children Railway Station')
    railway_station.set_description('Forgoten and abandoned childrens railway station.\
Old building and trains')

    striysky_park_fountain = game.Location('Stryiskyi Park Fountain')
    striysky_park_fountain.set_description('Fountain in Stryiskyi Park, with some\
infrastructure around')


    luno = game.Item('LUNO')
    luno.set_description('Mysterious and powerful object')
    luno.set_damage(150)


    guard = game.Character('Guard', 'Angry guard, you\'d better not mess up with him')
    guard_conv = read_conversation('guard.txt', False)
    guard.set_conversation(guard_conv)

    lotr1 = game.Enemy('Lotr 1', 'Aggressive tall and slim jerk, blocking you way')
    lotr1.set_properties(5, 7)
    lotr1_conv = read_conversation('lotr1.txt', False)
    lotr1.set_conversation(lotr1_conv)
    lotr1.not_passable()

    lotr2 = game.Enemy('Lotr 2', 'Angry fat but slow lotr, blocking you way')
    lotr2.set_properties(40, 3)
    lotr2_conv = read_conversation('lotr2.txt', False)
    lotr2.set_conversation(lotr2_conv)
    lotr2.not_passable()

    alcoholic = game.Enemy('Alcoholic', 'Old mysterous homeless alcoholic with white beard')
    alcoholic.set_properties(10, 10)
    alcoholic_conv = read_conversation('alcoholic.txt', False)
    alcoholic.set_conversation(alcoholic_conv)
    alcoholic.set_drop(luno)

    abaddon = game.Enemy('Abaddon', 'Mighty creature, blocking you way to win')
    abaddon.set_properties(125, 75)
    abaddon_conv = read_conversation('abaddon.txt', False)
    abaddon.set_conversation(abaddon_conv)
    abaddon.not_passable()


    vendor = game.Character('Vendor', 'Polite vendor in Trapezna')
    vendor_conv = read_conversation('vendor.txt', False)
    vendor.set_conversation(vendor_conv)

    spider = game.Enemy('Spider', 'Tiny spider hidding in his corner')
    spider.set_properties(1, 3)
    spider_conv = read_conversation('spider.txt', True)
    spider.set_conversation(spider_conv)

    hero = game.Hero()

    basement.link_loc(reception)
    reception.link_loc(striysky_park_south)
    reception.link_loc(it_space)
    reception.link_loc(trapezna)
    it_space.link_loc(trapezna)
    it_space.link_loc(striysky_park_south)
    it_space.link_loc(reception)
    trapezna.link_loc(reception)
    trapezna.link_loc(it_space)
    trapezna.link_loc(striysky_park_south)
    striysky_park_south.link_loc(railway_station)
    striysky_park_south.link_loc(striysky_park_fountain)
    striysky_park_south.link_loc(trapezna)
    striysky_park_south.link_loc(it_space)
    striysky_park_south.link_loc(reception)
    railway_station.link_loc(striysky_park_fountain)
    railway_station.link_loc(striysky_park_south)


    trapezna.set_character(vendor)
    reception.set_character(guard)
    striysky_park_south.set_character(lotr1)
    striysky_park_south.set_character(lotr2)
    it_space.set_character(spider)
    railway_station.set_character(alcoholic)
    striysky_park_fountain.set_character(abaddon)

    pencil = game.Item('Pencil')
    pencil.set_description('Sharp gray pencil')
    pencil.set_damage(20)
    basement.set_item(pencil)

    current_location = basement
    previous_location = None
    backpack = {}


    while True:
        time.sleep(0.9)
        print('\n')
        print(term.bold(f'HP: {hero.hp}'))
        print(f'{term.bold("BKPCK: ")}', end='')
        print(', '.join(backpack.keys()))
        time.sleep(0.2)
        could_pass = True
        current_location.get_details()
        time.sleep(0.3)

        personages, personages_dict = current_location.get_characters(), {}
        fightable_personages_dict = {}
        for personage in personages:
            time.sleep(0.1)
            personage.describe()
            personages_dict[personage.name] = personage
            if isinstance(personage, game.Enemy):
                fightable_personages_dict[personage.name] = personage
                could_pass = could_pass and personage.passable


        if current_location.name == 'Stryiskyi Park Fountain':
            if could_pass:
                print('Yey, you won')
                return
            print('This is the last stage. Defeat enemy, who block your pass here and you win')

        items, items_dict = current_location.get_items(), {}
        for item in items:
            item.describe()
            items_dict[item.name] = item

        print()
        linked_locs = []
        print(f'{term.bold("[GO]:    ")}', end='')
        for loc in current_location.linked_locs:
            linked_locs.append(loc.name)
        print(', '.join(linked_locs))
        time.sleep(0.1)

        print(f'{term.bold("[TAKE]:  ")}', end='')
        print(', '.join(items_dict.keys()))
        time.sleep(0.1)

        print(f'{term.bold("[TALK]:  ")}', end='')
        print(', '.join(personages_dict.keys()))
        time.sleep(0.1)

        print(f'{term.bold("[FIGHT]: ")}', end='')
        print(', '.join(fightable_personages_dict.keys()))
        time.sleep(0.1)


        command = input('> ')

        if command.lower() == 'go':
            if not could_pass:
                print('It was a trap, you should defeat enemy who is blocking your way ahead')
                print('But still, you can return to the previous location. Returning...')
                current_location, previous_location = previous_location, current_location
            elif len(linked_locs) > 1:
                print('Where you want to go?')
                goto_loc = input('> ')
                if goto_loc in linked_locs:
                    previous_location = current_location
                    current_location = current_location.move(goto_loc)
                else:
                    print(f'There is no such location as {goto_loc}')
            else:
                previous_location = current_location
                current_location = current_location.move(linked_locs[0])

        elif command.lower() == 'talk':
            if personages_dict:
                if len(personages_dict) > 1:
                    print('Whom you want to talk to?')
                    talkto_personage = input('> ')
                    if talkto_personage in list(personages_dict.keys()):
                        personages_dict[talkto_personage].talk()
                    else:
                        print(f'Your can\'t talk to {talkto_personage}')
                else:
                    personages_dict[list(personages_dict.keys())[0]].talk()
            else:
                print('There is nobody to talk to')

        elif command.lower() == 'take':
            if items_dict:
                if len(items_dict) > 1:
                    print('What you wann take?')
                    for item in items_dict:
                        print(item)
                        time.sleep(0.1)
                    take_item = input('> ')
                    if take_item in list(items_dict.keys()):
                        backpack[take_item] = items_dict[take_item]
                        current_location.items.remove(items_dict[take_item])
                    else:
                        print(f'Your can\'t take to {take_item}')
                else:
                    backpack_item_key = list(items_dict.keys())[0]
                    backpack[backpack_item_key] = items_dict[backpack_item_key]
                    current_location.items.remove(items_dict[backpack_item_key])
                    print(f'Put {backpack_item_key} in backpack')

            else:
                print('There is nothing to take')

        elif command.lower() == 'fight':
            if fightable_personages_dict:
                if len(fightable_personages_dict) > 1:
                    print('Whom you want to fight with?')
                    fightwith_personage = input('> ')
                    if fightwith_personage not in list(fightable_personages_dict.keys()):
                        print(f'You can\'t fight with {fightwith_personage}')
                        continue
                else:
                    fightwith_personage = list(fightable_personages_dict.keys())[0]

                adverser = fightable_personages_dict[fightwith_personage]
                print('What you wanna fight with?')
                for fightwith_item in backpack:
                    backpack[fightwith_item].describe()
                fightwith_item = input('> ')
                if fightwith_item in backpack:
                    fight_damage = adverser.fight(backpack[fightwith_item].damage)
                    hero.hp -= fight_damage
                    if hero.hp > 0:
                        hero.victories += 1
                        print('Congrats, you won. Remaining health:', hero.hp)
                        try:
                            current_location.set_item(adverser.get_drop_item())
                        except AttributeError:
                            pass
                        current_location.characters.remove(adverser)
                    else:
                        print('Oups, you are dead.')
                        break
                else:
                    print(f'You have no {fightwith_item}')
            else:
                print('There is nobody to fight with')
        else:
            print('Hmm, seems like a wrong command')


def print_intro_screen():
    '''
    This function print main screen infomation and legend
    '''
    print('It\'s Friday.', 'You are sitting in Sheptytsky Center Basement for 5 hour now\
in attempt to finish your project.', 'You can\'t go home, deadline ends in 13 minutes but you still\
have some work to do.', 'You wasn\'t watching at clock for a couple of hour so you don\'t\
know time.', 'Finally, you did it, you finished you work and glanced at clock terrified:\
it\'s 22:17 PM.', 'Outside darkness covered the streets. Time to go home.\n',
'In order to win you should survive and arrive to Sheptytsky Park Fountain', sep='\n')


if __name__ == '__main__':
    main_game()
