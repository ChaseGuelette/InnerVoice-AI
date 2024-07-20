async function submitForm() {
    const inputPastContext = document.getElementById('inputPastContext').value;
    const inputText = document.getElementById('inputText').value;
    const inputEmotions = document.getElementById('inputEmotions').value;

    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `inputPastContext=${encodeURIComponent(inputPastContext)}&inputText=${encodeURIComponent(inputText)}&inputEmotions=${encodeURIComponent(inputEmotions)}`
    });

    const data = await response.json();
    document.getElementById('responseText').innerText = data.responseText;
    
    const audioElement = document.getElementById('audio');
    const audioSource = document.getElementById('audioSource');
    audioSource.src = 'static/output.mp3' + '?' + new Date().getTime(); // Force reload the audio by adding a timestamp

    audioElement.hidden = false;
    
    audioElement.load(); // Reload the audio element to ensure it's ready to play

    // Ensure the audio file is completely loaded before playing it
    audioElement.oncanplaythrough = () => {
        audioElement.play();
    };

    // Refresh the chat history
    fetchChatHistory();
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
    authForm.style.display = 'none'; // Hide the auth form
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

async function signOut() {
    const response = await fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    const data = await response.json();
    showToast(data.message);

    if (data.success) {
        const signInBtn = document.getElementById('signInBtn');
        const signUpBtn = document.getElementById('signUpBtn');
        const greetingMsg = document.getElementById('greetingMsg');
        
        signInBtn.hidden = false;
        signUpBtn.hidden = false;
        greetingMsg.hidden = true;
        document.getElementById('preferredNameDisplay').innerText = ''; // Clear preferred name text

        // Clear past context, username and password
        document.getElementById('inputPastContext').value = '';
        document.getElementById('username').value = '';
        document.getElementById('preferredName').value = '';
        document.getElementById('password').value = '';
    }
}

async function fetchChatHistory() {
    const response = await fetch('/chat-history', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    const data = await response.json();
    displayChatHistory(data.conversation);
}

function displayChatHistory(conversation) {
    const chatHistoryDiv = document.getElementById('chatHistory');
    chatHistoryDiv.innerHTML = '';

    conversation.forEach(chat => {
        const chatMessage = document.createElement('div');
        chatMessage.className = 'chat-message';
        chatMessage.innerText = `${chat.role === 'user' ? 'User' : 'System'}: ${chat.content}`;
        chatHistoryDiv.appendChild(chatMessage);
    });
}