import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography Tool")
        self.root.geometry("800x600")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(self.main_frame, text="Image Steganography Tool", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Mode selection
        self.mode_var = tk.StringVar(value="encode")
        ttk.Radiobutton(self.main_frame, text="Encode", variable=self.mode_var, 
                       value="encode", command=self.toggle_mode).pack(pady=5)
        ttk.Radiobutton(self.main_frame, text="Decode", variable=self.mode_var, 
                       value="decode", command=self.toggle_mode).pack(pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Encode Tab
        self.encode_frame = ttk.Frame(self.notebook)
        self.decode_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.encode_frame, text="Encode")
        self.notebook.add(self.decode_frame, text="Decode")
        
        # Initialize both tabs
        self.setup_encode_tab()
        self.setup_decode_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                                  relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10,0))
        
        self.update_status("Ready")
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def toggle_mode(self):
        if self.mode_var.get() == "encode":
            self.notebook.select(self.encode_frame)
        else:
            self.notebook.select(self.decode_frame)
    
    def setup_encode_tab(self):
        # Cover Image Selection
        ttk.Label(self.encode_frame, text="Cover Image:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cover_path = tk.StringVar()
        ttk.Entry(self.encode_frame, textvariable=self.cover_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.encode_frame, text="Browse", command=self.browse_cover).grid(row=0, column=2, padx=5, pady=5)
        
        # Secret Image Selection
        ttk.Label(self.encode_frame, text="Secret Image/Message:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.secret_path = tk.StringVar()
        ttk.Entry(self.encode_frame, textvariable=self.secret_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.encode_frame, text="Browse", command=self.browse_secret).grid(row=1, column=2, padx=5, pady=5)
        
        # Output Options
        ttk.Label(self.encode_frame, text="Output File:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.output_path = tk.StringVar()
        ttk.Entry(self.encode_frame, textvariable=self.output_path, width=50).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.encode_frame, text="Save As", command=self.browse_output).grid(row=2, column=2, padx=5, pady=5)
        
        # Encode Button
        ttk.Button(self.encode_frame, text="Encode Image", command=self.encode_image).grid(row=3, column=1, pady=10)
        
        # Preview Area
        self.cover_preview = ttk.Label(self.encode_frame)
        self.cover_preview.grid(row=4, column=0, padx=10, pady=10)
        
        self.secret_preview = ttk.Label(self.encode_frame)
        self.secret_preview.grid(row=4, column=1, padx=10, pady=10)
        
        self.output_preview = ttk.Label(self.encode_frame)
        self.output_preview.grid(row=4, column=2, padx=10, pady=10)
    
    def setup_decode_tab(self):
        # Encoded Image Selection
        ttk.Label(self.decode_frame, text="Encoded Image:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.encoded_path = tk.StringVar()
        ttk.Entry(self.decode_frame, textvariable=self.encoded_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.decode_frame, text="Browse", command=self.browse_encoded).grid(row=0, column=2, padx=5, pady=5)
        
        # Output Options
        ttk.Label(self.decode_frame, text="Extracted Output:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.extracted_path = tk.StringVar()
        ttk.Entry(self.decode_frame, textvariable=self.extracted_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.decode_frame, text="Save As", command=self.browse_extracted).grid(row=1, column=2, padx=5, pady=5)
        
        # Decode Button
        ttk.Button(self.decode_frame, text="Decode Image", command=self.decode_image).grid(row=2, column=1, pady=10)
        
        # Preview Area
        self.encoded_preview = ttk.Label(self.decode_frame)
        self.encoded_preview.grid(row=3, column=0, padx=10, pady=10)
        
        self.extracted_preview = ttk.Label(self.decode_frame)
        self.extracted_preview.grid(row=3, column=1, padx=10, pady=10)
    
    # File browsing methods
    def browse_cover(self):
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filename:
            self.cover_path.set(filename)
            self.show_image_preview(filename, self.cover_preview)
    
    def browse_secret(self):
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filename:
            self.secret_path.set(filename)
            self.show_image_preview(filename, self.secret_preview)
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png", 
                                               filetypes=[("PNG Files", "*.png")])
        if filename:
            self.output_path.set(filename)
    
    def browse_encoded(self):
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        if filename:
            self.encoded_path.set(filename)
            self.show_image_preview(filename, self.encoded_preview)
    
    def browse_extracted(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png", 
                                              filetypes=[("PNG Files", "*.png")])
        if filename:
            self.extracted_path.set(filename)
    
    def show_image_preview(self, image_path, label_widget, size=(200, 200)):
        try:
            img = Image.open(image_path)
            img.thumbnail(size)
            photo = ImageTk.PhotoImage(img)
            label_widget.config(image=photo)
            label_widget.image = photo  # Keep a reference
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    # Core steganography functions
    def encode_image(self):
        if not self.cover_path.get() or not self.secret_path.get():
            messagebox.showerror("Error", "Please select both cover and secret images!")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please specify an output file!")
            return
        
        try:
            self.update_status("Encoding...")
            
            # Load images
            cover_img = Image.open(self.cover_path.get()).convert('RGB')
            secret_img = Image.open(self.secret_path.get()).convert('RGB')
            
            # Resize secret to match cover
            secret_img = secret_img.resize(cover_img.size, Image.Resampling.LANCZOS)
            
            # Convert to numpy arrays
            cover_arr = np.array(cover_img)
            secret_arr = np.array(secret_img)
            
            # Hide secret in LSB of cover
            encoded_arr = (cover_arr & 0xFE) | (secret_arr >> 7)
            
            # Save encoded image
            encoded_img = Image.fromarray(encoded_arr.astype(np.uint8))
            encoded_img.save(self.output_path.get())
            
            self.show_image_preview(self.output_path.get(), self.output_preview)
            self.update_status("Encoding complete!")
            messagebox.showinfo("Success", "Image encoded successfully!")
            
        except Exception as e:
            self.update_status("Error during encoding")
            messagebox.showerror("Error", f"Encoding failed: {str(e)}")
    
    def decode_image(self):
        if not self.encoded_path.get():
            messagebox.showerror("Error", "Please select an encoded image!")
            return
        
        if not self.extracted_path.get():
            messagebox.showerror("Error", "Please specify an output file for extraction!")
            return
        
        try:
            self.update_status("Decoding...")
            
            # Load encoded image
            encoded_img = Image.open(self.encoded_path.get()).convert('RGB')
            encoded_arr = np.array(encoded_img)
            
            # Extract secret from LSB
            extracted_arr = (encoded_arr & 0x01) * 255
            
            # Save extracted image
            extracted_img = Image.fromarray(extracted_arr.astype(np.uint8))
            extracted_img.save(self.extracted_path.get())
            
            self.show_image_preview(self.extracted_path.get(), self.extracted_preview)
            self.update_status("Decoding complete!")
            messagebox.showinfo("Success", "Secret image extracted successfully!")
            
        except Exception as e:
            self.update_status("Error during decoding")
            messagebox.showerror("Error", f"Decoding failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
