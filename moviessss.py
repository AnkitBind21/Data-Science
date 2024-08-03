import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
import pandas as pd

# Function to load the model and data from a .pkl or .csv file
def load_model():
    file_path = filedialog.askopenfilename(filetypes=[("Pickle or CSV files", "*.pkl *.csv")])
    if file_path:
        try:
            global model, data
            if file_path.endswith('.pkl'):
                with open(file_path, 'rb') as file:
                    content = pickle.load(file)
                    if isinstance(content, tuple) and len(content) == 2:
                        model, data = content
                        messagebox.showinfo("Success", "Model and data loaded successfully!")
                    else:
                        messagebox.showerror("Error", "Invalid .pkl file format.")
            elif file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
                model = None  # Set to None or load your model if it's separate
                messagebox.showinfo("Success", "Data loaded successfully from CSV file!")
            else:
                messagebox.showerror("Error", "Unsupported file type.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model and data: {str(e)}")

# Function to recommend movies based on user input
def recommend_movies():
    if data is None:
        messagebox.showwarning("Model/Data Not Loaded", "Please load data first.")
        return
    
    movie_name = entry.get()
    if not movie_name:
        messagebox.showwarning("Input Error", "Please enter a movie name!")
        return

    try:
        if model:
            recommended_movies = model.get_recommendations(movie_name, data)
        else:
            # Assuming the data is a DataFrame and has a 'title' column
            similar_movies = data[data['title'].str.contains(movie_name, case=False, na=False)]
            recommended_movies = similar_movies['title'].tolist() if not similar_movies.empty else ["No recommendations available."]
        
        result = "\n".join(recommended_movies)
        messagebox.showinfo("Recommended Movies", result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to recommend movies: {str(e)}")

# Set up the main GUI window
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("600x400")
root.configure(bg="#ECF0F1")  # Light grey background

# Create a border frame
border_frame = tk.Frame(root, bg="#BDC3C7", bd=10)
border_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Title Label
title_label = tk.Label(border_frame, text="MOVIE RECOMMENDATION SYSTEM", bg="#BDC3C7", fg="#2C3E50", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Main content frame
content_frame = tk.Frame(border_frame, bg="#ECF0F1")
content_frame.pack(padx=20, pady=20)

# Create widgets with enhanced styles
load_button = tk.Button(content_frame, text="Load Model & Data", command=load_model, bg="#3498DB", fg="white", font=("Arial", 14, "bold"), bd=0, padx=15, pady=10)
load_button.pack(pady=10)

label = tk.Label(content_frame, text="Enter a movie you like:", bg="#ECF0F1", fg="#2C3E50", font=("Arial", 14))
label.pack(pady=10)

entry = tk.Entry(content_frame, width=50, bd=2, relief="solid", font=("Arial", 12))
entry.pack(pady=10)

recommend_button = tk.Button(content_frame, text="Recommend Movies", command=recommend_movies, bg="#E67E22", fg="white", font=("Arial", 14, "bold"), bd=0, padx=15, pady=10)
recommend_button.pack(pady=10)

# Initialize global variables
model = None
data = None

# Run the GUI
root.mainloop()
