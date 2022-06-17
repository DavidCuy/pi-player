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