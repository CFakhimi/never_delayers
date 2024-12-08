// document.addEventListener('DOMContentLoaded', function() {
//     showPredictionForm(); // Automatically display the first form (the prediction form) on page load
// });

function selectOption(event, element) {
  event.preventDefault();

  // Get the form type from the 'form-type' attribute of the clicked element
  const formType = element.getAttribute('form-type');

  // Hide all forms
  const forms = document.querySelectorAll('.dataInput');
  forms.forEach(form => form.classList.remove('active'));

  // Show the selected form
  const selectedForm = document.getElementById(formType);
  if (selectedForm) {
    selectedForm.classList.add('active');
  }

  // Update the button label to match the clicked option's inner text
  const dropdownButton = document.getElementById('dropdownMainButton');
  dropdownButton.innerHTML = `${element.innerText} <span class="arrow">&#9662;</span>`;
}

// function selectOption(event, formType) {
//   event.preventDefault();

//   // Hide all forms
//   const forms = document.querySelectorAll('.dataInput');
//   forms.forEach(form => form.classList.remove('active'));

//   // Show the selected form
//   const selectedForm = document.getElementById(formType);
//   if (selectedForm) {
//     selectedForm.classList.add('active');
//   }
// }

function showDropdown() {
    document.getElementById('formSelect').style.display = "block";
}

function hideDropdown() {
    document.getElementById('formSelect').style.display = "none";
}

// function showPredictionForm() {
//     document.getElementById('delayPrediction').style.display = "block";
//     document.getElementById('delayUpload').style.display = "none";
//     document.getElementById('delayEdit').style.display = "none";
//     document.getElementById('delayDelete').style.display = "none";
// }

// function showUploadForm() {
//     document.getElementById('delayPrediction').style.display = "none";
//     document.getElementById('delayUpload').style.display = "block";
//     document.getElementById('delayEdit').style.display = "none";
//     document.getElementById('delayDelete').style.display = "none";
// }

// function showEditForm() {
//     document.getElementById('delayPrediction').style.display = "none";
//     document.getElementById('delayUpload').style.display = "none";
//     document.getElementById('delayEdit').style.display = "block";
//     document.getElementById('delayDelete').style.display = "none";
// }

// function showDeleteForm() {
//     document.getElementById('delayPrediction').style.display = "none";
//     document.getElementById('delayUpload').style.display = "none";
//     document.getElementById('delayEdit').style.display = "none";
//     document.getElementById('delayDelete').style.display = "block";
// }

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