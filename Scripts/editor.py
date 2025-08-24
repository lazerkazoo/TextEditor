from ttkbootstrap import *
from ttkbootstrap.tooltip import ToolTip
import os, sys, asyncio
from tkinter.filedialog import askopenfilename, asksaveasfilename
import theme as tm

class TextEditor:
    def __init__(self):

        # Initial Setup
        self.auto_save_enabled = False
        self.save_path = None
        self.pad = 2
        pad = self.pad
        self.window = Window(themename=tm.theme, title='Text Editor', size=(1280, 720))

        # Text Area
        self.text_area = Text(self.window, font=('', 12))
        self.text_area.pack(side='right', fill='both', expand=True, padx=pad, pady=pad)

        # Sidebar Stuff
        self.sidebar = Frame(self.window)
        self.sidebar.pack(side='left', fill='y', padx=pad, pady=pad)

        save_btn = Button(self.sidebar, text='Save', command=self.save_file)
        save_btn.pack(padx=pad, pady=pad, fill='x')

        open_btn = Button(self.sidebar, text='Open', command=self.open_file)
        open_btn.pack(padx=pad, pady=pad, fill='x')

        exit_btn = Button(self.sidebar, text='Exit', command=self.exit, style='danger-outline')
        exit_btn.pack(padx=pad, pady=pad, fill='x', side='bottom')

        settings_btn = Button(self.sidebar, text='Settings', command=self.open_settings)
        settings_btn.pack(padx=pad, pady=pad, fill='x', side='bottom')

        # Tooltips
        ToolTip(save_btn, text='Save File (CTRL+S)', bootstyle='info', delay=500, position='bottom right')
        ToolTip(open_btn, text='Open File (CTRL+O)', bootstyle='info', delay=500, position='bottom right')
        ToolTip(exit_btn, text='Exit Application', bootstyle='danger', delay=500, position='top right')

        # Bindings
        self.window.bind('<Control-s>', lambda _: self.save_file())
        self.window.bind('<Control-o>', lambda _: self.open_file())

        self.window.mainloop()

    def save_file(self):
        if self.save_path is None:
            self.save_file_as()
            return

        with open(self.save_path, 'w') as file:
            content = self.text_area.get(1.0, 'end')
            file.write(content)

    def save_file_as(self):

        file_path = asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*'), ('Python Files', '*.py')])

        if not file_path:
            return

        with open(file_path, 'w') as file:
            content = self.text_area.get(1.0, 'end')
            file.write(content)
            self.window.title(f'Text Editor - {file_path}')
            self.save_path = file_path

    def open_file(self):

        file_path = askopenfilename(filetypes=[('Text Files', '*.txt'), ('All Files', '*.*'), ('Python Files', '*.py')])

        if not file_path:
            return

        with open(file_path, 'r') as file:
            content = file.read()
            self.text_area.delete(1.0, 'end')
            self.text_area.insert('end', content)
            self.window.title(f'Text Editor - {file_path}')
            self.save_path = file_path

    def exit(self):
        popup = Toplevel(title='Exit')
        popup.title('Exit')
        Label(popup, text='Are you sure you want to exit?').pack(side='top', expand=True, fill='x', padx=self.pad, pady=self.pad)
        Button(popup, text='Save File', command=lambda:[self.save_file(), self.window.destroy()]).pack(side='left', expand=True, fill='x', padx=self.pad, pady=self.pad)
        Button(popup, text='Yes', command=self.window.destroy).pack(side='left', expand=True, fill='x', padx=self.pad, pady=self.pad)
        Button(popup, text='Cancel', command=popup.destroy).pack(side='left', expand=True, fill='x', padx=self.pad, pady=self.pad)
        popup.mainloop()

    def open_settings(self):
        def change_theme():
            with open('theme.py', 'w') as f:
                code = f.write(f'theme = "{theme_var.get()}"')

            self.window.style.theme_use(theme_var.get())

        settings_popup = Toplevel(title='Settings', size=(300, 200))

        # Theme Stuff
        theme_frame = LabelFrame(settings_popup, text='Theme')
        themes = ['sandstone', 'flatly', 'darkly', 'cyborg', 'superhero', 'vapor', 'minty', 'pulse', 'solar', 'litera', 'lumen', 'yeti', 'journal', 'cosmo', 'cerulean']
        theme_var = StringVar(value=self.window.style.theme_use())
        theme_combo = Combobox(theme_frame, values=themes, textvariable=theme_var, state='readonly')

        apply_btn = Button(theme_frame, text='Apply Theme', command=change_theme)

        theme_combo.pack(padx=self.pad, pady=self.pad, fill='x')
        apply_btn.pack(padx=self.pad, pady=self.pad, fill='x')
        theme_frame.pack(padx=self.pad, pady=self.pad, fill='x')
