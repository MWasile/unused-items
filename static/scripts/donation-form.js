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

function getCookie(name) {
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

        if (response.status === 200) {
            window.location.replace("/donation/confirmation/");
        }

    })
});
