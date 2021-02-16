from tkinter import *
import Main as main


root = Tk()
frame = Frame(root, height=300, width=380)
frame.pack()

#root2 = Tk()
#frame2 = Frame(root2, height=270, width=410)
#frame2.pack()

#Labels
enter_param_label = Label(root, text="Please set the following parameters")
nb_pics_label = Label(root, text="Number of pictures: ")
time_label = Label(root, text="Time interval (min): ")
maxdropsize_label = Label(root, text="Max droplet size allowed (unit?): ")
mindropsize_label = Label(root, text="Min droplet size allowed (unit?): ")
#light_warning_label = Label(root2, text="Please ensure that the light in the room is off", fg='blue')
#lamp_warning_label = Label(root2, text="Warning! Turn on the TH4 power supply before connecting cables", fg='red')

#Entries
nb_pics_entry = Entry(root, bd=3, width=6)
time_entry = Entry(root, bd=3, width=6)
maxdrop_entry = Entry(root, bd=3, width=6)
mindrop_entry = Entry(root, bd=3, width=6)

#Buttons

def Setting():

    main.IncubationTime(int(nb_pics_entry.get()), int(time_entry.get()))
    main.RunSetup(int(nb_pics_entry.get()), int(time_entry.get()), int(maxdrop_entry.get()))

    print("nb of pics entered: ", nb_pics_entry.get())
    print("time entered: ", time_entry.get())
    print("max size entered: ", maxdrop_entry.get())
    print("min size entered: ", mindrop_entry.get())

    def imagingStart():
        start_btn.config(state=DISABLED)

    root2 = Tk()
    frame2 = Frame(root2, height=270, width=410)
    frame2.pack()
    set_btn.config(state=DISABLED)
    light_warning_label = Label(root2, text="Please ensure that the light in the room is off", fg='blue')
    lamp_warning_label = Label(root2, text="Warning! Turn on the TH4 power supply before connecting cables", fg='red')
    start_btn = Button(root2, text="Begin imaging", width=12, command=imagingStart)

    start_btn.pack()
    start_btn.place(x=160, y=170)
    light_warning_label.pack()
    light_warning_label.place(x=20, y=10)

    lamp_warning_label.pack()
    lamp_warning_label.place(x=20, y=40)
    root2.mainloop()

#def imagingStart():
#    start_btn.config(state=DISABLED)

set_btn = Button(root, text="Set", width=5, command=Setting)

#start_btn = Button(root2, text="Begin imaging", width=12, command=imagingStart)

#Packing
enter_param_label.pack()
enter_param_label.place(x=100, y=10)

nb_pics_label.pack()
nb_pics_label.place(x=40, y=40)

time_label.pack()
time_label.place(x=40, y=70)

maxdropsize_label.pack()
maxdropsize_label.place(x=40, y=100)

mindropsize_label.pack()
mindropsize_label.place(x=40, y=130)

#light_warning_label.pack()
#light_warning_label.place(x=20, y=10)

#lamp_warning_label.pack()
#lamp_warning_label.place(x=20, y=40)

nb_pics_entry.pack()
nb_pics_entry.place(x=160, y=40)

time_entry.pack()
time_entry.place(x=160, y=70)

maxdrop_entry.pack()
maxdrop_entry.place(x=220, y=100)

mindrop_entry.pack()
mindrop_entry.place(x=220, y=130)

set_btn.pack()
set_btn.place(x=180, y=200)

#start_btn.pack()
#start_btn.place(x=160, y=170)
root.mainloop()
#root2.mainloop()
