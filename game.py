global defeated_num
defeated_num = 0

class Room:
    def __init__(self, name):
        self.name = name
        self.linked_rooms = []
        self.character = None
        self.item = None

    def set_description(self, description):
        self.description = description

    def link_room(self, room, side):
        self.linked_rooms.append([room, side])

    def set_character(self, character):
        self.character = character

    def set_item(self, item):
        self.item = item

    def get_item(self):
        return self.item

    def get_details(self):
        print(self.name)
        print('--------------------')
        print(self.description)
        for room in self.linked_rooms:
            print(f'{room[0].name} is {room[1]}')

    def move(self, command):
        for linked_room, side in self.linked_rooms:
            if side == command:
                return linked_room
        return self

    def get_character(self):
        return self.character


class Item:
    def __init__(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def describe(self):
        print(f'The [{self.name}] is here - {self.description}')

    def get_name(self):
        return self.name


class Character:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def describe(self):
        print(f'{self.name} is here!')
        print(self.description)

    def talk(self):
        print(self.conversation)


class Enemy(Character):
    def __init__(self, *attrs):
        super().__init__(*attrs)

    def set_conversation(self, conversation):
        self.conversation = conversation
    
    def set_weakness(self, weakness):
        self.weakness = weakness

    def fight(self, fight_with):
        if self.weakness == fight_with:
            global defeated_num
            print('defeated here:', defeated_num)
            defeated_num += 1
            return True
        return False

    def get_defeated(self):
        return defeated_num


class Friend(Character):
    pass

