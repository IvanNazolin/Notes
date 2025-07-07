import tkinter as tk
from tkinter import simpledialog, messagebox
import requests

API_BASE = "http://127.0.0.1:8000"

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Заметки")

        self.notes_listbox = tk.Listbox(root, width=30)
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.notes_listbox.bind("<<ListboxSelect>>", self.on_note_select)

        self.text_area = tk.Text(root, wrap=tk.WORD)
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Новая заметка", command=self.new_note)
        file_menu.add_command(label="Сохранить", command=self.save_note)
        file_menu.add_command(label="Удалить", command=self.delete_note)
        self.menu.add_cascade(label="Файл", menu=file_menu)

        self.selected_note = None
        self.refresh_notes()

    def refresh_notes(self):
        try:
            response = requests.get(f"{API_BASE}/list")
            names = response.json()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить список заметок:\n{e}")
            names = []

        self.notes_listbox.delete(0, tk.END)
        for name in names:
            self.notes_listbox.insert(tk.END, name)

    def on_note_select(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            index = selection[0]
            name = self.notes_listbox.get(index)
            self.selected_note = name
            try:
                response = requests.get(f"{API_BASE}/get", params={"name": name})
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, response.text)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить заметку:\n{e}")

    def new_note(self):
        name = simpledialog.askstring("Новая заметка", "Введите название:")
        if name:
            try:
                requests.get(f"{API_BASE}/new", params={"name": name})
                self.refresh_notes()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать заметку:\n{e}")

    def save_note(self):
        if not self.selected_note:
            messagebox.showinfo("Нет заметки", "Выберите заметку для сохранения.")
            return
        text = self.text_area.get("1.0", tk.END)
        try:
            requests.get(f"{API_BASE}/save", params={"name": self.selected_note, "text": text})
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить заметку:\n{e}")

    def delete_note(self):
        if not self.selected_note:
            messagebox.showinfo("Нет заметки", "Выберите заметку для удаления.")
            return
        confirm = messagebox.askyesno("Удаление", f"Удалить заметку '{self.selected_note}'?")
        if confirm:
            try:
                requests.get(f"{API_BASE}/del", params={"name": self.selected_note})
                self.selected_note = None
                self.text_area.delete("1.0", tk.END)
                self.refresh_notes()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить заметку:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
