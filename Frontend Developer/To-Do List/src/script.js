let add_task_button = document.getElementById("add-task-button")
let task_input = document.getElementById("input-task")
let ul = document.getElementById("task-list")


function add_task(task_text, is_checked=false){
    let li = document.createElement('li')
    let input = document.createElement('input')
    input.type = "checkbox"
    input.checked = is_checked


    let span = document.createElement('span')
    span.className = is_checked? "task checked" : "task"
    span.appendChild(document.createTextNode(task_text))
    let button = document.createElement('button')
    button.appendChild(document.createTextNode("X"))
    button.className = "delete-btn"

    li.append(input)
    li.append(span)
    li.append(button)
    ul.append(li)
    task_input.value = ""


    input.addEventListener('click', () => {
        console.log(input.checked)
        if (input.checked){
            span.classList.add('checked')
        }
        else{
            span.classList.remove('checked')
        }
        save_current_tasks()
    })

    button.addEventListener('click', () => {
        button.parentElement.remove()
        save_current_tasks()
    })
}

add_task_button.addEventListener('click', () => {
    add_task(task_input.value)
    save_current_tasks()
})

function save_current_tasks(){
    let task_list = []
    for(let task of ul.children){
        task_list.push([task.children[0].checked, task.children[1].innerHTML])
    }
    localStorage.setItem("tasks", JSON.stringify(task_list))
}


for(let task of JSON.parse(localStorage.getItem("tasks")) || []){
    add_task(task[1], task[0])

}