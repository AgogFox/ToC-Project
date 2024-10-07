

export function fetchData(url) {
    fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => console.log(data))
        .catch((error) => console.error("Fetch error:", error));
    return data
}


