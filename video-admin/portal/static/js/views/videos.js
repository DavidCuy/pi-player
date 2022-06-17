const searchInput = document.getElementById("searchInput");
searchInput.addEventListener("keyup", ({ key }) => {
    const text = searchInput.value;
    console.log(text)
    if (key === "Enter") {
        const params = new URLSearchParams()

        if (params.has('search-video_file')) {
            params.delete('search-video_file')
        }
        params.append('search-video_file', `*/${text}*`)
        const newLocation = `${window.location.origin}${window.location.pathname}?${params.toString()}`
        window.location = newLocation
    }
})


document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search)

    if (params.has('search-video_file')) {
        let searchValue = params.get('search-video_file')
        searchValue = searchValue.replace('/', '')
        searchValue = searchValue.replaceAll('*', '')
        const searchInput = document.getElementById("searchInput")
        searchInput.value = searchValue
        searchInput.focus()
    }
})

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

const videoUploadModal = document.getElementById('videoUploadModal')
videoUploadModal.addEventListener('hidden.bs.modal', function() {
    window.location.reload()
})


const deleteVideo = (id) => {
    const url = `/video/${id}`
    fetch(url, {
            method: 'DELETE'
        })
        .then((response) => response.json())
        .then((json) => {
            console.log(json)
            window.location.reload()
        });
}