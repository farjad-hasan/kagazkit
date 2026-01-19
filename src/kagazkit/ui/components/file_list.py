import os
from typing import Callable, List

import customtkinter as ctk


class FileItem(ctk.CTkFrame):
    """
    Component representing a single file in the list.
    """
    def __init__(self, master, path: str, on_remove: Callable, on_move_up: Callable, on_move_down: Callable):
        super().__init__(master)
        self.path = path
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        
        # Filename Label
        filename = os.path.basename(path)
        self.label = ctk.CTkLabel(self, text=filename, anchor="w", font=("Arial", 12))
        self.label.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Buttons Frame
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=0, column=1, padx=5, pady=5)
        
        # Up Button
        self.up_btn = ctk.CTkButton(self.btn_frame, text="▲", width=30, height=20, command=lambda: on_move_up(self))
        self.up_btn.grid(row=0, column=0, padx=2)
        
        # Down Button
        self.down_btn = ctk.CTkButton(self.btn_frame, text="▼", width=30, height=20, command=lambda: on_move_down(self))
        self.down_btn.grid(row=0, column=1, padx=2)
        
        # Remove Button
        self.remove_btn = ctk.CTkButton(self.btn_frame, text="X", width=30, height=20, fg_color="#FF5555", hover_color="#CC4444", command=lambda: on_remove(self))
        self.remove_btn.grid(row=0, column=2, padx=2)

class FileList(ctk.CTkScrollableFrame):
    """
    Scrollable list to manage files.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.file_items: List[FileItem] = []
        
    def add_file(self, path: str):
        """Adds a file to the list."""
        # Avoid duplicates? Or allow? Usually merge allows same file twice.
        item = FileItem(self, path, self.remove_item, self.move_up, self.move_down)
        item.pack(fill="x", padx=5, pady=2)
        self.file_items.append(item)
        
    def remove_item(self, item: FileItem):
        """Removes a file item."""
        if item in self.file_items:
            item.destroy()
            self.file_items.remove(item)
            
    def move_up(self, item: FileItem):
        """Moves an item up in the list."""
        idx = self.file_items.index(item)
        if idx > 0:
            # Swap in data
            self.file_items[idx], self.file_items[idx-1] = self.file_items[idx-1], self.file_items[idx]
            # Repack all (simplest way for CTk containers that don't support easy reordering)
            self._repack_all()
            
    def move_down(self, item: FileItem):
        """Moves an item down in the list."""
        idx = self.file_items.index(item)
        if idx < len(self.file_items) - 1:
            self.file_items[idx], self.file_items[idx+1] = self.file_items[idx+1], self.file_items[idx]
            self._repack_all()
            
    def _repack_all(self):
        """Clears and repacks (reorders) the views."""
        for item in self.file_items:
            item.pack_forget()
        for item in self.file_items:
            item.pack(fill="x", padx=5, pady=2)
            
    def get_paths(self) -> List[str]:
        """Returns ordered list of file paths."""
        return [item.path for item in self.file_items]
        
    def clear(self):
        """Clears all items."""
        for item in self.file_items:
            item.destroy()
        self.file_items = []
