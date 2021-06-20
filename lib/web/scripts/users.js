var users
var sortBy = "cards"

let main = () => {
    console.log("main")
    /* Fill array of card elements */
    users = Array.from(document.getElementsByClassName("user-box"))

    /* Set event listeners for rarity and user checkboxes and radio*/
    let userFilterChecks = Array.from(document.getElementsByTagName("input"))
    for (userFilterCheck of userFilterChecks) {
        userFilterCheck.addEventListener("change", changeSort)
    }
}

let changeSort = event => {
    
    sortBy = event.target.parentNode.id.split("-")[1]

    let sorted
    // Sort by id
    if (sortBy == "cards") {
        sorted = users.sort((a, b) => Number(b.dataset.cards) - Number(a.dataset.cards))
    }
    else if (sortBy == "balance") {
        sorted = users.sort((a, b) => Number(b.dataset.balance) - Number(a.dataset.balance))
    }
    else {
        sorted = users.sort((a, b) => Number(b.dataset.level) - Number(a.dataset.level))
    }

    document.getElementsByClassName("main")[0].replaceChildren(...sorted)
}


let replaceSelf = (oldNode) => {
    console.log("replaceself")
    let newNode = oldNode.cloneNode(true)
    oldNode.parentNode.replaceChild(newNode, oldNode)
}

window.onload = main


