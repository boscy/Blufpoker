from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def moveDiceBox(player):
    if player == 0: gui.diceBox.place(rely=0.57, relx = 0.1)
    elif player == 1: gui.diceBox.place(rely = 0.02, relx = 0.07)
    elif player == 2: gui.diceBox.place(rely=0.05, relx = 0.62)

def writePenalty(player, string):
    penalty = Label(gui.penalties, text=string, bg=info_colour)
    if player == 0: penalty.grid(row = 3, column=3)
    elif player == 1: penalty.grid(row = 5, column=3)
    elif player == 2: penalty.grid(row = 7, column=3)
        
def writeInfo(string):
    gui.gi_text.insert("1.0", string + "\n")

def drawDice(d1, d2, d3):
    # im = Image.open("6.png") #added
    # im = Image.resize(30,30)
    # im = ImageTk.PhotoImage(im) #revised

    # die = ImageTk.PhotoImage(Image.open("./6.png").resize((50,50)))
    # img = PhotoImage(file = "6.png")
    # im = cv2.imread("6.png")
    # img = Image.fromarray(im)
    # img = ImageTk.PhotoImage(img)

    # die_label = Label(gui.diceBox, image= img)
    # die_label.place(relx = 0.5, rely = 0.5)
    pass

WIDTH = 1200
HEIGHT = 750

bg_colour = "#0D865D"
info_colour = 'gray'
kn_colour = 'white'
db_colour = "#8B4513"

class GUI(Tk):
# class GUI():
    def __init__(self, strat1, strat2, strat3):
        Tk.__init__(self)
        # self.root = Tk()
        self.title('Blufpoker')
        self.resizable(False, False)

        canvas = Canvas(self, height=HEIGHT, width= WIDTH)
        canvas.pack()

        self.game = Frame(self, bg=bg_colour)
        self.info = Frame(self, bg=info_colour)
        self.penalties = Frame(self, bg=info_colour)
        self.knowledge = Frame(self, bg=kn_colour)

        self.gi_text = Text()
        self.diceBox = Canvas()

        initGame(self, strat1, strat2, strat3)
        initInfo(self)
        initPenalty(self)
        initKnowl(self)
        

def test():
    gui.gi_text.insert("1.0", "supertest2222")
    moveDiceBox(2)
    writePenalty(1,"oscar is een lul")
    # drawDice(1,2,3)

def buttonclick(self):
    self.gi_text.insert('1.0', "MOI \n")
    test()

def initGame(self, strat1, strat2, strat3):
    self.game.place(relwidth=0.7, relheight=0.8)

    button = Button(self.game, text= "Moi", bg='green', fg='red', command= lambda: buttonclick(self))
    button.place(rely=0.5, relx = 0.5)

    self.diceBox = Canvas(self.game, bg=bg_colour, height= 250, width=250, highlightthickness = 0)
    self.diceBox.create_oval(0, 0, 249, 249, outline="#800000", fill=db_colour, width=2)
    self.diceBox.place(rely=0.57, relx = 0.1)

    path = "./6.png"
    die = ImageTk.PhotoImage(Image.open((path)).resize((50,50)))
    die_label = Label(self.diceBox, image= die, bg="green")
    die_label.place(relx = 0.5, rely = 0.5)

    # diceBox = Canvas(self.game, bg=bg_colour, height= 250, width=250, highlightthickness = 0)
    # diceBox.create_oval(0, 0, 249, 249, outline="#800000", fill=db_colour, width=2)
    # diceBox.place(rely=0.57, relx = 0.1)

    # die = ImageTk.PhotoImage(Image.open("./6.png").resize((50,50)))
    # die_label = Label(diceBox, image= die)
    # die_label.place(relx = 0.5, rely = 0.5)

    pl1_label = Label(self.game, text= "Player1")
    pl1_label.place(rely = 0.9, relx = 0.01)
    pl1_strat = Label(self.game, text = strat1)
    pl1_strat.place(rely = 0.95, relx = 0.01)

    pl2_label = Label(self.game, text= "Player2")
    pl2_label.place(rely = 0.01, relx = 0.01)
    pl2_strat = Label(self.game, text = strat2)
    pl2_strat.place(rely = 0.06, relx = 0.01)

    pl3_label = Label(self.game, text= "Player3")
    pl3_label.place(rely = 0.01, relx = 0.9)
    pl3_strat = Label(self.game, text=strat3)
    pl3_strat.place(rely = 0.06, relx = 0.9)


def replaceBox():
    # diceBox.place(rely = 0.9)
    pass

def initInfo(self):
    self.info.place(rely=0.8 , relx =0, relheight = 0.2, relwidth = 0.5)

    gi_label = Label(self.info, text = "Game info")
    gi_label.grid(row=1, column=0)

    self.info.grid_rowconfigure(0, minsize=5)
    self.info.grid_rowconfigure(2, minsize=5)

    self.gi_text = Text(self.info)
    self.gi_text.grid(row=3, column=0)


def initKnowl(self):
    self.knowledge.place(relwidth = 0.3, relheight = 1, relx = 0.7)

    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')
    ax.grid()

    chart = FigureCanvasTkAgg(fig, self.knowledge)
    chart.get_tk_widget().pack(anchor=N)


def initPenalty(self):
    self.penalties.place(rely = 0.8, relx = 0.5, relheight = 0.2, relwidth = 0.2)

    self.penalties.grid_rowconfigure(0,minsize=5)
    self.penalties.grid_rowconfigure(2,minsize=15)
    self.penalties.grid_rowconfigure(4,minsize=10)
    self.penalties.grid_rowconfigure(6,minsize=10)
    self.penalties.grid_columnconfigure(0,minsize=5)
    self.penalties.grid_columnconfigure(2,minsize=10)

    pen_label = Label(self.penalties, text= "Penalties")
    pen_label.grid(row =1, column = 3)

    pen_label_1 = Label(self.penalties, pady = 3, text = "Player 1:")
    pen_label_1.grid(row = 3, column =1)

    penalty = "HORSE"
    pen_pl1 = Label(self.penalties, text=penalty, bg=info_colour)
    pen_pl1.grid(row = 3, column=3)

    pen_label_2 = Label(self.penalties, pady = 3, text = "Player 2:")
    pen_label_2.grid(row = 5, column =1)

    pen_label_3 = Label(self.penalties, pady=3, text = "Player 3:")
    pen_label_3.grid(row = 7, column =1)


gui = GUI("strat1", "strat2", "strat3")
gui.mainloop()