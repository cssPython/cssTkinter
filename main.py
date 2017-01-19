tinycss=None
tkinter=None
root = None
rules = None
PIL=None
global cssTkinter
cssTkinter=None

def fail():
    raise RuntimeError()

def body():
    pass

html="""<html>
    <script>
    body {
        width: 75%;
        height: 50%;
        background-color: #FFFFFF;
        background-image: url('gradient_bg.png');
        background-repeat: repeat-x;
    }
    div {
        width: 100%;
        height: 10%;
    }
    </script>
    <body>
    Hello world!
    <div style="background-color: #0F0F0F;">First</div>
    <div>Second</div>
    <div>Third</div>
    </body>
    </html>"""
pyfile="""

    """

PRINT_IDS = True



def create_window():
    root=tkinter.Tk()
    root.geometry("1280x720+0+0")
    root.update()
    return root

def create_canvas(root):
    canvas=tkinter.Canvas(root, highlightthickness=0, borderwidth=0)
    canvas.place(x=0,y=0,width=1280,height=720)
    canvas.update()
    return canvas

def test_run():
    import cssTkinter.css_processor, cssTkinter.html_processor
    b=cssTkinter.html_processor.parse_html(html)
    css=cssTkinter.css_processor.parse_css(b.script.text)
    root=create_window()
    canvas=create_canvas(root)

    def assignables(element, assigna):
        if not hasattr(element, "children"):
            return
        for child in element.children:
            print(child.name)
            assigna.append(child)
            assignables(child, assigna)

    assigna=[]
    assigna.append(b.select("html")[0])
    assignables(b.select("html")[0], assigna)
    for element in assigna:
        element.id=canvas.create_rectangle(0,0,0,0,width=0, fill="pink")
        element.child_ids=[]

    if PRINT_IDS:
        def print_ids(element):
            print("{} {}".format(element.name, element.id))
            if hasattr(element, "children"):
                for child in element.children:
                    print_ids(child)
        print_ids(b.select("html")[0])




    def filecontentprovider():
        pass

    def get(path):
        import os
        return open(os.path.join("tests",path), 'rb')

    filecontentprovider.get=get

    def resize(e=None):
        coords=canvas.coords(b.body.id)
        x0,y0,x1,y1=int(coords[0]),int(coords[1]),int(coords[2]),int(coords[3])

        root.geometry("{}x{}".format(x1-x0, y1-y0))

    root.after(1, cssTkinter.css_processor.process(css, b, canvas, fileprovider=filecontentprovider, callback=resize))
    root.mainloop()


def parse_rule(rule, path, frame):
    elementname = rule.selector[0].value
    if not elementname:
        fail()
    print(rule.selector[0].type)
    if rule.selector[0].type != "IDENT":
        fail()

    print(elementname)
    if elementname == "body":
        import cssTkinter.css_parser
        cssTkinter.css_parser.parse_size(frame, rule.declarations)
        cssTkinter.css_parser.parse_background(frame, rule.declarations, path)
    else:
        fail()

def parse_file(parser, filename, path, frame):

    stylesheet = parser.parse_stylesheet_file(filename)
    print(stylesheet)
    #print(stylesheet.rules)
    global rules
    rules = stylesheet.rules
    for rule in stylesheet.rules:
        parse_rule(rule, path, frame)





def run_tests(delay=5000):
    import os
    parser = tinycss.make_parser('page3')
    root=tkinter.Tk()
    root.geometry("1280x720+0+0")
    frame=tkinter.Canvas(root, highlightthickness=0)
    root.after(1, lambda: parse_file(parser, os.path.join("tests","4_sizes_relative.css"),"tests", frame))
    root.mainloop()

def main():
    test_run()

def pip_install(package, user=True):
    try:
        import pip
        if user:
            pip.main(["install","--user",package])
        else:
            pip.main(["install",package])
    except:
        print("pip not installed!")
        exit(1)

def init():
    print("Starting... ")

    restart=False

    try:
        global tinycss
        import tinycss
    except:
        print("tinycss not installed. Trying to use pip")
        pip_install("tinycss")
        restart=True

    try:
        global PIL
        import PIL
    except:
        print("PIL not installed. Trying to use pip")
        pip_install("pillow")
        restart=True

    try:
        global bs4
        import bs4
    except:
        print("BeautifulSoup not installed")
        pip_install("bs4")
        restart=True

    if restart:
        print("Restart the program!")
        exit(0)

    try:
        global tkinter
        import tkinter
    except:
        print("tkinter not installed")
        exit(1)

    import cssTkinter

if __name__ == "__main__":
    init()

    main()
