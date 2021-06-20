var rarityFilters = 0x1F  // m l e r c  -> 0b11111 by default
var userFilters = {

}  // user(n) - user(n-1) - ... - user(1) - (no)owner -> 0b11...11 by default
// is filled in main
var cards
var sortNumber = true  // true is number

let main = () => {
    console.log("main")
    /* Fill array of card elements */
    cards = Array.from(document.getElementsByClassName("card-box"))

    /* Set event listeners for rarity and user checkboxes and radio*/
    let userFilterChecks = document.getElementsByTagName("input")
    for (userFilterCheck of userFilterChecks) {
        if (userFilterCheck.type === "checkbox") {
            userFilterCheck.addEventListener("change", applyFilter)
        }
        else if (userFilterCheck.type === "radio") {
            userFilterCheck.addEventListener("change", toggleOrder)
        }

        if (userFilterCheck.parentNode.parentNode.id === "user-form") {
            userFilters[userFilterCheck.parentNode.id] = true
        }
    }
}

let applyFilter = event => {
    console.log("applyfilter")
    console.log(event.target.parentNode.id)
    let ending = event.target.parentNode.id.split("-")[1]
    // Rarity
    if (["c", "r", "e", "l", "m"].includes(ending)) {
        if (rarityFilters === 0x1F && event.target.checked) {
            rarityFilters = 0x0
        }
        rarityFilters = rarityFilters ^ getFilterEquivalent(ending)
        if (rarityFilters === 0x0 && !event.target.checked) {
            rarityFilters = 0x1F
        }
        let allowedRarities = getLetters(rarityFilters)
        console.log(allowedRarities)
        showBasedOnRarity(allowedRarities)
    }
    // User
    else {
        if (areAll(userFilters, true) && event.target.checked) {
            toggleAll(userFilters)
        }
        userFilters["check-" + ending] = !userFilters["check-" + ending]
        console.log(userFilters)
        if (areAll(userFilters, false) && !event.target.checked) {
            toggleAll(userFilters)
        }
        showBasedOnUser(userFilters)
    }
}

let toggleOrder = event => {
    sortNumber = !sortNumber
    let sorted
    // Sort by id then by pack
    if (sortNumber) {
        sorted = cards.sort((a, b) => Number(a.dataset.id) - Number(b.dataset.id))
        sorted = sorted.sort((a, b) => {
            if (a.dataset.pack < b.dataset.pack) { return -1 }
            if (a.dataset.pack > b.dataset.pack) { return 1 }
            return 0
        })
    }
    // By value
    else {
        sorted = cards.sort((a, b) => Number(b.dataset.value) - Number(a.dataset.value))
    }

    document.getElementsByClassName("main")[0].replaceChildren(...sorted)
}

let getFilterEquivalent = letter => {
    console.log("getfilter")
    switch (letter) {
        case "c": return 0x1
        case "r": return 0x2
        case "e": return 0x4
        case "l": return 0x8
        case "m": return 0x10
    }
}

let getLetters = number => {
    console.log("letters")
    let letters = []
    if ((number & 0x1) != 0) { letters.push("c") }
    if ((number & 0x2) != 0) { letters.push("r") }
    if ((number & 0x4) != 0) { letters.push("e") }
    if ((number & 0x8) != 0) { letters.push("l") }
    if ((number & 0x10) != 0) { letters.push("m") }
    return letters
}

let areAll = (obj, bool) => {
    for (el in obj) {
        if (!(obj[el] == bool)) {
            return false
        }
    }
    return true
}

let toggleAll = obj => {
    for (el in obj) {
        obj[el] = !obj[el]
    }
}

let showBasedOnRarity = allowedRarities => {
    console.log("based")
    for (card of cards) {
        if (allowedRarities.includes(card.dataset.rarity)) {
            card.style.display = "flex"
            // replaceSelf(card)
        }
        else {
            card.style.display = "none"
        }
    }
}

let showBasedOnUser = allowedUsers => {
    console.log("userbased")
    for (card of cards) {
        let allowed = false
        for (el in allowedUsers) {
            if (allowedUsers[el] && el.endsWith(card.dataset.owner)) {
                allowed = true
                break
            }
        }

        if (allowed) {
            card.style.display = "flex"
            // replaceSelf(card)
        }
        else {
            card.style.display = "none"
        }
    }
}

let replaceSelf = (oldNode) => {
    console.log("replaceself")
    let newNode = oldNode.cloneNode(true)
    oldNode.parentNode.replaceChild(newNode, oldNode)
}

window.onload = main


