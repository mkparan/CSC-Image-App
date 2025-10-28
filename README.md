# CSC Image Processing Desktop App  

A cross-platform desktop application for advanced image processing, built with **FastAPI (Python)** as the backend and **Electron (JavaScript/HTML/CSS)** as the frontend.  

Users can:  
- Upload images via drag & drop or file chooser  
- Apply operations (blur, sharpen, thresholding, morphology, etc.)  
- Preview **Original** and **Processed** images side-by-side  
- Download processed results  
- Switch between light/dark themes

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
│   ├── style.css
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
git clone https://github.com/mkparan/CSC-Image-App.git
cd csc-image-app
```

### 2. Backend Setup (FastAPI)

1. Navigate to backend folder:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (VS Code bash/git-bash)
   python -m venv venv
   source venv/Scripts/activate

   # Windows (PowerShell)
   py -3.11 -m venv venv
   .\venv\Scripts\activate

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
   # From backend folder
   uvicorn main:app --reload
   ```
   - Server runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
   - API docs available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

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

1. **Upload an Image**
   - Drag & drop into the upload area
   - Or click to choose file

2. **Process the Image**
   - Select an operation from the dropdown
   - Adjust parameters if available
   - Click "Process Image"
   - View original and processed previews side by side

3. **Theme Options**
   - Click the theme toggle button (top-right)
   - Switch between light and dark modes
   - Theme preference is saved automatically

---

## 🛠️ Development Notes

- CSP configured for `blob:` URLs and local development
- Responsive previews with auto-scaling
- Theme support using CSS variables
- Error handling for failed operations
- Real-time parameter adjustments

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