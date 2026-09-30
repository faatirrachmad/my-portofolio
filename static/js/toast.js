function showToast(title, message, type = "success", duration = 3000) {
    const toast = document.getElementById("toast");
    const titleElement = document.getElementById("toast-title");
    const messageElement = document.getElementById("toast-message");

    if (!toast || !titleElement || !messageElement) return;

    titleElement.textContent = title;
    messageElement.textContent = message;

    toast.classList.remove("toast-success", "toast-error", "toast-visible");
    toast.classList.add(type === "error" ? "toast-error" : "toast-success");

    // Paksa browser menghitung ulang animasi saat toast ditampilkan kembali.
    void toast.offsetWidth;
    toast.classList.add("toast-visible");

    window.clearTimeout(showToast.timeoutId);
    showToast.timeoutId = window.setTimeout(() => {
        toast.classList.remove("toast-visible");
    }, duration);
}

window.showToast = showToast;