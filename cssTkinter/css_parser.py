import tinycss
import tkinter

def fail():
    raise RuntimeError()

def parse_background(frame, declarations, path):
    color="#FFFFFF"
    background_image=None
    repeatx=True
    repeaty=True
    for declaration in declarations:
        if declaration.name=="background-color":
            if declaration.value[0].type=="HASH":
                color=declaration.value[0].value
            else:
                fail()
        elif declaration.name=="background-image":
            from PIL import ImageTk
            from PIL import Image
            if declaration.value[0].type=="URI":
                import os
                im=Image.open(os.path.join(path, declaration.value[0].value))
                background_image = ImageTk.PhotoImage(im)
            else:
                fail()
        elif declaration.name=="background-repeat":
            if declaration.value[0].type=="IDENT":
                if declaration.value[0].value=="repeat-x":
                    repeatx=True
                    #repeaty=False if not repeaty else True
                elif declaration.value[0].value=="repeat-y":
                    repeaty=True
                    #repeatx=False if not repeatx else True
                else:
                    fail()
            else:
                fail()


    frame.configure(background=color)
    if background_image:
        frame.update()
        width=frame.winfo_width()
        height=frame.winfo_height()
        frame.background_image_labels=[]
        if repeatx:
            for x in range(0, width, background_image.width()):
                if repeaty:
                    for y in range(0, height, background_image.height()):
                        background_image_label = tkinter.Label(frame, borderwidth=0, highlightthickness=0, image=background_image)
                        background_image_label.place(x=x, y=y)
                        background_image_label.image = background_image
                        frame.background_image_labels.append(background_image_label)
                else:
                    background_image_label = tkinter.Label(frame, borderwidth=0, highlightthickness=0, image=background_image)
                    background_image_label.place(x=x, y=0)
                    background_image_label.image = background_image
                    frame.background_image_labels.append(background_image_label)
        else:
            if repeaty:
                for y in range(0, height, background_image.height()):
                    background_image_label = tkinter.Label(frame, borderwidth=0, highlightthickness=0, image=background_image)
                    background_image_label.place(x=0, y=y)
                    background_image_label.image = background_image
                    frame.background_image_labels.append(background_image_label)
            else:
                background_image_label = tkinter.Label(frame, borderwidth=0, highlightthickness=0, image=background_image)
                background_image_label.place(x=0, y=0)
                background_image_label.image = background_image
                frame.background_image_labels.append(background_image_label)

def parse_size(frame, declarations):
    width=0
    height=0
    x=0
    y=0
    relwidth=False
    relheight=False
    relx=False
    rely=False
    for declaration in declarations:
        if declaration.name == "width":
            print(declaration.value[0])
            if declaration.value[0].type=="DIMENSION":
                width=declaration.value[0].value
            elif declaration.value[0].type=="PERCENTAGE":
                relwidth=True
                width=declaration.value[0].value/100
            else:
                fail()
        elif declaration.name == "height":
            if declaration.value[0].type=="DIMENSION":
                height=declaration.value[0].value
            elif declaration.value[0].type=="PERCENTAGE":
                relheight=True
                height=declaration.value[0].value/100
            else:
                fail()

    print("Setting size: {} {}".format(width, height))

    if relx:
        frame.place(relx=x)
    else:
        frame.place(x=x)
    if rely:
        frame.place(rely=y)
    else:
        frame.place(y=y)
    if relwidth:
        frame.place(relwidth=width)
    else:
        frame.place(width=width)
    if relheight:
        frame.place(relheight=height)
    else:
        frame.place(height=height)