const oneDayContainer = document.getElementById("oneDayContainer")
const repeatDaysContainer = document.getElementById("repeatDaysContainer")
const newPlaylistSelect = document.getElementById("newPlaylistSelect")

document.addEventListener('DOMContentLoaded', () => {
    const url = `/playlist/?per_page=1000`
    fetch(url, {
            method: 'GET',
            headers: {
                'accepts': 'application/json'
            }
        })
        .then((response) => response.json())
        .then((json) => json.Data)
        .then((playlists) => playlists.map((p) => { return { id: p.id, name: p.name } }))
        .then((playlists) => {
            const playlistOptions = playlists.map((p) => new Option(p.name, p.id))
            playlistOptions.forEach((vopt) => {
                newPlaylistSelect.appendChild(vopt)
            })
        });
})

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
        "id_playlist": body.get("id_playlist"),
        "color": body.get("color"),
        "start": body.get("start"),
        "end": body.get("end"),
        "repeat": body.get("repeat") == null ? false : true,
        "date": body.get("date"),
        "days": body.getAll("days")
    };
    console.log(object)
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
            window.location.reload()
        });
}

const deleteSchedule = (id) => {
    const url = `/schedule/${id}`
    fetch(url, {
            method: 'DELETE'
        })
        .then((response) => response.json())
        .then((json) => {
            window.location.reload()
        });
}