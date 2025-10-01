// activity/CSC-Activity/renderer.js
// (Runs in renderer context; uses fetch to call FastAPI backend)
const backend = "http://127.0.0.1:8000";

const fileEl = document.getElementById("file");
const dropArea = document.getElementById("drop-area");
const originalImg = document.getElementById("originalImg");
const processedImg = document.getElementById("processedImg");
const operationEl = document.getElementById("operation");
const paramPanel = document.getElementById("param-panel");
const processBtn = document.getElementById("processBtn");
const downloadLink = document.getElementById("downloadLink");
const batchBtn = document.getElementById("batchBtn");

let currentFile = null;
let multipleFiles = null; // for batch mode

async function loadOperations() {
    try {
        const res = await fetch(`${backend}/operations`);
        const ops = await res.json();
        operationEl.innerHTML = "";
        for (const key of Object.keys(ops)) {
            const opt = document.createElement("option");
            opt.value = key;
            opt.textContent = `${key} — ${ops[key].desc || ""}`;
            operationEl.appendChild(opt);
        }
        renderParamsFor(operationEl.value, ops[operationEl.value]);
    } catch (err) {
        console.warn("Could not load operations from backend:", err);
        // fallback: add a few defaults
        ["grayscale", "brightness", "gaussian_blur", "canny"].forEach(k => {
            const opt = document.createElement("option");
            opt.value = k;
            opt.textContent = k;
            operationEl.appendChild(opt);
        });
    }
}

operationEl.addEventListener("change", () => {
    // get operations from backend again (or keep cached). For simplicity call backend ops endpoint.
    fetch(`${backend}/operations`).then(r => r.json()).then(ops => {
        renderParamsFor(operationEl.value, ops[operationEl.value]);
    }).catch(() => renderParamsFor(operationEl.value, null));
});

function renderParamsFor(opName, meta) {
    paramPanel.innerHTML = "";
    if (!meta || !meta.params) return;
    for (const [p, info] of Object.entries(meta.params)) {
        const wrap = document.createElement("div");
        wrap.style.display = "flex";
        wrap.style.flexDirection = "column";
        wrap.style.gap = "6px";
        wrap.style.marginBottom = "6px";
        const label = document.createElement("label");
        label.textContent = p;
        const input = document.createElement("input");
        input.name = p;
        if (info.min !== undefined) input.min = info.min;
        if (info.max !== undefined) input.max = info.max;
        input.value = (info.default !== undefined) ? info.default : "";
        if (info.options) {
            const select = document.createElement("select");
            select.name = p;
            info.options.forEach(o => {
                const oel = document.createElement("option");
                oel.value = o;
                oel.textContent = o;
                select.appendChild(oel);
            });
            wrap.appendChild(label);
            wrap.appendChild(select);
            paramPanel.appendChild(wrap);
            continue;
        }
        input.type = "number";
        wrap.appendChild(label);
        wrap.appendChild(input);
        paramPanel.appendChild(wrap);
    }
}

fileEl.addEventListener("change", e => {
    currentFile = e.target.files[0];
    multipleFiles = e.target.files.length > 1 ? Array.from(e.target.files) : null;
    showOriginal(currentFile);
});

dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("drag");
});
dropArea.addEventListener("dragleave", () => dropArea.classList.remove("drag"));
dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("drag");
    const f = e.dataTransfer.files[0];
    fileEl.files = e.dataTransfer.files;
    currentFile = f;
    multipleFiles = e.dataTransfer.files.length > 1 ? Array.from(e.dataTransfer.files) : null;
    showOriginal(currentFile);
});

function showOriginal(file) {
    if (!file) return;
    const url = URL.createObjectURL(file);
    originalImg.src = url;
    originalImg.style.display = "block";
}


function collectParams() {
    const inputs = paramPanel.querySelectorAll("input,select");
    const obj = {};
    inputs.forEach(inp => {
        const val = inp.type === "number" ? Number(inp.value) : inp.value;
        obj[inp.name] = val;
    });
    return obj;
}

processBtn.addEventListener("click", async() => {
    if (!currentFile) { alert("Please select or drag an image."); return; }
    const op = operationEl.value;
    const params = collectParams();
    const fd = new FormData();
    fd.append("file", currentFile);
    fd.append("operation", op);
    fd.append("params", JSON.stringify(params));
    processBtn.disabled = true;
    processBtn.textContent = "Processing...";
    try {
        const res = await fetch(`${backend}/process`, { method: "POST", body: fd });
        if (!res.ok) throw new Error("Server error: " + res.statusText);
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        processedImg.src = url;
        downloadLink.href = url;
        downloadLink.download = `result_${op}.png`;
    } catch (err) {
        alert("Processing failed: " + err.message);
    } finally {
        processBtn.disabled = false;
        processBtn.textContent = "Process Image";
    }
});

// batch: sends all selected files
batchBtn.addEventListener("click", async() => {
    const files = multipleFiles || (fileEl.files.length > 1 ? Array.from(fileEl.files) : null);
    if (!files || files.length === 0) { alert("Select multiple files for batch"); return; }
    const op = operationEl.value;
    const params = collectParams();
    const fd = new FormData();
    files.forEach(f => fd.append("files", f));
    fd.append("operation", op);
    fd.append("params", JSON.stringify(params));
    batchBtn.disabled = true;
    batchBtn.textContent = "Processing batch...";
    try {
        const res = await fetch(`${backend}/batch_process`, { method: "POST", body: fd });
        if (!res.ok) throw new Error("Server error: " + res.statusText);
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        // download zip
        const a = document.createElement("a");
        a.href = url;
        a.download = "results.zip";
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (err) {
        alert("Batch processing failed: " + err.message);
    } finally {
        batchBtn.disabled = false;
        batchBtn.textContent = "Batch (multi-file)";
    }
});

window.addEventListener("DOMContentLoaded", async() => {
    await loadOperations();
});