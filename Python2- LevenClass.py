#SQL Server Database connection--------------------------------------------------------------------------------------------------------#
import pyodbc 
server   = 'dlserv.database.windows.net' 
database = 'LDB' 
username = '**********' 
password = '**********'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#--------------------------------------------------------------------------------------------------------------------------------------#

#----------------------------------------DB ROW COUNTERS-----------------------------------------------#
cursor.execute("select * from total2 WHERE Region=N'Πόντος'")
pontos=cursor.fetchall()

cursor.execute("select * from total2 WHERE Region=N'Καππαδοκία'")
kappadokia=cursor.fetchall()

cursor.execute("select * from total2 WHERE Region=N'Αϊβαλί'")
aivali=cursor.fetchall()

cursor.execute("select * from total2 WHERE Region=N'Κύπρος'")
cyprus=cursor.fetchall()

cursor.execute("SELECT COUNT(*) from total2")
result=cursor.fetchone()
number_of_total=result[0]


#---------------------------------------END OF DB ROW COUNTERS-------------------------------------------#

#------------------------------------------------Imports------------------------------------------------------------#

#Graphs imports
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy.core._dtype_ctypes
#Other .py files imports
from tooltip import *

#Web links import
import webbrowser
import tkinter.ttk as ttk
#General imports
from tkinter import * #imports these libs: Tk, ttk, Button, PhotoImage,StringVar,Toplevel,Label,TOP,IntVar,Radiobutton,Entry,Text,OptionMenu,END
import tkinter as tk
import tkinter.font as tkFont

#------------------------------------------------------End of Imports-------------------------------------------------------------------#


#------------------------------------------------------Global Functions-----------------------------------------------------------------#


#Web link functions and data
url = "http://www.ice.uniwa.gr"
url2= "https://en.wikipedia.org/wiki/Levenshtein_distance"
def openweb():
    webbrowser.open(url,True)
def openweb2():
    webbrowser.open(url2,True)


#Levensthein algorithm , returns int
def minimumEditDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]


#Levensthein algorithm , returns percentage
def minimumEditDistancePerc(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return (1-distances[-1] / max(len(s1), len(s2)))*100


#-----------------------------------------------End of Global Functions-------------------------------------------------------------------#

class Leven(object):

    def GeneralGraph(s):
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        fig.canvas.set_window_title('Αποτελέσματα κοινών λέξεων ανα διάλεκτο...') #insert window title
        pairs = ["Καππαδοκία-Κύπρος","Πόντος-Αϊβαλί","Πόντος-Κύπρος","Αϊβαλί-Καππαδοκία","Αϊβαλί-Κύπρος","Πόντος-Καππαδοκία"]
        c1=c2=c3=c4=c5=c6=1
        for x1 in pontos:
                    for y1 in kappadokia:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):        
                            c1=c1+1
        for x1 in aivali:
                    for y1 in cyprus:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):                   
                            c2=c2+1
        for x1 in aivali:
                    for y1 in kappadokia:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):
                            c3=c3+1
        for x1 in pontos:
                    for y1 in cyprus:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):
                            c4=c4+1
        for x1 in pontos:
                    for y1 in aivali:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):
                            c5=c5+1
        for x1 in kappadokia:
                    for y1 in cyprus:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):
                            c6=c6+1
        
        
        data = [c6, c5, c4, c3, c2, c1]

        wedges, texts, autotexts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40, autopct='%1.1f%%', pctdistance=0.7)

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(pairs[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),horizontalalignment=horizontalalignment, **kw)

        #Title inside the graph
        ax.set_title("Γράφημα κοινών λέξεων ανα διάλεκτο")
        #Show the graph
        plt.show()


        
    def PairGraph(s):
                matrix=['','','','','',''] # Empty matrix , awaits for 6 variables used for results(percentages)
                a1=a2=a3=a4=a5=a6=0        # Counters for adding percentages
                c1=c2=c3=c4=c5=c6=0        # Counters used for average (a/c)
                for x1 in pontos:          # Loop through Pontos words
                        for y1 in kappadokia:  # Loop through Kappadokia words
                                if(x1[3]==y1[3] or x1[3]==y1[4]):   # If Pontos Meaning 1 == Kappadokia Meaning 1
                                        xnew=(minimumEditDistancePerc(x1[0],y1[0])) # Store Levenshtein results for each comparison
                                        a1=a1+xnew                                  
                                        c1=c1+1
                                        d1=format(a1/c1,'7.2f')                     # Format result print
                                        matrix[0]=float(d1)                         # Store result in the first position of the matrix , printed later.
                for x1 in aivali:
                        for y1 in cyprus:
                                if(x1[3]==y1[3] or x1[3]==y1[4]):                  
                                        xnew=(minimumEditDistancePerc(x1[0],y1[0]))
                                        a2=a2+xnew
                                        c2=c2+1
                                        d2=format(a2/c2,'7.2f')
                                        matrix[4]=float(d2)
                for x1 in aivali:
                        for y1 in kappadokia:
                                if(x1[3]==y1[3] or x1[3]==y1[4]): 
                                        xnew=(minimumEditDistancePerc(x1[0],y1[0]))
                                        a3=a3+xnew
                                        c3=c3+1
                                        d3=format(a3/c3,'7.2f')
                                        matrix[2]=float(d3)
                for x1 in pontos:
                        for y1 in cyprus:
                                if(x1[3]==y1[3] or x1[3]==y1[4]): 
                                        xnew=(minimumEditDistancePerc(x1[0],y1[0]))
                                        a4=a4+xnew
                                        c4=c4+1
                                        d4=format(a4/c4,'7.2f')
                                        matrix[3]=float(d4)
                for x1 in pontos:
                        for y1 in aivali:
                                if(x1[3]==y1[3] or x1[3]==y1[4]): 
                                        xnew=(minimumEditDistancePerc(x1[0],y1[0]))
                                        a5=a5+xnew
                                        c5=c5+1
                                        d5=format(a5/c5,'7.2f')
                                        matrix[1]=float(d5)
                for x1 in kappadokia:
                        for y1 in cyprus:
                                if(x1[3]==y1[3] or x1[3]==y1[4]): 
                                        xnew=(minimumEditDistancePerc(x1[0],y1[0]))
                                        a6=a6+xnew
                                        c6=c6+1
                                        d6=format(a6/c6,'7.2f')
                                        matrix[5]=float(d6)

                plt.style.use('ggplot')
                objects = ["Πόντος\nΚαππαδοκία","Πόντος\nΑϊβαλί","Αϊβαλί\nΚαππαδοκία","Πόντος\nΚύπρος","Αϊβαλί\nΚύπρος","Καππαδοκία\nΚύπρος"]
                fig, ax = plt.subplots(figsize = (10,5))
                fig.canvas.set_window_title('Γράφημα ομοιότητας διαλέκτων ανα ζεύγος') #window title
                ax.bar(objects,matrix,width=0.1)
                for index,data in enumerate(matrix):
                    plt.text(x=index-0.1 , y =data+0.35 , s=f"{data}" , fontdict=dict(fontsize=10))
                plt.ylim(0, 100)
                plt.ylabel('Ποσοστό %')
                #title inside the graph
                plt.title('Ποσοστό ομοιότητας διαλέκτων ανα ζεύγος')
                plt.show()       


    #prints result for two selected dialects
    def combo(s):
            if((var1.get()=='Πόντος' and var2.get()=='Καππαδοκία')or(var1.get()=='Καππαδοκία' and var2.get()=='Πόντος')):
                s.tree.delete(*s.tree.get_children()) #clear previous prints
                s.tree.heading("Λέξη 1", text='Πόντος')
                s.tree.heading("Λέξη 2", text='Καππαδοκία') 
                c=1
                for x1 in pontos:
                    for y1 in kappadokia:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):
                            x=format(minimumEditDistancePerc(x1[0],y1[0]),'7.2f')
                            s.tree.insert('','end', values=(x1[0],y1[0],(" \t %s %%" % x),(x1[3])))
                            c=c+1
                           
            elif((var1.get()=='Πόντος' and var2.get()=='Αϊβαλί')or(var1.get()=='Αϊβαλί' and var2.get()=='Πόντος')):
                s.tree.delete(*s.tree.get_children()) #clear previous prints
                s.tree.heading("Λέξη 1", text='Πόντος') 
                s.tree.heading("Λέξη 2", text='Αϊβαλί')
                c=1
                for x1 in pontos:
                    for y1 in aivali:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):
                            x=format(minimumEditDistancePerc(x1[0],y1[0]),'7.2f')
                            s.tree.insert('','end', values=(x1[0],y1[0],(" \t %s %%" % x),(x1[3])))
                            c=c+1
                   
            elif((var1.get()=='Αϊβαλί' and var2.get()=='Καππαδοκία')or(var1.get()=='Καππαδοκία' and var2.get()=='Αϊβαλί')):
                s.tree.delete(*s.tree.get_children()) #clear previous prints
                s.tree.heading("Λέξη 1", text='Αϊβαλί')
                s.tree.heading("Λέξη 2", text='Καππαδοκία') 
                c=1
                for x1 in aivali:
                    for y1 in kappadokia:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):
                            x=format(minimumEditDistancePerc(x1[0],y1[0]),'7.2f')
                            s.tree.insert('','end', values=(x1[0],y1[0],(" \t %s %%" % x),(x1[3])))
                            c=c+1
                
            elif((var1.get()=='Κύπρος' and var2.get()=='Πόντος')or(var1.get()=='Πόντος' and var2.get()=='Κύπρος')):
                s.tree.delete(*s.tree.get_children()) #clear previous prints
                s.tree.heading("Λέξη 1", text='Κύπρος')
                s.tree.heading("Λέξη 2", text='Πόντος') 
                c=1
                for x1 in cyprus:
                    for y1 in pontos:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):
                            x=format(minimumEditDistancePerc(x1[0],y1[0]),'7.2f')
                            s.tree.insert('','end', values=(x1[0],y1[0],(" \t %s %%" % x),(x1[3])))
                            c=c+1
                
            elif((var1.get()=='Κύπρος' and var2.get()=='Αϊβαλί')or(var1.get()=='Αϊβαλί' and var2.get()=='Κύπρος')):
                s.tree.delete(*s.tree.get_children()) #clear previous prints
                s.tree.heading("Λέξη 1", text='Κύπρος')
                s.tree.heading("Λέξη 2", text='Αϊβαλί') 
                c=1
                for x1 in cyprus:
                    for y1 in aivali:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):
                            x=format(minimumEditDistancePerc(x1[0],y1[0]),'7.2f')
                            s.tree.insert('','end', values=(x1[0],y1[0],(" \t %s %%" % x),(x1[3])))
                            c=c+1
                
            elif((var1.get()=='Κύπρος' and var2.get()=='Καππαδοκία')or(var1.get()=='Καππαδοκία' and var2.get()=='Κύπρος')):
                s.tree.delete(*s.tree.get_children()) #clear previous prints
                s.tree.heading("Λέξη 1", text='Κύπρος')
                s.tree.heading("Λέξη 2", text='Καππαδοκία') 
                c=1
                for x1 in cyprus:
                    for y1 in kappadokia:
                        if(x1[3]==y1[3] or x1[3]==y1[4]):
                            x=format(minimumEditDistancePerc(x1[0],y1[0]),'7.2f')
                            s.tree.insert('','end', values=(x1[0],y1[0],(" \t %s %%" % x),(x1[3])))
                            c=c+1
                
            else:
                 s.tree.delete(*s.tree.get_children())
            

  
    #Levenclass window creation
    def ChildWindow(s):
        #Creates the window and names the window
        win2=tk.Toplevel()
        win2.title("Lexical Distance")
        win2.resizable(False, False)


#-------------------------------------------------------INNER FUNCTIONS AREA--------------------------------------------------------------------# 
        #LEVENSTHEIN TEST AREA
        #Clears the contents of the 2 textboxes,if clear button is pressed.
        def clear():
            textBox.delete('1.0', END)
            textBox2.delete('1.0', END)
            textBox3.delete('1.0', END)
            
        #Holds both the values of the 2 textboxes,calls leven func,prints result to the 3rd box.
        def EditDistance():
            textBox3.delete('1.0', END)
            inputValue=textBox.get("1.0","end-1c")  #'1.0 = start from first char in the text
            inputValue2=textBox2.get("1.0","end-1c") #'end-1c' = delete the last char that text creates every time
            a=(minimumEditDistance(inputValue,inputValue2))
            textBox3.insert('1.0',a)

#-------------------------------------------------------END OF INNER FUNCTIONS AREA--------------------------------------------------------------------#


#-------------------------------------------BUTTON AREA---------------------------------------------------------------------#
        #Example image
        example=tk.PhotoImage(file="./images/2.png")
        btn1= tk.Label(win2,image=example)
        btn1.image=example
        btn1.grid(column=0, row=0, columnspan=2,rowspan=2)

        #Creates a tooltip,by using another class,from tooltip.py
        button1_ttp = CreateToolTip(btn1, "Η έννοια του Edit Distance αφορά στην Εισαγωγή,την Αντικατάσταση και τη Διαγραφή χαρακτήρα.")

        #The title
        button1 = tk.Label(win2, width=31, height=4)
        button1.grid(column=2, row=0)

        #The title
        button2 = tk.Label(win2, text='Παρακαλώ επιλέξτε 2 περιοχές:')
        button2.grid(column=2, row=0, sticky='n')
        
        #Drop down menu for Region choice #1
        global var1
        var1 = StringVar(win2)
        var1.set("Περιοχή #1..") 
        option1 = OptionMenu(win2, var1, "Πόντος", "Καππαδοκία", "Αϊβαλί", "Κύπρος")
        option1.grid(column=2, row=0, sticky='w')
        
        #Drop down menu for Region choice #2
        global var2
        var2 = StringVar(win2)
        var2.set("Περιοχή #2..") 
        option2 = OptionMenu(win2, var2, "Πόντος", "Καππαδοκία", "Αϊβαλί", "Κύπρος")
        option2.grid(column=2, row=0,sticky='e')

        #Commit combo button
        b=Button(win2, text="OK",command=lambda:[s.combo()])
        b.grid(column=3, row=0)
        
        #GeneralGraph button
        btnBoth=Button(win2, text="   Γενικό Γράφημα   ", command=s.GeneralGraph)
        btnBoth.grid(column=4, row=0,sticky='wen')
        #PairGraph button
        btnBoth1=Button(win2, text="   Ποσοστά Ομοιότητας   ", command=s.PairGraph)
        btnBoth1.grid(column=4, row=0,sticky='wes')

        #InfoButton for tooltip Levensthein
        d=tk.PhotoImage(file="./images/i3.png")
        btn_ins= tk.Label(win2,image=d, width=20, height=20,bg='grey')
        btn_ins.image=d
        btn_ins.grid(column=0, row=3)
        leven_tip = CreateToolTip(btn_ins, "Εισάγετε 2 λέξεις \n και υπολογίστε τη διαφορά τους \n με τον αλγόριθμο του Levensthein")

        #Label above textBox1
        lb1 = tk.Label(win2, text='Λέξη #1')
        lb1.grid(column=0, row=4,sticky='s')

        #1st box creation for 1st user test levensthein
        textBox=Text(win2,height=1,width=10)
        textBox.grid(column=0, row=5, sticky='n')

        #Label above textBox2
        lb2 = tk.Label(win2, text='Λέξη #2')
        lb2.grid(column=0, row=6,sticky='s')

        #2nd box creation for 1st user test levensthein
        textBox2=Text(win2, height=1.3,width=10)
        textBox2.grid(column=0, row=7, sticky='n')

        #Label above textBox3
        lb3 = tk.Label(win2, text='Αποτέλεσμα')
        lb3.grid(column=0, row=8,sticky='s')

        #3rd box,output of f1,f2 will be placed here
        textBox3=Text(win2, height=1.3,width=10)
        textBox3.grid(column=0, row=9, sticky='n')

        #Insert,delete,substitution pic
        pic=PhotoImage(file="./images/two.png")
        picbtn=tk.Label(win2, image=pic)
        picbtn.image=pic
        picbtn.grid(column=1, row=3,sticky='n', rowspan=5)

        #Clear button
        btnClear=Button(win2,height=1,width=10,text="    Καθαρισμός    ",command=lambda: clear())
        btnClear.grid(column=1, row=7,rowspan=2, sticky='n')
            
        #Calculate button
        btnBoth=Button(win2,height=1,width=10,text="    Υπολογισμός    ",command=lambda: EditDistance())
        btnBoth.grid(column=1, row=8,sticky='s',rowspan=2)


        #Leven image
        dialect=tk.PhotoImage(file="./images/l.png")
        dial= tk.Button(win2, image=dialect,command=openweb2)
        dial.image=dialect
        dial.grid(column=0, row=13, columnspan=2,sticky='s')


#-------------------------------------------END OF BUTTON AREA---------------------------------------------------------------------#


    
        #Creates a tooltip,by using another class,from tooltip.py
        #For separated text with ENTER , we use \n just like the following text.
        dial_ttp = CreateToolTip(dial, " Ο αλγόριθμος Levenshtein,βασίζεται στον υπολογισμό \n του κόστους μεταβολής της μιας συμβολοσειράς στην άλλη.")
        


 
#-------------------------------------------TREEVIEW AREA---------------------------------------------------------------------#
        #Tree setup
        header = ['Λέξη 1', "Λέξη 2","Ποσοστό ομοιότητας","Ορισμός"]
        s.tree = ttk.Treeview(win2,columns=header, show="headings",height=15)
        vsb = ttk.Scrollbar(win2,orient="vertical",command=s.tree.yview)
        hsb = ttk.Scrollbar(win2,orient="horizontal",command=s.tree.xview)
        s.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        s.tree.grid(column=2, row=1, sticky='nsew', rowspan=13, columnspan=4)
        vsb.grid(column=5, row=0, sticky='ns', rowspan=14)
        hsb.grid(column=2, row=14, sticky='ew', columnspan=4)
        
      
        #Draws the tree inside the child window
        for col in header:
            s.tree.heading(col, text=col.title(),command=lambda c=col: sortby(s.tree, c, 0))
            s.tree.column(col,width=tkFont.Font().measure(col.title()))

#-------------------------------------------END OF TREEVIEW AREA---------------------------------------------------------------------#


#-------------------------------------------SORT AREA---------------------------------------------------------------------#
def sortby(tree, col, descending):  #sorts every column when it is pressed by user
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))
#-------------------------------------------END OF SORT AREA---------------------------------------------------------------------#
