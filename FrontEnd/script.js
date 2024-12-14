
// Function to switch between pages
function showHomePage() {
    hideAllPages();
    document.getElementById("home-page").style.display = "block";
}

function showAboutPage() {
    hideAllPages();
    document.getElementById("about-page").style.display = "block";
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

// Handle fingerprint detection
function captureFingerprint() {
    fetch('/capture_and_detect', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            const result = document.getElementById('result-text');
            if (data.blood_group) {
                result.innerText = "Blood Group Detected: " + data.blood_group;
            } else {
                result.innerText = "Error: Could not detect blood group.";
            }
        })
        .catch(error => {
            console.error(error);
            document.getElementById('result-text').innerText = "Server error. Please try again.";
        });
}

