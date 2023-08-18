let messageDiv = document.getElementById("removable-message")
let closeMessageX = document.getElementById("close-message")

function closeMessage(){
    messageDiv.remove()
}

closeMessageX.addEventListener("click", closeMessage)
