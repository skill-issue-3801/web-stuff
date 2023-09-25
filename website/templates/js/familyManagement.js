function openForm() {
  document.getElementById("familyForm").style.display = "block";
  document.getElementById("form-button").style.display = "none";
}

function closeForm() {
  document.getElementById("familyForm").style.display = "none";
  document.getElementById("form-button").style.display = "block";
}

function openEditForm(personName, personEmail, personCaltype, personUrl, personIcon) {
  document.getElementById("edit_form").reset();
  document.getElementById("personName").value = personName;
  document.getElementById("editForm").style.display = "block";
  document.getElementById("form-button").style.display = "none";
  document.getElementById("editName").defaultValue = personName;
  if (personEmail != "None") {
    document.getElementById("editEmail").defaultValue = personEmail;
  }
  if (personUrl != "None") {
    document.getElementById("editUrl").defaultValue = personUrl;
  }
  if (personCaltype == 'google') {
    document.getElementById("editGoogle").checked = true;
  } else if (personCaltype == 'apple') {
    document.getElementById("editApple").checked = true;
  }
  document.getElementById("personName").value = personName;
  document.getElementById(personIcon).checked = true;
}

function closeEditForm() {
  document.getElementById("editForm").style.display = "none";
  document.getElementById("form-button").style.display = "block";
}

function updateRequirements(urlId, typeId) {
  var url = document.getElementById(urlId).value;
  if (url == null) {
    document.getElementById(typeId).removeAttribute("required"); 
  } else if (url == '') {
    document.getElementById(typeId).removeAttribute("required"); 
    document.getElementById("editApple").checked = false;
    document.getElementById("editGoogle").checked = false;
  } else {
    document.getElementById(typeId).setAttribute("required", ""); 
  }
}

function validateForm(whichForm) {
  var url = document.forms[whichForm]["link"].value;
  var type = document.forms[whichForm]["calendarType"].value;
  if (url == "") {
    var type = document.forms[whichForm]["calendarType"].value = "none"
  } 
  else if (type == 'apple' && (url.slice(0,42) != "webcal://p122-caldav.icloud.com/published/")) {
    alert("That is not a valid Apple calendar url, please use the guides to find your correct url")
  } 
  else if (type == 'google' && 
      ((url.slice(0, 42) != "https://calendar.google.com/calendar/ical/") || (url.slice(-10) != "/basic.ics"))) {
    alert("That is not a valid Google calendar url, please use the guides to find your correct url")
  }

  if (whichForm == "editForm") {
    var originalName = document.forms[whichForm]["personName"].value;
    var newName = document.forms[whichForm]["name"].value;
    if (originalName != newName) {
      alert("You have changed '" + originalName + "'s' name to '" + newName + "'. Be sure to update their name to '" + newName + "' anywhere they have been added by name in anybody else's calendar for them to appear in group events")
    }
  }
}

