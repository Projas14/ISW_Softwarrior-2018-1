from tkinter import * 

for i in range(5): 
    for j in range(4): 
     l = Label(text='%d.%d' % (i, j), relief=RIDGE) 
     l.place(x=20*i+10,y=20*j+10)

mainloop() 