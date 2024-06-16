
function save(){
    
}

// let mylead = ["www.hello.com","www.bye.com","www.okay.com"];

let list = [];
        const text = document.getElementById("text");
        const button = document.getElementById("search");
        const ulel = document.getElementById("ulel");
        const delbtn = document.getElementById("delete");

        // Load data from localStorage
        const leads = JSON.parse(localStorage.getItem("list"));

        if (leads) {
            list = leads;
            render();
        }

        delbtn.addEventListener("click", function() {
            localStorage.removeItem("list");
            list = [];
            render();
        });

        button.addEventListener("click", function() {
            list.push(text.value);
            saveToLocalStorage();
            text.value = "";
            render();
        });

        function render() {
            let res = "";
            for (let i = 0; i < list.length; i++) {
                res += `<li>${list[i]}</li>`;
            }
            ulel.innerHTML = res;
        }

        function saveToLocalStorage() {
            localStorage.setItem("list", JSON.stringify(list));
        }

// <a target='${list[i]}' href=" ${list[i]}">
//     ${list[i]}
// </a>

// button.addEventListener("click", function() {

//     // console.log(mylead);
//     for(let i=0;i<mylead.length;i++){
//         // ulel.innerHTML += "<li>" + mylead[i] + "</li>";

//         const li = document.createElement("li")
//         li.textContent = mylead[i]
//         ulel.append(li)
//     }    
// })