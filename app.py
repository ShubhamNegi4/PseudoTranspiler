import os
import subprocess
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import io
import sys
import warnings
import tkinter as tk

import lexer
import parser
import AstVisual
import semantic
import codegen

#       enable copy 
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
                ast_image = None
                if os.path.exists(img_path):
                        pil = Image.open(img_path).resize((400, 400), RESAMPLE)
                        ast_image = CTkImage(light_image=pil, dark_image=pil, size=(400, 400))

                # Semantic Analysis
                sem_ok = semantic.SemanticAnalysis(ast)

                if sem_ok == False:
                        OutputWindow(lexer.lexer,None,ast_text,ast_image)
                        return

                # Code Generation
                python_code = codegen.CodeGenerator(ast)

                # Open the output window
                OutputWindow(lexer.lexer,None, ast_text, ast_image, python_code,True)



def makeComponent(tabview, tab_name, content, is_list=True):
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

        # Ensure the tab expands properly
        tabview.tab(tab_name).grid_rowconfigure(0, weight=1)
        tabview.tab(tab_name).grid_columnconfigure(0, weight=1)

        return text_widget



class OutputWindow(ctk.CTkToplevel):
        def __init__(self, lexer,syntaxerrors=None, ast_text=None, ast_image=None, python_code=None,semok = False):
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
                self.tab_view.add("AST Image")
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


                # *************************** IMAGE COMPONENT ***********************
                # AST Image
                if ast_image:
                        self.image_label = ctk.CTkLabel(
                            self.tab_view.tab("AST Image"),
                            text="AST will appear here" if not ast_image else "",
                            image=ast_image,
                            font=("Courier", 14)
                        )
                        self.image_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
                        self.tab_view.tab("AST Image").grid_rowconfigure(0, weight=1)
                        self.tab_view.tab("AST Image").grid_columnconfigure(0, weight=1)


                # *************************** python COMPONENT ***********************

                # Python Code
                if python_code:
                    self.python_text = makeComponent(self.tab_view, "Python Code", python_code, is_list=False)


if __name__ == "__main__":
        app = InputWindow()
        app.mainloop()