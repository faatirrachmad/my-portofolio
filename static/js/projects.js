document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("project-search-form");
    const searchInput = document.getElementById("project-search-input");
    const projectList = document.getElementById("project-list");
    const modal = document.getElementById("project-modal");
    const openModalButton = document.getElementById("open-project-modal");
    const closeModalButton = document.getElementById("close-project-modal");
    const projectForm = document.getElementById("ajax-project-form");

    if (!projectList) return;

    const placeholderId = "00000000-0000-0000-0000-000000000000";
    let debounceTimer;

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

    function makeLink(label, href, className = "button") {
        const link = document.createElement("a");
        link.className = className;
        link.href = href;
        link.textContent = label;
        return link;
    }

    function makePostForm(action, label, className, csrfToken) {
        const form = document.createElement("form");
        form.method = "post";
        form.action = action;

        const token = document.createElement("input");
        token.type = "hidden";
        token.name = "csrfmiddlewaretoken";
        token.value = csrfToken;
        form.appendChild(token);

        const button = document.createElement("button");
        button.type = "submit";
        button.className = className;
        button.textContent = label;
        form.appendChild(button);

        return form;
    }

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

        const actions = document.createElement("div");
        actions.className = "project-actions";

        if (project.project_url) {
            actions.appendChild(makeLink("Lihat Project", project.project_url));
        }

        if (projectList.dataset.canStar === "true") {
            const starUrl = projectList.dataset.starUrl.replace(
                placeholderId,
                project.id
            );
            const csrfToken =
                document.querySelector(
                    "#page-csrf-form [name=csrfmiddlewaretoken]"
                )?.value || "";

            const starButton = makePostForm(
                starUrl,
                `${project.is_starred ? "Unstar" : "Star"} ★ ${project.star_count}`,
                "button button-star",
                csrfToken
            );
            starButton.className = "star-form";
            actions.appendChild(starButton);
        }

        if (projectList.dataset.canEdit === "true") {
            const editUrl = projectList.dataset.editUrl.replace(
                placeholderId,
                project.id
            );
            actions.appendChild(
                makeLink("Edit Project", editUrl, "button button-secondary")
            );
        }

        if (projectList.dataset.canDelete === "true") {
            const deleteUrl = projectList.dataset.deleteUrl.replace(
                placeholderId,
                project.id
            );
            const csrfToken =
                document.querySelector(
                    "#page-csrf-form [name=csrfmiddlewaretoken]"
                )?.value || "";
            const deleteForm = makePostForm(
                deleteUrl,
                "Hapus Proyek",
                "button button-danger",
                csrfToken
            );
            deleteForm.addEventListener("submit", (event) => {
                if (!window.confirm(`Hapus proyek "${project.title}"?`)) {
                    event.preventDefault();
                }
            });
            actions.appendChild(deleteForm);
        }

        card.appendChild(actions);
        return card;
    }

    async function searchProjects() {
        const query = searchInput?.value.trim() || "";
        const url = new URL("/api/projects/", window.location.origin);
        if (query) url.searchParams.set("title", query);

        projectList.setAttribute("aria-busy", "true");
        projectList.replaceChildren();

        const loading = document.createElement("p");
        loading.className = "empty-state";
        loading.textContent = "Memuat proyek…";
        projectList.appendChild(loading);

        try {
            const response = await fetch(url, {
                headers: { Accept: "application/json" },
                credentials: "same-origin",
            });
            if (!response.ok) {
                throw new Error("Gagal mengambil data proyek dari server.");
            }

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
            projectList.replaceChildren();
            const errorMessage = document.createElement("p");
            errorMessage.className = "empty-state";
            errorMessage.textContent = "Proyek gagal dimuat. Silakan coba lagi.";
            projectList.appendChild(errorMessage);
            window.showToast?.("Pencarian gagal", error.message, "error");
        } finally {
            projectList.setAttribute("aria-busy", "false");
        }
    }

    searchInput?.addEventListener("input", () => {
        window.clearTimeout(debounceTimer);
        debounceTimer = window.setTimeout(searchProjects, 300);
    });

    searchForm?.addEventListener("submit", (event) => {
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
                headers: {
                    "X-CSRFToken": csrfToken,
                    Accept: "application/json",
                },
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

    searchProjects();
});
