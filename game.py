'''
Module with classes
'''
import time
import blessed

term = blessed.Terminal()

global defeated_num
defeated_num = 0


class Hero:
    '''
    Class for Hero - main character - representation
    '''
    def __init__(self):
        self.victories = 0
        self.coins = 0
        self.hp = 100

    def damage(self, points):
        self.hp -= points
        if self.hp <= 0:
            self.hp = 0

    def recover(self, points):
        self.hp += points
        if self.hp > 100:
            self.hp = 100

    def alive(self):
        '''
        Checks if hero is alive. Returns bool value True if yes (hp > 0), False otherwise
        '''
        return bool(self.hp)


class Location:
    def __init__(self, name):
        self.name = name
        self.linked_locs = []
        self.characters = []
        self.items = []

    def set_description(self, description):
        self.description = description

    def link_loc(self, loc):
        self.linked_locs.append(loc)

    def set_character(self, character):
        self.characters.append(character)

    def set_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items

    def get_details(self):
        print(self.name, '-', self.description)

    def move(self, goto_loc):
        for linked_loc in self.linked_locs:
            if linked_loc.name == goto_loc:
                return linked_loc
        print('fail')
        return self

    def get_characters(self):
        return self.characters


class Item:
    def __init__(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def describe(self):
        print(self.name, '-', self.description + term.bold(f'  Damage: {self.damage}'))

    def get_name(self):
        return self.name

    def set_damage(self, damage):
        self.damage = damage


class Character:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def describe(self):
        print(self.name, '-', self.description)

    def set_conversation(self, conversation):
        self.conversation = conversation

    def talk(self):
        for thesis in self.conversation:
            print(thesis)
            time.sleep(0.075)



class Enemy(Character):
    def __init__(self, *attrs):
        super().__init__(*attrs)
        self.passable = True

    def set_properties(self, hp, damage):
        self.hp = hp
        self.damage = damage

    def fight(self, fight_with):
        fight_damage = max(self.hp//fight_with, 1) * self.damage
        return fight_damage

    def get_defeated(self):
        return defeated_num

    def not_passable(self):
        self.passable = False

    def describe(self):
        print(self.name, '-', self.description, term.bold(f'HP: {self.hp}, Damage: {self.damage}'))

    def set_drop(self, item):
        self.drop_item = item

    def get_drop_item(self):
        return self.drop_item

class Friend(Character):
    pass

