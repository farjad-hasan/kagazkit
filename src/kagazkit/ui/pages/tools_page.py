import tkinter.messagebox
from tkinter import filedialog

import customtkinter as ctk

from ...core.actions import PDFManager


class ToolsPage(ctk.CTkFrame):
    """
    Page for additional PDF tools (Split, Rotate).
    """
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Header
        self.header = ctk.CTkLabel(self, text="PDF Tools", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(pady=10)
        
        # Tools Container
        self.scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Split Tool
        self.create_tool_card(
            self.scrollable, 
            "Split PDF", 
            "Split a PDF into separate files (one per page).",
            self.run_split
        )
        
        # Rotate Tool
        self.create_tool_card(
            self.scrollable, 
            "Rotate PDF", 
            "Rotate all pages of a PDF (90, 180, 270 degrees).",
            self.run_rotate
        )

    def create_tool_card(self, master, title, description, command):
        card = ctk.CTkFrame(master)
        card.pack(fill="x", pady=5, padx=5)
        
        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        lbl_title.pack(anchor="w", padx=10, pady=(10, 0))
        
        lbl_desc = ctk.CTkLabel(card, text=description, font=ctk.CTkFont(size=12))
        lbl_desc.pack(anchor="w", padx=10, pady=(0, 10))
        
        btn = ctk.CTkButton(card, text="Open Tool", command=command)
        btn.pack(side="right", padx=10, pady=10)

    def run_split(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return
            
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
            
        try:
            results = PDFManager.split_pdf(file_path, output_dir)
            tkinter.messagebox.showinfo("Success", f"PDF split into {len(results)} files!")
        except Exception as e:
            tkinter.messagebox.showerror("Error", str(e))

    def run_rotate(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return
            
        # Rotation dialog
        dialog = ctk.CTkInputDialog(text="Enter rotation degrees (90, 180, 270):", title="Rotate PDF")
        res = dialog.get_input()
        
        if not res:
            return
            
        try:
            rotation = int(res)
            if rotation not in [90, 180, 270]:
                raise ValueError("Rotation must be 90, 180, or 270.")
        except ValueError as e:
            tkinter.messagebox.showerror("Error", str(e))
            return
            
        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Rotated PDF"
        )
        
        if output_file:
            try:
                PDFManager.rotate_pdf(file_path, output_file, rotation)
                tkinter.messagebox.showinfo("Success", "PDF rotated successfully!")
            except Exception as e:
                tkinter.messagebox.showerror("Error", str(e))
