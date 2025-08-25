from ttkbootstrap import *
from ttkbootstrap.tooltip import ToolTip
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename
try:import settings.theme as tm
except ModuleNotFoundError:
    os.makedirs('settings', exist_ok=True)
    with open('settings/theme.py', 'w') as f:
        f.write('theme = "darkly"')
    import settings.theme as tm
try:import settings.last_doc as ld
except ModuleNotFoundError:
    os.makedirs('settings', exist_ok=True)
    with open('settings/last_doc.py', 'w') as f:
        f.write('last_doc = None\nremember = False')
    import settings.last_doc as ld

class TextEditor:
    def __init__(self):
        # Initial Setup
        self.save_path = None
        self.pad = 2
        pad = self.pad
        self.window = Window(themename=tm.theme, title='Text Editor', size=(1280, 720))

        # Text Area
        self.text_area = Text(self.window, font=('', 12))
        self.text_area.pack(side='right', fill='both', expand=True, padx=pad, pady=pad)
        self.text_area.focus_set()

        # Get Last Doc
        if ld.last_doc != None:
            with open(ld.last_doc, 'r') as f:
                self.text_area.insert(1.0, f.read() if ld.remember and ld.last_doc else '')
                self.save_path = ld.last_doc if ld.remember and ld.last_doc else None
                f.close()
            if self.save_path:
                self.window.title(f'Text Editor - {self.save_path}')

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
        ToolTip(settings_btn, text='Open Settings (CTRL+,)', bootstyle='info', delay=500, position='top right')
        ToolTip(exit_btn, text='Exit Application', bootstyle='danger', delay=500, position='top right')

        # Bindings
        self.window.bind('<Control-s>', lambda _: self.save_file())
        self.window.bind('<Control-o>', lambda _: self.open_file())
        self.window.bind('<Control-q>', lambda _: self.exit())
        self.window.bind('<Control-comma>', lambda _: self.open_settings())

        self.window.protocol("WM_DELETE_WINDOW", self.exit)

        self.window.mainloop()

    def save_file(self):
        def save_file_as():

            file_path = asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*'), ('Python Files', '*.py')])

            if not file_path:
                return

            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, 'end')
                file.write(content)
                self.window.title(f'Text Editor - {file_path}')
                self.save_path = file_path

        if self.save_path is None:
            save_file_as()
            return

        with open(self.save_path, 'w') as file:
            content = self.text_area.get(1.0, 'end')
            file.write(content)
        print(self.save_path)

    def open_file(self):
        file_path = askopenfilename(filetypes=[('Text Files', '*.txt'), ('All Files', '*.*'), ('Python Files', '*.py')])

        if not file_path:
            return

        with open(file_path, 'r') as file:
            content = file.read()
            self.text_area.delete(1.0, 'end')
            self.text_area.insert(1.0, content)
            self.window.title(f'Text Editor - {file_path}')
            self.save_path = file_path
        print(self.save_path)

    def exit(self):
        # Check if current content matches saved content
        current_content = self.text_area.get(1.0, 'end-1c')
        if self.save_path:
            try:
                with open(self.save_path, 'r') as file:
                    saved_content = file.read()
                if current_content == saved_content:
                    self.window.destroy()
                    return
            except:
                pass # If we can't read the file, continue with exit process

        if not current_content.strip(): # If the text area is empty (only whitespace), exit without confirmation
            self.window.destroy()
            return

        # Initialize Popup
        def save():
            self.save_file()
            exit_popup.destroy()
            self.window.destroy()

        def remember_last_doc():
            if self.remember_var == None:
                self.remember_var = BooleanVar(value=ld.remember)
            with open('settings/last_doc.py', 'w') as f:
                if self.remember_var.get():
                    f.write(f'last_doc = "{self.save_path}"\nremember = {self.remember_var.get()}')
                else:
                    f.write('last_doc = None\nremember = False')

        exit_popup = Toplevel(title='Exit')
        exit_popup.title('Exit')

        self.remember_var = BooleanVar(value=ld.remember)
        # Add Widgets
        Checkbutton(exit_popup, text='Remember Last Document', variable=self.remember_var, command=remember_last_doc).pack(padx=self.pad, pady=self.pad, fill='x', side='bottom')
        Label(exit_popup, text='Are you sure you want to exit?').pack(side='top', expand=True, fill='x', padx=self.pad, pady=self.pad)
        Button(exit_popup, text='Save 1st', command=lambda:[self.save_file(), self.window.destroy()]).pack(side='left', expand=True, fill='x', padx=self.pad, pady=self.pad)
        Button(exit_popup, text='Yes', command=self.window.destroy).pack(side='left', expand=True, fill='x', padx=self.pad, pady=self.pad)
        Button(exit_popup, text='Cancel', command=exit_popup.destroy).pack(side='left', expand=True, fill='x', padx=self.pad, pady=self.pad)


        # Finish Up
        exit_popup.protocol("WM_DELETE_WINDOW", save)
        exit_popup.mainloop()

    def open_settings(self):

        destroy_binds = ['<Escape>', '<Control-w>', '<Control-q>']

        def change_theme():
            with open('settings/theme.py', 'w') as f:
                f.write(f'theme = "{theme_var.get()}"')

            self.window.style.theme_use(theme_var.get())

        settings_popup = Toplevel(title='Settings', size=(300, 200))

        # Theme Stuff
        theme_frame = LabelFrame(settings_popup, text='Theme')
        themes = ['sandstone', 'flatly', 'darkly', 'cyborg', 'superhero', 'vapor', 'minty', 'pulse', 'solar']

        theme_var = StringVar(value=self.window.style.theme_use())
        theme_combo = Combobox(theme_frame, values=themes, textvariable=theme_var, state='readonly')

        apply_btn = Button(theme_frame, text='Apply Theme', command=change_theme)

        theme_combo.pack(padx=self.pad, pady=self.pad, fill='x')
        apply_btn.pack(padx=self.pad, pady=self.pad, fill='x')
        theme_frame.pack(padx=self.pad, pady=self.pad, fill='x')

        # Bindings
        for bind in destroy_binds:
            settings_popup.bind(bind, lambda _: settings_popup.destroy())

        settings_popup.focus_force()
        settings_popup.mainloop()
