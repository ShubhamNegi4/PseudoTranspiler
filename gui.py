import os
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import io
import sys
import warnings
import lexer
import parser
import AstVisual
import semantic

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

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Pseudo2PythonGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pseudocode to Python Converter")
        self.geometry("1000x700")

        # Main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # Left panel: pseudocode input
        left = ctk.CTkFrame(self)
        left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(left, text="Pseudocode Input:").grid(row=0, column=0, sticky="nw", padx=5, pady=(5,0))
        self.input_text = ctk.CTkTextbox(left)
        self.input_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        ctk.CTkButton(left, text="Convert", command=self.process_input).grid(row=2, column=0, pady=10)

        # Right panel container with navigation
        container = ctk.CTkFrame(self)
        container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Console page
        self.console_page = ctk.CTkFrame(container)
        self.console_page.grid_rowconfigure(1, weight=1)
        self.console_page.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.console_page, text="Console Output:").grid(row=0, column=0, sticky="nw", padx=5, pady=(5,0))
        self.output_box = ctk.CTkTextbox(self.console_page)
        self.output_box.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # AST page
        self.ast_page = ctk.CTkFrame(container)
        self.ast_page.grid_rowconfigure(1, weight=1)
        self.ast_page.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.ast_page, text="AST Image:").grid(row=0, column=0, sticky="nw", padx=5, pady=(5,0))
        self.image_label = ctk.CTkLabel(self.ast_page, text="AST will appear here")
        self.image_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(self.ast_page, text="Semantic Analysis:").grid(row=2, column=0, sticky="nw", padx=5, pady=(10,0))
        self.semantic_label = ctk.CTkLabel(self.ast_page, text="Not run yet")
        self.semantic_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Navigation buttons
        nav_frame = ctk.CTkFrame(self)
        nav_frame.grid(row=1, column=1, pady=(0,10), sticky="e")
        self.back_btn = ctk.CTkButton(nav_frame, text="<<", width=50, command=self.show_console)
        self.back_btn.grid(row=0, column=0, padx=5)
        self.forward_btn = ctk.CTkButton(nav_frame, text=">>", width=50, command=self.show_ast)
        self.forward_btn.grid(row=0, column=1, padx=5)

        # Start on console page
        self.current = 'console'
        self.console_page.grid(row=0, column=0, sticky="nsew")
        self.ast_page.grid_forget()

    def show_console(self):
        if self.current != 'console':
            self.ast_page.grid_forget()
            self.console_page.grid(row=0, column=0, sticky="nsew")
            self.current = 'console'

    def show_ast(self):
        if self.current != 'ast':
            self.console_page.grid_forget()
            self.ast_page.grid(row=0, column=0, sticky="nsew")
            self.current = 'ast'

    def process_input(self):
        # Clear
        self.output_box.delete("0.0", "end")
        self.semantic_label.configure(text="")
        data = self.input_text.get("0.0", "end-1c")
        if not data.strip(): return

        # Lex & parse
        lexer.lexer.lineno = 1; lexer.lexer.errors = 0; lexer.lexer.input(data)
        toks = list(lexer.lexer)
        if lexer.lexer.errors:
            self.output_box.insert("end", "Lexing errors detected.\n"); return
        try:
            ast = parser.parser.parse(data, lexer=lexer.lexer)
        except Exception as e:
            self.output_box.insert("end", f"Parser Error: {e}\n"); return

        # Console content
        self.output_box.insert("end", "Tokens:\nType | Value | Line | Pos\n")
        for tok in toks:
            val = tok.value if tok.value!='\n' else 'newline'
            self.output_box.insert("end", f"{tok.type} | {val} | {tok.lineno} | {tok.lexpos}\n")
        buf=io.StringIO(); old=sys.stdout; sys.stdout=buf
        try: AstVisual.visualizeText(ast)
        finally: sys.stdout=old
        self.output_box.insert("end", "\nAST (Text):\n"+buf.getvalue())

        # AST page content
        AstVisual.visualizeGraph(ast)
        img='astIMG.png'
        if os.path.exists(img):
            pil=Image.open(img).resize((600,600),RESAMPLE)
            ctk_img=CTkImage(light_image=pil,size=(600,600))
            self.image_label.configure(image=ctk_img,text=""); self.image_label.image=ctk_img
        sem_ok=semantic.SemanticAnalysis(ast)
        self.semantic_label.configure(text=("Semantically correct" if sem_ok else "Semantically incorrect"))

if __name__ == "__main__":
    app = Pseudo2PythonGUI(); app.mainloop()