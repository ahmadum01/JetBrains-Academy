first_name_field = document.getElementById('first-name')
last_name_field = document.getElementById('last-name')
email_field = document.getElementById('email')
phone_field = document.getElementById('phone')
company_field = document.getElementById('company')
address_field = document.getElementById('address')
button = document.getElementById('submit-button')
sync_input()

first_name_field.addEventListener('input', function (){
    localStorage.setItem('first-name', first_name_field.value)
})

last_name_field.addEventListener('input', function (){
    localStorage.setItem('last-name', last_name_field.value)
})

email_field.addEventListener('input', function (){
    localStorage.setItem('email', email_field.value)
})

phone_field.addEventListener('input', function (){
    localStorage.setItem('phone', phone_field.value)
})

company_field.addEventListener('input', function (){
    localStorage.setItem('company', company_field.value)
})

address_field.addEventListener('input', function (){
    localStorage.setItem('address', address_field.value)
})

button.addEventListener('click', function (){
    let user = {
        'first-name': first_name_field.value,
        'last-name': last_name_field.value,
        'email': email_field.value,
        'phone': phone_field.value,
        'company': company_field.value,
        'address': address_field.value
    }
    let key = first_name_field.value + last_name_field.value + email_field.value

    localStorage.setItem(key, JSON.stringify(user))
    first_name_field.value = ""
    last_name_field.value = ""
    email_field.value = ""
    phone_field.value = ""
    company_field.value = ""
    address_field.value = ""
    localStorage.setItem('first-name', "")
    localStorage.setItem('last-name', "")
    localStorage.setItem('email', "")
    localStorage.setItem('phone', "")
    localStorage.setItem('company', "")
    localStorage.setItem('address', "")
})


function sync_input() {
    first_name_field.value = localStorage.getItem('first-name')
    last_name_field.value = localStorage.getItem('last-name')
    email_field.value = localStorage.getItem('email')
    phone_field.value = localStorage.getItem('phone')
    company_field.value = localStorage.getItem('company')
    address_field.value = localStorage.getItem('address')
}

setInterval(sync_input, 500)