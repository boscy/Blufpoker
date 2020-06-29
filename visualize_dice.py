from tkinter import *
from PIL import ImageTk, Image
import itertools
import random
import numpy as np
import os
from copy import copy, deepcopy

background_color = "#0D865D"
BASE_DIR = os.getcwd()
continues = False
quit = False


def buttonClick(root):
    continues = True
    root.after(10)
    root.destroy()


def endProgam():
    print('Goodbye!')
    sys.exit()


class Visualized_game:
    def __init__(self, cup, public_knowledge, know1, know2, know3, turn, penal1, penal2, penal3, losername, current_bid, text, printtext):
        """
        Defines an object Cup in a game of Blufpoker.\n
        :param n_dice: Number of dice the cup is initialized with.
        """
        self.root = Tk()
        self.root.geometry("1080x730")
        self.root.title('Blufpoker')
        # self.root.configure(bg=background_color)

        self.myCanvas3 = Canvas(self.root, width=1080, height=180, bg="#FFFFFF")
        self.myCanvas3.pack(side="bottom", fill="both", expand=True)

        self.myCanvas2 = Canvas(self.root, width=360, height=540, bg="#DCDCDC")
        self.myCanvas2.pack(side=RIGHT, fill=X)

        self.myCanvas = Canvas(self.root, width=720, height=540, bg=background_color)
        self.myCanvas.pack(side=TOP)
        # self.myCanvas.place(x=50,y=0)
        #


        print_gui = self.myCanvas2.create_text(10, 10, anchor="nw")
        self.myCanvas2.itemconfig(print_gui, text=printtext)
        self.myCanvas2.insert(print_gui, 6, "")


        loser_string1 = [losername[j] for j in
                        range(penal1)]
        var1 = StringVar()
        self.p1 = Label(self.myCanvas, textvariable=var1, relief=RAISED)
        var1.set("Player 1 \n Naive \n" + "".join(loser_string1))
        self.p1.pack()
        self.p1.place(x=10, y=490)

        loser_string2 = [losername[j] for j in
                         range(penal2)]
        var2 = StringVar()
        p2 = Label(self.myCanvas, textvariable=var2, relief=RAISED)
        var2.set("Player 2 \n Naive \n"  + "".join(loser_string2))
        p2.pack()
        p2.place(x=335, y=10)

        loser_string3 = [losername[j] for j in
                         range(penal3)]
        var3 = StringVar()
        p3 = Label(self.myCanvas, textvariable=var3, relief=RAISED)
        var3.set("Player 3  \n (Knowledge Based)\n" + "".join(loser_string3))
        p3.pack()
        p3.place(x=600, y=490)


        continue_button = Button(self.myCanvas, text="Click to continue", command=lambda: buttonClick(self.root),
                                 width=15)
        continue_button.pack()
        continue_button.place(x=350, y=510)

        quit_button = Button(self.myCanvas, text="Quit", command=lambda: endProgam(), width=8)
        quit_button.pack()
        quit_button.place(x=260, y=510)

        # for i in public_knowledge:
        #     cup.remove(i)

        dice_coords = np.zeros((3,2), dtype="uint8")
        # turn = 0
        dice_size = 40
        if turn == 0:
            believex, believey = 70, 490
            cupx, cupy = 150, 400
            die1x, die1y = 125, 340
            die2x, die2y = 100, 400
            die3x, die3y = 160, 400


        elif turn == 1:
            believex, believey = 400, 10
            cupx, cupy = 360, 150
            die1x, die1y = 335, 90
            die2x, die2y = 310, 150
            die3x, die3y = 370, 150

        elif turn == 2:
            believex, believey = 620,450
            cupx, cupy = 550, 400
            die1x, die1y = 125 + 400, 340
            die2x, die2y = 100 + 400, 400
            die3x, die3y = 160 + 400, 400


        x0 = cupx - 80
        y0 = cupy - 80
        x1 = cupx + 80
        y1 = cupy + 80
        self.myCanvas.create_oval(x0, y0, x1, y1, outline="#800000", fill="#8B4513", width=2)

        text = str(text)
        if len(text) != 0:

            believeprint = self.myCanvas.create_text(believex, believey, anchor="nw")
            self.myCanvas.itemconfig(believeprint, text=text, font=("Courier", 15))
            self.myCanvas.insert(believeprint, 20, "")

        temp_pk = deepcopy(public_knowledge) # copy to remove dice, such that with pk=1 not double dice are printed
        if cup[0] in temp_pk:
            dice_bg1 = "green"
            temp_pk.remove(cup[0])
        else:
            dice_bg1 = "#8B4513"

        if cup[1] in temp_pk:
            dice_bg2 = "green"
            temp_pk.remove(cup[1])
        else:
            dice_bg2 = "#8B4513"

        if cup[2] in temp_pk:
            dice_bg3 = "green"
            temp_pk.remove(cup[2])
        else:
            dice_bg3 = "#8B4513"

        first_die_path = f"./{cup[0]}.png"
        first_die_image = ImageTk.PhotoImage(Image.open(first_die_path).resize((dice_size, dice_size)))
        first_die_label = Label(self.myCanvas, image=first_die_image, bg=dice_bg1)
        first_die_label.pack()
        first_die_label.place(x=die1x, y=die1y)

        second_die_path = f"./{cup[1]}.png"
        second_die_image = ImageTk.PhotoImage(Image.open((second_die_path)).resize((dice_size, dice_size)))
        second_die_label = Label(self.myCanvas, image=second_die_image, bg=dice_bg2)
        second_die_label.pack()
        second_die_label.place(x=die2x, y=die2y)

        third_die_path = f"./{cup[2]}.png"
        third_die_image = ImageTk.PhotoImage(Image.open((third_die_path)).resize((dice_size, dice_size)))
        third_die_label = Label(self.myCanvas, image=third_die_image, bg=dice_bg3)
        third_die_label.pack()
        third_die_label.place(x=die3x, y=die3y)

        # canvas 2 prints the knowledge
        # self.myCanvas2 = Canvas(self.root, width=360, height=540, bg="#FFFFFF")
        # self.myCanvas2.pack(side = "right",fill="both", expand = True)


        if len(know1) == 56:
            string1 = "Player 1 possible worlds: \n all worlds"
        else:
            string1 = "Player 1 possible worlds: \n" + ' '.join(str(e) for e in list(know1))

        texttest = self.myCanvas3.create_text(10, 10, anchor="nw")
        self.myCanvas3.itemconfig(texttest, text=string1)
        self.myCanvas3.insert(texttest, 6, "")

        if len(know2) == 56:
            string2 = "Player 2 possible worlds: \n all worlds"
        else:
            string2 = "Player 2 possible worlds: \n" + ' '.join(str(e) for e in list(know2))

        texttest2 = self.myCanvas3.create_text(10, 50, anchor="nw")
        self.myCanvas3.itemconfig(texttest2, text=string2)
        self.myCanvas3.insert(texttest2, 6, "")

        if len(know3) == 56:
            string3 = "Player 3 possible worlds: \n all worlds"
        else:
            string3 = "Player 3 possible worlds: \n" + ' '.join(str(e) for e in list(know3))

        texttest3 = self.myCanvas3.create_text(10, 90, anchor="nw")
        self.myCanvas3.itemconfig(texttest3, text=string3)
        self.myCanvas3.insert(texttest3, 6, "")

        string4 = "Common Knowledge: \n" + ' '.join(str(e) for e in list(public_knowledge))
        texttest4 = self.myCanvas3.create_text(10, 130, anchor="nw")
        self.myCanvas3.itemconfig(texttest4, text=string4)
        self.myCanvas3.insert(texttest4, 6, "")

        bid_string = f"Current bid: \n" + ''.join(str(current_bid))

        bid = self.myCanvas.create_text(290, 250, anchor="nw")
        self.myCanvas.itemconfig(bid, text=bid_string,font=("Courier", 15))
        self.myCanvas.insert(bid, 20, "")

        self.root.mainloop()

        # third_die_path = f"./{cup[2]}.png"
        # third_die_image = ImageTk.PhotoImage(Image.open((third_die_path)).resize((dice_size, dice_size)))
        # third_die_label = Label(self.myCanvas, image=third_die_image, bg="#8B4513")
        # third_die_label.pack()
        # third_die_label.place(x=die3x + 50, y=die3y)
        #
        # self.myCanvas.update()
        # self.root.mainloop()




if __name__ == '__main__':
    for turn in range(3):
        visualise_dice(turn=turn)
