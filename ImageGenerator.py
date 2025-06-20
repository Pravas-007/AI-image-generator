import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO


API_KEY = "Your API KEY here" 
# Replace with your Stability AI API key

API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

#Function to generate image
def generate_image():
    prompt = prompt_entry.get()
    if not prompt:
        messagebox.showwarning("Input Error", "Please enter a prompt!")
        return

    generate_button.config(state=tk.DISABLED)
    status_label.config(text="Generating image...")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "image/*"
    }

    files = {
        "prompt": (None, prompt),
        "model": (None, "stable-diffusion-xl"),
        "output_format": (None, "png")
    }

    response = requests.post(API_URL, headers=headers, files=files)

    if response.ok:
        img_data = BytesIO(response.content)
        global generated_image
        generated_image = Image.open(img_data)

        tk_img = ImageTk.PhotoImage(generated_image.resize((300, 300)))
        image_label.config(image=tk_img)
        image_label.image = tk_img

        status_label.config(text="✅ Image generated.")
        save_button.config(state=tk.NORMAL)
    else:
        status_label.config(text="❌ Failed to generate image.")
        messagebox.showerror("Error", f"{response.status_code}: {response.text}")

    generate_button.config(state=tk.NORMAL)

#Function to save image
def save_image():
    if generated_image:
        generated_image.save("generated_image.png")
        messagebox.showinfo("Saved", "✅ Image saved as 'generated_image.png'")

#GUI Setup
app = tk.Tk()
app.title("AI Image Generator")
app.geometry("400x500")

tk.Label(app, text="Enter a prompt:", font=("Arial", 12)).pack(pady=10)
prompt_entry = tk.Entry(app, width=40)
prompt_entry.pack(pady=5)

generate_button = tk.Button(app, text="Generate Image", command=generate_image)
generate_button.pack(pady=10)

image_label = tk.Label(app)
image_label.pack(pady=10)

save_button = tk.Button(app, text="Save Image", command=save_image, state=tk.DISABLED)
save_button.pack(pady=5)

status_label = tk.Label(app, text="", fg="blue")
status_label.pack(pady=10)

app.mainloop()

# Note: Make sure to handle your API key securely and not expose it in public repositories
