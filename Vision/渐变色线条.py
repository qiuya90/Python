import matplotlib.pyplot as plt
import numpy as np

y = np.arange(1, 5)
print(y)
R=0
G=0
B=0
# draw the figure so the animations will work
fig = plt.gcf()
fig.show()
fig.canvas.draw()

def changecolor():
    global R, G, B, cR, cG, cB
    cR = (R+5) % 255
    cG = (G+15) % 255
    cB = (B+45) % 255
    R = cR
    G = cG
    B = cB

while True:
    # compute something
    changecolor()
    plt.plot(y, color=(cR/255.0, cG/255.0, cB/255.0, 1))  # plot something
    # update canvas immediately
    plt.xlim([0, 5])
    plt.ylim([0, 5])
    plt.pause(0.1)  # I ain't needed!!!
    fig.canvas.draw()

