function createPasswordEntries(entries) {
    const listGroup = document.querySelector(".list-group");

    entries.forEach(entry => {
        const listItem = document.createElement("div");
        listItem.className = "list-group-item d-flex justify-content-between align-items-center";

        listItem.innerHTML = `
            <div>
                <a href="${entry.URL}" target="_blank">${entry.Title}</a>
                <p class="mb-0"><strong>Username:</strong> <span class="username">${entry.Username}</span></p>
                <p class="mb-0"><strong>Password:</strong> <span class="password blurred">${entry.Password}</span></p>
            </div>
            <div>
                <button class="btn btn-sm btn-outline-primary copy-username">Copy Username</button>
                <button class="btn btn-sm btn-outline-secondary copy-password">Copy Password</button>
            </div>
        `;

        listGroup.appendChild(listItem);
    });

    const copyButtons = document.querySelectorAll(".copy-username, .copy-password");
    copyButtons.forEach(button => {
        button.addEventListener("click", () => {
            const isUsername = button.classList.contains("copy-username");
            const textToCopy = isUsername
                ? button.closest(".list-group-item").querySelector(".username").textContent
                : button.closest(".list-group-item").querySelector(".password").textContent;

            navigator.clipboard.writeText(textToCopy)
                .then(() => alert(`Copied ${isUsername ? "username" : "password"}!`))
                .catch(err => console.error("Error copying text: ", err));
        });
    });
}

document.addEventListener("DOMContentLoaded", async() => {
    const res = await fetch("../getpasswords")

    createPasswordEntries(await res.json());
});
