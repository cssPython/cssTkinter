tinycss=None
tkinter=None
root = None
rules = None
PIL=None
global cssTkinter
cssTkinter=None

def fail():
    raise RuntimeError()



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
    frame=tkinter.Frame(root)
    root.after(1, lambda: parse_file(parser, "tests\\4_sizes_relative.css","tests", frame))
    root.mainloop()

def main():
    run_tests()

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

    try:
        global tinycss
        import tinycss
    except:
        print("tinycss not installed. Trying to use pip")
        pip_install("tinycss")
        print("restart this program.")
        exit(0)

    try:
        global PIL
        import PIL
    except:
        print("PIL not installed. Trying to use pip")
        pip_install("pillow")
        print("restart!")
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
