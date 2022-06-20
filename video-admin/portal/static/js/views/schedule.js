const oneDayContainer = document.getElementById("oneDayContainer")
const repeatDaysContainer = document.getElementById("repeatDaysContainer")

const displayRepeatDays = (element) => {
    if (element.checked) {
        oneDayContainer.style.setProperty("display", "none")
        repeatDaysContainer.style.setProperty("display", "block")
    } else {
        oneDayContainer.style.setProperty("display", "block")
        repeatDaysContainer.style.setProperty("display", "none")
    }
}
const createSchedule = (event, form) => {
    event.preventDefault();
    const body = new FormData(form)
    var object = {
        "name": body.get("name"),
        "color": body.get("color"),
        "start": body.get("start"),
        "end": body.get("end"),
        "repeat": body.get("repeat") == null ? false : true,
        "date": body.get("date"),
        "days": body.getAll("days")
    };
    console.log(object)
    return
    fetch(form.action, {
            method: 'post',
            headers: {
                'accepts': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(object)
        })
        .then((response) => response.json())
        .then((data) => {
            debugger
            window.location.reload()
        });
}