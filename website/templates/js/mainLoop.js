async function update() {
    let response = await fetch("/calendar/do_update", {method: "POST"});
    let text = await response.text();
    console.log(text);
}
async function updateTimeData () {
    const now = new Date();
    /* update co-ordinates for wave */
    hour = (now.getHours()).toString().padStart(2, '0');
    minutes = ((15 * (Math.floor(now.getMinutes()/15))).toString()).padStart(2, '0');
    coordinates = `r${hour}-${minutes} / cSunday / r${hour}-${minutes} / c-1`;
    document.getElementById("currentTime").style["gridArea"] = coordinates;

    /* now do date and time up top*/
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
