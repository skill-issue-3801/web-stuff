// Importing required libraries
const lineReader = require('line-reader');
  
// eachLine() method call on gfg.txt
// It got a callback function
// Printing content of file line by line
// on the console
let timeParentDiv = document.querySelector(".timeRows");

// let text = greeting.textContent;

//ELI YOU'RE HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERE V
var timeDivs = "";
var timeID ="id=";
lineReader.eachLine('times.txt', (timeLine, last) => {
    console.log(timeLine);
    timeID= timeID + timeLine;
    // Below should give <div style="grid-area:a00-00" id="timeId"> <p>timeLine</p></div>
    timeDivs= timeDivs + "<div style=\"grid-area:a00-00" + " id=" + "\"" + timeID + "\"" +"\">" + "<p>" + timeLine + "</p>" + "</div>";
    //reset timeID
    timeID = "id=";
});
document.getElementById("timeRows").innerHTML = timeDivs;


// grid-area: a00-00




//family management things
function deleteUser() {
    //delete a user from existence
    return;
}

function addUser() {
    //add a new user :)
    return;
}


function editUser() {
    //edit user
    return;
}
