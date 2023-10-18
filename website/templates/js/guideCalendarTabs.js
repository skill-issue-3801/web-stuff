function showTab(event, tabName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("calendar-type");

    // Changed all calendar content to none to reset 
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }

    // Get's the tab nav link elements
    guideTabLinks = document.getElementsByClassName("guideTab");
    // Removes the underline class from all tab nav links
    for (i = 0; i < x.length; i++) {
        guideTabLinks[i].className = guideTabLinks[i].className.replace(" guideTabLinksSelectedBorder", "");
    }
    // Displays the correct tab and add's an underline to the tab nav link
    document.getElementById(tabName).style.display = "block";
    event.currentTarget.firstElementChild.className += " guideTabLinksSelectedBorder";
  }