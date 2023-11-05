document.addEventListener('DOMContentLoaded', function () {
    const categoryDropdown = document.getElementById('productCategory');
    const subcategoryDropdown = document.getElementById('productSubcategory');

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

    // Initial population of subcategories
    populateSubcategories();
});
