function insertValue(value) {
    const inputField = document.getElementById('input_expression');
    inputField.removeAttribute('readonly'); // Remove readonly to allow appending
    inputField.value += value;
}

function insertFunction(functionName) {
    const inputField = document.getElementById('input_expression');
    inputField.removeAttribute('readonly'); // Remove readonly to allow appending
    inputField.value += functionName + '('; // Append the function name and an open parenthesis
}

// Function to clear the input field
function clearInput() {
    document.getElementById('input_expression').value = '';
    document.getElementById('error_message').textContent = ''; // Clear error message
}

// Function to toggle the sign of the current number in the input field
function toggleSign() {
    const inputField = document.getElementById('input_expression');
    let currentValue = inputField.value.trim();

    const lastPart = currentValue.split(/[\s+\-*\/()]/).pop();

    if (!isNaN(lastPart) && lastPart !== "") {
        if (lastPart.startsWith('-')) {
            inputField.value = currentValue.slice(0, -lastPart.length) + lastPart.substring(1);
        } else {
            inputField.value = currentValue.slice(0, -lastPart.length) + '-' + lastPart;
        }
    } else if (/[a-zA-Z_]+\($/.test(currentValue)) {
        inputField.value += '(-';
    }
}

// Function to insert a decimal point if the number doesn't already contain one
function insertDecimal() {
    const inputField = document.getElementById('input_expression');
    const currentValue = inputField.value.trim();
    const lastNumber = currentValue.split(/[\s+\-*\/()]/).pop();

    if (!lastNumber.includes('.')) {
        inputField.value += '.';
    }
}

function deleteLast() {
    const inputField = document.getElementById('input_expression');
    let currentValue = inputField.value.trim();

    const functionRegex = /[a-zA-Z_]+\($/;

    if (functionRegex.test(currentValue)) {
        const functionName = currentValue.match(functionRegex)[0];
        inputField.value = currentValue.slice(0, -functionName.length);
    } else {
        inputField.value = currentValue.slice(0, -1);
    }
}

// Function to handle form submission
function handleCalculation(event) {
    event.preventDefault(); // Prevent form from submitting

    const inputField = document.getElementById('input_expression');
    const expression = inputField.value;

    fetch('/', { // Endpoint is '/'
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ expression: expression }),
    })
    
        .then(response => response.json()) // Parse the response as JSON
        .then(data => {
            if (data.result !== undefined) {
                inputField.value = data.result; // Display the result in the input field
                document.getElementById('error_message').textContent = ''; // Clear any previous error
            } else {
                document.getElementById('error_message').textContent = 'Error: ' + data.error; // Display an error if something went wrong
            }
        })
        .catch(error => {
            document.getElementById('error_message').textContent = 'There was an error connecting to the server: ' + error; // Handle connection errors
        });
}
