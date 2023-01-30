import { API_URL } from "../index.js";

let pageSize = 2;
let currentPage = 1;
var data, table;
let rowIndex = 0;

if(currentPage === 1){
  document.getElementById("prevButton").style.visibility = "hidden";
}

document.querySelector('#nextButton').addEventListener('click', nextPage, false);
document.querySelector('#prevButton').addEventListener('click', previousPage, false);

export function loadLeaderboard() {
  table = document.querySelector('#usersTable tbody');
  let result = '';
  var pageOffset = (currentPage-1)*pageSize;
  let rowIndex = pageOffset + 1;

  fetch(`${API_URL}high_scores?` + new URLSearchParams({
    page_size: pageSize,
    page_offset: pageOffset,
  }))
  .then((response) => response.json())
  .then(async (responseData) => {    
    data = responseData;
    data.scores.forEach(userScore => {
      result += `<tr>
        <td>${rowIndex++}</td>
        <td>${userScore.user_name}</td>
        <td>${userScore.score}</td>
      </tr>`
      table.innerHTML = result;
    });
    var nextPageResultSize = await getResultSize(currentPage + 1);
    console.log("Next page result size: " + nextPageResultSize);
    if(data.scores.length < pageSize) {
      document.getElementById("nextButton").style.visibility = "hidden";
    } else {
      document.getElementById("nextButton").style.visibility = "visible";
    }
  });
}

function nextPage() {
  currentPage = currentPage + 1;
  loadLeaderboard();
  document.getElementById("prevButton").style.visibility = "visible";
}

function previousPage() {
  currentPage--;
  if(currentPage === 1){
    document.getElementById("prevButton").style.visibility = "hidden";
  }
  loadLeaderboard();
}

async function getResultSize(page) {

  var pageOffset = (page-1)*pageSize;

  fetch(`${API_URL}high_scores?` + new URLSearchParams({
    page_size: pageSize,
    page_offset: pageOffset,
  }))
  .then((response) => response.json())
  .then((responseData) => {
    console.log("FUNCTION RESULT: " + responseData.scores.length);
    return responseData.scores.length;
  });
  return 0;
}