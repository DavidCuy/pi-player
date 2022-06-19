const newPlaylistVideosSelect = document.getElementById("newPlaylistVideosSelect")
const orderContainer = document.getElementById('orderContainer')

document.addEventListener('DOMContentLoaded', () => {
    const url = `/video/?per_page=100`
    fetch(url, {
            method: 'GET',
            headers: {
                'accepts': 'application/json'
            }
        })
        .then((response) => response.json())
        .then((json) => json.Data)
        .then((videos) => videos.map((v) => { return { id: v.id, name: v.video_file.split('/').slice(-1)[0] } }))
        .then((videos) => {
            const videoOptions = videos.map((v) => new Option(v.name, v.id))
            videoOptions.forEach((vopt) => {
                newPlaylistVideosSelect.appendChild(vopt)
            })
        });
})

const videoSelect = new SlimSelect({
    select: '#newPlaylistVideosSelect'
})

const createPlaylist = (event, form) => {
    event.preventDefault();
    const body = new FormData(form)
    var object = {
        "name": body.get("name"),
        "description": body.get("description"),
        "videos": body.getAll("videos")
    };
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

const updatePlayVideo = (id) => {
    const url = `/video/${id}`
    fetch(url, {
            method: 'GET'
        })
        .then((response) => response.json())
        .then((json) => {
            const video = document.getElementById('videoPlayer');
            let source = document.createElement('source');

            source.setAttribute('src', `http://${window.location.host}/static/${json.video_file}`);
            source.setAttribute('type', json.format);

            video.appendChild(source);
            video.load();
            video.play();

        });
}

const videoplayModal = document.getElementById('videoplayModal')
videoplayModal.addEventListener('hidden.bs.modal', function() {
    const video = document.getElementById('videoPlayer');
    video.pause();
    video.currentTime = 0
    video.innerHTML = ''
})

const deletePlaylist = (id) => {
    const url = `/playlist/${id}`
    fetch(url, {
            method: 'DELETE'
        })
        .then((response) => response.json())
        .then((json) => {
            window.location.reload()
        });
}

let orderList = null
let playlistId = null

const drawOrderCard = (item, position) => {
    const addIcon = document.createElement("i")
    addIcon.className = "material-icons"
    addIcon.innerHTML = "add"

    const spanAddIcon = document.createElement("span")
    spanAddIcon.className = "btn-inner--icon"
    spanAddIcon.appendChild(addIcon)

    const addBtn = document.createElement("button")
    addBtn.className = "btn btn-icon btn-2 btn-success btn-icon-only rounded-circle float-end float-right"
    addBtn.setAttribute("type", "button")
    addBtn.setAttribute("onclick", `addOrderItem(${position}, ${JSON.stringify(item)})`)
    addBtn.appendChild(spanAddIcon)

    const spanName = document.createElement("span")
    spanName.innerHTML = item.video_file.split('/').slice(-1)[0]

    const inputId = document.createElement("input")
    inputId.setAttribute("type", "hidden")
    inputId.setAttribute("name", "id")
    inputId.setAttribute("value", item.id)

    const inputPosition = document.createElement("input")
    inputPosition.setAttribute("type", "hidden")
    inputPosition.setAttribute("name", "position")
    inputPosition.setAttribute("value", position)

    const card = document.createElement("div")
    card.className = "card"
    card.appendChild(inputId)
    card.appendChild(inputPosition)
    card.appendChild(spanName)
    card.appendChild(addBtn)

    // Comprobacion de unico
    const videos = orderList.filter(v => v.id == item.id)
    if (videos.length > 1) {
        const deleteIcon = addIcon.cloneNode()
        deleteIcon.innerHTML = 'delete'
        const spanDeleteIcon = spanAddIcon.cloneNode()
        spanDeleteIcon.innerHTML = ''
        spanDeleteIcon.appendChild(deleteIcon)
        const deleteBtn = document.createElement("button")
        deleteBtn.className = "btn btn-icon btn-2 btn-danger btn-icon-only rounded-circle float-end float-right"
        deleteBtn.setAttribute("type", "button")
        deleteBtn.setAttribute("onclick", `removeOrderItem(${position - 1})`)
        deleteBtn.appendChild(spanDeleteIcon)

        card.appendChild(deleteBtn)
    }

    orderContainer.appendChild(card)

}

const addOrderItem = (index, video) => {
    if (index > -1) {
        orderList.splice(index, 0, video); // 2nd parameter means remove one item only
    }
    orderContainer.innerHTML = ''
    let counter = 1
    orderList.forEach(element => {
        drawOrderCard(element, counter++)
    })
}

const removeOrderItem = (index) => {
    if (index > -1) {
        orderList.splice(index, 1); // 2nd parameter means remove one item only
    }
    orderContainer.innerHTML = ''
    let counter = 1
    orderList.forEach(element => {
        drawOrderCard(element, counter++)
    })
}

const openOrderModal = (idPlaylist) => {
    const playlist = Playlists.find(p => p.id == idPlaylist)
    playlistId = idPlaylist
    if (playlist === null || playlist === undefined) {
        alert("Ocurrio un error al buscar playlist")
        return
    }
    fetch(`/static/${playlist.order_file}`)
        .then((response) => response.json())
        .then((data) => {
            orderList = data
            let index = 1;
            orderContainer.innerHTML = ''
            orderList.forEach(element => {
                drawOrderCard(element, index++)
            })
        })
}
dragula([orderContainer])
    .on('drop', function(el) {
        const idElement = el.querySelector("input[name='id']")
        const video = orderList.find(e => e.id == idElement.value)

        let counter = 1
        let backup_orderList = []
        for (let ch of orderContainer.children) {
            const positionElement = ch.querySelector("input[name='position']")
            const idElement = ch.querySelector("input[name='id']")

            const video = orderList.find(e => e.id == idElement.value)
            backup_orderList.push(video)
            positionElement.setAttribute("value", counter++)
        }
        orderList = JSON.parse(JSON.stringify(backup_orderList))
    });

const saveOrderFile = () => {
    const url = `/playlist/${playlistId}/order-file`
    fetch(url, {
            method: 'POST',
            headers: {
                'accepts': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderList)
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            debugger
            window.location.reload()
        });
}