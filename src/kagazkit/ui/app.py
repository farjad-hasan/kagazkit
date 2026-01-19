"""
Main application window module.
"""
import tkinter as tk
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
from .pages.merge_page import MergePage
from .pages.image_page import ImagePage
from .pages.tools_page import ToolsPage

# Set theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class PDFMasterApp(ctk.CTk, TkinterDnD.DnDWrapper):
    """
    Main application class for PDF Master.
    Inherits from CTk for modern UI and DnDWrapper for Drag and Drop support.
    """
    
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        self.title("KagazKit")
        self.geometry("900x600")
        
        # Configure grid layout (1x2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="KagazKit", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_merge = ctk.CTkButton(self.sidebar_frame, text="Merge PDFs", command=self.show_merge_page)
        self.sidebar_button_merge.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_convert = ctk.CTkButton(self.sidebar_frame, text="Image to PDF", command=self.show_image_page)
        self.sidebar_button_convert.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_button_tools = ctk.CTkButton(self.sidebar_frame, text="Tools", command=self.show_tools_page)
        self.sidebar_button_tools.grid(row=3, column=0, padx=20, pady=10)
        
        # Pages - Container
        self.pages_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.pages_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.pages_frame.grid_rowconfigure(0, weight=1)
        self.pages_frame.grid_columnconfigure(0, weight=1)
        
        self.merge_page = MergePage(self.pages_frame)
        self.image_page = ImagePage(self.pages_frame)
        self.tools_page = ToolsPage(self.pages_frame)
        
        # Show default page
        self.show_merge_page()

    def show_merge_page(self):
        self.select_frame(self.sidebar_button_merge)
        self.image_page.grid_forget()
        self.tools_page.grid_forget()
        self.merge_page.grid(row=0, column=0, sticky="nsew")

    def show_image_page(self):
        self.select_frame(self.sidebar_button_convert)
        self.merge_page.grid_forget()
        self.tools_page.grid_forget()
        self.image_page.grid(row=0, column=0, sticky="nsew")

    def show_tools_page(self):
        self.select_frame(self.sidebar_button_tools)
        self.merge_page.grid_forget()
        self.image_page.grid_forget()
        self.tools_page.grid(row=0, column=0, sticky="nsew")
        
    def select_frame(self, button):
        # Reset all buttons
        self.sidebar_button_merge.configure(fg_color=["#3B8ED0", "#1F6AA5"]) # Default blue
        self.sidebar_button_convert.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.sidebar_button_tools.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        # Highlight selected
        button.configure(fg_color=["#36719F", "#144870"])

if __name__ == "__main__":
    app = PDFMasterApp()
    app.mainloop()
