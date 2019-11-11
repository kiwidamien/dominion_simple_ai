from typing import List, Optional

from dominion_ai.menu.menu_item import MenuItem, PlayGameItem


class Menu:
    def __init__(self, menu_items: List[MenuItem],
                 header_prompt=''):
        self.menu_items = menu_items
        self.header_prompt = header_prompt
        self.allowed_responses = [''] + [str(index + 1) for index in range(len(menu_items))]
        self.default = PLAY_MOVE

    def __str__(self, n_tabs:int = 1):
        sep = '\t' * n_tabs
        choice_str = [f'{sep}{index+1:2d}. {menu_item}' for index, menu_item
                        in enumerate(self.menu_items)]
        return '\n'.join(choice_str)

    def __repr__(self):
        return f'Menu object with {len(self.menu_items)} choices'

    def validate(self, choice: str) -> bool:
        choice = choice.strip()
        if choice == '':
            return True

        opt, *args = choice.split()
        try:
            opt = int(float(opt))
        except:
            print(f'Invalid choice {opt}')
            return False

        index = opt - 1
        try:
            menu_item_chosen = self.menu_items[index]
        except IndexError:
            print(f"Menu option {opt} doesn't correspond to a valid number")
        return menu_item_chosen.validate(args)

    def get_menu_item(self, choice: str) -> Optional[MenuItem]:

    def do_round(self):
        if self.header_prompt:
            print(self.header_prompt)
        if len(self.menu) == 0:
            end_prompt = "\nPress Enter to take a turn...\n"
        else:
            end_prompt = "Make a choice, or press Enter to move to the next phase"
            print(self)
        choice = input(end_prompt)
        if not self.validate(choice):
            self.do_round()
        else:
            self.
