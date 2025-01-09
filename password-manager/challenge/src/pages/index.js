function showAlert(message) {
    const alertDiv = document.getElementById('alertMessage');
    alertDiv.innerHTML = '<p>' + message + '</p>';
    alertDiv.classList.remove('d-none');
}

document.getElementById("submit").onclick = async function() {
    fetch("./login", {
        method: "POST",
        body: JSON.stringify({
            usr: document.getElementById("username").value,
            pwd: document.getElementById("password").value,
        }),
    }).then(async (response) => {
        const body = await response.text()

        try {
            JSON.parse(body)
            window.location.href = "./passwords"
        } catch(_) {
            showAlert(body)
        }
    })
}