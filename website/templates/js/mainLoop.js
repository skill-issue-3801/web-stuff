async function update() {
    let response = await fetch("/calendar/do_update", {method: "POST"});
    let text = await response.text();
    console.log(text);
}
async function updateTimeData () {
    const now = new Date();
    const day = now.toLocaleString('en-GB', {day: 'numeric'});
    switch (day % 10) {
        case 1:
            mod = "st";
        case 2:
            mod = "nd";
        case 3:
            mod = "rd";
        default:
            mod = "th";
    }
    const displayString = (
        now.toLocaleString('en-GB', {hour: 'numeric', minute: 'numeric', hour12: true }) + ", " + 
        now.toLocaleString('en-GB', {weekday: 'long'}) + " " + day + mod + " " +
        now.toLocaleString('en-GB', {month: 'long'}));
    document.getElementById("datetime").innerHTML = displayString;
}
setInterval(updateTimeData, 1000);
update()
