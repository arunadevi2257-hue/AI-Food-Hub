function addCart(food) {
    alert(food + " added to cart.");
}

function searchFood() {

    let input = document.getElementById("searchFood").value.toUpperCase();
    let cards = document.getElementsByClassName("food-card");

    for (let i = 0; i < cards.length; i++) {

        let title = cards[i].getElementsByTagName("h4")[0];

        if (title.innerHTML.toUpperCase().indexOf(input) > -1) {
            cards[i].parentElement.style.display = "";
        } else {
            cards[i].parentElement.style.display = "none";
        }
    }
}

function filterFood() {

    let filter = document.getElementById("categoryFilter").value.toUpperCase();
    let cards = document.getElementsByClassName("food-card");

    for (let i = 0; i < cards.length; i++) {

        let text = cards[i].innerText.toUpperCase();

        if (filter === "ALL" || text.indexOf(filter) > -1) {
            cards[i].parentElement.style.display = "";
        } else {
            cards[i].parentElement.style.display = "none";
        }
    }
}