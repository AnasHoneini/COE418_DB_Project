/*
function setMessage(Element, type, msg) {
    const messageElement = Element.querySelector(".message");

    messageElement.textContent = msg;
    messageElement.classList.remove(".message--success", ".message--error");
    messageElement.classList.add(`message ${type}`);
}

function setInputError(inputElement, msg) {
    inputElement.classList.add("input--error");
    inputElement.parentElement.querySelector(".input-error-message").textContent = msg;
}

function clearInputError(inputElement) {
    inputElement.classList.remove("input--error");
    inputElement.parentElement.querySelector(".input-error-message").textContent = "";
}

document.addEventListener("DOMContentLoaded", () => {
    const login = document.querySelector("#login");
    const createAccount = document.querySelector("#createAccount");

    document.querySelector("#linkCreateAccount").addEventListener("click", e => {
        
    });

    document.querySelector("#linkLogin").addEventListener("click", e => {
      
    });

    login.addEventListener("submit", e => {
        

        // Perform your AJAX/Fetch login

        setMessage(login, "error", "Invalid username/password combination");
    });

    document.querySelectorAll(".input").forEach(inputElement => {
        inputElement.addEventListener("blur", e => {
            if (e.target.id === "signupUsername" && e.target.value.length > 0 && e.target.value.length < 5) {
                setInputError(inputElement, "Username must be at least 5 characters in length");
            }
        });
        inputElement.addEventListener("input", e => {
            clearInputError(inputElement);
           
        });
    });
});*/