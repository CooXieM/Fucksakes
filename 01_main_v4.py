import tkinter
from tkinter import *
from math import *
from functools import partial


class Converter:

    def __init__(self):

        # initialise variables such as feedback
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []
        button_font = ("Arial", "12", "bold")
        # set up GUI Frame
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()
        self.temp_heading = Label(self.temp_frame,
                                  text="Temperature Converter",
                                  font=("Arial", "16", "bold"),
                                  )
        self.temp_heading.grid(row=0)

        instructions = "Please enter a temperature in the box below " \
                       "then press one of the buttons to convert " \
                       "your temperature from Celsius or Fahrenheit"
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wrap=250, width=40,
                                       )
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Arial", "12")
                                )
        self.temp_entry.grid(row=2, padx=10, pady=10)

        error = "Please enter a number greater than -459"
        self.temp_error = Label(self.temp_frame,
                                text="",
                                font=("Arial", "12", "bold"),
                                fg="#9C0000")

        self.temp_error.grid(row=3)

        # Button Frames

        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        self.temp_celsius = Button(self.button_frame,
                                   text="To Celsius C",
                                   font=button_font,
                                   bg="#0080FF",
                                   width=15,
                                   command=lambda: self.temp_convert(-459)
                                   )
        self.temp_celsius.grid(row=0, column=0, padx=1, pady=1)

        self.temp_fahrenheit = Button(self.button_frame,
                                      text="To Fahrenheit F",
                                      font=button_font,
                                      bg="#FF8000",
                                      width=15,
                                      command=lambda: self.temp_convert(-273)
                                      )
        self.temp_fahrenheit.grid(row=0, column=1, padx=1, pady=1)

        self.to_help = Button(self.button_frame,
                              text="Help / Info",
                              font=button_font,
                              bg="#00FF80",
                              width=15,
                              command=self.to_help
                              )
        self.to_help.grid(row=1, column=0, padx=1, pady=1)

        self.to_history = Button(self.button_frame,
                                 text="History / Export",
                                 font=button_font,
                                 bg="#FF0080",
                                 width=15,
                                 state=DISABLED,
                                 command=self.to_history
                                 )
        self.to_history.grid(row=1, column=1, padx=1, pady=1)

    # Check input is more than -273 // future test make it -273C and 470F
    def check_input(self, min_temp):

        has_error = "no"
        error = "Please enter a number that is more than {}".format(min_temp)
        degree_sign = u'\N{DEGREE SIGN}'
        response = self.temp_entry.get()

        try:
            response = float(response)

            if response < min_temp:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        # if num invalid display error
        if has_error == "yes":
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"

        else:
            # set no to previous errors
            self.var_has_error.set("no")
            # enable history
            self.to_history.config(state=NORMAL)
            return response

    def output_ans(self):
        output = self.var_feedback.get()
        has_error = self.var_has_error.get()

        if has_error == "yes":
            self.temp_error.config(fg="#9C0000")
            self.temp_entry.config(bg="#F8CECC")

        else:
            self.temp_error.config(fg="#004C00")
            self.temp_entry.config(bg="#ffffff")

        self.temp_error.config(text=output)

    @staticmethod
    def round_ans(val):
        var_round = (val * 2 + 1) // 2
        return "{:.0f}".format(var_round)

    def temp_convert(self, min_val):
        to_convert = self.check_input(min_val)
        deg_sign = u'\N{DEGREE SIGN}'
        set_feedback = "yes"
        answer = ""
        from_to = ""

        if to_convert == "invalid":
            set_feedback = "no"

        # convert to celsius
        elif min_val == -459:
            # calculations
            answer = (to_convert - 32) * 5 / 9
            from_to = "{} F{} is {} C{}"

        # convert to fahrenheit
        else:
            answer = to_convert * 1.8 + 32
            from_to = "{} C{} is {} F{}"

        if set_feedback == "yes":
            to_convert = self.round_ans(to_convert)
            answer = self.round_ans(answer)

            feedback = from_to.format(to_convert, deg_sign, answer, deg_sign)
            self.var_feedback.set(feedback)

            self.all_calculations.append(feedback)

            # delete code below when history component is working
            print(self.all_calculations)

        self.output_ans()

    def to_help(self):
        DisplayHelp(self)

    def to_history(self):
        DisplayHistory()


class DisplayHelp:

    def __init__(self, partner):
        background = "#ffe6cc"

        self.help_box = Toplevel()
        # disable help button
        partner.to_help.config(state=DISABLED)

        # if user presses cross at top, close help and release help.
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading = Label(self.help_frame,
                                  font=("Arial", "14", "bold"),
                                  bg=background,
                                  text="Help / Info")
        self.help_heading.grid(row=0)

        help_text = "To use this program, enter a number into" \
                    "the text bar. then simply press the  'To Celsius'" \
                    "or the 'To Fahrenheit' button to convert to the" \
                    "respective temperature... \n\n" \
                    "Note that -273 degrees C and -459 degrees F" \
                    "are the lowest possible temperature."
        self.help_text_label = Label(self.help_frame, bg=background,
                                     font=("Arial", "12"),
                                     text=help_text, wraplength=300)
        self.help_text_label.grid(row=1, padx=10)
        # dismiss button
        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue
    def close_help(self, partner):
        # put button back to normal
        partner.to_help.config(state=NORMAL)
        self.help_box.destroy()


# History page

# fix the help by getting rid of the extra help button
class DisplayHistory:
    def __init__(self):
        button_font = ("Arial", "12", "bold")
        button_fg = "#FFFFFF"

        # temporary
        self.all_calculations = ["PLEASE WORK"]
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()
        self.button_frame = Frame(pady=30, padx=30)
        self.button_frame.grid(row=0)

        self.to_history = Button(self.button_frame,
                                 text="help",
                                 fg=button_fg,
                                 font=button_font,
                                 bg="#004C99",
                                 state=DISABLED,
                                 command=self.to_history)
        self.to_history.grid(row=1, column=1, padx=5, pady=5)
        self.to_history.config(state=NORMAL)

    def to_history(self):
        HistoryExport(self)


class HistoryExport:
    def __init__(self, partner):
        self.history_box = Toplevel()
        partner.to_history.config(state=DISABLED)

        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history,
                                          partner))

        self.history_frame = Frame(self.history_box, width=300, height=200)
        self.history_frame.grid()
        self.history_heading_label = Label(self.history_frame,
                                           text="History / Export",
                                           font=("Arial", "16", "bold"))
        self.history_heading_label.grid(row=0)

        hist_text = "Below are your recent calculations" \
                    "showing 3 / 3 calculations. " \
                    "All calculations are shown to the nearest degree"
        self.text_instructions_label = Label(self.history_frame,
                                             text=hist_text,
                                             width=45, justify="left",
                                             wraplength=300,
                                             padx=10, pady=10)
        self.all_calculations_label = Label(self.history_frame,
                                            text="calculations go here",
                                            pady=10, padx=10,
                                            bg="#ffe6ee",
                                            width=40, justify="left")
        self.all_calculations_label.grid(row=2)

        save_text = "Either choose a custom file name (and push" \
                    "<Export>) or simply push <Export> to save your" \
                    "calculations in a text file. If the filename already exist," \
                    "it will be overwritten."
        self.text_instructions_label.grid(row=1)
        self.dismiss_button = Button(self.history_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#666666",
                                     fg="#FFFFFF",
                                     command=lambda: self.close_history(partner
                                                                        ))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    def close_history(self, partner):
        partner.to_history.config(state=NORMAL)
        self.history_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
