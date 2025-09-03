from ttkbootstrap import *
from ttkbootstrap.tooltip import ToolTip
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename
try:import settings.theme as tm
except ModuleNotFoundError:
    os.makedirs('settings', exist_ok=True)
    with open('settings/theme.py', 'w') as f:
        f.write('theme = "sandstone"')
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
        self.finding = False
        self.save_path = None
        self.pad = 2
        self.search_matches = []
        self.current_match_index = -1
        self.last_search = ""
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

        find_btn = Button(self.sidebar, text='Find', command=self.find_text)
        find_btn.pack(padx=pad, pady=pad, fill='x')

        exit_btn = Button(self.sidebar, text='Exit', command=self.exit, style='danger-outline')
        exit_btn.pack(padx=pad, pady=pad, fill='x', side='bottom')

        settings_btn = Button(self.sidebar, text='Settings', command=self.open_settings)
        settings_btn.pack(padx=pad, pady=pad, fill='x', side='bottom')

        # Tooltips
        ToolTip(save_btn, text='Save File (CTRL+S)', bootstyle='info', delay=500, position='bottom right')
        ToolTip(open_btn, text='Open File (CTRL+O)', bootstyle='info', delay=500, position='bottom right')
        ToolTip(find_btn, text='Search in File (CTRL+F)', bootstyle='info', delay=500, position='bottom right')
        ToolTip(settings_btn, text='Open Settings (CTRL+,)', bootstyle='info', delay=500, position='top right')
        ToolTip(exit_btn, text='Exit Application', bootstyle='danger', delay=500, position='top right')

        # Bindings
        self.window.bind('<Control-s>', lambda _: self.save_file())
        self.window.bind('<Control-o>', lambda _: self.open_file())
        self.window.bind('<Control-q>', lambda _: self.exit())
        self.window.bind('<Control-comma>', lambda _: self.open_settings())

        self.window.bind('<Control-z>', lambda _: self.text_area.edit_undo())
        self.window.bind('<Control-y>', lambda _: self.text_area.edit_redo())
        self.window.bind('<Control-Shift-z>', lambda _: self.text_area.edit_redo())

        self.window.bind('<Control-f>', lambda _: self.find_text())

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

        self.destroy_binds = ['<Escape>', '<Control-w>', '<Control-q>']

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
        for bind in self.destroy_binds:
            settings_popup.bind(bind, lambda _: settings_popup.destroy())

        settings_popup.focus_force()
        settings_popup.mainloop()

    def find_text(self):
        def stop():
            self.window.unbind('<Escape>')
            self.finding = False
            self.clear_highlights()
            find_frame.pack_forget()
            self.text_area.focus_set()

        def perform_search():
            search_text = find_var.get()
            if not search_text:
                return

            self.clear_highlights()
            self.search_matches = []
            self.current_match_index = -1
            self.last_search = search_text

            # Get all text content
            content = self.text_area.get(1.0, 'end-1c')

            # Perform case-sensitive or case-insensitive search
            if case_var.get():
                search_content = content
                search_term = search_text
            else:
                search_content = content.lower()
                search_term = search_text.lower()

            # Find all matches
            start_pos = 0
            while True:
                pos = search_content.find(search_term, start_pos)
                if pos == -1:
                    break

                # Convert position to line.column format
                lines_before = content[:pos].count('\n')
                line_start = content.rfind('\n', 0, pos) + 1
                col = pos - line_start

                start_index = f"{lines_before + 1}.{col}"
                end_index = f"{lines_before + 1}.{col + len(search_text)}"

                self.search_matches.append((start_index, end_index))
                start_pos = pos + 1

            # Highlight all matches
            for start_idx, end_idx in self.search_matches:
                self.text_area.tag_add("search_match", start_idx, end_idx)
                self.text_area.tag_configure("search_match", background="yellow", foreground="black")

            # Update status
            if self.search_matches:
                status_label.config(text=f"Found {len(self.search_matches)} matches")
                next_match()
            else:
                status_label.config(text="No matches found")

        def next_match():
            if not self.search_matches:
                return

            # Clear current highlight
            self.text_area.tag_remove("current_match", 1.0, 'end')

            # Move to next match
            self.current_match_index = (self.current_match_index + 1) % len(self.search_matches)
            start_idx, end_idx = self.search_matches[self.current_match_index]

            # Highlight current match
            self.text_area.tag_add("current_match", start_idx, end_idx)
            self.text_area.tag_configure("current_match", background="orange", foreground="black")

            # Scroll to match
            self.text_area.see(start_idx)

            # Update status
            status_label.config(text=f"Match {self.current_match_index + 1} of {len(self.search_matches)}")

        def prev_match():
            if not self.search_matches:
                return

            # Clear current highlight
            self.text_area.tag_remove("current_match", 1.0, 'end')

            # Move to previous match
            self.current_match_index = (self.current_match_index - 1) % len(self.search_matches)
            start_idx, end_idx = self.search_matches[self.current_match_index]

            # Highlight current match
            self.text_area.tag_add("current_match", start_idx, end_idx)
            self.text_area.tag_configure("current_match", background="orange", foreground="black")

            # Scroll to match
            self.text_area.see(start_idx)

            # Update status
            status_label.config(text=f"Match {self.current_match_index + 1} of {len(self.search_matches)}")

        def replace_current():
            if self.current_match_index < 0 or self.current_match_index >= len(self.search_matches):
                return

            replace_text = replace_var.get()
            start_idx, end_idx = self.search_matches[self.current_match_index]

            # Replace the text
            self.text_area.delete(start_idx, end_idx)
            self.text_area.insert(start_idx, replace_text)

            # Refresh search to update positions
            perform_search()

        def replace_all():
            if not self.search_matches:
                return

            search_text = find_var.get()
            replace_text = replace_var.get()

            if not search_text:
                return

            # Get all content
            content = self.text_area.get(1.0, 'end-1c')

            # Perform replacement
            if case_var.get():
                new_content = content.replace(search_text, replace_text)
            else:
                # Case-insensitive replacement is more complex
                import re
                pattern = re.compile(re.escape(search_text), re.IGNORECASE)
                new_content = pattern.sub(replace_text, content)

            # Update text area
            self.text_area.delete(1.0, 'end')
            self.text_area.insert(1.0, new_content)

            # Clear search
            self.clear_highlights()
            self.search_matches = []
            self.current_match_index = -1

            status_label.config(text="Replaced all matches")

        # Search Stuff
        self.window.bind('<Escape>', lambda _: stop())

        if not self.finding:
            find_frame = LabelFrame(self.window, text='Find & Replace')

            # Search input
            find_var = StringVar()
            find_entry = Entry(find_frame, textvariable=find_var)
            find_entry.pack(padx=self.pad, pady=self.pad, fill='x')

            # Replace input
            replace_var = StringVar()
            replace_entry = Entry(find_frame, textvariable=replace_var)
            replace_entry.pack(padx=self.pad, pady=self.pad, fill='x')

            # Options
            options_frame = Frame(find_frame)
            case_var = BooleanVar(value=False)
            case_check = Checkbutton(options_frame, text='Case sensitive', variable=case_var)
            case_check.pack(side='left', padx=self.pad)
            options_frame.pack(fill='x', padx=self.pad)

            # Buttons frame
            btn_frame = Frame(find_frame)

            find_btn = Button(btn_frame, text='Find All', command=perform_search)
            find_btn.pack(side='left', padx=self.pad, pady=self.pad, fill='x', expand=True)

            prev_btn = Button(btn_frame, text='Previous', command=prev_match)
            prev_btn.pack(side='left', padx=self.pad, pady=self.pad, fill='x', expand=True)

            next_btn = Button(btn_frame, text='Next', command=next_match)
            next_btn.pack(side='left', padx=self.pad, pady=self.pad, fill='x', expand=True)

            btn_frame.pack(fill='x', padx=self.pad)

            # Replace buttons frame
            replace_btn_frame = Frame(find_frame)

            replace_btn = Button(replace_btn_frame, text='Replace', command=replace_current)
            replace_btn.pack(side='left', padx=self.pad, pady=self.pad, fill='x', expand=True)

            replace_all_btn = Button(replace_btn_frame, text='Replace All', command=replace_all)
            replace_all_btn.pack(side='left', padx=self.pad, pady=self.pad, fill='x', expand=True)

            replace_btn_frame.pack(fill='x', padx=self.pad)

            # Status label
            status_label = Label(find_frame, text="Enter search term")
            status_label.pack(padx=self.pad, pady=self.pad)

            find_frame.pack(padx=self.pad, pady=self.pad, fill='x')

            # Focus on find entry and bind Enter key
            find_entry.focus_set()
            find_entry.bind('<Return>', lambda _: perform_search())
            replace_entry.bind('<Return>', lambda _: perform_search())

            self.finding = True

    def clear_highlights(self):
        """Clear all search highlights from the text area"""
        self.text_area.tag_remove("search_match", 1.0, 'end')
        self.text_area.tag_remove("current_match", 1.0, 'end')

def main():
    editor = TextEditor()

main()
