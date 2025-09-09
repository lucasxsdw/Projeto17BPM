document.getElementById("fileInput").addEventListener("change", function(e) {
    const file = e.target.files[0];
    if (file) {
        document.getElementById("filePreview").classList.remove("d-none");
        document.getElementById("fileName").textContent = file.name;
        document.getElementById("fileSize").textContent = (file.size / 1024).toFixed(2) + " KB";
    }
});
