import curses as C
import time
import json

(STATE_CORRECT, STATE_INCORRECT, STATE_BLANK) = (1,2,3)

class Harf:
    def __init__(self, character:str, state:int=STATE_BLANK, press_time:int = 0):
        self.character = character
        self.state = state
        self.press_time = press_time

    def __repr__(self):
        return f'({self.character}), ({self.state}), ({self.press_time})'

    def __str__(self):
        return f'({self.character}), ({self.state}), ({self.press_time})'



paragraphs = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,",
              "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,",
              "sunt in culpa qui officia deserunt mollit anim id est laborum."]




cursed_screen = C.initscr()
C.start_color()
C.init_pair(1, C.COLOR_GREEN, C.COLOR_BLACK)
C.init_pair(2, C.COLOR_WHITE, C.COLOR_BLACK)
C.init_pair(3, C.COLOR_RED, C.COLOR_BLACK)
C.init_pair(4, C.COLOR_YELLOW, C.COLOR_BLACK)


for paragraph in paragraphs:

    start_time = time.time()
    par_arr = [Harf(x) for x in paragraph] 
    
    paragraph_len = len(paragraph)
    first_space = paragraph.index(' ') 

    last_char = ''
    last_edit_pos = 0
    last_word_start = 0
    last_word_stop = first_space
    typed_word = ''
    done = False
    typing_speed = 0

    get_current_char = lambda: paragraph[last_edit_pos]
    is_typed_correctly = lambda: last_char == get_current_char()

    
    i=0
    while i < paragraph_len:
        cursed_screen.clear()
        

        # ekrana paragrafı yazdır
        j = 0
        while j < paragraph_len:
            if par_arr[j].state == STATE_CORRECT:
                cursed_screen.addstr(3, j, par_arr[j].character, C.color_pair(4))
            elif par_arr[j].state == STATE_INCORRECT:
                cursed_screen.addstr(3, j, par_arr[j].character, C.color_pair(3))
                
            else: # state_blank
                if last_word_start <= j < last_word_stop:
                    if j == last_edit_pos: 
                        cursed_screen.addstr(3, j, par_arr[j].character, C.color_pair(1))
                    else:
                        cursed_screen.addstr(3, j, par_arr[j].character, C.color_pair(2))
                else:
                    cursed_screen.addnstr(3, j, par_arr[j].character, C.color_pair(1))
       
            j += 1

        cursed_screen.refresh()
        # ~ ekrana paragrafı yazdır

        last_char = cursed_screen.getch()

        if last_char == 27:
            cursed_screen.clear()
            C.endwin()
            exit(0)

        if chr(last_char) == par_arr[i].character:
            par_arr[i].state = STATE_CORRECT
            par_arr[i].press_time = time.time()
        else:
            par_arr[i].state = STATE_INCORRECT
            par_arr[i].press_time = time.time()

        print(par_arr , end='\n' , file=open('outfile.txt', 'w+'))

        cursed_screen.refresh()




        last_edit_pos += 1
        last_char = paragraph[last_edit_pos]
        if last_char == ' ':
            last_word_start = last_edit_pos
            last_word_stop = paragraph.index(' ', last_edit_pos+1)
            typed_word = paragraph[last_word_start:last_word_stop-1]
            correct_word = paragraph[last_word_start:last_word_stop]

        if last_edit_pos == paragraph_len-1:
            pass
        gecen_time = time.time() - start_time
        typing_speed = len(paragraph) / gecen_time * 60 / 5
        cursed_screen.addstr(0, 10, f'Typing speed: {typing_speed:.2f} words per minute')
        cursed_screen.refresh()
        C.napms(100)
            # print(f'Typing speed: {typing_speed:.2f} words per minute')

        i += 1
            




cursed_screen.clear()
C.endwin()

