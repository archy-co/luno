'''
Module with classes
'''
import time
import blessed

term = blessed.Terminal()


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
        '''
        This method is not used yet, but potentially could be realized to recover health with
        consumables
        '''
        self.hp += points
        if self.hp > 100:
            self.hp = 100


class Location:
    def __init__(self, name):
        self.name = name
        self.linked_locs = []
        self.characters = []
        self.items = []

    def set_description(self, description):
        self.description = description

    def link_loc(self, loc):
        '''
        Links another location to current location. It is ignorant to direction
        '''
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
        '''
        Moves location to new
        '''
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
        'This method prints thesis of speacers in conversation'
        for thesis in self.conversation:
            print(thesis)
            time.sleep(0.15)



class Enemy(Character):
    def __init__(self, *attrs):
        super().__init__(*attrs)
        self.passable = True

    def set_properties(self, hp, damage):
        '''
        This method sets enemies properties: health points and damage
        '''
        self.hp = hp
        self.damage = damage

    def fight(self, fight_with):
        '''
        This method returns damage, taken during the fight
        '''
        fight_damage = max(self.hp//fight_with, 1) * self.damage
        return fight_damage

    def not_passable(self):
        '''
        This method sets passable value of enemy. If enemy is not passable, hero can\'t go
        further without defeating him
        '''
        self.passable = False

    def describe(self):
        print(self.name, '-', self.description, term.bold(f'HP: {self.hp}, Damage: {self.damage}'))

    def set_drop(self, item):
        self.drop_item = item

    def get_drop_item(self):
        return self.drop_item
