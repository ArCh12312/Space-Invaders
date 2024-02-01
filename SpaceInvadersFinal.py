#1280x700 resolution
from tkinter import *
import tkinter.simpledialog
import tkinter.messagebox
import time
def configureWindow(w,h):
	window = Tk()
	window.title("Space Invaders")
	ws = window.winfo_screenwidth()
	hs = window.winfo_screenheight()
	x = (ws/2) - (w/2) 
	y = (hs/2) - (h/2)
	window.geometry('%dx%d+%d+%d' % (w, h, x, y))
	window.configure(background = "black")
	return window
x = 175
y = 500
L = 1
Lives = 3
cheat1b = "1"
cheat2b = "2"
s = " "
global direction
direction = "r"
e_all = []
shots = []
shotcounter = 0
counter1 = -1
hits = 0
cheat_code1 = False
cheat_code2 = False
speed = 1000
count = 9
movedown = False
bulletshot = False
control = False
score = 0

def win():
    global score
    try:
        f = open("Leaderboard.txt","a")
        f.write(str(score)+",")
        f.close()
    except:
        pass
    clear()
    c.delete('all')
    c.create_text(height/2-50, width/2-50, font= ("consolas",80), text= "YOU WIN!", fill = "green", tag = "game won" )
    button1 = Button(text='Play again!', command= lambda: createMenu())
    c.create_window(200, 180, window=button1)

    return

def game_over():
    global Lives
    global score
    if cheat_code2 == False:
        Lives -= 1
    if Lives == 0:
        global score
        f = open("Leaderboard.txt","a")
        data= (str(score)+",")
        f.write(data)
        f.close()
        c.delete('all')
        c.create_text(height/2-50, width/2-50, font= ("consolas",80), text= "GAME OVER!", fill = "red", tag = "game over"  )
        button1 = Button(text='Play again!', command= lambda: createMenu())
        c.create_window(200, 180, window=button1)
        return
    elif Lives > 0:
        global speed
        speed = 100
        loadgame(2)

def movealien():
    global speed
    global count
    global direction
    global L
    if direction == "r":
        if count < 0:
            L +=1
            if L == 4:
                win()
            else:
                loadgame(2)
        bound = c.bbox(e_all[count])
        if bound[0] < width-50:
            for alien in e_all:
                c.move(alien,5,0)
                alienbounds = c.bbox(alien)
                if alienbounds == None:
                    pass
                elif p.coordinates[0]> alienbounds[0] and p.coordinates[0]< alienbounds[2]:
                    if p.coordinates[1]-50> alienbounds[1] and p.coordinates[1]< alienbounds[3]:
                        game_over()
            window.after(speed,movealien)
        else:
            for alien in e_all:
                c.move(alien,0,50)
                direction = "l"
            window.after(speed,movealien)
    else: 
        bound = c.bbox(e_all[0])
        if bound[0] > 0:
            for alien in e_all:
                c.move(alien,-5,0)
                alienbounds = c.bbox(alien)
                if alienbounds == None:
                    pass
                elif alienbounds[3] > 550:
                    if p.coordinates[0]> alienbounds[0]-20 and p.coordinates[0]< alienbounds[2]+20:
                        game_over()
            window.after(speed,movealien)
        else:
            for alien in e_all:
                c.move(alien,0,50)
                #detect_collision()
                direction = "r"
            window.after(speed,movealien)


def spawnaliens():
    global aliensprite
    global e_all
    e_all = []
    y = 50*L
    for i in range(3):
        x = 25
        for i in range(10):
            x += 60
            e = c.create_image(x,y,image = aliensprite,anchor=NW)
            e_all.append(e)
        y += 50
    movealien()


class bullet:
    def __init__(self):
        self.coordinates = [p.coordinates[0],p.coordinates[1]]
        global shot
        global bulletshot
        shot = c.create_rectangle(self.coordinates[0]+20,self.coordinates[1]-15,self.coordinates[0]+30,self.coordinates[1],fill="White", tag = "shot")
        bulletshot = True
        def move_b():
            global bulletshot,count
            c.move(shot, 0, -7)
            self.coordinates[1] -= 7
            if self.coordinates[1]>25:
                detect_collision()
                window.after(5, move_b)
            else:
                c.delete("shot")
                bulletshot = not(bulletshot)
                return
        move_b()

def detect_collision():
    global shot, bulletshot,speed,count,Score,score,L
    if bulletshot == True:
        for i in range(len(e_all)-1, -1, -1):
            if bulletshot == True:
                alienBounds = c.bbox(e_all[i])
                bulletBounds = c.bbox(shot)
                if bulletBounds == None:
                    bulletshot == False
                elif alienBounds[0] < bulletBounds[2] and alienBounds[2] > bulletBounds[0] and alienBounds[1] < bulletBounds[3] and alienBounds[3] > bulletBounds[1]:
                    if e_all[i] == e_all[count]:
                        count -= 1
                    if i < count:
                        count -= 1
                    c.delete(e_all[i])
                    c.delete("shot")
                    e_all.remove(e_all[i])
                    if cheat_code1 == False:
                        speed -= 3
                    score +=100
                    c.itemconfig(Score,text = "Score:" + str(score))
                    #if score %1200 == 0:
                    if count < 0:
                        L += 1
                        if L == 4:
                            win()
                        else:
                            loadgame(2)
                    if len(e_all) == 0:
                        L = score/1200+1
                        if L == 4:
                            win()
                        else:
                            loadgame(2)
                    shot = c.create_rectangle(0,0,0,0)
                    break
                    return


def pause(event):
    time.sleep(1)

def save():
    f = open("Save.txt","w")
    f.write(str(Lives))
    f.write(str(L))
    f.write(str(score))
    f.close()
    window.destroy()

def images():
    img = PhotoImage(file = "c:/Users/aryan/Documents/SpaceInvaders/boss.png") 
    window.img = img
    c.create_image(0,0, image = img, anchor = 'nw')

class player:
    def __init__(self):
        self.coordinates = [width/2,height-150]
        self.sprites = PhotoImage(file="c:/Users/aryan/Documents/SpaceInvaders/spaceship.png")
        self.lives = Lives
        def draw(self):
            global ship
            ship = c.create_image(self.coordinates[0], self.coordinates[1],
                          image=self.sprites,
                          anchor=NW)
            c.create_text(40, 10, text="Lives: " + str(self.lives),
                         fill="white", font="Consolas")
            
        def keystroke(event):
            global s,cheat1b,cheat2b
            x = 0
            y = 0
            if event.keysym == "Left":
                if self.coordinates[0] > 10:
                    x = -10
            if event.keysym == "Right":
                if self.coordinates[0] < width-60:
                    x = 10
            c.move(ship,x,y)
            if event.keysym == "x": save()
            if event.keysym == cheat1b: 
                global cheat_code1
                cheat_code1 = True
            if event.keysym == cheat2b: 
                global cheat_code2
                cheat_code2 = True
            if event.keysym == "b":
                images()
            if event.keysym == "r": delet()
            if event.char == s:
                if bulletshot == False:
                    b = bullet()
            self.coordinates[0] += x
        window.bind("<Key>",keystroke)
        draw(self)
    
score = 0
width = 1280
height = 700
window = configureWindow(width,height)

def createMenu():
    c.delete('all')
    clear()
    start = Button(window, text = "New game", activeforeground = "white", command = lambda: username(), fg = "red", font = ("Consolas", int(height/15)))
    start.place(x=width/2 - width/5, y = height/11)
    load = Button(window, text = "Load", activeforeground = "white", command = lambda: loadgame(1), fg = "red", font = ("Consolas", int(height/15)))
    load.place(x=width/2 - width/10, y = 3 * height/11)
    leaderboard = Button(window, text = "Leaderboard", activeforeground = "white", command = lambda: displayLeaderboard(), fg = "red", font = ("Consolas", int(height/15)))
    leaderboard.place(x=width/2 - width/3.6, y = 5 * height/11)
    settings = Button(window, text = "Settings", activeforeground = "white", command = lambda: Settings(), fg = "red", font = ("Consolas", int(height/15)))
    settings.place(x = width/2 - width/5.4, y = 7 * height/11)

def username():
    clear()
    entry1 = Entry(window) 
    c.create_window(200, 140, window=entry1)

    def save_name():
        username = entry1.get()
        username = username + ":"
        try:
            f = open("Leaderboard.txt","a")
            f.write((str(username)))
        except:
            f = open("Leaderboard.txt","a")
            f.write((str(username)))
        f.close()
        startgame()
    
    button1 = Button(text='submit', command= lambda: save_name())
    c.create_window(200, 180, window=button1)


def displayLeaderboard():
    f = open("Leaderboard.txt", "r")
    data = f.read()
    for i in range(len(data)):
        if data[i] ==",":
            player = f.read(i)
            print (player)
        f.seek(i)
    f.close()


def clear():
    for widget in window.winfo_children():
        if widget.winfo_class() != "Canvas":
            widget.destroy() 
def startgame():
    global Score, speed,Lives
    Lives = 3
    score = 0
    speed = 10
    Score = c.create_text(width-60,10,text ="Score: "+ str(score),font ="Consolas", fill = "white" )
    global p
    clear()
    p = player()
    spawnaliens()     
def loadgame(input):
    clear()
    global Lives
    global p
    global e_all
    global bulletshot 
    bullletshot = False
    global count
    global L
    global score,Score
    global speed
    if input == 1:
        f = open("Save.txt","r")
        f.seek(0)
        Lives = f.read(1)
        f.seek(1)
        L = f.read(1)
        f.seek(2)
        score = f.read()
        f.close()
        print (Lives)
        print (L)
        print (score)
    score = int(score)
    L = int(L)
    Lives = int(Lives)
    if L == 4:
        win()
    else:
        count = 9
        speed = 10
        c.delete('all')
        p = player()
        Score = c.create_text(width-60,10,text ="Score: "+ str(score),font ="Consolas", fill = "white" )
        spawnaliens()   

def Settings():
    global s,cheat1b,cheat2b
    s = " "
    cheat1b = "1"
    cheat2b = "2"
    clear()
    entry1 = Entry(window) 
    c.create_window(400, 140, window=entry1)
    entry2label = Label(window,text = "Shoot cheat1 control(Default = 1)")
    entry2label.pack
    entry2 = Entry(window) 
    c.create_window(300, 200, window=entry2)
    entry3label = Label(window,text = "Shoot cheat2 control(Default = 2)")
    entry3label.pack
    entry3 = Entry(window) 
    c.create_window(200, 140, window=entry3)

    def getbutton():
        global s
        input = entry1.get()
        s = str(input)
    def getbutton1():
        global cheat1b
        input = entry2.get()
        cheat2b = str(input)
    def getbutton2():
        global cheat2b
        input2 = entry3.get()
        cheat2b = str(input2)
    
    button1 = Button(text='Shoot', command= lambda: getbutton())
    c.create_window(400, 180, window=button1)
    button2 = Button(text='cheat1', command= lambda: getbutton1())
    c.create_window(300, 240, window=button2)
    button3 = Button(text='cheat2', command= lambda: getbutton2())
    c.create_window(200, 180, window=button3)
    button1 = Button(text='Back to menu', command= lambda: createMenu())
    c.create_window(400, 300, window=button1)



c = Canvas(window,background="black",width = width, height = height)
c.pack()
aliensprite = PhotoImage(file = r"c:/Users/aryan/Documents/SpaceInvaders/AlienL1.png")
def images():
    img = PhotoImage(file = "c:/Users/aryan/Documents/SpaceInvaders/boss.png") 
    window.img = img
    c.create_image(0,0, image = img, anchor = 'nw',tag = "image")
def delet():
    c.delete("image") 
window.bind("p",pause)

createMenu()

window.mainloop()