const videoPlayer = document.getElementById("pivideo")

const fetchVideo = () => {
    const cur_datetime = new Date()
    const url = `http://localhost:5000/static/order_files/1.json`
    fetch(url, {
            method: 'GET',
            headers: {
                'accepts': 'application/json'
            }
        })
        .then((response) => response.json())
        .then((json) => console.log(json))
}

document.addEventListener('DOMContentLoaded', () => {
    const url = `http://localhost:5000/static/order_files/1.json`
    fetch(url, {
            method: 'GET',
            headers: {
                'accepts': 'application/json'
            }
        })
        .then((response) => response.json())
        .then((json) => console.log(json))
})

videoPlayer.onended = () => {
    alert("The video has ended");
};