function addCart(food){

    alert(food + " added to cart.");

}

function searchFood(){

    let input=document.getElementById("searchFood").value.toUpperCase();

    let cards=document.getElementsByClassName("food-card");

    for(let i=0;i<cards.length;i++){

        let title=cards[i].getElementsByTagName("h4")[0];

        if(title.innerHTML.toUpperCase().indexOf(input)>-1){

            cards[i].parentElement.style.display="block";

        }else{

            cards[i].parentElement.style.display="none";

        }

    }

}

function filterFood(){

    alert("Category Filter will connect with MySQL in next step.");

}