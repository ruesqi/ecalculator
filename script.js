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

function sendCalculation() {
    const inputField = document.getElementById('input_expression');
    const expression = inputField.value;

    // Send the expression to the external server (eternitycalculatorteamo.co)
    fetch('https://eternitycalculatorteamo.co/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer pk1_83df53988e8796f23db912b80c0d0930a41805ec361d9571a1b76ab5a581b46a' // Use the Public Key
        },
        body: JSON.stringify({ expression: expression }), // Send the input as JSON data
    })
        .then(response => response.json()) // Parse the response as JSON
        .then(data => {
            if (data.result !== undefined) {
                alert('Result: ' + data.result); // Display the result to the user
            } else {
                alert('Error: ' + data.error); // Display an error if something went wrong
            }
        })
        .catch(error => {
            alert('There was an error connecting to the server: ' + error); // Handle connection errors
        });
}
