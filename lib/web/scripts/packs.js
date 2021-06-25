var packs
var sortBy = "name"
var allPacks

let main = () => {
    allPacks = document.getElementById("allPacks").cloneNode(true)

    console.log("main")
    /* Fill array of card elements */
    packs = Array.from(document.getElementsByClassName("pack-box"))

    /* Set event listeners for rarity and user checkboxes and radio*/
    let userFilterChecks = Array.from(document.getElementsByTagName("input"))
    for (userFilterCheck of userFilterChecks) {
        userFilterCheck.addEventListener("change", changeSort)
    }
}

let changeSort = event => {

    let sorted
    // Sort by card count
    if (sortBy == "name") {
        sortBy = "cards"
        sorted = packs.sort((a, b) => Number(b.dataset.cards) - Number(a.dataset.cards))
    }
    else /* if (sortBy == "cards") */ {
        sortBy = "name"
        sorted = packs.sort((a, b) => {
            if (a.dataset.name < b.dataset.name) { return -1 }
            if (a.dataset.name > b.dataset.name) { return 1 }
            return 0
        })
    }

    document.getElementsByClassName("main")[0].replaceChildren(allPacks, ...sorted)
}


let replaceSelf = (oldNode) => {
    console.log("replaceself")
    let newNode = oldNode.cloneNode(true)
    oldNode.parentNode.replaceChild(newNode, oldNode)
}

window.onload = main


