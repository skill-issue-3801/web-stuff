async function updateTimeData () {
    const now = new Date();
    /* update co-ordinates for wave */
    hour = (now.getHours()).toString().padStart(2, '0');
    minutes = ((15 * (Math.floor(now.getMinutes()/15))).toString()).padStart(2, '0');
    coordinates = `r${hour}-${minutes} / cSunday / r${hour}-${minutes} / c-1`;
    document.getElementById("currentTime").style["gridArea"] = coordinates;

    document.getElementById("currentTime").scrollIntoView(true);

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
    <div class="event" id="${event['uid']}div" style="grid-area:r${event['rowstart']} / a${event['colstart']} / r${event['rowend']} / a${event['colend']};">
    <p id="eventHeading">${event['summary']}<p>
    <p>${event['start']} - ${event['end']}</p>
    ${people}
    </div>
    `;
    document.getElementById("calendarGridMain").innerHTML += constructed;
}

async function update() {
    let response = await fetch("/calendar/do_update", {method: "POST"});
    let text = await response.json();
    console.log("UPDATING CALENDAR EVENTS");

    // clear old events
    document.getElementById("calendarGridMain").innerHTML = `<div id = "currentTime" style = "grid-area: r00-00 / cSunday / r-00-00 / c-1;">~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</div>
                    <div class = "timeLabel" style = "grid-area: r00-00 / c00-00 / r01-00 / c00-00;"><p>12:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r01-00 / c00-00 / r02-00 / c00-00;"><p>1:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r02-00 / a00-00 / r03-00 / a00-00;"><p>2:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r03-00 / a00-00 / r04-00 / a00-00;"><p>3:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r04-00 / a00-00 / r05-00 / a00-00;"><p>4:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r05-00 / a00-00 / r06-00 / a00-00;"><p>5:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r06-00 / a00-00 / r07-00 / a00-00;"><p>6:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r07-00 / a00-00 / r08-00 / a00-00;"><p>7:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r08-00 / a00-00 / r09-00 / a00-00;"><p>8:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r09-00 / a00-00 / r10-00 / a00-00;"><p>9:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r10-00 / a00-00 / r11-00 / a00-00;"><p>10:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r11-00 / a00-00 / r12-00 / a00-00;"><p>11:00 AM</p></div>
                    <div class = "timeLabel" style = "grid-area: r12-00 / c00-00 / r13-00 / c00-00;"><p>12:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r13-00 / c00-00 / r14-00 / c00-00;"><p>1:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r14-00 / a00-00 / r15-00 / a00-00;"><p>2:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r15-00 / a00-00 / r16-00 / a00-00;"><p>3:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r16-00 / a00-00 / r17-00 / a00-00;"><p>4:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r17-00 / a00-00 / r18-00 / a00-00;"><p>5:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r18-00 / a00-00 / r19-00 / a00-00;"><p>6:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r19-00 / a00-00 / r20-00 / a00-00;"><p>7:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r20-00 / a00-00 / r21-00 / a00-00;"><p>8:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r21-00 / a00-00 / r22-00 / a00-00;"><p>9:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r22-00 / a00-00 / r23-00 / a00-00;"><p>10:00 PM</p></div>
                    <div class = "timeLabel" style = "grid-area: r23-00 / a00-00 / r-1 / a00-00;"><p>11:00 PM</p></div>
                    `;

    // add new events
    for (const event of text) {
        render(event);
    }
    
    // generate "current time" wave
    updateTimeData();
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
    update();
}

main();
