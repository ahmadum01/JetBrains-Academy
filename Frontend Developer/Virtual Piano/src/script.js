keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'w', 'e', 't', 'y', 'u']

document.addEventListener('keydown', function (event){
    if (keys.includes(event.key)){
        console.log(`The '${event.key}' key is pressed.`)
        let sound = new Audio(`./sounds/${event.key.toUpperCase()}.mp3`)
        sound.play()
    }
    else{
        console.log("Нет такой клавиши")
    }
})