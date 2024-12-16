// document.addEventListener('DOMContentLoaded', function() {
//     showPredictionForm(); // Automatically display the first form (the prediction form) on page load
// });

// Prevent forms from submitting on reload
// const all_forms = document.getElementsByClassName('dataInput');
// all_forms.forEach(form => form.addEventListener('submit', function(event) {
//                         event.preventDefault();
//                         //this.reset();
//                     }));

function showForm(formType) {
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
    const element = document.getElementById(formType + 'Button');
    dropdownButton.innerHTML = `${element.innerText} <span class="arrow">&#9662;</span>`;
}

function selectOption(element) {
    // Get the form type from the 'form-type' attribute of the clicked element
    const formType = element.getAttribute('form-type');

    localStorage.setItem('selectedForm', formType);

    // Hide all forms
    showForm(formType);
}

window.addEventListener('DOMContentLoaded', () => {
    const savedValue = localStorage.getItem('selectedForm') || 'predict';
    showForm(savedValue);
})

function showDropdown() {
    document.getElementById('formSelect').style.display = "block";
}

function hideDropdown() {
    document.getElementById('formSelect').style.display = "none";
}

function getInputType(flightID) {
    const inputContainer = document.getElementById(`editInputContainer${flightID}`);
    inputContainer.innerHTML = "";
    const inputType = document.getElementById(`attributeSelection${flightID}`).value;
    switch (inputType) {
        case "Airline":
            inputContainer.innerHTML = "<input list='airlines' name='new_value' required placeholder='Airline (e.g. United)'>";
            break;
        case "Origin":
            inputContainer.innerHTML = "<input type='text' maxlength='3' name='new_value' required placeholder='Origin Airport (e.g. SFO) '>";
            break;
        case "Destination":
            inputContainer.innerHTML = "<input type='text' maxlength='3' name='new_value' required placeholder='Destination Airport (e.g. LAX)'>";
            break;
        case "DepartureDate":
            inputContainer.innerHTML = "<input type='date' name='new_value' required>";
            break;
        case "DelayMinutes":
            inputContainer.innerHTML = "<input type='number' name='new_value' required>";
            break;
    }
}     