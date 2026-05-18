# 🏠 House Price Prediction System

A Machine Learning based web application that predicts house prices using user-provided property details.  
Built using **Python, Flask, Scikit-learn, HTML, CSS, and Bootstrap**.

---

## 🚀 Features

- Predict house prices instantly
- User-friendly web interface
- Machine Learning model trained using real housing data
- Responsive frontend design
- Flask backend integration
- Easy deployment using Vercel/Render

---

## 🛠️ Technologies Used

- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- HTML5
- CSS3
- Bootstrap
- Joblib / Pickle

---

## 📁 Project Structure

```bash
house-price-app/
│
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
│
├── model/
│   ├── house_price_model.pkl
│   └── model_columns.pkl
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── images/
│
├── dataset/
│   └── housing.csv
│
└── notebooks/
    └── model_training.ipynb
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/santhanuuuu/house-price-prediction.git
```

---

### 2️⃣ Navigate to Project Folder

```bash
cd house-price-prediction
```

---

### 3️⃣ Create Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate virtual environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python app.py
```

Open browser and visit:

```bash
http://127.0.0.1:5000
```

---

## 🧠 Machine Learning Model

The project uses:

- Gradient Boosting Regressor
- Scikit-learn Pipeline
- Feature preprocessing
- Model serialization using Pickle

---

## 📊 Input Features

Users can enter details like:

- Location
- Number of Bedrooms
- Bathrooms
- Square Feet Area
- Floors
- Age of House
- Parking Availability
- Furnishing Status

---

## 📈 Output

The system predicts:

✅ Estimated House Price

---

## 🌐 Deployment

You can deploy this project using:

- Vercel
- Render

---

## 📦 Requirements

Example dependencies:

```txt
Flask
numpy
pandas
scikit-learn
gunicorn
joblib
```

---

## 🖼️ Future Improvements

- Add charts and analytics
- Integrate map-based location selection
- Add price trend visualization
- Improve model accuracy
- Add user authentication

---

## 👨‍💻 Author

**Santhanu**

GitHub: https://github.com/santhanuuuu

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub.
