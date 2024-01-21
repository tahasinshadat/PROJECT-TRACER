// Function to execute code and display in the terminal
validCommands = ["t-forward", "t-backward", "--help", "--user", "t-scan", "t-status", "clear", "t-locate"];
const terminalElement = document.getElementById('terminal');
function executeCode() {
    const input = document.getElementById('input').value;
    const codeElement = document.createElement('pre');

    // Wrap input in span for styling and determine the color based on if its a valid command
    (validCommands.includes(input)) ? commandColor = "recognized-command" : commandColor = "user-input";
    codeElement.innerHTML = '<span class="arrow"> >> </span><span class="' + commandColor + '">' + input + '</span>';
    terminalElement.appendChild(codeElement);

    switch (input) {
        case "--help":
            explainedCommands = [
                "--help - list of commands",
                "--user - current user's authorization level",
                "t-forward - move TRACER forward 6 inches",
                "t-backward - move TRACER backward 6 inches",
                "t-scan - burst scan with TRACER's lidar sensor",
                "t-status - TRACER's battery status",
                "t-locate - TRACER's current location",
                "clear - clear terminal history",
            ];
            explainedCommands.forEach(command => { terminalResponse(command) });
            break;
        case "t-forward":
            sendCommand(input);
            TRACERCommandResponse();
            break;
        case "t-backward":
            sendCommand(input);
            TRACERCommandResponse();
            break;
        case "t-scan": 
            TRACERCommandResponse();
            break;
        case "t-status": 
            TRACERCommandResponse();
            break;
        case "t-locate": 
            TRACERCommandResponse();
            break;
        case "--user": 
            terminalResponse("Authorization Level: 0 - Administrator");
            break;
        case "clear": 
            terminalElement.innerHTML = "<pre>Terminal re-initialized...</pre>";
            break;
        default: 
            terminalResponse("Un-recognized command", true);
            break;
    }

    console.log('>> ' + input); // Log input in the console
    document.getElementById('input').value = ''; // Clear input field after execution

    // Scroll the terminal to the bottom
    terminalElement.scrollTop = terminalElement.scrollHeight;
}

// Send POST request to Flask
function sendCommand(command) {
    fetch('/move', { // Sends a POST request to Flask route '/move'
        method: 'POST', // Specifies the HTTP method as POST
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `command=${command}`, // Command data sent in the body as form data
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); // Returns the response body as text
    })
    .then(data => {
        terminalResponse(data); // Displays the response data in the terminal
    })
    .catch(error => {
        terminalResponse('Error: ' + error, true); // Handles any errors occurred during fetch and displays error to user's terminal
    });
}

// Function to response to user via terminal commands
function terminalResponse(tResponse, error=false) {
    (error) ? color = 'unrecognized-command' : color = 'executed-command';
    const response = document.createElement('pre');
    response.innerHTML = '<span class="' + color + '">' + tResponse + '</span>';
    terminalElement.append(response);
}

function TRACERCommandResponse() {
    terminalResponse("TRACER Command Recognized...");
    terminalResponse("  Enumerating byte packages...");
    terminalResponse("  -- Command successfully sent to TRACER");
}

// Function to handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter') executeCode(); 
}

// Function to send a POST request for camera switch
function switchCameras() {
    fetch('/switch_camera', {
        method: 'POST',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(data => {
        console.log(data);  // Log the response to the console
    })
    .catch(error => {
        console.error('Error: ' + error);
    });
}


// To check if current webpage is connected with socket IO
var socket = io.connect('https://' + document.domain + ':' + location.port);

socket.on('connect', function () {
    console.log('Connected to SocketIO server');
});

socket.on('disconnect', function () {
    console.log('Disconnected from SocketIO server');
});
