import customtkinter as ctk

from .pages.image_page import ImagePage
from .pages.merge_page import MergePage
from .pages.tools_page import ToolsPage


class PDFMasterApp(ctk.CTk):
    """
    Main Application class for KagazKit.
    """
    def __init__(self):
        super().__init__()

        self.title("KagazKit")
        self.geometry("1100x700")

        # Set appearance mode
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Grid Layout (1x2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="KagazKit", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.merge_btn = ctk.CTkButton(self.sidebar_frame, text="Merge PDFs", command=lambda: self.show_page("merge"))
        self.merge_btn.grid(row=1, column=0, padx=20, pady=10)

        self.image_btn = ctk.CTkButton(self.sidebar_frame, text="Images to PDF", command=lambda: self.show_page("image"))
        self.image_btn.grid(row=2, column=0, padx=20, pady=10)

        self.tools_btn = ctk.CTkButton(self.sidebar_frame, text="PDF Tools", command=lambda: self.show_page("tools"))
        self.tools_btn.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("Dark")

        # Main Page Container
        self.pages = {}
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Initialize Pages
        for PageClass, name in [(MergePage, "merge"), (ImagePage, "image"), (ToolsPage, "tools")]:
            page = PageClass(self.container)
            self.pages[name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("merge")

    def show_page(self, name):
        page = self.pages.get(name)
        if page:
            page.tkraise()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
