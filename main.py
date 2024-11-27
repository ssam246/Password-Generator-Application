import customtkinter as ctk
import string
import random
import pyperclip
import hashlib
from datetime import datetime
from pathlib import Path
import os


class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Generator")
        self.geometry("800x600")
        self.resizable(False, False)

        custom_font = ("mono", 18)

        # Seed Word Entry
        self.seed_label = ctk.CTkLabel(self, text="Seed Word:", font=custom_font)
        self.seed_label.pack(pady=10)
        self.seed_entry = ctk.CTkEntry(self, font=custom_font, placeholder_text="Enter an optional seed word")
        self.seed_entry.pack(pady=10)

        # Password Length Slider
        self.length_label = ctk.CTkLabel(self, text="Password Length:", font=custom_font)
        self.length_label.pack(pady=10)

        self.slider_frame = ctk.CTkFrame(self)
        self.slider_frame.pack(pady=10)

        self.length_slider = ctk.CTkSlider(self.slider_frame, from_=8, to=32, number_of_steps=24, command=self.update_slider_label)
        self.length_slider.grid(row=0, column=0, padx=5)
        self.length_slider.set(12)  # Set initial slider value

        self.slider_value_label = ctk.CTkLabel(self.slider_frame, text=f"{int(self.length_slider.get())}", font=custom_font)
        self.slider_value_label.grid(row=0, column=1, padx=5)

        # Checkboxes
        self.uppercase_var = ctk.BooleanVar(value=True)
        self.lowercase_var = ctk.BooleanVar(value=True)
        self.symbols_var = ctk.BooleanVar(value=True)
        self.numbers_var = ctk.BooleanVar(value=True)

        self.uppercase_check = ctk.CTkCheckBox(self, text="Include Uppercase Letters", variable=self.uppercase_var, font=custom_font)
        self.uppercase_check.pack(pady=5)
        self.lowercase_check = ctk.CTkCheckBox(self, text="Include Lowercase Letters", variable=self.lowercase_var, font=custom_font)
        self.lowercase_check.pack(pady=5)
        self.symbols_check = ctk.CTkCheckBox(self, text="Include Symbols (!@#$)", variable=self.symbols_var, font=custom_font)
        self.symbols_check.pack(pady=5)
        self.numbers_check = ctk.CTkCheckBox(self, text="Include Numbers (0-9)", variable=self.numbers_var, font=custom_font)
        self.numbers_check.pack(pady=5)

        # Generate Button
        self.generate_button = ctk.CTkButton(self, text="Generate Password", command=self.generate_password, font=custom_font)
        self.generate_button.pack(pady=20)

        # Live Preview Area
        self.password_label = ctk.CTkLabel(self, text="Generated Password:", font=custom_font)
        self.password_label.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, font=custom_font, state="readonly", width=400)
        self.password_entry.pack(pady=10)

        # Copy Button
        self.copy_button = ctk.CTkButton(self, text="Copy to Clipboard", command=self.copy_to_clipboard, font=custom_font)
        self.copy_button.pack(pady=5)

    def update_slider_label(self, value):
        """Update the label next to the slider to show the selected password length."""
        self.slider_value_label.configure(text=f"{int(value)}")

    def generate_password(self):
        """Generate a random password based on the selected options."""
        seed_word = self.seed_entry.get()
        length = int(self.length_slider.get())
        include_uppercase = self.uppercase_var.get()
        include_lowercase = self.lowercase_var.get()
        include_symbols = self.symbols_var.get()
        include_numbers = self.numbers_var.get()

        characters = ""
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_lowercase:
            characters += string.ascii_lowercase
        if include_symbols:
            characters += string.punctuation
        if include_numbers:
            characters += string.digits

        if not characters:
            # Default to a combination of all types if none are selected
            characters = string.ascii_letters + string.digits + string.punctuation

        # Combine the seed word with current time hash to create randomness
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        time_hash = hashlib.md5(current_time.encode()).hexdigest()
        combined_seed = seed_word + time_hash
        random.seed(combined_seed)

        password = "".join(random.choice(characters) for _ in range(length))

        # Display the password in the password entry
        self.password_entry.configure(state="normal")
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)
        self.password_entry.configure(state="readonly")

    def copy_to_clipboard(self):
        """Copy the generated password to the clipboard."""
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            self.show_message_box("Password copied to clipboard", "✅")

    def show_message_box(self, message, icon):
        """Show a message box with the provided message and icon."""
        message_box = ctk.CTkToplevel(self)
        message_box.title("Information")
        message_box.geometry("400x200")

        label = ctk.CTkLabel(message_box, text=f"{icon} {message}", font=("mono", 18))
        label.pack(pady=20)

        ok_button = ctk.CTkButton(message_box, text="OK", command=message_box.destroy, font=("mono", 16))
        ok_button.pack(pady=10)


if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()


