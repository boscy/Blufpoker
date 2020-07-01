from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import seaborn as sns
from matplotlib import colors

WIDTH = 1200
HEIGHT = 750

bg_colour = "#0D865D"
info_colour = 'gray'
kn_colour = 'white'
db_colour = "#8B4513"

labels = [
        ["666","664","652","632","552","532","441","332"],
        ["555","663","651","631","551","531","433","331"],
        ["444","662","644","622","544","522","432","322"],
        ["333","661","643","621","543","521","431","321"],
        ["222","655","642","611","542","511","422","311"],
        ["111","654","641","554","541","443","421","221"],
        ["665","653","633","553","533","442","411","211"]
    ]

hm_colours = colors.ListedColormap([ 'green', 'silver' ,'red'])

class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
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

        die1 = ImageTk.PhotoImage(Image.open("./1.png").resize((50,50)))
        die2 = ImageTk.PhotoImage(Image.open("./2.png").resize((50,50)))
        die3 = ImageTk.PhotoImage(Image.open("./3.png").resize((50,50)))
        die4 = ImageTk.PhotoImage(Image.open("./4.png").resize((50,50)))
        die5 = ImageTk.PhotoImage(Image.open("./5.png").resize((50,50)))
        die6 = ImageTk.PhotoImage(Image.open("./6.png").resize((50,50)))

        self.dice = [die1, die2, die3, die4, die5, die6]
        self.show_d1 = Label()
        self.show_d2 = Label()
        self.show_d3 = Label() 

        self.openDie1 = Label()
        self.openDie2 = Label()

        self.currentBid = Button()

        self.chart = FigureCanvasTkAgg(plt.figure())
        self.labels = labels
        self.hm_colours = hm_colours

        initGame(self)
        initInfo(self)
        initPenalty(self)
        initKnowl(self)

def initGame(self):
    self.game.place(relwidth=0.7, relheight=0.8)

    self.currentBid = Button(self.game, text="Current bid: ")
    self.currentBid.place(relx = 0.4, rely = 0.5)

    self.diceBox = Canvas(self.game, bg=bg_colour, height= 250, width=250, highlightthickness = 0)
    self.diceBox.create_oval(0, 0, 249, 249, outline="#800000", fill=db_colour, width=2)
    self.diceBox.place(rely=0.57, relx = 0.1)

    pl1_label = Label(self.game, text= "Player 1")
    pl1_label.place(rely = 0.9, relx = 0.01)
    pl1_strat = Label(self.game, text = "Naive")
    pl1_strat.place(rely = 0.95, relx = 0.01)

    pl2_label = Label(self.game, text= "Player 2")
    pl2_label.place(rely = 0.01, relx = 0.01)
    pl2_strat = Label(self.game, text = "Naive")
    pl2_strat.place(rely = 0.06, relx = 0.01)

    pl3_label = Label(self.game, text= "Player 3")
    pl3_label.place(rely = 0.01, relx = 0.85)
    pl3_strat = Label(self.game, text= "Knowledge-Based")
    pl3_strat.place(rely = 0.06, relx = 0.85)


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

    openDice = Label(self.knowledge, text = "Common knowledge (open dice): ")
    openDice.place(relx = 0.05, rely = 0.85)

    fig = plt.figure()

    data = np.ones((7,8))
    ax = sns.heatmap(data, annot=self.labels, fmt='',xticklabels=False, yticklabels=False, cmap=hm_colours, cbar= False, linewidths=1, linecolor='white')
    fig.add_subplot(ax)

    self.chart = FigureCanvasTkAgg(fig, self.knowledge)
    self.chart.get_tk_widget().pack(anchor=N)

    title = Label(self.knowledge, text= "  Player 3 knowledge base  ")
    title.place(relx = 0.25, rely = 0.025)

    lbl1 = Label(self.knowledge, text= "  Possible worlds higher or equal than current bid  ", bg='green', pady = 2, fg='white')
    lbl1.place(rely = 0.59, relx = 0.125)

    lbl2 = Label(self.knowledge, text= "  Possible worlds lower than current bid  ", bg = 'red', pady = 2, fg='white')
    lbl2.place(rely = 0.63, relx = 0.125)

    lbl3 = Label(self.knowledge, text= "    Impossible worlds    ", bg= 'silver', pady = 2)
    lbl3.place(rely = 0.67, relx = 0.125)

    
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

    pen_label_2 = Label(self.penalties, pady = 3, text = "Player 2:")
    pen_label_2.grid(row = 5, column =1)

    pen_label_3 = Label(self.penalties, pady=3, text = "Player 3:")
    pen_label_3.grid(row = 7, column =1)


##----------------------------------------------------------------------------------##