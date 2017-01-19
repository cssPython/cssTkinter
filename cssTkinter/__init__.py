
class Element(object):

    def __init__(self, canvas, bs_element=None, declarations=None, canvas_ids=[]):
        self.canvas=canvas
        self.canvas_ids=canvas_ids
        self.declarations = declarations
        self.bs_element = bs_element
        if self.bs_element:
            self.bs_element.cssTkinter_element = self

    def add_id(self, canvas_id):
        self.canvas_ids.append(canvas_id)

    def set_canvas(self, canvas):
        """Specifies the canvas the canvas_id belongs to.
        """
        self.canvas = canvas

    def set_rules(self, declarations):
        """Specifies the custom declarations for this element.
        """
        self.declarations = declarations

    def set_bs_element(self, bs_element):
        """Specifies the BeautifulSoup element associated with this Element.
        """
        if not bs_element and self.bs_element:
            del self.bs_element.cssTkinter_element
            return
        self.bs_element = bs_element
        if self.bs_element:
            self.bs_element.cssTkinter_element = self



def create_element(canvas, htmlelement, stylesheet):
    import cssTkinter.css_processor as CSS
    htmlstyle = ""
    if htmlelement.has_attr("style"):
        htmlstyle=htmlelement.attrs["style"]
    style = CSS.parse_style(htmlstyle)

    e = Element(canvas, htmlelement, style)

