/**
 * HomePage - Help section
 */
class Help {
    constructor($el) {
        this.$el = $el;
        this.$buttonsContainer = $el.querySelector(".help--buttons");
        this.$slidesContainers = $el.querySelectorAll(".help--slides");
        this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
        this.init();
    }

    init() {
        this.events();
    }

    events() {
        /**
         * Slide buttons
         */
        this.$buttonsContainer.addEventListener("click", e => {
            if (e.target.classList.contains("btn")) {
                this.changeSlide(e);
            }
        });

        /**
         * Pagination buttons
         */
        this.$el.addEventListener("click", e => {
            if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                this.changePage(e);
            }
        });
    }

    changeSlide(e) {
        e.preventDefault();
        const $btn = e.target;

        // Buttons Active class change
        [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
        $btn.classList.add("active");

        // Current slide
        this.currentSlide = $btn.parentElement.dataset.id;

        // Slides active class change
        this.$slidesContainers.forEach(el => {
            el.classList.remove("active");

            if (el.dataset.id === this.currentSlide) {
                el.classList.add("active");
            }
        });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
        e.preventDefault();
        const page = e.target.dataset.page;

        console.log(page);
    }
}

const helpSection = document.querySelector(".help");
if (helpSection !== null) {
    new Help(helpSection);
}

/**
 * Form Select
 */
class FormSelect {
    constructor($el) {
        this.$el = $el;
        this.options = [...$el.children];
        this.init();
    }

    init() {
        this.createElements();
        this.addEvents();
        this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
        // Input for value
        this.valueInput = document.createElement("input");
        this.valueInput.type = "text";
        this.valueInput.name = this.$el.name;

        // Dropdown container
        this.dropdown = document.createElement("div");
        this.dropdown.classList.add("dropdown");

        // List container
        this.ul = document.createElement("ul");

        // All list options
        this.options.forEach((el, i) => {
            const li = document.createElement("li");
            li.dataset.value = el.value;
            li.innerText = el.innerText;

            if (i === 0) {
                // First clickable option
                this.current = document.createElement("div");
                this.current.innerText = el.innerText;
                this.dropdown.appendChild(this.current);
                this.valueInput.value = el.value;
                li.classList.add("selected");
            }

            this.ul.appendChild(li);
        });

        this.dropdown.appendChild(this.ul);
        this.dropdown.appendChild(this.valueInput);
        this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
        this.dropdown.addEventListener("click", e => {
            const target = e.target;
            this.dropdown.classList.toggle("selecting");

            // Save new value only when clicked on li
            if (target.tagName === "LI") {
                this.valueInput.value = target.dataset.value;
                this.current.innerText = target.innerText;
            }
        });
    }
}

document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
});

/**
 * Hide elements when clicked on document
 */
document.addEventListener("click", function (e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
        return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
        return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
        el.classList.remove("selecting");
    });
});

/**
 * Switching between form steps
 */
class FormSteps {
    constructor(form) {
        this.$form = form;
        this.$next = form.querySelectorAll(".next-step");
        this.$prev = form.querySelectorAll(".prev-step");
        this.$step = form.querySelector(".form--steps-counter span");
        this.currentStep = 1;

        this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
        const $stepForms = form.querySelectorAll("form > div");
        this.slides = [...this.$stepInstructions, ...$stepForms];

        this.init();
    }

    /**
     * Init all methods
     */
    init() {
        this.events();
        this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
        // Next step
        this.$next.forEach(btn => {
            btn.addEventListener("click", e => {
                e.preventDefault();
                this.currentStep++;
                this.updateForm();
            });
        });

        // Previous step
        this.$prev.forEach(btn => {
            btn.addEventListener("click", e => {
                e.preventDefault();
                this.currentStep--;
                this.updateForm();
            });
        });

        // Form submit
        this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
        this.$step.innerText = this.currentStep;

        // TODO: Validation

        this.slides.forEach(slide => {
            slide.classList.remove("active");

            if (slide.dataset.step == this.currentStep) {
                slide.classList.add("active");
            }
        });

        this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
        this.$step.parentElement.hidden = this.currentStep >= 6;

        // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
        e.preventDefault();
        this.currentStep++;
        this.updateForm();
    }
}

const form = document.querySelector(".form--steps");
if (form !== null) {
    new FormSteps(form);
}


/** console log checkbox values */
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

class FormDetails {
    constructor() {
        this.bagCount = 0;
        this.organizationId = null;
        this.organizationName = null;
        this.userStreet = null;
        this.userCity = null;
        this.userPostCode = null;
        this.userPhone = null;
        this.userDate = null;
        this.userTime = null;
        this.userPickUpComment = null;
    }

    setBagCount(bagCount) {
        this.bagCount = bagCount;
    }

    setOrganization(idx, name) {
        this.organizationId = idx;
        this.organizationName = name;
    }

    setUserDetails(userStreet, userCity, userPostCode, userPhone, userDate, userTime, userPickUpComment) {
        this.userStreet = userStreet;
        this.userCity = userCity;
        this.userPostCode = userPostCode;
        this.userPhone = userPhone;
        this.userDate = userDate;
        this.userTime = userTime;
        this.userPickUpComment = userPickUpComment;
    }

    resetForm(stage) {
        if (stage === 'bagCount') {
            this.bagCount = 0;
        } else if (stage === 'organization') {
            this.organization = null;
        } else if (stage === 'userDetails') {
            this.userStreet = null;
            this.userCity = null;
            this.userPostCode = null;
            this.userPhone = null;
            this.userDate = null;
            this.userTime = null;
            this.userPickUpComment = null;
        }
    }
}

let donationFormDetails = new FormDetails();


btnStageTwo = document.querySelector('.btn.next-step.stage-2');
btnStageTwo.addEventListener('click', function (e) {
    e.preventDefault();
    let bagCount = document.querySelector('[name="bags"]').value;
    donationFormDetails.setBagCount(bagCount);
});


btnStageFour = document.querySelector('.btn.next-step.stage-4');
btnStageFour.addEventListener('click', function (e) {
    e.preventDefault();
    let organization = document.querySelectorAll('.institution');
    organization.forEach((el) => {
        let radioButton = el.querySelector('[type="radio"]');
        if (radioButton.checked) {
            donationFormDetails.setOrganization(radioButton.getAttribute('data-institution-id'), radioButton.getAttribute('data-institution-name'));
        }
    });
});


function summaryDetails() {
    let summaryBagCount = document.querySelector('#bags');
    let summaryOrganization = document.querySelector('#organization');
    let summaryAddress = document.querySelector('#address');
    let summaryCity = document.querySelector('#city');
    let summaryPostCode = document.querySelector('#post-code');
    let summaryPhone = document.querySelector('#phone');
    let summaryDate = document.querySelector('#date');
    let summaryTime = document.querySelector('#hour');
    let summaryComment = document.querySelector('#more_info');

    summaryBagCount.innerText = `${donationFormDetails.bagCount} worki!`;
    summaryOrganization.innerText = `Dla fundacji: "${donationFormDetails.organizationName}"!`;
    summaryAddress.innerText = donationFormDetails.userStreet;
    summaryCity.innerText = donationFormDetails.userCity;
    summaryPostCode.innerText = donationFormDetails.userPostCode;
    summaryPhone.innerText = donationFormDetails.userPhone;
    summaryDate.innerText = donationFormDetails.userDate;
    summaryTime.innerText = donationFormDetails.userTime;
    summaryComment.innerText = donationFormDetails.userPickUpComment;
};


btnStageFive = document.querySelector('.btn.next-step.stage-5');
btnStageFive.addEventListener('click', function (e) {
    e.preventDefault();
    let userStreet = document.querySelector('[name="address"]').value;
    let userCity = document.querySelector('[name="city"]').value;
    let userPostCode = document.querySelector('[name="postcode"]').value;
    let userPhone = document.querySelector('[name="phone"]').value;
    let userDate = document.querySelector('[name="data"]').value;
    let userTime = document.querySelector('[name="time"]').value;
    let userPickUpComment = document.querySelector('[name="more_info"]').value;

    donationFormDetails.setUserDetails(userStreet, userCity, userPostCode, userPhone, userDate, userTime, userPickUpComment);
    summaryDetails();
});

function getCookie(name){
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

btnStageSix = document.querySelector('.btn.stage-6');
btnStageSix.addEventListener('click', function (e) {
    e.preventDefault();
    fetch('http://127.0.0.1:8000/donation/', {
        method: 'POST',
        headers: {"X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify(donationFormDetails)
    }).then((response) => {
        console.log('success');
        console.log(response.status);

        if (response.status === 200) {
            window.location.replace("/donation/confirmation/");
        }

    })
});
