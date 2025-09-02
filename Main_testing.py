import tkinter as tk
from tkinter import filedialog
from tkinter import Label, Button, Text, END
import cv2
import numpy as np
from glob import glob
from PIL import Image, ImageTk
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# -------------------- Load Model --------------------
model = load_model("CNN2D.h5")

# -------------------- Classes --------------------
classes = [item[10:-1] for item in sorted(glob("./dataset/*/"))]

# -------------------- Helper --------------------
def path_to_tensor(img_path, width=224, height=224):
    img = image.load_img(img_path, target_size=(width, height))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0) / 255.0
    return x

# -------------------- GUI --------------------
class PredictionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Heart Disease Prediction")
        self.geometry("800x600")
        self.configure(bg="white")

        # Title label
        title = Label(self, text="Heart Disease Prediction", font=("Helvetica", 18, "bold"), bg="white")
        title.pack(pady=20)

        # Browse button
        browse_btn = Button(self, text="Select Image", command=self.browse_image, width=20, height=2, bg="lightblue")
        browse_btn.pack(pady=10)

        # Image placeholder
        self.image_label = Label(self, bg="white")
        self.image_label.pack(pady=10)

        # Prediction result
        self.result_text = Text(self, height=5, width=50, bg="lightyellow")
        self.result_text.pack(pady=20)

    def browse_image(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.jfif")]
        )
        if not filepath:
            return

        # Display selected image
        img = Image.open(filepath)
        img = img.resize((300, 300))
        render = ImageTk.PhotoImage(img)
        self.image_label.configure(image=render)
        self.image_label.image = render

        # Run prediction
        tensor = path_to_tensor(filepath)
        pred = model.predict(tensor)
        class_idx = np.argmax(pred)
        confidence = pred[0][class_idx]

        result = f"Predicted: {classes[class_idx]}\nConfidence: {confidence:.2f}"

        # Extra meaning (optional)
        if class_idx == 0:
            result += "\nHealthy person"
        elif class_idx == 1:
            result += "\nHeart failure"
        elif class_idx == 2:
            result += "\nAtrial fibrillation"
        elif class_idx == 3:
            result += "\nHeart attack"
        elif class_idx == 4:
            result += "\nCoronary artery disease"

        self.result_text.delete(1.0, END)
        self.result_text.insert(END, result)

# -------------------- Run App --------------------
if __name__ == "__main__":
    app = PredictionApp()
    app.mainloop()
