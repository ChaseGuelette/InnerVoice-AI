async function submitForm() {
    const inputText = document.getElementById('inputText').value;
    const inputEmotions = document.getElementById('inputEmotions').value;

    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `inputText=${encodeURIComponent(inputText)}&inputEmotions=${encodeURIComponent(inputEmotions)}`
    });

    const data = await response.json();
    document.getElementById('responseText').innerText = data.responseText;
    
    const audioElement = document.getElementById('audio');
    const audioSource = document.getElementById('audioSource');
    audioSource.src = 'static/output.mp3' + '?' + new Date().getTime(); // Force reload the audio by adding a timestamp
    
    audioElement.load(); // Reload the audio element to ensure it's ready to play

    // Ensure the audio file is completely loaded before playing it
    audioElement.oncanplaythrough = () => {
        audioElement.play();
    };
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.innerText = message;
    toast.className = "toast show";
    setTimeout(() => { toast.className = toast.className.replace("show", ""); }, 3000);
}

function showAuthForm(type) {
    showToast(type + ' button clicked');
    
    const authForm = document.getElementById('authForm');
    const authFormTitle = document.getElementById('authFormTitle');
    const submitBtn = document.getElementById('submitBtn');
    
    authForm.style.display = 'flex'; // Show the auth form
    authFormTitle.innerText = type;
    submitBtn.onclick = type === 'Sign In' ? signIn : signUp;
}

function cancelAuthForm() {
    const authForm = document.getElementById('authForm');
    authForm.style.display= 'none'; // Hide the auth form
}

async function submitAuthForm(event) {
    event.preventDefault(); // Prevent default form submission
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const preferredName = document.getElementById('preferredName').value;
    const authFormTitle = document.getElementById('authFormTitle').innerText;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password, preferredName })
    });

    const data = await response.json();
    showToast(data.message);

    if (data.success) {
        document.getElementById('authForm').style.display = 'none';
        if (authFormTitle === 'Sign In') {
            signIn(username, preferredName);
        } else {
            signUp(username, preferredName);
        }
    }
}

function signIn(username, preferredName) {
    // Update the displayed preferred name
    document.getElementById('preferredNameDisplay').innerText = preferredName;

    // Simulate user sign-in
    showToast('Sign In successful');
    const signInBtn = document.getElementById('signInBtn');
    const signUpBtn = document.getElementById('signUpBtn');
    const greetingMsg = document.getElementById('greetingMsg');
    
    signInBtn.hidden = true;
    signUpBtn.hidden = true;
    greetingMsg.hidden = false;
}

function signUp(username, preferredName) {
    // Update the displayed preferred name
    document.getElementById('preferredNameDisplay').innerText = preferredName;

    // Simulate user sign-up
    showToast('Sign Up successful');
    const signInBtn = document.getElementById('signInBtn');
    const signUpBtn = document.getElementById('signUpBtn');
    const greetingMsg = document.getElementById('greetingMsg');
    
    signInBtn.hidden = true;
    signUpBtn.hidden = true;
    greetingMsg.hidden = false;
}

function signOut() {
    showToast('Sign Out button clicked');
    
    // Simulate user sign-out
    const signInBtn = document.getElementById('signInBtn');
    const signUpBtn = document.getElementById('signUpBtn');
    const greetingMsg = document.getElementById('greetingMsg');
    
    signInBtn.hidden = false;
    signUpBtn.hidden = false;
    greetingMsg.hidden = true;
    document.getElementById('preferredNameDisplay').innerText = ''; // Clear preferred name text
}