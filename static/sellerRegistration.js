// document.addEventListener('DOMContentLoaded', function() {
//     const shopName = document.getElementById('shopName');
//     const userName = document.getElementById('userName');
//     const email = document.getElementById('email');
//     const password = document.getElementById('password');
//     const confirmPassword = document.getElementById('confirmPassword');
//     const phone = document.getElementById('phone');
//     const shopAddress = document.getElementById('shopAddress');
//     const taxID = document.getElementById('taxID');

//     const shopNameValidation = document.getElementById('shopNameValidation');
//     const userNameValidation = document.getElementById('userNameValidation');
//     const emailValidation = document.getElementById('emailValidation');
//     const passwordValidation = document.getElementById('passwordValidation');
//     const confirmPasswordValidation = document.getElementById('confirmPasswordValidation');
//     const phoneValidation = document.getElementById('phoneValidation');
//     const shopAddressValidation = document.getElementById('shopAddressValidation');
//     const taxIDValidation = document.getElementById('taxIDValidation');

//     shopName.addEventListener('input', function() {
//         shopNameValidation.textContent = /^[a-zA-Z\s]+$/.test(this.value) ? '' : 'Shop name can only contain alphabets';
//     });

//     userName.addEventListener('input', function() {
//         userNameValidation.textContent = /^[a-zA-Z]+$/.test(this.value) ? '' : 'Username can only contain alphabets';
//     });

//     email.addEventListener('input', function() {
//         emailValidation.textContent = /^[a-zA-Z0-9._%+-]+@(ajce\.com|gmail\.com)$/.test(this.value) ? '' : 'Invalid email address';
//     });

//     password.addEventListener('input', function() {
//         const validPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;
//         passwordValidation.textContent = validPassword.test(this.value) ? '' : 'Password must contain at least one lowercase, one uppercase, one numeric, one special character, and be at least 6 characters long';
//     });

//     confirmPassword.addEventListener('input', function() {
//         confirmPasswordValidation.textContent = this.value === password.value ? '' : 'Passwords do not match';
//     });

//     phone.addEventListener('input', function() {
//         phoneValidation.textContent = /^\d{10}$/.test(this.value) ? '' : 'Enter a valid phone number';
//     });

//     shopAddress.addEventListener('input', function() {
//         shopAddressValidation.textContent = this.value.trim() !== '' ? '' : 'Shop address cannot be empty';
//     });

//     taxID.addEventListener('input', function() {
//         taxIDValidation.textContent = /^[a-zA-Z0-9]{10}$/.test(this.value) ? '' : 'Tax identification number must be 10 alphanumeric characters';
//     });

//     const form = document.querySelector('form');

//     form.addEventListener('submit', function(event) {
//         event.preventDefault(); // Prevents the form from submitting in the traditional way

//         // Your form submission logic goes here

//         // After successful registration, redirect to login page
//         window.location.href = 'login.html';
//     });
// });
// document.addEventListener('DOMContentLoaded', function() {
//     const shopName = document.getElementById('shopName');
//     const userName = document.getElementById('userName');
//     const email = document.getElementById('email');
//     const password = document.getElementById('password');
//     const confirmPassword = document.getElementById('confirmPassword');
//     const phone = document.getElementById('phone');
//     const shopAddress = document.getElementById('shopAddress');
//     const taxID = document.getElementById('taxID');
//     const registerButton = document.getElementById('registerButton'); // Add this line

//     const shopNameValidation = document.getElementById('shopNameValidation');
//     const userNameValidation = document.getElementById('userNameValidation');
//     const emailValidation = document.getElementById('emailValidation');
//     const passwordValidation = document.getElementById('passwordValidation');
//     const confirmPasswordValidation = document.getElementById('confirmPasswordValidation');
//     const phoneValidation = document.getElementById('phoneValidation');
//     const shopAddressValidation = document.getElementById('shopAddressValidation');
//     const taxIDValidation = document.getElementById('taxIDValidation');

//     // Function to check if all fields are filled
//     function areAllFieldsFilled() {
//         return (
//             shopName.value.trim() !== '' &&
//             userName.value.trim() !== '' &&
//             email.value.trim() !== '' &&
//             password.value.trim() !== '' &&
//             confirmPassword.value.trim() !== '' &&
//             phone.value.trim() !== '' &&
//             shopAddress.value.trim() !== '' &&
//             taxID.value.trim() !== ''
//         );
//     }

//     // Function to enable/disable the register button based on field completion
//     function toggleRegisterButton() {
//         registerButton.disabled = !areAllFieldsFilled();
//     }

//     shopName.addEventListener('input', function() {
//         shopNameValidation.textContent = /^[a-zA-Z\s]+$/.test(this.value) ? '' : 'Shop name can only contain alphabets';
//         toggleRegisterButton(); // Enable/disable register button on input change
//     });

//     userName.addEventListener('input', function() {
//         userNameValidation.textContent = /^[a-zA-Z]+$/.test(this.value) ? '' : 'Username can only contain alphabets';
//         toggleRegisterButton();
//     });

//     email.addEventListener('input', function() {
//         emailValidation.textContent = /^[a-zA-Z0-9._%+-]+@(ajce\.com|gmail\.com)$/.test(this.value) ? '' : 'Invalid email address';
//         toggleRegisterButton();
//     });

//     password.addEventListener('input', function() {
//         const validPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;
//         passwordValidation.textContent = validPassword.test(this.value) ? '' : 'Password must contain at least one lowercase, one uppercase, one numeric, one special character, and be at least 6 characters long';
//         toggleRegisterButton();
//     });

//     confirmPassword.addEventListener('input', function() {
//         confirmPasswordValidation.textContent = this.value === password.value ? '' : 'Passwords do not match';
//         toggleRegisterButton();
//     });

//     phone.addEventListener('input', function() {
//         phoneValidation.textContent = /^\d{10}$/.test(this.value) ? '' : 'Enter a valid phone number';
//         toggleRegisterButton();
//     });

//     shopAddress.addEventListener('input', function() {
//         shopAddressValidation.textContent = this.value.trim() !== '' ? '' : 'Shop address cannot be empty';
//         toggleRegisterButton();
//     });

//     taxID.addEventListener('input', function() {
//         taxIDValidation.textContent = /^[a-zA-Z0-9]{10}$/.test(this.value) ? '' : 'Tax identification number must be 10 alphanumeric characters';
//         toggleRegisterButton();
//     });

//     const form = document.querySelector('form');

//     form.addEventListener('submit', function(event) {
//         event.preventDefault(); // Prevents the form from submitting in the traditional way

//         if (areAllFieldsFilled()) {
//             // Your form submission logic goes here
//             // After successful registration, redirect to login page
//             window.location.href = 'login.html';
//         } else {
//             alert('Please fill in all fields before submitting.'); // You can customize this message
//         }
//     });
// });

document.addEventListener('DOMContentLoaded', function() {
    const shopName = document.getElementById('shopName');
    const userName = document.getElementById('userName');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');
    const phone = document.getElementById('phone');
    const shopAddress = document.getElementById('shopAddress');
    const taxID = document.getElementById('taxID');
    const registerButton = document.getElementById('registerButton'); // Add an id to your register button

    const shopNameValidation = document.getElementById('shopNameValidation');
    const userNameValidation = document.getElementById('userNameValidation');
    const emailValidation = document.getElementById('emailValidation');
    const passwordValidation = document.getElementById('passwordValidation');
    const confirmPasswordValidation = document.getElementById('confirmPasswordValidation');
    const phoneValidation = document.getElementById('phoneValidation');
    const shopAddressValidation = document.getElementById('shopAddressValidation');
    const taxIDValidation = document.getElementById('taxIDValidation');

    // Function to check if all fields are filled
    function areAllFieldsFilled() {
        return (
            shopName.value.trim() !== '' &&
            userName.value.trim() !== '' &&
            email.value.trim() !== '' &&
            password.value.trim() !== '' &&
            confirmPassword.value.trim() !== '' &&
            phone.value.trim() !== '' &&
            shopAddress.value.trim() !== '' &&
            taxID.value.trim() !== ''
        );
    }

    // Function to enable/disable the register button based on field completion
    function toggleRegisterButton() {
        registerButton.disabled = !areAllFieldsFilled();
    }

    // Add event listeners for input in each field
    shopName.addEventListener('input', function() {
        shopNameValidation.textContent = /^[a-zA-Z\s]+$/.test(this.value) ? '' : 'Shop name can only contain alphabets';
        toggleRegisterButton();
    });

    userName.addEventListener('input', function() {
        userNameValidation.textContent = /^[a-zA-Z]+$/.test(this.value) ? '' : 'Username can only contain alphabets';
        toggleRegisterButton();
    });

    email.addEventListener('input', function() {
        emailValidation.textContent = /^[a-zA-Z0-9._%+-]+@(ajce\.com|gmail\.com)$/.test(this.value) ? '' : 'Invalid email address';
        toggleRegisterButton();
    });

    password.addEventListener('input', function() {
        const validPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;
        passwordValidation.textContent = validPassword.test(this.value) ? '' : 'Password must contain at least one lowercase, one uppercase, one numeric, one special character, and be at least 6 characters long';
        toggleRegisterButton();
    });

    confirmPassword.addEventListener('input', function() {
        confirmPasswordValidation.textContent = this.value === password.value ? '' : 'Passwords do not match';
        toggleRegisterButton();
    });

    phone.addEventListener('input', function() {
        phoneValidation.textContent = /^\d{10}$/.test(this.value) ? '' : 'Enter a valid phone number';
        toggleRegisterButton();
    });

    shopAddress.addEventListener('input', function() {
        shopAddressValidation.textContent = this.value.trim() !== '' ? '' : 'Shop address cannot be empty';
        toggleRegisterButton();
    });

    taxID.addEventListener('input', function() {
        taxIDValidation.textContent = /^[a-zA-Z0-9]{10}$/.test(this.value) ? '' : 'Tax identification number must be 10 alphanumeric characters';
        toggleRegisterButton();
    });

    // Disable the register button initially
    registerButton.disabled = true;

    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevents the form from submitting in the traditional way

        // Your form submission logic goes here

        // After successful registration, redirect to login page
        window.location.href = 'login.html';
    });
});
