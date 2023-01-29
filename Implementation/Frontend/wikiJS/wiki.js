import { getInfoCards } from "../gameJS/cards.js";

let data, table;
const pageSize = 10;
let curPage = 1;

if(curPage === 1){
  document.getElementById("prevButton").style.visibility = "hidden";
}

export async function loadWiki() {
  table = document.querySelector('#wikiTable tbody');
  renderTable();

  document.querySelector('#nextButton').addEventListener('click', nextPage, false);
  document.querySelector('#prevButton').addEventListener('click', previousPage, false);
}

export function getDetails(btn){
  var cardName =  btn.getAttribute("data-button")
  console.log("CARD NAME:" + cardName);
}

function renderTable() {
  let result = '';

  fetch("http://localhost:5053/gada_card_deck/generate?" + new URLSearchParams({
    deck_offset: (curPage-1)*pageSize,
    deck_size: pageSize,
    randomize: false
  }))
  .then((response) => response.json())
  .then((responseData) => {
    data = responseData;
    data.cards.forEach(card => {
      result += `<tr>
      <td>${card.name}</td>
      <td>${card.score}</td>
      <td>TO DO</td>
      <td><button type="button"  class="btn btn-primary" id="detailsBtn" onclick="module.getDetails(this)" data-button="${card.name}">Details</button></td>
      </tr>`;
   });
     initJsonLD(data.cards);
     table.innerHTML = result;
  });
}

function previousPage() {
  curPage--;
  if(curPage === 1){
    document.getElementById("prevButton").style.visibility = "hidden";
  }
  renderTable();
}

function nextPage() {
  curPage = curPage + 1;
  renderTable();
  document.getElementById("prevButton").style.visibility = "visible";
}

async function initJsonLD(jsonldCards) {
  var jsonlds = await getInfoCards(jsonldCards, true);
  document.getElementById("dynamicJSONLD").innerHTML = JSON.stringify(
    jsonlds.cards
  );
}