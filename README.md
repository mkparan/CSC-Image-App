# CSC Image Processing Desktop App  

A cross-platform desktop application for advanced image processing, built with **FastAPI (Python)** as the backend and **Electron (JavaScript/HTML/CSS)** as the frontend.  

Users can:  
- Upload single or multiple images  
- Apply operations (grayscale, blur, sharpen, thresholding, morphology, edge detection, etc.)  
- Preview **Original** and **Processed** images side-by-side  
- Download results individually or as a ZIP (for batch)  

---

## 📂 Project Structure

```
csc-image-app/
├── backend/       # FastAPI + OpenCV backend
│   ├── main.py
│   ├── image_ops.py
│   ├── requirements.txt
│   └── start_server.py
├── frontend/      # Electron desktop app
│   ├── index.html
│   ├── styles.css
│   ├── main.js
│   ├── preload.js
│   ├── renderer.js
│   └── package.json
└── README.md
```

---

## ⚙️ Requirements

- [Python 3.11](https://www.python.org/downloads/release/python-3119/) (recommended, 64-bit)
- [Node.js 18+](https://nodejs.org/) (with npm)
- Git (to clone the repo)

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/csc-image-app.git
cd csc-image-app
```

---

### 2. Backend Setup (FastAPI)

1. Navigate to backend folder:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell)
   py -3.11 -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```
   - Server runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
   - API docs available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 3. Frontend Setup (Electron)

1. Open a new terminal and navigate to frontend:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Electron app:
   ```bash
   npm start
   ```

---

## 🖥️ Usage

- **Upload an image** (drag & drop or file chooser)  
- Select an **operation** from the dropdown  
- Adjust parameters (if available)  
- Click **Process Image** → preview updates  
- For multiple images, select several files and click **Batch (multi-file)** → ZIP download  
- **Original** and **Processed** previews are shown side by side, scaled to fit your screen  

---

## 🛠️ Development Notes

- CSP is configured to allow `blob:` URLs for previews  
- Previews are auto-scaled (`max-height: 70vh`) to fit most screens  
- To package the app into a distributable installer:  
  - Use [PyInstaller](https://pyinstaller.org/) to bundle the backend into an executable  
  - Configure `electron-builder` in `frontend/package.json` to include the backend  

---

## 📦 Packaging (optional)

To build a distributable Electron app:

```bash
cd frontend
npm run package
```

Configure targets (Windows, macOS, Linux) in `package.json` under `"build"`.

---

## 👥 Contributors

- **Paran** – System Analyst / Frontend  
- **Pepito** – Frontend  
- **Rocales** – Backend  

---

## 📝 License

MIT License – free to use, modify, and distribute.  
