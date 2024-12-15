// Function to switch between pages
function showHomePage() {
    hideAllPages();
    document.getElementById("home-page").style.display = "block";
}

function showLoginPage() {
    hideAllPages();
    document.getElementById("login-page").style.display = "block";
}

function showSignupPage() {
    hideAllPages();
    document.getElementById("signup-page").style.display = "block";
}

function hideAllPages() {
    document.querySelectorAll(".page-content").forEach(page => {
        page.style.display = "none";
    });
}

// Login function
function loginUser(event) {
    event.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    fetch('/login', {
        method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Login Successful");
                    document.getElementById("login-result").innerText = "Login Successful!";
                    showHomePage(); // Redirect to home
                } else {
                    alert("Login Failed: " + data.message);
                }
            })
            .catch(error => {
                console.error("Error during login:", error);
                alert("Server error. Please try again.");
            });
        }

        // Signup function
        function signupUser(event) {
            event.preventDefault();
            const username = document.getElementById("signup-username").value;
            const password = document.getElementById("signup-password").value;

            fetch('/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Sign Up Successful");
                    document.getElementById("signup-result").innerText = "Sign Up Successful!";
                    showLoginPage(); // Redirect to login page
                } else {
                    alert("Sign Up Failed: " + data.message);
                }
            })
            .catch(error => {
                console.error("Error during signup:", error);
                alert("Server error. Please try again.");
            });
        }

        window.onload = showHomePage; // Show the home page initially
    