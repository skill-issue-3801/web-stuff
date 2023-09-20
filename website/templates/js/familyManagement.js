function openForm() {
  document.getElementById("familyForm").style.display = "block";
  document.getElementById("form-button").style.display = "none";
}

function closeForm() {
  document.getElementById("familyForm").style.display = "none";
  document.getElementById("form-button").style.display = "block";
}

function openEditForm(personName, personEmail, personCaltype, personUrl, personIcon) {
  document.getElementById("editForm").style.display = "block";
  document.getElementById("form-button").style.display = "none";
  document.getElementById("editName").defaultValue = personName;
  document.getElementById("editEmail").defaultValue = personEmail;
  document.getElementById("editUrl").defaultValue = personUrl;
  document.getElementById(personCaltype).checked = true;
  document.getElementById("personName").value = personName;
}

function closeEditForm() {
  document.getElementById("editForm").style.display = "none";
  document.getElementById("form-button").style.display = "block";
}
