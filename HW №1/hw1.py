import argparse
import os
import tarfile
import tempfile
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog  # Импортируем filedialog

class ShellEmulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Shell Emulator")
        
        self.vfs_path = None
        self.current_dir = None
        
        self.output_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=20)
        self.output_area.pack(padx=10, pady=10)
        
        self.input_area = tk.Entry(master, width=50)
        self.input_area.pack(padx=10, pady=10)
        
        self.input_area.bind("<Return>", self.process_command)
        
        self.start_button = tk.Button(master, text="Start VFS", command=self.start_vfs)
        self.start_button.pack(pady=5)

    def start_vfs(self):
        self.vfs_path = filedialog.askopenfilename(title="Select VFS Archive", filetypes=[("Tar files", "*.tar")])
        if self.vfs_path:
            self.current_dir = self.extract_vfs(self.vfs_path)
            self.output_area.insert(tk.END, f"Welcome to the Shell Emulator! Current directory: {self.current_dir}\n")

    def extract_vfs(self, vfs_path):
        temp_dir = tempfile.mkdtemp()
        with tarfile.open(vfs_path, 'r') as tar:
            tar.extractall(temp_dir)
        return temp_dir

    def process_command(self, event):
        command = self.input_area.get()
        self.input_area.delete(0, tk.END)
        
        try:
            if command.startswith("ls"):
                output = self.ls(self.current_dir)
                self.display_output("\n".join(output))
            elif command.startswith("cd "):
                _, new_dir = command.split(maxsplit=1)
                self.current_dir = self.cd(self.current_dir, new_dir)
                self.display_output(f"Changed directory to: {self.current_dir}")
            elif command == "exit":
                self.exit_emulator()
            elif command == "whoami":
                output = self.whoami()
                self.display_output(output)
            elif command.startswith("mv "):
                _, source, destination = command.split(maxsplit=2)
                source_path = os.path.join(self.current_dir, source)
                destination_path = os.path.join(self.current_dir, destination)
                self.mv(source_path, destination_path)
                self.display_output(f"Moved {source} to {destination}")
            elif command.startswith("tree"):
                output = self.tree(self.current_dir)
                self.display_output(output)
            else:
                self.display_output(f"Command not found: {command}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_output(self, text):
        self.output_area.insert(tk.END, text + "\n")

    def ls(self, current_dir):
        return os.listdir(current_dir)

    def cd(self, current_dir, new_dir):
        new_path = os.path.join(current_dir, new_dir)
        if os.path.isdir(new_path):
            return new_path
        else:
            raise FileNotFoundError(f"{new_dir} not found")

    def exit_emulator(self):
        self.output_area.insert(tk.END, "Exiting emulator.\n")
        self.master.quit()

    def whoami(self):
        return os.getlogin()

    def mv(self, source, destination):
        os.rename(source, destination)

    def tree(self, directory):
        result = []
        for root, dirs, files in os.walk(directory):
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * (level)
            result.append(f"{indent}{os.path.basename(root)}/")
            for f in files:
                result.append(f"{indent}    {f}")
        return "\n".join(result)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShellEmulatorGUI(root)
    root.mainloop()
