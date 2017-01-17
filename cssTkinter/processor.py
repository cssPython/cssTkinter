import tinycss, tkinter

global parser
parser = tinycss.make_parser('page3')


def fail():
    raise RuntimeError()

def process(css, html, canvas, fileprovider=None, callback=None):

    def parse_text(rule, htmlobject, id):
        if htmlobject.text:
            coords=canvas.coords(id)
            x0,y0,x1,y1=int(coords[0]),int(coords[1]),int(coords[2]),int(coords[3])
            text=canvas.create_text(x0, y0, anchor=tkinter.W,text=htmlobject.text)
            htmlobject.child_ids.append(text)

    def parse_size(rule, htmlobject, id):
        width=0
        height=0
        x=0
        y=0
        relwidth=False
        relheight=False
        relx=False
        rely=False
        for declaration in rule.declarations:
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

        print("parent:")
        print("Setting size: {} {}".format(width, height))


        if relx:
            x0=x*canvas.winfo_width()
        else:
            x0=x
        if rely:
            y0=y*canvas.winfo_height()
        else:
            y0=y
        if relwidth:
            x1=x+(width*canvas.winfo_width())
        else:
            x1=x+width
        if relheight:
            y1=y+(height*canvas.winfo_height())
        else:
            y1=y+height
        print("Setting coords: {} {} {} {}".format(x0, y0, x1, y1))
        canvas.coords(id, x0, y0, x1, y1)
#         if relx:
#             canvas.coords(id, x0=x*canvas.winfo_width())
#         else:
#             canvas.coords(id, x0=x)
#         if rely:
#             canvas.coords(id, y0=y*canvas.winfo_height())
#         else:
#             canvas.coords(id, y0=y)
#         if relwidth:
#             canvas.coords(id, x1=x+(width*canvas.winfo_width()))
#         else:
#             canvas.coords(id, x1=x+width)
#         if relheight:
#             canvas.coords(id, y1=y+(height*canvas.winfo_height()))
#         else:
#             canvas.coords(id, y1=y+height)

    def parse_background(rule, htmlobject, id):
        color="#FFFFFF"
        background_image=None
        repeatx=False
        repeaty=False
        for declaration in rule.declarations:
            if declaration.name=="background-color":
                if declaration.value[0].type=="HASH":
                    color=declaration.value[0].value
                else:
                    fail()
            elif declaration.name=="background-image":
                from PIL import ImageTk
                from PIL import Image
                if declaration.value[0].type=="URI":
                    im=Image.open(fileprovider.get(declaration.value[0].value) if fileprovider else None)
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

        if not repeatx and not repeaty:
            repeatx=True
            repeaty=True

        canvas.itemconfigure(id, fill=color)
        if background_image:
            coords = canvas.coords(id)
            x0, y0, x1, y1 = int(coords[0]),int(coords[1]),int(coords[2]),int(coords[3])
            width=int(x1-x0)
            height=int(y1-y0)
            #width=canvas.itemcget(id, "width")
            #height=canvas.itemcget(id, "height")
            if repeatx:
                for x in range(int(x0), int(x1), background_image.width()):
                    if repeaty:
                        for y in range(int(y0), int(y1), background_image.height()):
                            background_image_label = canvas.create_image(x, y, image=background_image,anchor=tkinter.NW)
                            #canvas.itemconfigure(background_image_label, x=x, y=y)
                            #background_image_label.image = background_image
                            htmlobject.child_ids.append((background_image_label,background_image))
                    else:
                        background_image_label = canvas.create_image(x,y0, image=background_image,anchor=tkinter.NW)
                        #canvas.itemconfigure(background_image_label, x=x, y=0)
                        #background_image_label.image = background_image
                        htmlobject.child_ids.append((background_image_label,background_image))
            else:
                if repeaty:
                    for y in range(int(y0), int(y1), background_image.height()):
                        background_image_label = canvas.create_image(x0,y,image=background_image,anchor=tkinter.NW)
                        #canvas.itemconfigure(background_image_label, x=0, y=y)
                        #background_image_label.image = background_image
                        htmlobject.child_ids.append((background_image_label,background_image))
                else:
                    background_image_label = canvas.create_image(x0,y0,image=background_image,anchor=tkinter.NW)
                    #canvas.itemconfigure(background_image_label, x=0, y=0)
                    #background_image_label.image = background_image
                    htmlobject.child_ids.append((background_image_label,background_image))
            print("Set images: {} {} {} {}".format(x0,y0,width,height))


    def process_rule(rule):
        selector = rule.selector[0].value
        htmlobjects = html.select(selector)
        for htmlobject in htmlobjects:
            parse_size(rule, htmlobject, htmlobject.id)
            parse_background(rule, htmlobject, htmlobject.id)


    canvas.update()
    stylesheet = parser.parse_stylesheet(css)
    if len(stylesheet.errors) > 0:
        fail()
    for rule in stylesheet.rules:
        process_rule(rule)
    if callback:
        callback()



