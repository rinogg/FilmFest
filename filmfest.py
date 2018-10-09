import urllib
import requests
from Tkinter import *
from PIL import ImageTk
from PIL import Image
from resizeimage import resizeimage
from collections import OrderedDict
from BeautifulSoup import BeautifulSoup
import cStringIO
import time

log = OrderedDict(eval(open("filmfestlog.txt").read()))
descrlog = OrderedDict(eval(open("filmfestdescr.txt").read()))
copy = u"\u00A9"

class MyDialog:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text=copy + "Filmfest(2017) \nMade by Andrew Vatavu .\nThis program is made using Python and Tkinter.\n Enjoy your movies!").pack()

        b = Button(top, text="Thanks Andrew", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        self.top.destroy()

def About():
    d = MyDialog(root)

def DeleteSelection():
    items = listbox.curselection()
    name = listbox.get(items)
    try:
        log.pop(name)
    except KeyError:
        pos = 0
        for i in items :
            idx = int(i) - pos
            listbox.delete( idx,idx )
            pos = pos + 1
    pos = 0
    for i in items :
        idx = int(i) - pos
        listbox.delete( idx,idx )
        pos = pos + 1
    with open('filmfestlog.txt', 'w') as filmfestlog:
        filmfestlog.write(str(log))
    lab1.destroy()
    lab2.destroy()
    lab3.destroy()
    print log

def InsertEntry():
    name = e1.get()
    genre = e2.get()
    year = e3.get()
    if e1.get() == "" or e1.get() == " ":
        return 0
    if name in log:
        name = e1.get() + " "
    log[name] = (genre, year)
    listbox.insert(END, name)
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    print log
    with open('filmfestlog.txt', 'w') as filmfestlog:
        filmfestlog.write(str(log))
    print log[name]

def ClearFields():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)



def OnSelect(evt):


    global lab1, lab2, lab3, poster, msg

    w = evt.widget
    index = int(w.curselection()[0])
    items = listbox.curselection()
    name = listbox.get(items)
    value = log[name]

    # MOVIE POSTER & DESCR FUNCTION

            #description
    msg.destroy() # destroy previous message

                # try getting descr from descrlogfirst
    try:
        descr = descrlog[name]
    except KeyError:

                    #Get Descr from the internet

        imdbid = IdFromTitle(name)
        url = urllib.urlopen("http://www.imdb.com/title/" + imdbid + "/")
        content = url.read()
        soup = BeautifulSoup(content)
        links = soup.find("div", {"class" : "summary_text"})#.find("img")
                    #Format Descr
        format1 = str(links)
        format2 = format1.replace('<div class="summary_text" itemprop="description">',"")
        format3 = format2.replace("</div>","")
        format4 = list(format3)
        del format4[0:21]
        descr = "".join(format4)
        descrlog[name] = descr
                    #save the downloaded descr from the internet to file
        with open('filmfestdescr.txt', 'w') as filmfestdescr:
            filmfestdescr.write(str(descrlog))


    msg = Message(root, text=descr)
    msg.config(justify=CENTER,font=("Times", 13),aspect = 500, anchor=CENTER)
    msg.place(relx=0.41, rely=0.77)

            #name verification for jpg saving
    chars = ["~", "#", "%", "&", "*", "{", "}", "\\", ":", "<", ">", "?", "/", "+", "|", "\""]
    for i in chars:
        if i in list(name):
            localjpg = str(name)
            localjpg2 = localjpg.replace(str(i), " ")
            break
        else:
            localjpg2 = str(name)

    try: # if there is a jpg already

        img = Image.open(localjpg2 + ".jpg")
        basewidth = 260
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)


    except IOError:  # if there isn't a jpg downlaod one

                    #grab poster from the internets
        imdbid = IdFromTitle(name)
        url = urllib.urlopen("http://www.imdb.com/title/" + imdbid + "/")
        content = url.read()
        soup = BeautifulSoup(content)
        links = soup.find("div", {"class" : "poster"}).find("img")
        link = re.findall(r'src=[\'"]?([^\'" >]+)', str(links))[0]
        file = cStringIO.StringIO(urllib.urlopen(link).read())
        img = Image.open(file)

                    #resize image and save
        basewidth = 260
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img.save(localjpg2 + '.jpg')

                #convert image in TK friendly and display
    poster = ImageTk.PhotoImage(img)
    posterplace = Label(root, image=poster).place(relx=0.5, rely=0.065)

                #labels on the right
    lab1.destroy()
    lab2.destroy()
    lab3.destroy()
    lab1 = Message(root, text=name)
    lab2 = Label(root, text=value[1])
    lab3 = Label(root, text=value[0])
    lab1.place(relx=0.65, rely=0.04, anchor=CENTER)
    lab2.place(relx=0.810, rely=0.14, anchor=W)
    lab3.place(relx=0.810, rely=0.25, anchor=W)
    lab1.config(font=("Impact", 14), aspect=1000)
    lab2.config(font=("Arial", 12))
    lab3.config(font=("Arial", 12))


def IdFromTitle(title):
    #     return IMDB id for search string
    #
    #     Args::
    #         title (str): the movie title search string
    #
    #     Returns:
    #         str. IMDB id, e.g., 'tt0095016'
    #         None. If no match was found

    pattern = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q={movie_title}'
    url = pattern.format(movie_title=urllib.quote(title))
    r = requests.get(url)
    res = r.json()
    # sections in descending order or preference
    for section in ['popular','exact','substring']:
        key = 'title_' + section
        if key in res:
            return res[key][0]['id']

def Quit():
    sys.exit()

#TITLE AND INIT
root = Tk()
root.iconbitmap('ff.ico')
root.title("Film Fest 0.8.7")
root.maxsize(900,600);
root.minsize(900,600);

#ENTRY FIELDS
Label(root, text="Name").place(relx=0.05, rely=0.05, anchor=CENTER)
Label(root, text="Genre").place(relx=0.05, rely=0.13, anchor=CENTER)
Label(root, text="Year").place(relx=0.05, rely=0.21, anchor=CENTER)

e1 = Entry(root)
e2 = Entry(root)
e3 = Entry(root)
e1.place(relx=0.1, rely=0.09, anchor=CENTER)
e2.place(relx=0.1, rely=0.17, anchor=CENTER)
e3.place(relx=0.1, rely=0.25, anchor=CENTER)

# ADD BUTTON
Button(root,
       text="Add",
       pady=5,
       padx=11,
       command=InsertEntry).place(relx=0.03, rely=0.29)

# DELETE BUTTON
Button(root,
       text="Delete entry",
       padx=54,
       command=DeleteSelection).place(relx=0.22, rely=0.68)

# CLEAR FIELDS BUTTON
Button(root,
       text="Clear fields",
       pady=5,
       command=ClearFields).place(relx=0.093, rely=0.29)

# QUIT BUTTON
Button(root,
       text="QUIT",
       padx=10,
       pady=5,
       command=Quit).place(relx=0.93, rely=0.93)
# ABOUT BUTTON
Button(root,
       text="About",
       padx=10,
       pady=5,
       command=About).place(relx=0.03, rely=0.93)

# LISTBOX AND SCROLLBAR
scrollbar = Scrollbar(root)
scrollbar.place(relx=0.4, rely=0.07, height=360)
listbox = Listbox(root)
listbox.place(relx=0.22, rely=0.07, height=360, width=160)



for i in log:
    listbox.insert(END, i)

        # attach listbox to scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

        #bind list selection to OnSelect command
listbox.bind('<<ListboxSelect>>', OnSelect)

#grid(row=0, column=7, pady=10, sticky=E, rowspan=10)



# MOVIE DESCR


#grid(row=11, column=7, pady=10, columnspan=8)

# NAME, YEAR, GENRE of SELECTED MOVIE
    #here they are empty and updated on the OnSelect function all the time
name = ""
value = ""
lab1 = Message(root, text=name)#grid(row=0, sticky=W, column=0)
lab2 = Label(root, text=value)
lab3 = Label(root, text=value)
lab1.place(relx=0.825, rely=0.09, anchor=CENTER)
lab2.place(relx=0.825, rely=0.17, anchor=CENTER)
lab3.place(relx=0.825, rely=0.25, anchor=CENTER)

# cv = Canvas(bg='white')
# cv.place(relx=0.5, rely=0.065)
# put the image on the canvas with
# create_image(xpos, ypos, image, anchor)

# VAR REFERENCES
msg = msg = Message(root, text=None)
img1 = "poster_thumb.jpg"
poster = PhotoImage(img1)
load = Message(root, text=None)



#Label(root, image=poster).place(relx=0.5, rely=0.065)


mainloop()
