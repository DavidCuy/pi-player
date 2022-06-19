const newPlaylistVideosSelect = document.getElementById("newPlaylistVideosSelect")

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
            console.warn(data)
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
            console.log(json)
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
            console.log(json)
            window.location.reload()
        });
}