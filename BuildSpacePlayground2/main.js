let trackInput = document.getElementById('trackInput');
let submitButton = document.getElementById('submitButton');
submitButton.onclick = searchTracks(); 
function searchTracks() {
let searchResults = trackInput.value;
//var fetchApi;
//console.log(fetchApi);
fetch('https://api.soundcloud.com/tracks/?client_id=86b6a66bb2d863f5d64dd8a91cd8de94&q=' + searchResults).then(function(response) {
if (response.status = 200) {
console.log('Looks like there was a problem. Status Code' + response.status);
return;
}
response.json().then(function(data) {
let track = data;
console.log(track);
let searchedFor= document.createElement('div');
searchedFor.id='searchedFor';
document.body.appendChild(searchedFor);
document.getElementById('searched').appendChild(searchedFor); searchedFor.className = 'searchedFor';
searchedFor.innerHTML += "showing results for" +":"+ searchResults;
function renderTracks() {
return
$(track.map(track =>
`<div class="box">
<div class="blankImage"></div>
<div><img src="${track.artwork_url}"></img></div>
<div id="songTitle" class="title"><a href="">${track.title} </a></div>
</div>`
))}
let songTitleArray = [];
let songTitle = document.getElementById('songTitle');
for(var i=0;i<songTitleArray.length;i++)
{
    songTitleArray[i].addEventListener('click', function playSong(e){
        console.log(playSong);
    })
}
})})}
