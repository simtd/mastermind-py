import tkinter as tk
from tkinter import messagebox
import random


class MasterMind:
    def __init__(self):
        self.colors = ["red", "yellow", "green", "orange",
                       "pink", "purple", "blue", "white"]
        self.colors_computer = []
        self.pick_length = 0  # amount of columns
        self.computer_picks_colors()
        self.counter = 0  # column counter

    def computer_picks_colors(self):
        columns = 4
        random_can_repeat = random.choices(self.colors, k=columns)
        random_no_repetition = random.sample(self.colors, k=columns)
        random_types_list = [random_can_repeat, random_no_repetition]
        self.colors_computer = random.choices(random_types_list, k=1,
                                              weights=[1, 3])[0]
        self.pick_length = len(self.colors_computer)
        # print(self.colors_computer)

    def compare_colors(self, picked_colors):
        """makes a list of the same colors in colors_computer and
        picked_colors, then makes a list of either yellow or red:
        -red means color exists and have same index in both lists
        -yellow means color just exists somewhere without same index in both"""
        same_colors = []
        picked_colors_copy = picked_colors.copy()
        for color in self.colors_computer:
            if color in picked_colors_copy:
                picked_colors_copy.remove(color)
                same_colors.append(color)

        colors_placing_info = []
        # making all yellow first:
        for color in same_colors:
            colors_placing_info.append(self.colors[1])
        # replacing amount that has same index with red
        for i in range(len(self.colors_computer)):
            if self.colors_computer[i] == picked_colors[i]:
                colors_placing_info[
                    colors_placing_info.index(self.colors[1])
                ] = self.colors[0]
        return sorted(colors_placing_info)

    def counter_reset(self):
        self.counter = 0
        return self.counter

    def counter_set_value(self, value):
        self.counter = value
        return self.counter

    def counter_move(self, direction, change_counter=True):
        """moves the counter forward or backward
        Arguments:
            direction {str} -- either "r" (right) or "l" (left)

        Keyword Arguments:
            change_counter {bool} -- decides wheter calling the function
            changes the actual counter or not. (default: {True})

        Returns:
            int -- an index of next or previous value of the counter
        """
        if direction == "r":  # move right
            if change_counter:
                self.counter = self.counter_next(self.counter)
                return self.counter
            else:
                a_counter = self.counter_next(self.counter)
                return a_counter
        elif direction == "l":  # move left
            if change_counter:
                self.counter = self.counter_previous(self.counter)
                return self.counter
            else:
                a_counter = self.counter_previous(self.counter)
                return a_counter

    def counter_next(self, counter_int):
        if counter_int == self.pick_length-1:
            counter_int = 0
        else:
            counter_int += 1
        return counter_int

    def counter_previous(self, counter_int):
        if counter_int == 0:
            counter_int = self.pick_length-1
        else:
            counter_int -= 1
        return counter_int


class GUI:
    def __init__(self, mastermind_object):
        self.mastermind = mastermind_object
        self.has_won = False
        self.has_lost = False
        self.colors_placing_info = []
        self.color_idx = self.mastermind.counter  # indicates current column
        self.row_counter = -1  # starts from bottom row
        self.row_amount = 11
        self.colors_computer = self.mastermind.colors_computer
        self.pick_length = self.mastermind.pick_length
        self.chosen_colors = []
        self.winning_info = []  # using this to compare with actual info result
        for i in range(self.pick_length):
            self.winning_info.append(self.mastermind.colors[0])
            self.chosen_colors.append(0)  # makes chosen_colors an zero-list
        # random background from selection
        # self.background_colors = ["lightslategray", "cadetblue", "rosybrown"]
        # self.background_color = random.choices(self.background_colors,
        #                                        k=1, weights=[5, 1, 1])
        self.background_color = "lightslategray"
        self.outline_color = "black"
        self.outline_color_highlight = "white"

        # master window:
        self.width, self.height = 300, 550
        self.window = tk.Tk()
        self.window.geometry(f"{self.width+30}x{self.height}")
        self.window.configure(bg=self.background_color)
        self.window.title("Mastermind")
        self.window.resizable(width=False, height=False)
        self.window.columnconfigure(2, weight=1)
        self.window.update()

        self.width_piece = self.width*(1/6)

        # placement info canvas:
        self.canvas_info = tk.Canvas(
            self.window, bg=self.background_color, highlightthickness=0,
            height=self.height, width=self.width_piece
        )
        self.canvas_info.grid(column=0, row=0)

        # main canvas:
        self.canvas_main = tk.Canvas(
            self.window, bg=self.background_color, highlightthickness=0,
            height=self.height, width=self.width_piece*4
        )
        self.canvas_main.grid(column=1, row=0)

        # button frames:
        self.button_frame = tk.Frame(self.window, bg=self.background_color)
        self.button_frame.grid(column=2, row=0)
        self.button_width, self.button_heigth = 5, 3

        # color buttons:
        self.color_buttons = []
        for idx, color in enumerate(self.mastermind.colors):
            self.color_buttons.append(
                tk.Button(master=self.button_frame,
                          text=color.title(), width=self.button_width,
                          height=self.button_heigth,
                          command=lambda s=color: self.add_color_choice(s)
                          )
            )
            self.color_buttons[idx].grid(column=0, row=idx+1)

        # submit button:
        self.submit_button = tk.Button(
            self.button_frame, text=">",
            width=self.button_width, height=self.button_heigth,
            command=self.enter_colors
        )
        self.submit_button.grid(row=len(self.color_buttons)+2)

        # forward/backward frame
        self.move_buttons_frame = tk.Frame(self.button_frame,
                                           bg=self.background_color)
        self.move_buttons_frame.grid(row=len(self.color_buttons)+1, pady=6)

        # forward button
        self.forward_button = tk.Button(
            self.move_buttons_frame, text="->",
            width=self.button_width-2, height=self.button_heigth-1,
            command=self.move_forward
        )
        self.forward_button.grid(row=0, column=1)

        # backward button
        self.backward_button = tk.Button(
            self.move_buttons_frame, text="<-",
            width=self.button_width-2, height=self.button_heigth-1,
            command=self.move_backward
        )
        self.backward_button.grid(row=0, column=0)

        # creating color circles:
        self.color_circles = []
        self.draw_color_circles()
        self.color_circles_rows = self.divide_list(self.color_circles,
                                                   self.pick_length)
        for i in range(self.pick_length):  # making secret code gray
            self.canvas_main.itemconfig(
                self.color_circles_rows[0][i], fill="gray"
            )
        self.highlight_color_circles()

        # creating info circles:
        self.info_cirles = []
        self.draw_info_circles()
        self.info_cirles_rows = self.divide_list(self.info_cirles,
                                                 self.pick_length)

        tk.mainloop()

    def divide_list(self, lst, n):
        """divides a list into n-sized chunks"""
        divided_list = []
        for i in range(0, len(lst), n):
            divided_list.append(lst[i:i + n])
        return divided_list

    def add_color_choice(self, color):
        """colored buttons - adding to chosen colors, advanced indexing,
        calling filling+highlight"""
        self.chosen_colors[self.color_idx] = color

        if 0 in self.chosen_colors:  # if there is an empty spot

            if (self.chosen_colors[
                self.mastermind.counter_move("r", change_counter=False)
            ]) != 0:  # if next circle is filled

                # jumping to first unfilled circle:
                zero_index = self.chosen_colors.index(0)
                self.color_idx = self.mastermind.counter_set_value(zero_index)
            else:
                self.color_idx = self.mastermind.counter_move("r")
        else:
            self.color_idx = self.mastermind.counter_move("r")

        self.canvas_main.after(20, self.fill_color_circles)
        self.highlight_color_circles()

    def enter_colors(self):
        """submit button - get placement info, go to next row,
        clear chosen colors, call coloring previous info circles,
        check if winning or loosing, call highlighting"""
        if 0 not in self.chosen_colors:  # if chosen colors is full
            self.colors_placing_info = self.mastermind.compare_colors(
                self.chosen_colors)
            for i in range(self.pick_length):  # clear chosen colors
                self.chosen_colors[i] = 0
            self.color_idx = self.mastermind.counter_reset()
            self.row_counter -= 1
        self.fill_info_circles()

        # winning or losing
        if self.colors_placing_info == self.winning_info:
            self.winning()
        elif -(self.row_counter) > (self.row_amount)-1:
            self.loosing()

        # highlighting
        if not self.has_won and not self.has_lost:
            self.highlight_color_circles()
        self.highlight_clear_row()

    def create_circle(self, x, y, r, canvas_name):  # coordinates, radius
        spaciousness = 5
        r -= spaciousness
        x0 = x + spaciousness
        y0 = y + spaciousness
        x1 = x + r
        y1 = y + r
        circle_id = canvas_name.create_oval(x0, y0, x1, y1)
        return circle_id

    def draw_color_circles(self):
        y_coord = 0
        x_coords = []
        for i in range(self.pick_length):
            x_coords.append(self.width_piece*i)

        radius = self.width_piece
        for row in range(self.row_amount):
            self.color_circles.append(
                self.create_circle(x_coords[0], y_coord, radius,
                                   self.canvas_main)
            )
            for idx in range(3):
                self.color_circles.append(
                    self.create_circle(x_coords[idx+1], y_coord, radius,
                                       self.canvas_main)
                )
            y_coord += self.width_piece

    def fill_color_circles(self):
        for idx, color in enumerate(self.chosen_colors):
            if color != 0:
                self.canvas_main.itemconfig(
                    self.color_circles_rows[self.row_counter][idx], fill=color
                )

    def highlight_color_circles(self):
        self.canvas_main.itemconfig(
            self.color_circles_rows[self.row_counter][self.color_idx],
            outline=self.outline_color_highlight
        )
        for i in range(self.pick_length):
            if i != self.color_idx:
                self.canvas_main.itemconfig(
                    self.color_circles_rows[self.row_counter][i],
                    outline=self.outline_color
                )

    def highlight_clear_row(self):
        for i in range(self.pick_length):
            self.canvas_main.itemconfig(
                self.color_circles_rows[self.row_counter+1][i],
                outline=self.outline_color
            )

    def draw_info_circles(self):
        y_coord = self.width_piece
        x_coords = [0, self.width_piece//2]

        radius = self.width_piece//2
        for row in range((self.row_amount-1)*2):
            self.color_circles.append(
                self.create_circle(x_coords[0], y_coord, radius,
                                   self.canvas_info)
            )
            self.color_circles.append(
                self.create_circle(x_coords[1], y_coord, radius,
                                   self.canvas_info)
            )
            y_coord += self.width_piece//2

    def fill_info_circles(self):
        for idx, color in enumerate(self.colors_placing_info):
            self.canvas_info.itemconfig(
                self.color_circles_rows[self.row_counter][idx], fill=color
            )

    def move_forward(self):
        self.color_idx = self.mastermind.counter_move("r")
        self.highlight_color_circles()

    def move_backward(self):
        self.color_idx = self.mastermind.counter_move("l")
        self.highlight_color_circles()

    def winning(self):
        self.has_won = True
        self.show_secret_code()
        self.disable_buttons()
        tries = (-self.row_counter)-1
        if tries == 1:
            message = ("What is going on??? You guessed the correct code "
                       f"with only {tries} try! Nice.")
        elif tries == self.row_amount-1:
            message = ("Correct code! Phew! "
                       f"You spent all of your {tries} tries.")
        else:
            message = ("Well done! You guessed the correct code in "
                       f"{(-self.row_counter)-1} tries.")
        messagebox.showinfo(message=message, parent=self.window)

    def loosing(self):
        self.has_lost = True
        self.show_secret_code()
        self.disable_buttons()
        message = "Looks like you ran out of tries! You Lost."
        messagebox.showinfo(message=message, parent=self.window)

    def show_secret_code(self):
        for idx, color in enumerate(self.mastermind.colors_computer):
            self.canvas_main.itemconfig(
                self.color_circles_rows[0][idx], fill=color
            )

    def disable_buttons(self):
        for button in self.color_buttons:
            button["state"] = "disabled"
        self.submit_button["state"] = "disabled"
        self.forward_button["state"] = "disabled"
        self.backward_button["state"] = "disabled"


if __name__ == "__main__":
    mastermind_object = MasterMind()
    game = GUI(mastermind_object)
