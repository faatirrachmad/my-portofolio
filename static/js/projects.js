document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("project-search-form");
    const input = document.getElementById("project-search-input");
    const projectList = document.getElementById("project-list");

    const modal = document.getElementById("project-modal");
    const openModalButton = document.getElementById("open-project-modal");
    const closeModalButton = document.getElementById("close-project-modal");
    const projectForm = document.getElementById("ajax-project-form");

    function setModalOpen(isOpen) {
        if (!modal) return;
        modal.classList.toggle("is-open", isOpen);
        modal.setAttribute("aria-hidden", String(!isOpen));
    }

    openModalButton?.addEventListener("click", () => setModalOpen(true));
    closeModalButton?.addEventListener("click", () => setModalOpen(false));
    modal?.addEventListener("click", (event) => {
        if (event.target === modal) setModalOpen(false);
    });
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") setModalOpen(false);
    });

    if (!form || !input || !projectList) return;

    let debounceTimer;

    function createProjectCard(project) {
        const card = document.createElement("article");
        card.className = "experience-card";

        if (project.project_image_url) {
            const image = document.createElement("img");
            image.src = project.project_image_url;
            image.alt = `Gambar ${project.title}`;
            image.className = "project-image";
            card.appendChild(image);
        }

        const title = document.createElement("h2");
        title.textContent = project.title;
        card.appendChild(title);

        const tech = document.createElement("span");
        tech.className = "experience-category";
        tech.textContent = project.tech_stack;
        card.appendChild(tech);

        const description = document.createElement("p");
        description.className = "experience-description";
        description.textContent = project.description;
        card.appendChild(description);

        if (project.project_url) {
            const link = document.createElement("a");
            link.className = "button";
            link.href = project.project_url;
            link.textContent = "Lihat Project";
            card.appendChild(link);
        }

        return card;
    }

    async function searchProjects() {
        const query = input.value.trim();
        const url = new URL("/api/projects/", window.location.origin);
        url.searchParams.set("title", query);

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error("Gagal mengambil data proyek.");

            const projects = await response.json();
            projectList.replaceChildren();

            if (projects.length === 0) {
                const empty = document.createElement("p");
                empty.className = "empty-state";
                empty.textContent = query
                    ? "Tidak ada proyek dengan nama tersebut."
                    : "Belum ada proyek yang ditambahkan.";
                projectList.appendChild(empty);
                return;
            }

            projects.forEach((project) => {
                projectList.appendChild(createProjectCard(project));
            });
        } catch (error) {
            window.showToast?.("Pencarian gagal", error.message, "error");
        }
    }

    input.addEventListener("input", () => {
        window.clearTimeout(debounceTimer);
        debounceTimer = window.setTimeout(searchProjects, 300);
    });

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        window.clearTimeout(debounceTimer);
        searchProjects();
    });

    projectForm?.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(projectForm);
        const csrfToken = formData.get("csrfmiddlewaretoken");

        try {
            const response = await fetch(projectForm.dataset.url, {
                method: "POST",
                headers: { "X-CSRFToken": csrfToken },
                body: formData,
                credentials: "same-origin",
            });
            const result = await response.json();

            if (!response.ok) {
                const errors = Object.values(result.errors || {})
                    .flat()
                    .map((error) => error.message)
                    .join(" ");
                throw new Error(errors || "Proyek gagal ditambahkan.");
            }

            projectForm.reset();
            setModalOpen(false);
            window.showToast?.("Berhasil", result.message, "success");
            await searchProjects();
        } catch (error) {
            window.showToast?.("Gagal", error.message, "error");
        }
    });
});
