let content_div = document.createElement("div")
content_div.className = 'content'
let labels = ['First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Address']
let classes = ['card-first-name', 'card-last-name', 'card-email', 'card-phone', 'card-company', 'card-address']
let user_keys = ['first-name', 'last-name', 'email', 'phone', 'company', 'address']

function set_notes(a) {
    content_div.remove()
    content_div = document.createElement("div")
    content_div.className = 'content'

    let users = []
    for(let i = 0; i < localStorage.length; i++){
        let temp = localStorage.getItem(localStorage.key(i))
        if (! user_keys.includes(localStorage.key(i))) {
            users.push(JSON.parse(temp))
        }
    }

    for(let i = 0; i < users.length; i++){

        let block = document.createElement("div")
        block.className =
            block.className = "submit-history-card"
        for(let j = 0; j < 6; j++){
            let p_label = document.createElement('p')
            p_label.className = "label-text text"
            let p_data = document.createElement('p')
            p_data.className = classes[j] + " text"
            p_label.appendChild(document.createTextNode(labels[j]))
            p_data.appendChild(document.createTextNode(users[i][user_keys[j]]))
            block.append(p_label)
            block.append(p_data)
        }
        let form = document.createElement('form')
        let button = document.createElement('button')
        button.type = 'submit'
        button.className = 'delete-button'
        button.appendChild(document.createTextNode('Delete'))
        button.addEventListener('click', function (){
            let a = button.parentElement.parentElement.querySelector('.' + classes[0]).textContent
            let b = button.parentElement.parentElement.querySelector('.' + classes[1]).textContent
            let c = button.parentElement.parentElement.querySelector('.' + classes[2]).textContent
            localStorage.removeItem(a + b + c)
            button.parentElement.parentElement.remove()
        })
        form.append(button)
        block.append(form)
        content_div.append(block)
    }
    document.body.insertBefore(content_div, document.querySelector('script'))
}


set_notes()
setInterval(set_notes, 500)
