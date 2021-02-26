#SQL Server Database connection-------------------------------------------------------------------------------------------------------#
import pyodbc
server   = 'dlserv.database.windows.net'
database = 'LDB'
username = '**********'
password = '**********'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#--------------------------------------------------------------------------------------------------------------------------------------#

#----------------------------------------ROW COUNTER-----------------------------------------------#
cursor.execute("SELECT COUNT(*) from total2")
result=cursor.fetchone()
number_of_total=result[0]

cursor.execute("SELECT COUNT(*) from total2 where Region=N'Πόντος'")
result=cursor.fetchone()
cp=result[0]

cursor.execute("SELECT COUNT(*) from total2 where Region=N'Καππαδοκία'")
result=cursor.fetchone()
ck=result[0]

cursor.execute("SELECT COUNT(*) from total2 where Region=N'Αϊβαλί'")
result=cursor.fetchone()
ca=result[0]

cursor.execute("SELECT COUNT(*) from total2 where Region=N'Κύπρος'")
result=cursor.fetchone()
cc=result[0]

#---------------------------------------END OF ROW COUNTER-------------------------------------------#


#------------------------------------------------Imports------------------------------------------------------------#
import matplotlib.pyplot as plt #import module for graphs
from LevenClass import * #import levensthein class
from time import time, sleep, clock,perf_counter #module for intro timer
import numpy.core._dtype_ctypes
from tkinter import *   #imports these libs: Tk, ttk, Button, PhotoImage,StringVar,Toplevel,Label,TOP,IntVar,Radiobutton,Entry,Text,OptionMenu
import webbrowser
import tkinter.ttk as ttk
import tkinter as tk
import tkinter.messagebox as tm #module for messages
import tkinter.font as tkFont

#------------------------------------------------------End of Imports-------------------------------------------------------------------#


#------------------------------------------------------Global Functions-----------------------------------------------------------------#
def xstr(s): #removes None from any string given,global function               
        if s is None:
            return ''
        return str(s)

url = "http://www.ice.uniwa.gr" 
def openweb():
    webbrowser.open(url,True)

def on_entry_click(event): #Creates the field and blanks it and waits for input    
    #function that gets called whenever entry is clicked
    search = Entry(textvariable=SEARCH)
    if search.get() == 'Πληκτρολογήστε εδώ':
        search.delete(0, "end") # delete all the text in the entry
        search.insert(0, '') #Insert blank for user input
        search.config(fg = 'black')       
#-----------------------------------------------End of Global Functions-------------------------------------------------------------------#


#---------------------------------------------INTRO WINDOW Splash Class---------------------------------------------------------------------------------#
class Splash:
    def __init__(self, root, file, wait):
        self.__root = root
        self.__file = file
        self.__wait = wait + perf_counter()
    def __enter__(self):
        # Hide the root while it is built.
        self.__root.withdraw()
        # Create components of splash screen.
        window = Toplevel(self.__root)
        splash = PhotoImage(master=window, file=self.__file)
        canvas = Label(window, textvariable=d_status, fg='white', bg='black', image=splash, compound=TOP)
        # Get the screen's width and height.
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        # Get the images's width and height.
        imgW = splash.width()
        imgH = splash.height()
        # Compute positioning for splash screen.
        Xpos = (scrW - imgW) // 3
        Ypos = (scrH - imgH) // 2
        # Configure the window showing the logo.
        window.overrideredirect(True)
        window.geometry('+{}+{}'.format(Xpos, Ypos))
        canvas.grid()
        # Show the splash screen on the monitor.
        window.update()
        # Save the variables for later cleanup.
        self.__window = window
        self.__canvas = canvas
        self.__splash = splash
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure that required time has passed.
        now = perf_counter()
        if now < self.__wait:
            sleep(self.__wait - now)
        # Free used resources in reverse order.
        del self.__splash
        self.__canvas.destroy()
        self.__window.destroy()
        # Give control back to the root program.
        self.__root.update_idletasks()
        #self.__root.deiconify()
    def foo(self, x):
        d_status.set(str(x))
        self.__root.update_idletasks()
def initializeMyApplication(notify_status):
    for x in range(1,4):
        notify_status(x)
        sleep(1)
def buildTheGUI(object):
    for x in range(100, 101):
        sleep(1)
#---------------------------------------------End of Splash Class------------------------------------------------------------------------------#


#---------------------------------------------Dialects Class(MAIN)-------------------------------------------------------------------------------#
class Dialects(object):

#-------------------------------------------UPDATE FUNC-----------------------------------------------------------------------------------------#
    #Prompt for insert_credentials,  UpdateWindow->UpdateCred->UpdateButtonCl
    def update_credentials(s):
        win00=tk.Toplevel()
        win00.title("Login")
        win00.geometry('215x75')
        win00.resizable(False, False)
        win00.attributes("-topmost", True) #set window to stay at toplevel
        
        s.label_username = Label(win00, text="Όνομα χρήστη")
        s.label_username.grid(row=0, column=0, sticky='e')
        s.entry_username = Entry(win00)
        s.entry_username.grid(row=0, column=1)
  
        s.label_password = Label(win00, text="Κωδικός")
        s.label_password.grid(row=1, column=0, sticky='e')
        s.entry_password = Entry(win00, show="*")
        s.entry_password.grid(row=1, column=1)

        s.logbtn = Button(win00, text="Σύνδεση", command=lambda:[s.update_btn_clicked(),win00.destroy()]) #press login and destroy previous window
        s.logbtn.grid(columnspan=2)


    def UpdateWindow(s):
        if(s.tree.focus()==''): #if no record is selected...
            tm.showerror("Σφάλμα", "Παρακαλώ επιλέξτε εγγραφή...")
            return None #exit function
        
        win33=tk.Toplevel()
        win33.title("Επεξεργασία επιλεγμένης εγγραφής")
        win33.resizable(False, False)
        win33.attributes("-topmost", True)
        label1=Label(win33,text='Λέξη')
        label1.grid(column=0, row=0, sticky='w')
        label2=Label(win33,text='Κύριος Ορισμός')
        label2.grid(column=0, row=1, sticky='w')
        label3=Label(win33,text='Ορισμός 2')
        label3.grid(column=0, row=2, sticky='w')
        label4=Label(win33,text='Φωνητική Απόδοση')
        label4.grid(column=0, row=3, sticky='w')
        label5=Label(win33,text='Περιοχή')
        label5.grid(column=0, row=4)

        for item in s.tree.selection():  #fetch selections while looping through the tree
            x=cursor.execute("SELECT * FROM total2 WHERE ID=?", (s.tree.set(item, '#6'),))
            row=cursor.fetchone()
            
        global get_id
        get_id=row[5]
        
        #1st box , Word
        textBox=Text(win33,height=1,width=30)
        textBox.grid(column=1, row=0,sticky='w')
        textBox.insert('1.0',row[0])
        global y1
        y1=textBox
      
        #2nd box,M1
        textBox2=Text(win33, height=1.3,width=60)
        textBox2.grid(column=1, row=1,sticky='w')
        textBox2.insert('1.0',row[3])
        global y2
        y2=textBox2
        
        #3rd box,M2
        textBox3=Text(win33, height=1.3,width=60)
        textBox3.grid(column=1, row=2,sticky='w')
        textBox3.insert('1.0',xstr(row[4]))
        global y3
        y3=textBox3

        #4th box,Vocal
        textBox4=Text(win33, height=1.3,width=30)
        textBox4.grid(column=1, row=3,sticky='w')
        textBox4.insert('1.0',xstr(row[2]))
        global y4
        y4=textBox4

        #Drop down menu for Region choice
        global var0
        var0 = StringVar(win33)
        var0.set(row[1])  #Places user's choice as region
        option = OptionMenu(win33, var0, "Πόντος", "Καππαδοκία", "Αϊβαλί", "Κύπρος") #creates option menu (drop down)
        option.grid(column=1, row=4,sticky='w')
        
        #gets data and passes them to update_credentials
        btn_commit = tk.Button(win33,text="ΟΚ", width=5, command=s.update_credentials)
        btn_commit.grid(column=1, row=4,sticky='nse')

        
    def update_btn_clicked(s): #used only for update 
                username = s.entry_username.get()
                password = s.entry_password.get()

                inputValue=y1.get("1.0","end-1c")  
                inputValue2=y2.get("1.0","end-1c")
                inputValue3=y3.get("1.0","end-1c")
                inputValue4=y4.get("1.0","end-1c")
                inputValue5=var0.get()
                
                if username == "cs" and password == "cs":
                    qry = '''UPDATE total2 SET Word=?,Region=?,Vocal=?,M1=?,M2=? WHERE ID=?'''
                    param_values = [inputValue.upper(), inputValue5, inputValue4, inputValue2, inputValue3,get_id]
                    cursor.execute(qry, param_values)
                    cursor.commit() #Use this to commit the insert operation
                    tm.showinfo("Επιτυχής σύνδεση", "Η ενέργεια ολοκληρώθηκε") 
                else:
                    tm.showerror("Σφάλμα σύνδεσης", "Λάθος στοιχεία...")
#-------------------------------------------END OF UPDATE FUNC----------------------------------------------------------------------------------#



#--------------------------------------------INSERT FUNC----------------------------------------------------------------------------------------#
    def insert_credentials(s):
            win=tk.Toplevel()
            win.title("Login")
            win.geometry('215x75')
            win.resizable(False, False)
            win.attributes("-topmost", True) #win above all windows
            s.label_username = Label(win, text="Όνομα χρήστη")
            s.label_username.grid(row=0, column=0, sticky='e')
            s.entry_username = Entry(win)
            s.entry_username.grid(row=0, column=1)
            
            s.label_password = Label(win, text="Κωδικός")
            s.label_password.grid(row=1, column=0, sticky='e')
            s.entry_password = Entry(win, show="*")
            s.entry_password.grid(row=1, column=1)

            s.logbtn = Button(win, text="Σύνδεση", command=lambda:[s.insert_btn_clicked(),win.destroy()])
            s.logbtn.grid(columnspan=2)
            
    def insert_window(s):
        
        win3=tk.Toplevel()
        win3.title("Εισαγωγή νέας λέξης")
        win3.resizable(False, False)
        win3.attributes("-topmost", True) #win above all windows
        label1=Label(win3,text='Λέξη')
        label1.grid(column=0, row=0, sticky='w')
        label2=Label(win3,text='Περιοχή')
        label2.grid(column=0, row=3, sticky='w')
        label3=Label(win3,text='Φωνητική Απόδοση')
        label3.grid(column=0, row=1, sticky='w')
        label4=Label(win3,text='Ορισμός')
        label4.grid(column=0, row=2, sticky='w')

        #1st box creation
        textBox=Text(win3,height=1,width=30)
        textBox.grid(column=1, row=0,sticky='w')
        global x
        x=textBox
      
        #Drop down menu for Region choice
        global var
        var = StringVar(win3)
        var.set("Επιλέξτε..") 
        option = OptionMenu(win3, var, "Πόντος", "Καππαδοκία", "Αϊβαλί", "Κύπρος")
        option.grid(column=1, row=3,sticky='w')

        #3rd box
        textBox3=Text(win3, height=1.3,width=30)
        textBox3.grid(column=1, row=1,sticky='w')
        global x3
        x3=textBox3
        
        #4th box
        textBox4=Text(win3, height=1.3,width=60)
        textBox4.grid(column=1, row=2,sticky='w')
        global x4
        x4=textBox4


        #calls insert_clear insert buttons function
        btn_clr = tk.Button(win3,text="Καθαρισμός",command=lambda: insert_clear())
        btn_clr.grid(column=1, row=3,sticky='ns')
        btn_commit = tk.Button(win3,text="Εισαγωγή", command=s.insert_credentials)
        btn_commit.grid(column=1, row=3,sticky='nse')

 
        def insert_clear(): #clears insert boxes
                textBox.delete('1.0', END)
                var.set("Επιλέξτε..") 
                textBox3.delete('1.0', END)
                textBox4.delete('1.0', END)

                
    def insert_btn_clicked(s): #used only for insert
                cursor.execute("SELECT COUNT(*) from total2")
                result14=cursor.fetchone()
                number_of_total_latest=result14[0]
                username = s.entry_username.get()
                password = s.entry_password.get()

                inputValue=x.get("1.0","end-1c")  
                inputValue2=var.get()
                inputValue3=x3.get("1.0","end-1c")
                inputValue4=x4.get("1.0","end-1c")
                
                if username == "cs" and password == "cs":
                    qry = '''INSERT INTO total2 (Word,Region,Vocal,M1,ID) VALUES(?, ?, ?, ?, ?)'''
                    id_new=number_of_total_latest+1
                    param_values = [inputValue.upper(), inputValue2, inputValue3.lower(),inputValue4.lower(),id_new]
                    cursor.execute(qry, param_values)
                    cursor.commit() #Use this to commit the insert operation
                    tm.showinfo("Επιτυχής σύνδεση", "Η ενέργεια ολοκληρώθηκε")    
                else:
                    tm.showerror("Σφάλμα σύνδεσης", "Λάθος στοιχεία...")
#--------------------------------------------END OF INSERT FUNC----------------------------------------------------------------------------------------#



#--------------------------------------------DELETE FUNC-----------------------------------------------------------------------------------------------#        
    #Deletes a selected row/record 
    def delete_Window(s):
        if(s.tree.focus()==''): #if no record is selected...
            tm.showerror("Σφάλμα", "Παρακαλώ επιλέξτε εγγραφή...")
            return None #exit function
        win0=tk.Toplevel()
        win0.title("Login")
        win0.geometry('215x75')
        win0.resizable(False, False)
            
        s.label_username = Label(win0, text="Όνομα χρήστη")
        s.label_username.grid(row=0, column=0, sticky='e')
        s.entry_username = Entry(win0)
        s.entry_username.grid(row=0, column=1)
  
        s.label_password = Label(win0, text="Κωδικός")
        s.label_password.grid(row=1, column=0, sticky='e')
        s.entry_password = Entry(win0, show="*")
        s.entry_password.grid(row=1, column=1)

        s.logbtn = Button(win0, text="Σύνδεση", command=lambda:[s.delete_btn_clicked(),win0.destroy()]) #press login and destroy previous window
        s.logbtn.grid(columnspan=2)
        
    #Used only for delete
    def delete_btn_clicked(s):
             username = s.entry_username.get()
             password = s.entry_password.get()

             if username == "cs" and password == "cs":
                  for item in s.tree.selection():  #fetch selections while looping through the tree
                    cursor.execute("DELETE FROM total2 WHERE ID=?", (s.tree.set(item, '#6'),)) #delete a row in Total if Word=item) , item=user selected value
                    cursor.commit() #commit the deletion
                    s.tree.delete(item) #delete it from the current tree that user sees
                    tm.showinfo("Επιτυχής σύνδεση", "Η ενέργεια ολοκληρώθηκε")
             else:
                tm.showerror("Σφάλμα σύνδεσης", "Λάθος στοιχεία...")
#--------------------------------------------END OF DELETE FUNC-----------------------------------------------------------------------------------------------#    

                        
    #Searching by Word,M1,M2,M3 , input given in a search field by user , ONLY when the magnifier button is pressed
    def Search(k1):
        if SEARCH.get() != "":
            k1.tree.delete(*k1.tree.get_children()) #clears tree
            cursor.execute("SELECT * FROM total2 WHERE Word LIKE ? OR Region LIKE ? OR M1 LIKE ? OR M2 LIKE ? ",
                       ('%'+str(SEARCH.get())+'%', '%'+str(SEARCH.get())+'%','%'+str(SEARCH.get())+'%', '%'+str(SEARCH.get())+'%'))
            
            
            fetch1 = cursor.fetchall()
            for sol in fetch1:
                k1.tree.insert('', 'end', values=(sol[0],sol[3],xstr(sol[4]),xstr(sol[2]),sol[1],str(int(sol[5]))))
                

    #Called only when ENTER key is pressed,event as an arguement 
    def SearchEnter(k1,event): 
        if SEARCH.get() != "":
            k1.tree.delete(*k1.tree.get_children()) #clears tree
            cursor.execute("SELECT * FROM total2 WHERE Word LIKE ? OR Region LIKE ? OR M1 LIKE ? OR M2 LIKE ? ",
                       ('%'+str(SEARCH.get())+'%', '%'+str(SEARCH.get())+'%','%'+str(SEARCH.get())+'%', '%'+str(SEARCH.get())+'%'))
            
         

            fetch1 = cursor.fetchall()
            for sol in fetch1:
                k1.tree.insert('', 'end', values=(sol[0],sol[3],xstr(sol[4]),xstr(sol[2]),sol[1],str(int(sol[5]))))
                
         
    #Resets everything to the initial situtation(just prints the radiobuttons and the tree as they were)
    def Reset(s2):
        #Recount total rows,solves index none type problems,latest counter is initially correct and every next time "sees" the correct #rows
        cursor.execute("SELECT COUNT(*) from total2")
        result14=cursor.fetchone()
        number_of_total_latest=result14[0]
    
        #Cleans up the tree and prints initial values or new values upon deletion!
        s2.tree.delete(*s2.tree.get_children())
        cursor.execute("Select * from total2 ORDER BY Word")
        sol = cursor.fetchone()
        i=0
        while i<(number_of_total_latest): 
            s2.tree.insert('','end', values=(sol[0],sol[3],xstr(sol[4]),xstr(sol[2]),sol[1],str(int(sol[5]))))
            sol = cursor.fetchone()
            i=i+1


    def Graphs(s): #General graph , shows total data per dialect
        #Data
        labels = 'Πόντος', 'Καππαδοκία', 'Αϊβαλί', 'Κύπρος' 
        sizes = [cp,ck,ca,cc]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        explode = (0, 0, 0, 0)  # explode 1st slice

        #Name the window
        fig = plt.figure(0)
        fig.canvas.set_window_title('Γράφημα για τις 4 διαλέκτους')
 
        # Plot
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)    
        plt.axis('equal')

        #Title inside the window
        plt.title("Γράφημα των τεσσάρων διαλέκτων,\n" + "δεδομένα υπό μορφή Pie Chart.", bbox={'facecolor':'0.8', 'pad':5})
        plt.show()
    
    def Pon(s): #Prints Pontos when called
        s.tree.delete(*s.tree.get_children())
        cursor.execute("select * from total2 where Region=N'Πόντος'")
        fetch1 = cursor.fetchall()
        for sol in fetch1:
              s.tree.insert('','end', values=(sol[0],sol[3],xstr(sol[4]),xstr(sol[2]),sol[1],str(int(sol[5]))))
     
    def Kap(s): #Prints Kappadokia when called
        s.tree.delete(*s.tree.get_children())
        cursor.execute("select * from total2 where Region=N'Καππαδοκία'")
        fetch1 = cursor.fetchall()
        for sol in fetch1:
              s.tree.insert('','end', values=(sol[0],sol[3],xstr(sol[4]),xstr(sol[2]),sol[1],str(int(sol[5]))))

    def Aiv(s): #Prints Aivali when called
        s.tree.delete(*s.tree.get_children())
        cursor.execute("select * from total2 where Region=N'Αϊβαλί'")
        fetch1 = cursor.fetchall()
        for sol in fetch1:
              s.tree.insert('','end', values=(sol[0],sol[3],xstr(sol[4]),xstr(sol[2]),sol[1],str(int(sol[5]))))

    def Cyp(s): #Prints Cyprus when called
        s.tree.delete(*s.tree.get_children())
        cursor.execute("select * from total2 where Region=N'Κύπρος'")
        fetch1 = cursor.fetchall()
        for sol in fetch1:
              s.tree.insert('','end', values=(sol[0],sol[3],xstr(sol[4]),xstr(sol[2]),sol[1],str(int(sol[5]))))

    def About(s): #info about project and creators
        win_about=tk.Toplevel()
        win_about.title("Credits")
        win_about.geometry('300x100')
        win_about.resizable(False, False)
        win_about.attributes("-topmost", True) #win above all windows
        s.label_teacher1 = Label(win_about, text=' Φοιτητές:\t'+'Καλογήρου Δημήτριος\n\n'+'\t\tΡουσσάκης Ελευθέριος\n'
                                                 +'\n\n Επόπτρια Καθηγήτρια:\t'+'Γαλιώτου Ελένη')
        s.label_teacher1.grid(row=3, column=0)



    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()
        

    def _setup_widgets(self):
        #Frame for resizing the window
        c=ttk.Frame()
        c.pack(fill='both', expand=True)

#-------------------------------------------BUTTON AREA---------------------------------------------------------------------#
        #Info about the project and the people
        test = tk.Button(text='Credits', command=self.About)
        test.grid(column=0, row=0, columnspan=2, in_=c)
        
        #Pada image
        pada=tk.PhotoImage(file="./images/u2.png")
        buttonpada= tk.Button(image=pada,command=openweb)
        buttonpada.image=pada
        buttonpada.grid(column=0, row=2, sticky='n', columnspan=2,in_=c)

        #Generates variables for the radio buttons
        var2 =  IntVar()

        #Adds width to PK
        button1 = tk.Label(width=50)
        button1.grid(column=2, row=0,in_=c)

        #First radio button
        rad1 = Radiobutton(text='   Πόντος   ',value=1,variable=var2,bd=5,command=self.Pon)
        rad1.grid(column=2, row=0, sticky='w',in_=c)

        #Second radio button
        rad2 = Radiobutton(text='   Καππαδοκία   ',bd=5, value=2,variable=var2, command=self.Kap)
        rad2.grid(column=2, row=0, sticky='e',in_=c)

        #Adds width to PK,AK
        button2 = tk.Label(width=25)
        button2.grid(column=3, row=0,in_=c)

        #Adds width to AK
        button3 = tk.Label(width=50)
        button3.grid(column=4, row=0,in_=c)

        #Third radio button
        rad3 = Radiobutton(text='   Αϊβαλί   ',bd=5, value=3,variable=var2,command=self.Aiv)
        rad3.grid(column=4, row=0, sticky='w',in_=c)

        #Fourth radio button
        rad4 = Radiobutton(text='   Κύπρος   ',bd=5, value=4,variable=var2,command=self.Cyp )
        rad4.grid(column=4, row=0, sticky='e',in_=c)


        #Creates and packs a field.Entry given by SEARCH-->StringVar()
        search = Entry(textvariable=SEARCH)
        search.insert(0, 'Πληκτρολογήστε εδώ')
        search.bind("<FocusIn>",on_entry_click)  #when the field is clcked....
        search.bind('<Return>',self.SearchEnter) #when enter is pressed....
        search.config(fg = 'grey')
        search.grid(column=0, row=3,columnspan=2,sticky='we',in_=c)
        
        #Search Photo-Button
        photo1 = tk.PhotoImage(file="./images/6.png") 
        btn_search = Button(text="Αναζήτηση",image=photo1, fg='White', width=20, height=20, command=self.Search)  #when the button is pressed...
        btn_search.image = photo1
        btn_search.grid(column=1, row=3, sticky='e',in_=c)
        
        #Reset Button and clears the radio buttons with lambda
        btn_reset = tk.Button(text="Επαναφορά", fg='Red', command=lambda:[self.Reset(),var2.set(0)])
        btn_reset.grid(column=1, row=4, sticky='wens',in_=c)
        
        #Delete Button
        btn_del2 = tk.Button(text="Διαγραφή",fg='Green',command=self.delete_Window)
        btn_del2.grid(column=0, row=4, sticky='we',in_=c)

        #Lexical Distance Button
        self.Leven = Leven() #sets self.Leven to the Leven class
        btn_ld = tk.Button(text="Lexical Distance",command=self.Leven.ChildWindow) #if buttons is pressed use method from another class.
        btn_ld.grid(column=0, row=5,sticky='wes',in_=c)

        #Update button
        button_graph = tk.Button(text='Επεξεργασία',command=self.UpdateWindow)
        button_graph.grid(column=1, row=5, sticky='wes', in_=c)

        #Insert button
        btn_ins = tk.Button(text="Εισαγωγή", fg='Blue', command=self.insert_window)
        btn_ins.grid(column=0, row=6, sticky='wesn',in_=c)

        #Graphs button
        btn_graphs= tk.Button(text="Γράφημα", fg='Blue',command=self.Graphs)
        btn_graphs.grid(column=1, row=6, sticky='wesn',in_=c)

        #Dialect image
        dialect=tk.PhotoImage(file="./images/dialect.png")
        dial= tk.Label(image=dialect)
        dial.image=dialect
        dial.grid(column=0, row=7, columnspan=2,sticky='s',in_=c)
#-------------------------------------------END OF BUTTON AREA---------------------------------------------------------------------#


#-------------------------------------------TREEVIEW AREA---------------------------------------------------------------------#
        #create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        #tree placement
        self.tree.grid(column=2, row=1, sticky='nsew', rowspan=7, columnspan=3,in_=c)
        vsb.grid(column=5, row=0, sticky='ns', rowspan=8,in_=c)
        hsb.grid(column=2, row=8, sticky='ew', columnspan=3,in_=c)

        #Window Maximization 
        c.grid_columnconfigure(0, weight=2)
        c.grid_columnconfigure(1, weight=2)
        c.grid_columnconfigure(2, weight=2)
        c.grid_rowconfigure(1, weight=1)
        c.grid_rowconfigure(2, weight=2)
        c.grid_rowconfigure(7, weight=2)
        
        
        #creates the tree
    def _build_tree(self):
        for col in header:
            self.tree.heading(col, text=col.title(),command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,width=tkFont.Font().measure(col.title()))

        
        #Fills the tree with values from db,prints total2 table    
        cursor.execute("select * from total2 order by Word")
        sol = cursor.fetchone()
        i=0
        while i<(number_of_total):
            self.tree.insert('','end', values=(sol[0],sol[3],xstr(sol[4]),xstr(sol[2]),sol[1],str(int(sol[5]))))
            sol = cursor.fetchone()
            i=i+1
#-------------------------------------------END  AREA---------------------------------------------------------------------#


#-------------------------------------------SORT AREA---------------------------------------------------------------------#
def sortby(tree, col, descending):  #sorts every column when it is pressed by user
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    data.sort(reverse=descending)
    
    for ix, item in enumerate(data):
            if col=="I.D":  #if ID column is clicked then print an error msg
                tm.showerror("Σφάλμα", "Μη εφικτή ταξινόμηση...")
                break
            tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))
#-------------------------------------------END OF SORT AREA---------------------------------------------------------------------#

#Column titles
header = ['Λέξη', "Κύριος ορισμός","Ορισμός 2","Φωνητική Απόδοση","Περιοχή","I.D"]


#-------------------------------------------GUI AREA---------------------------------------------------------------------#
if __name__ == '__main__':
    root = tk.Tk()
    #used for Splash class (intro timer)
    d_status = StringVar()
    d_status.set("Initializing...")
    with Splash(root, './images/e.png', 3.0) as s:
       initializeMyApplication(s.foo)
       s.foo("Η φόρτωση ολοκληρώθηκε!!")
       buildTheGUI(root)

    SEARCH = StringVar() #StringVar() for search field
    root.title("Υπολογιστική Επεξεργασία Διαλέκτων της Ελληνικής Γλώσσας")
    listbox = Dialects() #calls the main class
    root.deiconify() #keeps main window hidden until splash class timer finishes
    root.mainloop()
