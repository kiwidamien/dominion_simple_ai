import pytest
import dominion_ai.menu.menu as dmenu

def test_print_dmenu():
    print(dmenu.DEFAULT_MENU)


def test_default_menu_has_one_choice():
    assert dmenu.DEFAULT_MENU.num_choices == 1


def test_empty_string_valid():
    assert dmenu.DEFAULT_MENU.validate('') == True
    assert dmenu.DRAW_DISCARD_MENU.validate('') == True
    assert dmenu.DRAW_DISCARD_CURSE_MENU.validate('') == True
