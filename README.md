# cssTkinter
CSS styling for Tkinter widgets.

Would it not be easier if you can style Tk windows in Python with CSS? This repo aims to achieve just that.


## Desired features
- Organizing Tk objects in a window with CSS styling definitions
- Providing Tk window definitions with a text file format such as HTML or XML definitions.

### Desired CSS support for:
- position
- width, height
- border
- font-size
- text-align
- padding
- margin
- background-color
- display

## Dependencies
- tinycss2: https://github.com/Kozea/tinycss2

## Example of desired usage
```python
import tinycss2

ss = tinycss2.parse_stylesheet("""

body {
  display: block;
  width: 100%;
  height: 100%;
  background-color: red;
}

import tkinter 

root = (...) # Creation of a tkinter window

style(root, ss) # Where the magic happens

""", skip_comments=False, skip_whitespace=False)
```
