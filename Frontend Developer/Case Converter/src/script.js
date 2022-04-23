upper_case_button = document.getElementById("upper-case")
lower_case_button = document.getElementById("lower-case")
proper_case_button = document.getElementById("proper-case")
sentence_case_button = document.getElementById("sentence-case")
save_text_button = document.getElementById("save-text-file")
text_box = document.querySelector("textarea")

upper_case_button.addEventListener('click', function (){
    text_box.value = text_box.value.toUpperCase()
})

lower_case_button.addEventListener('click', function (){
    text_box.value = text_box.value.toLowerCase()
})

proper_case_button.addEventListener('click', function (){
    let words = text_box.value.split(' ')
    for(let i = 0; i < words.length; i++){
        if (words[i].trim() === ""){
            words.splice(i, 1);
        }     
    }
    for(let i = 0; i < words.length; i++){
        words[i] = words[i][0].toUpperCase() + words[i].substring(1).toLowerCase()
    }
    text_box.value = words.join(" ")
})

sentence_case_button.addEventListener('click', function (){
    let sentences = text_box.value.split('.')
    for(let i = 0; i < sentences.length; i++){
        if (sentences[i].trim() === ""){
            sentences.splice(i, 1);
        }     
    }
    for(let i = 0; i < sentences.length; i++){
        sentences[i] = sentences[i].trim()
        sentences[i] = sentences[i][0].toUpperCase() + sentences[i].substring(1).toLowerCase()
    }
    text_box.value = sentences.join('. ') + '.'
})

save_text_button.addEventListener('click', function (){
        let element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text_box.value));
        element.setAttribute('download', 'text.txt');
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
})