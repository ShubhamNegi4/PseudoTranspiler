import os
import subprocess
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import io
import sys
import warnings
import tkinter as tk
from tkinter import ttk

import lexer
import parser
import AstVisual
import semantic
import codegen

# enable copy 
def enable_copy_shortcut(widget):
    widget.bind("<Control-c>", lambda event: widget.event_generate("<<Copy>>"))

# Suppress CtkLabel UserWarning about PhotoImage
warnings.filterwarnings(
        "ignore",
        message=".*Given image is not CTKImage.*",
        module="customtkinter"
)

# For Pillow >= 10 compatibility
try:
        RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
        RESAMPLE = Image.LANCZOS

# Set appearance to dark mode only
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class InputWindow(ctk.CTk):
        def __init__(self):
                super().__init__()
                self.title("Pseudocode Input")
                self.geometry("1000x1000")

                # Configure main window grid
                self.grid_columnconfigure(0, weight=1)
                self.grid_rowconfigure(1, weight=1)

                # Label
                ctk.CTkLabel(self, text="Enter Pseudocode:", font=("Helvetica", 14)).grid(
                        row=0, column=0, sticky="nw", padx=10, pady=(10, 0)
                )

                # Textbox for pseudocode input with padding
                input_wrapper = ctk.CTkFrame(self, fg_color="#E6E6FA", border_color="#FF6F61", border_width=1)
                input_wrapper.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
                input_wrapper.grid_rowconfigure(0, weight=1)
                input_wrapper.grid_columnconfigure(0, weight=1)

                self.input_text = tk.Text(
                        input_wrapper,
                        font=("Courier", 16),
                        bg="#E6E6FA",
                        fg="#1A1A2E",
                        insertbackground="#1A1A2E",
                        borderwidth=0,
                        highlightthickness=0,
                        wrap="word"
                )
                self.input_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
                enable_copy_shortcut(self.input_text)
                self.input_text.bind("<KeyRelease>", self.highlight_syntax)

                # Buttons
                button_frame = ctk.CTkFrame(self, fg_color="transparent")
                button_frame.grid(row=2, column=0, pady=10)
                ctk.CTkButton(
                        button_frame, text="Convert", command=self.convert,
                        fg_color="#1E90FF", hover_color="#00DDEB"
                ).grid(row=0, column=0, padx=10)
                ctk.CTkButton(
                        button_frame, text="Clear", command=self.clear_input,
                        fg_color="#E94560", hover_color="#FF6F61"
                ).grid(row=0, column=1, padx=10)

        def highlight_syntax(self, event=None):
                """Highlight pseudocode keywords in the input textbox."""
                self.input_text.tag_remove("keyword", "1.0", "end")
                content = self.input_text.get("1.0", "end-1c")
                keywords = ['INPUT', 'SET', 'TO', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'END', 'PRINT']

                self.input_text.tag_configure("keyword", foreground="#FF6F61")
                for keyword in keywords:
                        start = "1.0"
                        while True:
                                pos = self.input_text.search(keyword, start, stopindex="end")
                                if not pos:
                                        break
                                end_pos = f"{pos}+{len(keyword)}c"
                                self.input_text.tag_add("keyword", pos, end_pos)
                                start = end_pos

        def clear_input(self):
                """Clear the input textbox."""
                self.input_text.delete("1.0", "end")

        def convert(self):
                """Process the pseudocode and open the output window."""
                data = self.input_text.get("1.0", "end-1c")
                if not data.strip():
                        return  # Silently ignore empty input

                # Lex & Parse
                lexer.lexer.input(data)
                if lexer.lexer.errors > 0:
                        OutputWindow(lexer.lexer)
                        return  # Silently fail
                

                try:
                        ast = parser.parser.parse(data, lexer=lexer.lexer)
                        lexer.lexer.lineno = 1
                        lexer.lexer.input(data)
                except Exception:
                        OutputWindow(lexer.lexer,parser.parser.errorList)
                        return  # Silently fail

                # AST
                ast_text = AstVisual.visualizeText(ast)

                AstVisual.visualizeGraph(ast)
                img_path = 'astIMG.png'
                original_pil_image = None
                if os.path.exists(img_path):
                        original_pil_image = Image.open(img_path)
                        # Open separate window for AST image
                        ImageWindow(original_pil_image)

                # Semantic Analysis
                sem_ok = semantic.SemanticAnalysis(ast)

                if sem_ok == False:
                        OutputWindow(lexer.lexer,None,ast_text)
                        return

                # Code Generation
                python_code = codegen.CodeGenerator(ast)

                # Open the output window
                OutputWindow(lexer.lexer,None, ast_text, python_code,True)

def makeComponent(tabview, tab_name, content, is_list=True, is_python=False):
        frame = ctk.CTkFrame(tabview.tab(tab_name), fg_color="#E6E6FA")
        frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        text_widget = tk.Text(
            frame,
            font=("Courier", 14),
            bg="#E6E6FA",
            fg="#1A1A2E",
            borderwidth=0,
            highlightthickness=0,
            wrap="word"
        )
        enable_copy_shortcut(text_widget)
        text_widget.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        if content:
            if is_list:
                for item in content:
                    text_widget.insert("end", f"{item}\n\n")
            else:
                text_widget.insert("end", content)
                
            if is_python:
                # Configure tags for Python syntax highlighting
                text_widget.tag_configure("keyword", foreground="#FF6F61")
                text_widget.tag_configure("string", foreground="#00FF00")
                text_widget.tag_configure("comment", foreground="#808080")
                # Highlight Python code
                highlight_python_syntax(text_widget, content)

        # Ensure the tab expands properly
        tabview.tab(tab_name).grid_rowconfigure(0, weight=1)
        tabview.tab(tab_name).grid_columnconfigure(0, weight=1)

        return text_widget

def highlight_python_syntax(text_widget, content):
    """Highlight Python keywords, strings, and comments in the text widget."""
    text_widget.tag_remove("keyword", "1.0", "end")
    text_widget.tag_remove("string", "1.0", "end")
    text_widget.tag_remove("comment", "1.0", "end")

    # Python keywords
    keywords = [
        'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return', 
        'import', 'from', 'as', 'with', 'try', 'except', 'finally', 'raise',
        'break', 'continue', 'pass', 'in', 'is', 'and', 'or', 'not'
    ]

    # Highlight keywords
    for keyword in keywords:
        start = "1.0"
        while True:
            pos = text_widget.search(r'\y' + keyword + r'\y', start, stopindex="end", regexp=True)
            if not pos:
                break
            end_pos = f"{pos}+{len(keyword)}c"
            text_widget.tag_add("keyword", pos, end_pos)
            start = end_pos

    # Highlight strings (both single and double quotes)
    start = "1.0"
    while True:
        pos = text_widget.search(r'[\'"]', start, stopindex="end")
        if not pos:
            break
        quote_type = text_widget.get(pos)
        end_pos = text_widget.search(quote_type, f"{pos}+1c", stopindex="end")
        if not end_pos:
            end_pos = "end"
        else:
            end_pos = f"{end_pos}+1c"
        text_widget.tag_add("string", pos, end_pos)
        start = end_pos

    # Highlight comments
    start = "1.0"
    while True:
        pos = text_widget.search(r'#', start, stopindex="end")
        if not pos:
            break
        end_pos = text_widget.search(r'\n', pos, stopindex="end")
        if not end_pos:
            end_pos = "end"
        text_widget.tag_add("comment", pos, end_pos)
        start = end_pos

class ImageWindow(tk.Toplevel):
    def __init__(self, original_pil_image):
        super().__init__()
        self.title("AST Image")
        self.geometry("800x600")

        # Configure main window grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create canvas with scrollbars
        canvas_frame = tk.Frame(self)
        canvas_frame.grid(row=0, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, bg="#E6E6FA")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Add scrollbars
        h_scroll = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        v_scroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        h_scroll.grid(row=1, column=0, sticky="ew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        # Store original PIL image
        self.original_pil_image = original_pil_image
        self.zoom_level = 1.0

        # Initial image display
        self.update_image()

        # Bind zoom events
        self.canvas.bind("<MouseWheel>", self.zoom_image)  # Windows
        self.canvas.bind("<Button-4>", self.zoom_image)   # Linux scroll up
        self.canvas.bind("<Button-5>", self.zoom_image)   # Linux scroll down

        # Update scroll region
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def update_image(self):
        """Update the displayed image based on the current zoom level."""
        # Calculate new size based on zoom level
        original_size = self.original_pil_image.size
        new_size = (int(original_size[0] * self.zoom_level), int(original_size[1] * self.zoom_level))

        # Resize image
        resized_image = self.original_pil_image.resize(new_size, RESAMPLE)
        self.photo = ImageTk.PhotoImage(resized_image)

        # Update or create image on canvas
        if hasattr(self, 'image_id'):
            self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_image(self, event):
        """Handle image zooming with mouse wheel."""
        # Adjust zoom level
        if event.delta > 0 or event.num == 4:
            self.zoom_level *= 1.1  # Zoom in
        elif event.delta < 0 or event.num == 5:
            self.zoom_level /= 1.1  # Zoom out

        # Limit zoom level
        self.zoom_level = max(0.5, min(self.zoom_level, 3.0))

        # Update image
        self.update_image()

class OutputWindow(ctk.CTkToplevel):
        def __init__(self, lexer, syntaxerrors=None, ast_text=None, python_code=None, semok=False):
                super().__init__()
                self.title("Conversion Results")
                self.geometry("1000x1000")

                # Configure main window grid
                self.grid_columnconfigure(0, weight=1)
                self.grid_rowconfigure(0, weight=1)

                # Tab View
                self.tab_view = ctk.CTkTabview(self, fg_color="#1A1A2E")
                self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
                self.tab_view.add("Tokens")
                self.tab_view.add("Syntax Text ( IR )")
                self.tab_view.add("Python Code")

                # *************************** TOKEN COMPONENT ***********************
                # Populate Tokens
                tokens_list = [f"{tok}\n\n" for tok in lexer.errorList]
                for tok in lexer:
                    val = tok.value if tok.value != '\n' else 'newline'
                    tokens_list.append(
                        f"\n\t\t\t\ttype : {tok.type} \n\t\t\t\tvalue : {val} "
                        f"\n\t\t\t\tline number : {tok.lineno} \n\t\t\t\tPosition : {tok.lexpos}\n\n"
                    )
                self.tokens_text = makeComponent(self.tab_view, "Tokens", tokens_list)

                # *************************** AST COMPONENT ***********************
                # AST Text or Syntax Errors
                if ast_text is not None:
                        synlist = []
                        for i in ast_text:
                                synlist.append(f'\t{i}\n')
                        if semok:
                                synlist.append("\nSemantically correct\n")
                        else:
                                synlist.append("\nSemantically not correct\n")
                        self.ast_text = makeComponent(self.tab_view, "Syntax Text ( IR )", synlist)
                elif syntaxerrors is not None:
                        synlist = []
                        for i in syntaxerrors:
                                synlist.append(f'\t{i}\n')
                        if semok:
                                synlist.append("\nSemantically correct\n")
                        else:
                                synlist.append("\nSemantically not correct\n")
                        self.syntaxerrors = makeComponent(self.tab_view, "Syntax Text ( IR )", synlist)

                # *************************** PYTHON COMPONENT ***********************
                # Python Code
                if python_code:
                    self.python_text = makeComponent(self.tab_view, "Python Code", python_code, is_list=False, is_python=True)

if __name__ == "__main__":
        app = InputWindow()
        app.mainloop()