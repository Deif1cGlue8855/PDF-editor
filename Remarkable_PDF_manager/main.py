import tkinter as tk
import fitz
from PIL import Image, ImageTk
import io
import PDF_Splitter
import math
import os


destination = "C:/Users/arlot/Downloads/test_modded.pdf"

#currPath = "C:/Users/arlot/Downloads/test.pdf"
currPath = ""

mouseVal = 0
file = 0
fileRect = 0

cutPoints = []
lineNums = []
cutY = []
distsAllow = []
trueBox = []

jumpDist = 20
selectedLine = 1
minLineNum = 0

offset =20


def initPdfFile(filePath):
    global minLineNum,file, fileRect, mouseVal, jumpDist, selectedLine

    file = fitz.open(filePath)
    pg = file[0]
    fileRect = pg.rect

    split = math.ceil(fileRect.height / 670)

    minLineNum = split

    for i in range(split):
        line = tk.Frame(root, bg = "black", height = 1, width = 470)
        line.place(x = 10, y = 50 + (i * 670))

        cutPoints.append(line)

        label = tk.Label(root, text = str(i))
        box = tk.Label(root, bg ="red")
        box2 = tk.Label(root, bg ="red")
        trueBox.append([box,box2])

        lineNums.append(label)

        distsAllow.append([True, True])

        cutY.append(i * 670)
    
def onMouseWheel(event):
    global mouseVal
    if event.delta > 0:
        mouseVal -= 20
        if(mouseVal < 0):
            mouseVal = 0
    elif event.delta < 0:
        mouseVal += 20
        if(mouseVal + 700 > fileRect.height):
            mouseVal = fileRect.height - 700


    load_pdf()
    drawCutLines()

def load_pdf():
    global pdf_image, mouseVal
    
    doc = file

    page = doc[0]  

    tail = mouseVal + 700

    cropper = fitz.Rect(0,mouseVal,455,tail)

    pix = page.get_pixmap(clip=cropper)

    img = Image.open(io.BytesIO(pix.tobytes()))

    pdf_image = img
    show_page()

def show_page():
   if pdf_image:
        # Convert the PIL image to Tkinter format
        pdf_tk_image = ImageTk.PhotoImage(pdf_image)

        # Display the cropped image in the Tkinter label
        label.config(image=pdf_tk_image)
        label.image = pdf_tk_image

        label.place(x = 20, y = 50)
        
def drawCutLines():
    
    for i,line in enumerate(cutPoints):
        currY = line.winfo_y()
        eh = False
        if(i < len(lineNums)):
            text = lineNums[i]
            allowTop = trueBox[i][0]
            allowBot = trueBox[i][1]
            eh = True
        if(cutY[i] > mouseVal and cutY[i] < mouseVal + 700):
            yPos = 50 + (cutY[i] - mouseVal)
            line.place(x = 10, y = yPos)
            line.lift()
            if(eh):
                text.place(x = 5,y = yPos - 10)
                text.lift()

                allowTop.config(bg = "red")
                allowBot.config(bg = "red")

                if(distsAllow[i][0]):
                    allowTop.config(bg = "green")
                if(distsAllow[i][1]):
                    allowBot.config(bg = "green")

                allowTop.place(x = 470, y=yPos - 20)
                allowTop.lift()
                allowBot.place(x = 470, y=yPos + 2)
                allowBot.lift()
            #root.after(100, drawCutLines)
        else:
            line.place_forget()
            if(eh):
                text.place_forget()
                allowTop.place_forget()
                allowBot.place_forget()

def checkValidOfLines():
    for i in range(len(cutY)):
        if( i == 0):
            continue
        prevY = cutY[i-1]
        currY = cutY[i]
        if(len(cutY) - i != 1):
            nextY = cutY[i + 1]
        else:
            nextY = fileRect.height

        if(abs(currY - prevY) > 670):
            distsAllow[i][0] = False
        else:
            distsAllow[i][0] = True

        if(abs(currY - nextY) > 670):
            distsAllow[i][1] = False
        else:
            distsAllow[i][1] = True

def addLine():
    line = tk.Frame(root, bg = "black", height = 1, width = 470)
    line.place(x = 10, y = 650 * 2)

    cutPoints.append(line)

    label = tk.Label(root, text = str(len(cutY)))
    box = tk.Label(root, bg ="red")
    box2 = tk.Label(root, bg ="red")
    trueBox.append([box,box2])

    lineNums.append(label)

    distsAllow.append([True, True])

    cutY.append(fileRect.height - 10)

def removeLine():
    if(len(cutY) - 1 >= minLineNum):
        cutPoints[-1].place_forget()
        cutPoints.pop()

        lineNums[-1].place_forget()
        lineNums.pop()

        distsAllow.pop()

        cutY.pop()

        trueBox[-1][0].place_forget()
        trueBox[-1][1].place_forget()
        trueBox.pop()

def checkToSendOff():

    allow = True
    err = None
    name = nameTag.get()
    for i in range(len(distsAllow)):
        for j in range(2):
            if(distsAllow[i][j] == False):
                allow = False
                err = f"on line {i}"
                break
        if(not allow):
            break
    if(name == "" or name == "Enter name" or name == " "):
        allow = False
        err = "in name"


    if(allow == True):
        PDF_Splitter.splitPDF(currPath, name, cutY)
        error.config(text = f"Slice Completed")
    else:
        error.config(text = f"Error {err}")

    error.place(x = 500, y = 700)


def moveUp():
    getLineSelect()
    saveJumpDist()
    cutY[selectedLine] -= jumpDist 
    drawCutLines()
    checkValidOfLines()
def moveDown():
    getLineSelect()
    saveJumpDist()
    cutY[selectedLine] += jumpDist
    drawCutLines()
    checkValidOfLines()

def getLineSelect():
    global selectedLine
    temp = int(lineSelect.get())
    if(temp > 0 and temp < len(cutY)):
        selectedLine = temp

def saveJumpDist():
    global jumpDist
    jumpDist = int(jumpDistEnter.get())
        
while(True):
    fPath = input(">") 
    #fPath = "C:/Users/arlot/Downloads/test.pdf"
    if(fPath[0] == "\"" and fPath[-1] == "\""):
        fPath = fPath[1:-1]

    if(os.path.exists(fPath) and fPath[-4:] == ".pdf"):
        currPath = fPath

        break
    else:
        print("INVALID PATH")
    
root = tk.Tk()

initPdfFile(currPath)

root.title("PDF Edior")

root.geometry("1000x800")

root.configure(bg = "gray")

label = tk.Label(root, bg="gray")

label = tk.Label(root)
label.pack()

error = tk.Label(root, text = "")


#Select cut line text box
lineSelect = tk.Entry(root, width = 3, font =("Arial", 20))

#Change line jump value
jumpDistEnter = tk.Entry(root, width = 3, font =("Arial", 20))

#Button to move line up
moveUpButton = tk.Button(root, text = "UP",width = 30, height = 2, command=moveUp)

#Button to move line down
moveDownButton = tk.Button(root, text = "DOWN", width = 30, height = 2, command=moveDown)

#Button to add new line 
addLineButton = tk.Button(root, text = "Add",width = 40, height = 2, command=addLine)

#Button to remove line 
remLineButton = tk.Button(root, text = "Delete", width = 40, height = 2,command=removeLine)

#Naming thing
nameTag = tk.Entry(root, width = 19, font = ("Arial", 20))

#Button to activate cut up function
cutUp = tk.Button(root, text = "Slice",width = 40, height = 2, command=checkToSendOff)   

#BIG TITLE
title = tk.Label(root, text = "PDF Editor", bg = "grey", font = ("Arial",35, "underline"))
    
lineSelect.place(x = 730, y = 102+ offset)
lineSelect.insert(0, str(selectedLine))
jumpDistEnter.place(x = 730, y=152+ offset)
jumpDistEnter.insert(0, str(jumpDist))
moveUpButton.place(x = 500, y = 100+ offset)
moveDownButton.place(x = 500, y = 150+ offset)
addLineButton.place(x = 500,y=330+ offset)
remLineButton.place(x = 500,y=380+ offset)
cutUp.place(x=500, y=600+ offset)
nameTag.place(x=500, y= 550 + offset)
nameTag.insert(0, "Enter name")
title.place(x = 500, y=10 + offset)

#draw the PDF
load_pdf()

#Scroll through the document
root.bind_all("<MouseWheel>", onMouseWheel)


root.mainloop()

