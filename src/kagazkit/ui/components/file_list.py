import customtkinter as ctk


class FileList(ctk.CTkScrollableFrame):
    """
    Component for displaying and managing a list of files.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.files = []
        self.rows = []

    def add_file(self, file_path):
        if file_path not in self.files:
            self.files.append(file_path)
            self._draw_list()

    def remove_file(self, file_path):
        if file_path in self.files:
            self.files.remove(file_path)
            self._draw_list()

    def move_up(self, index):
        if index > 0:
            self.files[index], self.files[index-1] = self.files[index-1], self.files[index]
            self._draw_list()

    def move_down(self, index):
        if index < len(self.files) - 1:
            self.files[index], self.files[index+1] = self.files[index+1], self.files[index]
            self._draw_list()

    def clear(self):
        self.files = []
        self._draw_list()

    def get_paths(self):
        return self.files

    def _draw_list(self):
        # Clear existing rows
        for row in self.rows:
            row.destroy()
        self.rows = []

        for i, f in enumerate(self.files):
            row = ctk.CTkFrame(self)
            row.pack(fill="x", pady=2, padx=5)
            self.rows.append(row)

            # File Name
            lbl = ctk.CTkLabel(row, text=f, anchor="w")
            lbl.pack(side="left", fill="x", expand=True, padx=10)

            # Controls
            btn_up = ctk.CTkButton(row, text="▲", width=30, command=lambda idx=i: self.move_up(idx))
            btn_up.pack(side="left", padx=2)

            btn_down = ctk.CTkButton(row, text="▼", width=30, command=lambda idx=i: self.move_down(idx))
            btn_down.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(row, text="X", width=30, fg_color="red", hover_color="darkred", 
                                   command=lambda path=f: self.remove_file(path))
            btn_del.pack(side="left", padx=2)
