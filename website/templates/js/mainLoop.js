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

function render(event) {
    people = "";
    for (const person of event['attendees']) {
        people += `<img class="icon" src="/templates/${person['icon']}">

        <p>${person['name']}</p>
        `;
    }
    
    constructed = `
    <div class="event" id="${event['uid']}" style="grid-area:r${event['rowstart']} / a${event['colstart']} / r${event['rowend']} / a${event['colend']}; background-color:aqua;">
    <h4>Summary: ${event['summary']}<h4>
    <p>Start: ${event['start']}</p>
    <p>End: ${event['end']}</p>
    <h5>Attendees:</h4>
    ${people}
    </div>
    `;
    document.getElementById("calendarGridMain").innerHTML += constructed;
}

async function update() {
    let response = await fetch("/calendar/do_update", {method: "POST"});
    let text = await response.json();
    console.log("UPDATING CALENDAR EVENTS:");
    console.log(text);

    // clear old events
    document.getElementById("calendarGridMain").innerHTML = "";

    // add new events
    for (const event of text) {
        render(event);
    }
}

async function main() {
    let resp = await fetch("/is_prod", { method: "POST" });
    let check = await resp.json();
    if (check) {
        console.log("Running in prod mode.");
        setInterval(update, 300000); // 300 seconds (5 minutes) for prod
    } else {
        console.log("Running in dev mode.");
        setInterval(update, 10000); // 10 seconds for dev
    }
}

main();
