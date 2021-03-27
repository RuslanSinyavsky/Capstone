from tkinter import *
import Main as main
import Main2 as main2
#import Holder as holder

root = Tk()
frame = Frame(root, height=300, width=380)
frame.pack()

#Labels
enter_param_label = Label(root, text="Please set the following parameters")
nb_pics_label = Label(root, text="Number of pictures: ")
time_label = Label(root, text="Time interval: ")
maxcellsize_label = Label(root, text="Max fungal surface area (% of droplet): ")
mindropsize_label = Label(root, text="Min droplet size allowed (um^2): ")
error_label = Label(root, text="", fg='red')
status_label = Label(root, text="")

#Entries
nb_pics_entry = Entry(root, bd=3, width=6)
time_entry = Entry(root, bd=3, width=6)
maxcell_entry = Entry(root, bd=3, width=6)
mindrop_entry = Entry(root, bd=3, width=6)

#Time units option Menu
#creating a Tkinter variable
tkvar = StringVar(root)

#time unit options
time_units = ['s', 'min', 'hr']
unit_list = OptionMenu(frame, tkvar, *time_units)

def chooseUnit(*args):
    print("Unit chosen:", tkvar.get())
    error_label.config(text="")
tkvar.trace('w', chooseUnit)

#Buttons
def Setting():
    def imagingStart():
        start_btn.config(state=DISABLED)
        #main.RunSetup(int(nb_pics_entry.get()), int(time_entry.get()), tkvar.get(), int(maxcell_entry.get()), int(mindrop_entry.get()))
        main2.RunSetup(int(nb_pics_entry.get()), int(time_entry.get()), tkvar.get(),
                       int(maxcell_entry.get()), int(mindrop_entry.get()), CheckVar.get())

    if not tkvar.get():
        #print("Please select a time unit to continue")
        error_label.config(text="Please select a time unit to continue")
    else:
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
        #status_label.config(text=holder.Status())
        root2.mainloop()

set_btn = Button(root, text="Set", width=5, command=Setting)

def statusUpdate(msg):
    print("")

#Checkbox
CheckVar = IntVar()    #tracks the state of the checkbutton
C1 = Checkbutton(root, text= "Exclude empty droplets", variable = CheckVar,
                 onvalue = 1, offvalue = 0, height=2, width = 20)


#Packing
enter_param_label.pack()
enter_param_label.place(x=100, y=10)

nb_pics_label.pack()
nb_pics_label.place(x=40, y=40)

time_label.pack()
time_label.place(x=40, y=70)

maxcellsize_label.pack()
maxcellsize_label.place(x=40, y=100)

mindropsize_label.pack()
mindropsize_label.place(x=40, y=130)

status_label.pack()
status_label.place(x=40, y=160)

error_label.pack()
error_label.place(x=80, y=185)

nb_pics_entry.pack()
nb_pics_entry.place(x=160, y=40)

time_entry.pack()
time_entry.place(x=160, y=70)

maxcell_entry.pack()
maxcell_entry.place(x=260, y=100)

mindrop_entry.pack()
mindrop_entry.place(x=220, y=130)

set_btn.pack()
set_btn.place(x=180, y=220)

unit_list.pack()
unit_list.place(x=210, y=66)

C1.pack()
C1.place(x=30, y=150)
root.mainloop()

