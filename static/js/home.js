document.addEventListener('DOMContentLoaded', function() {
    showPredictionForm(); // Automatically display the first form (the prediction form) on page load
});

// function toggleDropdown() {
//   const dropdownContent = document.getElementById('formSelect');
//   dropdownContent.classList.toggle('show');
// }

// function selectOption(selectedElement) {
//   // Get the button element
//   const dropdownButton = document.getElementById('dropdownMainButton');
  
//   // Update button text to selected option's text
//   dropdownButton.innerHTML = `${selectedElement.textContent} <span class="arrow">&#9662;</span>`;
  
//   // Close the dropdown
//   const dropdownContent = document.getElementById('formSelect');
//   dropdownContent.classList.remove('show');
  
//   // Call the original onclick function if it exists
//   if (selectedElement.getAttribute('onclick')) {
//       window.eval(selectedElement.getAttribute('onclick'));
//   }
// }

// // Close the dropdown if user clicks outside
// window.addEventListener('click', function(event) {
//   const dropdownContent = document.getElementById('formSelect');
//   const dropdownButton = document.getElementById('dropdownMainButton');
  
//   if (!event.target.matches('.formDropdownButton, .formDropdownButton *')) {
//       dropdownContent.classList.remove('show');
//   }
// });

function showDropdown() {
    document.getElementById('formSelect').style.display = "block";
}

function hideDropdown() {
    document.getElementById('formSelect').style.display = "none";
}

function showPredictionForm() {
    document.getElementById('delayPrediction').style.display = "block";
    document.getElementById('delayUpload').style.display = "none";
    document.getElementById('delayEdit').style.display = "none";
    document.getElementById('delayDelete').style.display = "none";
}

function showUploadForm() {
    document.getElementById('delayPrediction').style.display = "none";
    document.getElementById('delayUpload').style.display = "block";
    document.getElementById('delayEdit').style.display = "none";
    document.getElementById('delayDelete').style.display = "none";
}

function showEditForm() {
    document.getElementById('delayPrediction').style.display = "none";
    document.getElementById('delayUpload').style.display = "none";
    document.getElementById('delayEdit').style.display = "block";
    document.getElementById('delayDelete').style.display = "none";
}

function showDeleteForm() {
    document.getElementById('delayPrediction').style.display = "none";
    document.getElementById('delayUpload').style.display = "none";
    document.getElementById('delayEdit').style.display = "none";
    document.getElementById('delayDelete').style.display = "block";
}

function getInputType() {
    const inputContainer = document.getElementById("editInputContainer");
    inputContainer.innerHTML = "";
    const inputType = document.getElementById("attributeSelection").value;
    switch (inputType) {
        case "Airline":
            inputContainer.innerHTML = "<input type='text' maxlength='255' name='new_value' placeholder='Enter new airline' required>";
            break;
        case "Origin":
            inputContainer.innerHTML = "<input type='text' maxlength='3' name='new_value' placeholder='Enter new origin airport' required>";
            break;
        case "Destination":
            inputContainer.innerHTML = "<input type='text' maxlength='3' name='new_value' placeholder='Enter new destination airport' required>";
            break;
        case "DepartureDate":
            inputContainer.innerHTML = "<input type='date' name='new_value' required>";
            break;
        case "DelayMinutes":
            inputContainer.innerHTML = "<input type='number' name='new_value' required>";
            break;
    }
}     