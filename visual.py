import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

labels = [
        ["666","664","652","632","552","532","441","332"],
        ["555","663","651","631","551","531","433","331"],
        ["444","662","644","622","544","522","432","322"],
        ["333","661","643","621","543","521","431","321"],
        ["222","655","642","611","542","511","422","311"],
        ["111","654","641","554","541","443","421","221"],
        ["665","653","633","553","533","442","411","211"]
    ]

c = colors.ListedColormap(['green', 'white', 'red'])

class Visual:
    def __init__(self):
        pass

    def update(self, pw, prob, bid):
        nul = np.zeros((7,8))
        print(f'nul2 = {nul}')
        for w in pw:
            # remove commas from world
            val = (w[0]*100)+(w[1]*10)+w[2]
            for i in range(7):
                for j in range(8):
                    # fill prob if world is in poss worlds into
                    if labels[i][j] == str(val):
                        print("hier komt ie")
                        if (w >= bid):
                            print("hier ook")
                            nul[i][j] = prob[pw.index(w)]
                        else:
                            nul[i][j] = -1 * prob[pw.index(w)]
        print(f'\n nul 1 = {nul} \n')
