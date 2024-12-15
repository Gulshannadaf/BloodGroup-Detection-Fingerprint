
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
//************************************************************************************************************* *//

function submitForm() {
    const url = 'https://localhost:8443/SGIFPCapture';
    // For some reason, this format works for about 4 parameters, SgiBioSrv doesn't get imageWSQRate
    //const params = {
    //    'Timeout': '10000',
    //    'Quality': '50',
    //    'licstr': '',
    //    'templateFormat': 'ISO',
    //    'imageWSQRate': '0.75'
    //}

    var params = "timeout=" + {{ user_input.Timeout }};
    params += "&quality=" + {{ user_input.Quality }};
    params += "&licstr=" + encodeURIComponent("{{ user_input.SecuGen_Lic }}"); 
    params += "&templateformat=" + "{{ user_input.TemplateFormat }}";
    params += "&imagewsqrate=" + "{{ user_input.ImageWSQRate }}";

    // Prepare form submission to backend
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/Display_Image';

    // Fetching data from the external API
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: params
    }).then( response => {
        return response.json();
    })
    .then((responsedata) => {
        let result = responsedata;

        // Fill form with received data
        ['ErrorCode', 'Manufacturer', 'Model', 'SerialNumber', 'ImageWidth', 'ImageHeight', 'ImageDPI', 'ImageQuality', 'NFIQ', 'TemplateBase64', 'WSQImageSize', 'WSQImage', 'BMPBase64'].forEach(key => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = key;
            input.value = result[key];
            form.appendChild(input);
        });
        document.body.appendChild(form);

        // This is sending data back to server, so that python has this data; this is really so that advanced scan maps over to same display_image.html
        ['timeout', 'quality', 'fake_detect', 'template_format', 'imagewsqrate'].forEach(key => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = key;
            input.value = document.getElementById(key).value;
            form.appendChild(input);
        });
        document.body.appendChild(form);
        form.submit();
        return;

    }).catch(error => {
        alert("Check if SGIBIOSRV is running; Status = ERROR:");
    });
    return;
}
    
