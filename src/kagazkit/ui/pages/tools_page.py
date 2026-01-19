import tkinter.messagebox
from tkinter import filedialog

import customtkinter as ctk

from ...core.actions import PDFManager


class ToolsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.header = ctk.CTkLabel(self, text="PDF Tools", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(pady=10)
        
        # Split Section
        self.split_frame = ctk.CTkFrame(self)
        self.split_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(self.split_frame, text="Split PDF (Extract Pages)", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.split_btn = ctk.CTkButton(self.split_frame, text="Select PDF to Split", command=self.run_split)
        self.split_btn.pack(pady=10)
        
        # Rotate Section
        self.rotate_frame = ctk.CTkFrame(self)
        self.rotate_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(self.rotate_frame, text="Rotate PDF", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.rotation_var = ctk.IntVar(value=90)
        self.radio_90 = ctk.CTkRadioButton(self.rotate_frame, text="90° Clockwise", variable=self.rotation_var, value=90)
        self.radio_90.pack(pady=2)
        self.radio_180 = ctk.CTkRadioButton(self.rotate_frame, text="180°", variable=self.rotation_var, value=180)
        self.radio_180.pack(pady=2)
        self.radio_270 = ctk.CTkRadioButton(self.rotate_frame, text="270° Clockwise", variable=self.rotation_var, value=270)
        self.radio_270.pack(pady=2)
        
        self.rotate_btn = ctk.CTkButton(self.rotate_frame, text="Select PDF to Rotate", command=self.run_rotate)
        self.rotate_btn.pack(pady=10)

    def run_split(self):
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file:
            return
            
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
            
        try:
            files = PDFManager.split_pdf(file, output_dir)
            tkinter.messagebox.showinfo("Success", f"Split into {len(files)} pages successfully!")
        except Exception as e:
            tkinter.messagebox.showerror("Error", str(e))

    def run_rotate(self):
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file:
            return
            
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_file:
            return
            
        try:
            PDFManager.rotate_pdf(file, output_file, self.rotation_var.get())
            tkinter.messagebox.showinfo("Success", "PDF Rotated successfully!")
        except Exception as e:
            tkinter.messagebox.showerror("Error", str(e))
