import threading
import tkinter.messagebox
from tkinter import filedialog

import customtkinter as ctk
from tkinterdnd2 import DND_FILES

from ...core.actions import PDFManager
from ..components.file_list import FileList


class MergePage(ctk.CTkFrame):
    """
    Page for merging PDFs.
    """
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Header
        self.header = ctk.CTkLabel(self, text="Merge PDFs", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(pady=10)
        
        # Controls (Add Files, Clear)
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(fill="x", padx=10)
        
        self.add_btn = ctk.CTkButton(self.controls_frame, text="Add PDFs", command=self.add_files)
        self.add_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(self.controls_frame, text="Clear List", fg_color="gray", command=self.clear_list)
        self.clear_btn.pack(side="left", padx=5)
        
        # File List
        self.file_list = FileList(self, height=300)
        self.file_list.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Action Area
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=20, pady=20)

        self.progress_bar = ctk.CTkProgressBar(self.action_frame, mode="indeterminate")
        # Hidden by default, pack when needed
        
        self.merge_btn = ctk.CTkButton(self.action_frame, text="Merge Files Now", height=40, font=ctk.CTkFont(size=16), command=self.run_merge)
        self.merge_btn.pack(fill="x")

        # Drag and Drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        if event.data:
            try:
                files = self.tk.splitlist(event.data)
                for f in files:
                    if f.lower().endswith('.pdf'):
                        self.file_list.add_file(f)
            except Exception as e:
                print(f"Error handling drop: {e}")

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            for f in files:
                self.file_list.add_file(f)

    def clear_list(self):
        self.file_list.clear()

    def run_merge(self):
        paths = self.file_list.get_paths()
        if not paths:
            tkinter.messagebox.showwarning("Warning", "No files added to list!")
            return
            
        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Merged PDF"
        )
        
        if output_file:
            # Start background thread
            self.set_loading_state(True)
            threading.Thread(target=self._merge_thread, args=(paths, output_file), daemon=True).start()

    def _merge_thread(self, paths, output_file):
        try:
            PDFManager.merge_pdfs(paths, output_file)
            self.after(0, lambda: self._on_merge_complete(True, f"Merged {len(paths)} files successfully!"))
        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda: self._on_merge_complete(False, err_msg))

    def _on_merge_complete(self, success, message):
        self.set_loading_state(False)
        if success:
            tkinter.messagebox.showinfo("Success", message)
        else:
            tkinter.messagebox.showerror("Error", message)

    def set_loading_state(self, is_loading):
        if is_loading:
            self.merge_btn.configure(state="disabled", text="Merging...")
            self.progress_bar.pack(fill="x", pady=(0, 10))
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.merge_btn.configure(state="normal", text="Merge Files Now")
