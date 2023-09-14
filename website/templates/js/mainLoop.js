async function update() {
    let response = await fetch("/calendar/do_update", {method: "POST"});
    let text = await response.text();
    console.log(text);
}

update()
