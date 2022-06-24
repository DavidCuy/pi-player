const videoPlayer = document.getElementById("pivideo")
let video_order = 0
let video_source = null

const formatDatetime = (date) => {
    return `${date.getFullYear().toString().padStart(4, '0')}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const update_url = () => {
    const qParams = new URLSearchParams({
        order: video_order,
    })
    let newurl = `${window.location.protocol}//${window.location.host}${window.location.pathname}?${qParams}`
    window.history.pushState({ path: newurl }, '', newurl)
}

const draw_source_video = (video_url, format = 'vide/mp4') => {
    videoPlayer.innerHTML = ''
    const source = document.createElement('source')
    source.setAttribute('src', video_url)
    source.setAttribute('type', format)

    videoPlayer.appendChild(source)
    videoPlayer.load()
    videoPlayer.play()
}

const fetchVideo = () => {
    const qParams = new URLSearchParams({
        current_datetime: formatDatetime(new Date()),
        current_order: video_order,
    })
    const url = `http://localhost:5000/schedule/current_video?${qParams}`
    fetch(url, {
            method: 'GET',
            headers: {
                'accepts': 'application/json'
            }
        })
        .then((response) => response.json())
        .then((dataVideo) => {
            update_url()
            video_order = dataVideo.order
            video_source = `http://localhost:5000/static/${dataVideo.video_file}`

            draw_source_video(video_source, dataVideo.format)
        }).catch((err) => {
            console.error(err)
            video_source = `http://localhost/unavailable.mp4`
            draw_source_video(video_source)
        })
}

document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search)
    const order_query = params.get('order')
    if (order_query == null) {
        update_url()
    } else {
        video_order = parseInt(order_query)
    }
    fetchVideo()
})

videoPlayer.onended = () => {
    fetchVideo()
};