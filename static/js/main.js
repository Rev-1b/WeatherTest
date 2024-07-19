function padZero(number) {
    return number < 10 ? '0' + number : number;
}


function updateTime(element) {
    let currentTime = element.textContent.split(':');
    let hours = parseInt(currentTime[0], 10);
    let minutes = parseInt(currentTime[1], 10);
    let seconds = parseInt(currentTime[2], 10);

    seconds++;

    if (seconds >= 60) {
        seconds = 0;
        minutes++;
    }
    if (minutes >= 60) {
        minutes = 0;
        hours++;
    }
    if (hours >= 24) {
        hours = 0;
    }

    element.textContent = padZero(hours) + ':' + padZero(minutes) + ':' + padZero(seconds);
}

// Находим элемент с временем
let timeElement = document.getElementById('timer');

if (timeElement !== null) {
    setInterval(function () {
        updateTime(timeElement);
    }, 1000);
}
/*
-----------------------------------------------------------
*/

const cityInput = document.getElementById('city-input');
const suggestionsContainer = document.getElementById('suggestions-container');

async function fetchCities(query) {
    const token = '64fa0dc77175cb7e0e0ca71686db88f6bac3dce2';
    const url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address';
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Token ' + token
        },
        body: JSON.stringify({
            query: query,
            count: 5,
            from_bound: {value: "city"},
            to_bound: {value: "city"},
            locations: [{"city_type_full": "город"}]
        })
    };

    const response = await fetch(url, options);
    const data = await response.json();
    return data.suggestions.map(suggestion => suggestion.value);
}

async function updateSuggestions() {
    const query = cityInput.value.toLowerCase();
    suggestionsContainer.innerHTML = '';

    if (query.length > 0) {
        const suggestions = await fetchCities(query);
        suggestions.forEach(suggestion => {
            const suggestionElement = document.createElement('div');
            suggestionElement.className = 'autocomplete-suggestion';
            suggestionElement.textContent = suggestion;
            suggestionElement.onclick = () => {
                cityInput.value = cleanCityName(suggestion);
                suggestionsContainer.innerHTML = '';
            };
            suggestionsContainer.appendChild(suggestionElement);
        });
    }
}

cityInput.addEventListener('input', updateSuggestions);

document.addEventListener('click', (event) => {
    if (event.target !== cityInput && !suggestionsContainer.contains(event.target)) {
        suggestionsContainer.innerHTML = '';
    }
});

function cleanCityName(city) {
    return city.replace(/^(г\.?|пгт\.?)/i, '').trim();
}
