function checkboxValues() {
    let arr = [];
    let checkboxes = document.querySelectorAll('[name="categories"]');

    checkboxes.forEach((el) => {
        if (el.checked) {
            arr.push(el.value);
        }
    })

    return arr;
}

function showOnlyCheckedCategories() {
    let checkedCategories = checkboxValues();
    let allCategories = document.querySelectorAll('.to-filter');


    allCategories.forEach((el) => {
        let category = el.querySelector('.description').getAttribute('data-category');

        let arr2 = category.split(',').map(function (item) {
            return item.trim();
        });

        if (!checkedCategories.some(r => arr2.includes(r))) {
            el.style.display = 'none';
        } else {
            el.style.display = 'block';
        }
    })

}


let categoriesEventBtn = document.querySelector('.cat-event');

categoriesEventBtn.addEventListener('click', function (e) {
    e.preventDefault();
    showOnlyCheckedCategories();
});


let resetBtn = document.querySelector('.btn.prev-step.institution-show-reset');

resetBtn.addEventListener('click', function (e) {
    e.preventDefault();
    let institutions = document.querySelectorAll('.institution');

    institutions.forEach((el) => {
        el.style.display = 'none';
        el.classList.remove('visible');
    })
});