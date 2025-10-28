const backend = "http://127.0.0.1:8000";

// Updated element references to match new HTML
const fileEl = document.getElementById("file");
const dropArea = document.getElementById("drop-area");
const originalPreview = document.getElementById("originalPreview");
const processedPreview = document.getElementById("processedPreview");
const operationSelect = document.getElementById("operationSelect");
const parameters = document.getElementById("parameters");
const processBtn = document.getElementById("processBtn");
const downloadBtn = document.getElementById("downloadBtn"); // Download button
const themeToggle = document.getElementById("themeToggle");

let currentFile = null;
let multipleFiles = null;
let processedUrl = null; // Store processed image URL

// Define operation parameters
const operationParams = {
    'blur': [{ name: 'kernel_size', type: 'range', default: 5, min: 1, max: 99, step: 2 }],
    'gaussian_blur': [{ name: 'kernel_size', type: 'range', default: 5, min: 1, max: 99, step: 2 }],
    'median_blur': [{ name: 'kernel_size', type: 'range', default: 5, min: 1, max: 99, step: 2 }],
    'threshold': [{ name: 'threshold_value', type: 'range', default: 127, min: 0, max: 255, step: 1 }],
    'sharpen': [{ name: 'amount', type: 'range', default: 1, min: 0, max: 5, step: 0.1 }],
    'dilation': [{ name: 'kernel_size', type: 'range', default: 3, min: 1, max: 21, step: 2 }],
    'erosion': [{ name: 'kernel_size', type: 'range', default: 3, min: 1, max: 21, step: 2 }],
    'opening': [{ name: 'kernel_size', type: 'range', default: 3, min: 1, max: 21, step: 2 }],
    'closing': [{ name: 'kernel_size', type: 'range', default: 3, min: 1, max: 21, step: 2 }]
};

// File handling
fileEl.addEventListener("change", e => {
    currentFile = e.target.files[0];
    multipleFiles = e.target.files.length > 1 ? Array.from(e.target.files) : null;
    showOriginal(currentFile);
});

// Drag and drop handlers
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("drag-over");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("drag-over");
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("drag-over");
    const f = e.dataTransfer.files[0];
    fileEl.files = e.dataTransfer.files;
    currentFile = f;
    multipleFiles = e.dataTransfer.files.length > 1 ? Array.from(e.dataTransfer.files) : null;
    showOriginal(currentFile);
});

// Show original image
function showOriginal(file) {
    if (!file) return;
    const url = URL.createObjectURL(file);
    const img = document.createElement('img');
    img.src = url;
    img.alt = "Original preview";
    originalPreview.innerHTML = '';
    originalPreview.appendChild(img);
}

// Operation parameter handling
operationSelect.addEventListener("change", () => {
    updateParameterControls(operationSelect.value);
});

function updateParameterControls(operation) {
    parameters.innerHTML = "";
    if (!operationParams[operation]) return;

    operationParams[operation].forEach(param => {
        const wrap = document.createElement("div");
        wrap.className = "parameter-wrap";

        const label = document.createElement("label");
        label.textContent = param.name.replace('_', ' ').toUpperCase();

        const input = document.createElement("input");
        input.type = param.type;
        input.id = param.name;
        input.value = param.default;
        input.min = param.min;
        input.max = param.max;
        input.step = param.step;

        const valueDisplay = document.createElement("span");
        valueDisplay.className = "param-value";
        valueDisplay.textContent = param.default;

        input.addEventListener('input', () => {
            valueDisplay.textContent = input.value;
        });

        wrap.appendChild(label);
        wrap.appendChild(input);
        wrap.appendChild(valueDisplay);
        parameters.appendChild(wrap);
    });
}

// Collect parameters from inputs
function collectParams() {
    const params = {};
    const inputs = parameters.querySelectorAll('input');
    inputs.forEach(input => {
        params[input.id] = input.type === 'number' ? Number(input.value) : input.value;
    });
    return params;
}

// Process button handler
processBtn.addEventListener("click", async() => {
    if (!currentFile) {
        alert("Please select or drag an image.");
        return;
    }

    const operation = operationSelect.value;
    if (!operation) {
        alert("Please select an operation.");
        return;
    }

    processBtn.disabled = true;
    processedPreview.classList.add('processing');

    try {
        const formData = new FormData();
        formData.append("file", currentFile);
        formData.append("operation", operation);
        formData.append("params", JSON.stringify(collectParams()));

        const response = await fetch(`${backend}/process`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error(`Server error: ${response.statusText}`);

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        const img = document.createElement('img');
        img.src = url;
        img.alt = "Processed preview";
        processedPreview.innerHTML = '';
        processedPreview.appendChild(img);

        // Store blob URL and enable toolbar Download button
        processedUrl = url;
        if (downloadBtn) {
            downloadBtn.disabled = false;
            downloadBtn.dataset.filename = `result_${operation}.png`;
        }
    } catch (error) {
        console.error('Processing failed:', error);
        processedPreview.innerHTML = `<div class="error">Processing failed: ${error.message}</div>`;
    } finally {
        processBtn.disabled = false;
        processedPreview.classList.remove('processing');
    }
});

// Download toolbar button behaviour
if (downloadBtn) {
    downloadBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (!processedUrl) return;
        const a = document.createElement('a');
        a.href = processedUrl;
        a.download = downloadBtn.dataset.filename || 'result.png';
        document.body.appendChild(a);
        a.click();
        a.remove();
    });
}

// Add theme toggle functionality
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    themeToggle.innerHTML = theme === 'dark' ? '☀️ Toggle Theme' : '🌙 Toggle Theme';
}

// Initialize theme
window.addEventListener("DOMContentLoaded", async() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    await loadOperations();
});

// Theme toggle handler
themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
});