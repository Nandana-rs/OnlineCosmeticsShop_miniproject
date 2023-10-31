// // add_product.js
// document.addEventListener('DOMContentLoaded', function () {
//     const categoryDropdown = document.getElementById('productCategory');
//     const subcategoryDropdown = document.getElementById('productSubcategory');

//     // Define subcategories for each category
//     const subcategories = {
//         'Face Makeup': ['Foundations', 'Concealers', 'Blush'],
//         'Eye Makeup': ['Eyeshadows', 'Eyeliners', 'Mascaras', 'Eyebrow Products'],
//         'Lip Makeup': ['Lipsticks', 'Lip Liners', 'Lip Balm', 'Lip Gloss', 'Lip Crayon'],
//         'Skincare': ['Cleansers', 'Moisturizers', 'Sunscreens', 'Serums', 'Masks'],
//         'Hair Care': ['Hair Color', 'Shampoos', 'Conditioners', 'Hair Serums', 'Hair Styling'],
//         'Fragrances': ['Perfumes', 'Body Sprays'],
//     };

//     // Function to populate the subcategory dropdown
//     function populateSubcategories() {
//         const selectedCategory = categoryDropdown.value;
//         const subcategoriesForCategory = subcategories[selectedCategory] || [];

//         subcategoryDropdown.innerHTML = '';
//         for (const subcategory of subcategoriesForCategory) {
//             const option = document.createElement('option');
//             option.value = subcategory;
//             option.text = subcategory;
//             subcategoryDropdown.appendChild(option);
//         }
//     }

//     // Add an event listener to the category dropdown
//     categoryDropdown.addEventListener('change', populateSubcategories);

//     // Initial population of subcategories
//     populateSubcategories();
// });


document.addEventListener('DOMContentLoaded', function () {
    const categoryDropdown = document.getElementById('productCategory');
    const subcategoryDropdown = document.getElementById('productSubcategory');
    const productNameInput = document.getElementById('productName');
    const productPriceInput = document.getElementById('productPrice');
    const addProductButton = document.getElementById('addProductButton');

    // Define subcategories for each category
    const subcategories = {
        'Face Makeup': ['Foundations', 'Concealers', 'Blush'],
        'Eye Makeup': ['Eyeshadows', 'Eyeliners', 'Mascaras', 'Eyebrow Products'],
        'Lip Makeup': ['Lipsticks', 'Lip Liners', 'Lip Balm', 'Lip Gloss', 'Lip Crayon'],
        'Skincare': ['Cleansers', 'Moisturizers', 'Sunscreens', 'Serums', 'Masks'],
        'Hair Care': ['Hair Color', 'Shampoos', 'Conditioners', 'Hair Serums', 'Hair Styling'],
        'Fragrances': ['Perfumes', 'Body Sprays'],
    };

    // Function to populate the subcategory dropdown
    function populateSubcategories() {
        const selectedCategory = categoryDropdown.value;
        const subcategoriesForCategory = subcategories[selectedCategory] || [];

        subcategoryDropdown.innerHTML = '';
        for (const subcategory of subcategoriesForCategory) {
            const option = document.createElement('option');
            option.value = subcategory;
            option.text = subcategory;
            subcategoryDropdown.appendChild(option);
        }
    }

    // Add an event listener to the category dropdown
    categoryDropdown.addEventListener('change', populateSubcategories);

    // Function to enable or disable the "Add Product" button based on validation
    function updateButtonState() {
        const productName = productNameInput.value;
        const productPrice = parseFloat(productPriceInput.value);

        if (productName.trim() !== '' && !isNaN(productPrice) && productPrice > 0) {
            addProductButton.removeAttribute('disabled');
        } else {
            addProductButton.setAttribute('disabled', 'disabled');
        }
    }

    // Attach input event listeners to run the validation on input change
    productNameInput.addEventListener('input', updateButtonState);
    productPriceInput.addEventListener('input', updateButtonState);

    // Initial population of subcategories
    populateSubcategories();

    // Call the validation function on page load
    updateButtonState();
});
