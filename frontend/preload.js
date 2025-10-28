const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
    ping() {
        return { ok: true };
    }
});