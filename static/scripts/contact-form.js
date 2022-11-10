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

class ContactForm {
    constructor() {
        this.userName = {'qs': "[name='name']", 'value': undefined, 'error': undefined};
        this.userEmail = {'qs': "[name='email']", 'value': undefined, 'error': undefined};
        this.userMessage = {'qs': "[name='message']", 'value': undefined, 'error': undefined};
    }

    setField() {
        this.userName.value = document.querySelector(this.userName.qs).value;
        this.userEmail.value = document.querySelector(this.userEmail.qs).value;
        this.userMessage.value = document.querySelector(this.userMessage.qs).value;
    }

    setError() {
        document.querySelector('h3').innerHTML = 'Dane są niepoprawne.';
    }

    afterSubmit() {
        let form = document.querySelector('.form--contact');
        form.remove();
    }

    sendForm() {
        fetch('/send/contact-form', {
            method: 'POST',
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            body: JSON.stringify(this)
        }).then((response) => {
            if (response.status === 400) {
                this.setError();
            } else {
                 document.querySelector('#err-text').innerHTML = 'Dziękujemy za wiadomość.';
                 document.querySelector('#info').innerHTML = '';
                 this.afterSubmit();
            }


        })
    };

}


let contactFormBtn = document.querySelector('.contact-form');
contactFormBtn.addEventListener('click', function (e) {
    e.preventDefault();
    let contactForm = new ContactForm();
    contactForm.setField();
    contactForm.sendForm();
});