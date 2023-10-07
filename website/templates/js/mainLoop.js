let latestJson = "";
let userBrightnessArray = ['default-5', 'default-4', 'default-3', 'default-2', 'default-1', 'default', 'default1', 'default2', 'default3','default4', 'default5'];

var inactiveTimeout;
var screensaver_active = false;
var idletime = 10;

document.onkeypress = function () {
    //console.log("you pressed something!!");
    detectedSomething();
}

document.onmousemove = function() {
    //console.log("you moved your mouse!");
    detectedSomething();
}

function detectedSomething() {
    clearTimeout(inactiveTimeout);
    if (screensaver_active) {
        stop_screensaver();
    }
    inactiveTimeout = setTimeout(show_screensaver, 1000 * idletime);
}

// show screensaver function
function show_screensaver(){
    document.getElementById('screensaver').style.display = "block";
    screensaver_active = true;
    //reset to defaults
    deselectUsers();
    resetHighlighted();
    document.getElementById("selectedUserBrightness").value = "default";
}

// stop screensaver
function stop_screensaver(){
    document.getElementById('screensaver').style.display = "none";
    screensaver_active = false;
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}


function updateWaterBackground() {
    // day and night version of water background, inspired by https://wordpress.stackexchange.com/questions/375122/change-background-image-based-on-the-hour
    if (document.getElementById("waterBackgroundVideo") != null) {
        //change background of #waterBackgroundVideo to fit time of day
        var d = new Date();
        var n = d.getHours();
        if (n >= 20 || n <= 6) {
            // Between 8pm and 6am, apply night class to #waterBackgroundVideo
            document.getElementById("waterBackgroundVideo").className = "waterBackgroundNight";
        } else {
            // Else apply day class to #waterBackgroundVideo
            document.getElementById("waterBackgroundVideo").className = "waterBackgroundDay";
        }

    }
}


async function updateTimeData() {
    const now = new Date();
    /* update co-ordinates for wave */
    hour = (now.getHours()).toString().padStart(2, '0');
    minutes = ((15 * (Math.floor(now.getMinutes() / 15))).toString()).padStart(2, '0');
    coordinates = `r${hour}-${minutes} / cSunday / r${hour}-${minutes} / c-1`;
    document.getElementById("currentTime").style["gridArea"] = coordinates;

    document.getElementById("currentTime").scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });

    /* now do date and time up top*/
    const day = now.toLocaleString('en-GB', { day: 'numeric' });
    switch (day % 10) {
        case 1:
            mod = "st";
            break;
        case 2:
            mod = "nd";
            break;
        case 3:
            mod = "rd";
            break;
        default:
            mod = "th";
    }
    const displayString = (
        now.toLocaleString('en-GB', { hour: 'numeric', minute: 'numeric', hour12: true }) + ", " +
        now.toLocaleString('en-GB', { weekday: 'long' }) + " " + day + mod + " " +
        now.toLocaleString('en-GB', { month: 'long' }));
    document.getElementById("datetime").innerHTML = displayString;

    updateWaterBackground();
    
    const days = document.getElementsByClassName("todayHeader");
    for (var i = 0; i < days.length; i++) {
        days[i].classList.add("todayHeader");
    }
    document.getElementById(now.toLocaleString('en-GB', {weekday: 'long'})).classList.add("todayHeader");
}

function changeWeek(thisWeekIndex, direction, numWeeks, datesArray) {
    datesArray.replaceAll("\'", "\"");
    datesArray = Array.from(JSON.parse(datesArray));
    const currentViewingWeek = parseInt(document.getElementById("currentWeekViewing").value);
    if (direction == 0) {
        document.getElementById("currentWeekViewing").value = thisWeekIndex;
        putWeeksEvents(thisWeekIndex, datesArray);
        document.getElementById("weeksAgoAheadFlag").innerHTML = flagString(thisWeekIndex, thisWeekIndex);
    } else if (direction == -1 && currentViewingWeek > 0) {
        document.getElementById("currentWeekViewing").value = currentViewingWeek - 1;
        putWeeksEvents(currentViewingWeek - 1, datesArray);
        document.getElementById("weeksAgoAheadFlag").innerHTML = flagString(thisWeekIndex, currentViewingWeek - 1);
    } else if (direction == 1 && currentViewingWeek < numWeeks - 1) {
        document.getElementById("currentWeekViewing").value = currentViewingWeek + 1;
        putWeeksEvents(currentViewingWeek + 1, datesArray);
        document.getElementById("weeksAgoAheadFlag").innerHTML = flagString(thisWeekIndex, currentViewingWeek + 1);;
    }
}

function flagString(thisWeekIndex, viewingWeek) {
    if (viewingWeek == thisWeekIndex) {
        document.getElementById("weeksAgoAheadFlag").style.display = "none";
        return ("");
    }
    const diff = thisWeekIndex - viewingWeek;
    var fs = "";
    fs += Math.abs(diff);
    if (Math.abs(diff) == 1) {
        fs += " week";
    } else {
        fs += " weeks";
    }
    if (diff < 0) {
        fs += " ahead";
    } else {
        fs += " ago";
    }
    document.getElementById("weeksAgoAheadFlag").style.display = "block";
    return (fs);
}

function dayHeadingDates(datesArray) {
    document.getElementById("sundayDate").innerHTML = datesArray[0];
    document.getElementById("mondayDate").innerHTML = datesArray[1];
    document.getElementById("tuesdayDate").innerHTML = datesArray[2];
    document.getElementById("wednesdayDate").innerHTML = datesArray[3];
    document.getElementById("thursdayDate").innerHTML = datesArray[4];
    document.getElementById("fridayDate").innerHTML = datesArray[5];
    document.getElementById("saturdayDate").innerHTML = datesArray[6];
}

async function putWeeksEvents(viewingWeek, datesArray) {
    writeTimeLabels();
    while (latestJson == "") {
        // just wait until update has called once, its easier this way
        await delay(1000);
    }
    // add new events
    for (const event of latestJson[viewingWeek]) {
        render(event);
    }
    // find who is highlighted right now and click their button to highlight them
    const highlightedPerson = document.getElementById("currentlyHighlighted").value;
    document.getElementById(highlightedPerson).click();

    dayHeadingDates(datesArray[viewingWeek]);
    // generate "current time" wave
    updateTimeData();
}

function uidSelect(name) {
    console.log("clicked " + name);
    resetHighlighted();
    highlightEvents();
}

function highlightEvents() {
    console.log("highight events");
    var people = document.getElementsByClassName("userSelectRadio");
    const current = document.getElementById("selectedUserBrightness").value;
    for (var i = 0; i < people.length; i++) {
        if (people[i].checked) {
            var uids = (people[i].value).replaceAll("\'","\"");
            uids = Array.from(JSON.parse(uids));
            for (const uid of uids) {
                var evs = document.getElementsByClassName(uid);
                for (var j = 0; j < evs.length; j++) {
                    evs[j].classList.add("highlightedEvent");
                    evs[j].classList.add(current);
                }
            }
        }
    }   
}

function deselectUsers() {
    console.log("deselect users");
    var users = document.getElementsByClassName("userSelectRadio");
    for (var i = 0; i < users.length; i++) {
        users[i].checked = false;
    }
}

function resetHighlighted() {
    console.log("reset highlighted");
    var elements = document.getElementsByClassName("event");
    const current = document.getElementById("selectedUserBrightness").value;
    for (var i = 0; i < elements.length; i++) {
        elements[i].classList.remove("highlightedEvent");
        elements[i].classList.remove(current);
        elements[i].classList.add("default");
    }
}

function userBrightnessChange(delta) {
    const current = document.getElementById("selectedUserBrightness").value;
    console.log("current: " + current);
    if (!(delta == -1 && current == 'default-5') && !(delta == 1 && current == 'default5')) {
        const highlighted = document.getElementsByClassName("highlightedEvent");
        const newSetting = userBrightnessArray[(userBrightnessArray.indexOf(current) + delta)];
        console.log("new: " + newSetting);
        for (var i = 0; i < highlighted.length; i++) {
            highlighted[i].classList.remove(current);
            highlighted[i].classList.add(newSetting);
        }
        document.getElementById("selectedUserBrightness").value = newSetting;
    }
}

function render(event) {
    people = "";
    if (event['short']) {
        people += `<p>`;
        let first = true;
        for (const person of event['attendees']) {
            if (first) {
                first = false;
            } else {
                people += `, `;
            }
            people += `${person['name']}`;
        }
        people += `</p>`;
    } else {
        for (const person of event['attendees']) {
            people += `<div class="personWrapper"><img class="icon" src="/templates/${person['icon']}"><p>${person['name']}</p></div>`;
        }
    }

    stEventHrs = Number(event['start'].split(':')[0]);
    stEventMin = event['start'].split(':')[1];
    ndEventHrs = Number(event['end'].split(':')[0]);
    ndEventMin = event['end'].split(':')[1];

    stEventAMPM = stEventHrs >= 12 ? 'AM' : 'PM';
    ndEventAMPM = ndEventHrs >= 12 ? 'AM' : 'PM';
    stEventHrs = (stEventHrs % 12) ? (stEventHrs % 12) : 0;
    ndEventHrs = (ndEventHrs % 12) ? (ndEventHrs % 12) : 0;

    constructed = `
    <div class="event ${event['uid']}" style="grid-area:r${event['rowstart']} / a${event['colstart']} / r${event['rowend']} / a${event['colend']};">
    <p id="eventHeading">${event['summary']}<p>
    <p>${stEventHrs}:${stEventMin} ${stEventAMPM} - ${ndEventHrs}:${ndEventMin} ${ndEventAMPM}</p>
    <div class="eventAttendees">
        ${people}
    </div>
    </div>
    `;
    document.getElementById("calendarGridMain").innerHTML += constructed;
}

function writeTimeLabels() {
    document.getElementById("calendarGridMain").innerHTML = `<div id = "currentTime"></div>
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
}
function dimCalendarView(value) {
    if (value == 0) {
        document.getElementsByClassName("dimmingContent")[0].style.opacity = "0";
    } else {
        // Set given value to a float
        let dimValue = parseFloat(value);
        // Get current opacity
        let currentDimOpacity = document.getElementsByClassName("dimmingContent")[0].style.opacity;
        document.getElementsByClassName("dimmingContent")[0].style.opacity = dimValue;

        // Get the current opacity and turn it into a float
        let currentDimOpacityFloat = parseFloat(currentDimOpacity);
        // Add floats together
        let newDimOpacity = dimValue + currentDimOpacityFloat;
        // Ensuring it doesn't exceed 0 or 1 for opacity.
        if (newDimOpacity >= 1) {
            document.getElementsByClassName("dimmingContent")[0].style.opacity = "1";
        }
        else if (newDimOpacity <= 0) {
            document.getElementsByClassName("dimmingContent")[0].style.opacity = "0";
        } else {
            // Change opacity and change it to a string
            document.getElementsByClassName("dimmingContent")[0].style.opacity = newDimOpacity.toString();
        }
    }
}

async function update() {
    let response = await fetch("/calendar/do_update", { method: "POST" });
    let text = await response.json();
    console.log("UPDATING CALENDAR EVENTS");

    writeTimeLabels();

    const viewingWeek = document.getElementById("currentWeekViewing").value;
    // add new events
    for (const event of text[viewingWeek]) {
        render(event);
    }

    highlightEvents();
    

    updateTimeData();
    latestJson = text;
}

async function main() {
    let resp = await fetch("/is_prod", { method: "POST" });
    let check = await resp.json();
    if (check) {
        console.log("Running in prod mode.");
        setInterval(update, 300000); // 300 seconds (5 minutes) for prod
    } else {
        console.log("Running in dev mode.");
        setInterval(update, 300000); // 10 seconds for dev
    }
    update();
}

main();
