import { getInfoCards } from "../gameJS/cards.js";
import { API_URL, QUIZ_API_URL } from "../index.js";

let data, table;
const pageSize = 10;
let curPage = 1;

if (curPage === 1) {
  document.getElementById("prevButton").style.visibility = "hidden";
}

const cardContainer = document.getElementById("cardInfo");

export async function loadWiki() {
  table = document.querySelector("#wikiTable tbody");
  renderTable();

  document
    .querySelector("#nextButton")
    .addEventListener("click", nextPage, false);
  document
    .querySelector("#prevButton")
    .addEventListener("click", previousPage, false);
}

export async function getDetails(btn) {
  let result = [];
  var cardName = btn.getAttribute("data-button");

  var cardsList = [];
  cardsList.push({
    name: cardName,
  });

  var cardsListInfo = await getInfoCards(cardsList, false);
  var cardInfo = cardsListInfo.cards[0];

  document.getElementById("cardName").innerHTML = cardInfo.name;

  result.push(
    `<img src="${cardInfo.avatar}" class="card-img-top mx-auto d-block rounded" style='width:40%' alt="Avatar" >`
  );
  delete cardInfo.avatar;

  /*
  for(var prop in cardInfo) {
    if (typeof cardInfo[prop] === "string") {
      result.push(`
        <div class="row mt-2">
          <div class="col-md-3"><b>${prop.charAt(0).toUpperCase() + prop.slice(1)}</b></div>
          <div class="col-md-5 ms-auto">${cardInfo[prop].charAt(0).toUpperCase() + cardInfo[prop].slice(1)}</div>
        </div>`
      );
    }
  }
  cardContainer.innerHTML = result.join('');
  */
  for (var prop in cardInfo) {
    result.push(`
      <div class="row">
        <div class="col-md-2"><b>${
          prop.charAt(0).toUpperCase() + prop.slice(1)
        }</b></div>
        <div class="col-md-6 ms-auto">
          <ul class="list-unstyled">
    `);
    result.push(objectToString(cardInfo[prop]));
    result.push(`
          </ul>
        </div>
      </div>
    `);
  }
  cardContainer.innerHTML = result.join("");
}

function objectToString(obj) {
  if (typeof obj != "object") {
    // str += `<div class="col-md-5 ms-auto">${String(obj).charAt(0).toUpperCase() + String(obj).slice(1)}</div>`;
    return `<li class="mt-0 mb-0">${
      String(obj).charAt(0).toUpperCase() + String(obj).slice(1)
    }</li>`;
  }

  var str = "";
  if (Array.isArray(obj)) {
    for (var i in obj) {
      str = str.concat(objectToString(obj[i]));
    }
    return str;
  }

  if (obj.constructor == Object) {
    for (var p in obj) {
      str = str.concat(`${p} (${objectToString(obj[p])})<br>`);
    }
    return str;
  }
  return str;
}

function renderTable() {
  let result = "";

  fetch(
    `${API_URL}/gada_card_deck/generate?` +
      new URLSearchParams({
        deck_offset: (curPage - 1) * pageSize,
        deck_size: pageSize,
        randomize: false,
      })
  )
    .then((response) => response.json())
    .then((responseData) => {
      data = responseData;
      data.cards.forEach(async (card) => {
        var cardExtraInfo = await getCardInfo(card);

        result += `<tr>
      <td style='width:10%'><img src="${cardExtraInfo.avatar}" class="rounded img-responsive"  style='width:85%' alt="Avatar" ></td>
      <td>${card.name}</td>
      <td>${cardExtraInfo.universe}</td>
      <td>${card.score}</td>
      <td><button type="button"  class="btn btn-primary" id="detailsBtn" onclick="module.getDetails(this)" data-button="${card.name}" data-bs-toggle="modal" data-bs-target="#cardModal">Details</button></td>
      </tr>`;
        table.innerHTML = result;
      });
      if (data.cards.length < pageSize) {
        document.getElementById("nextButton").style.visibility = "hidden";
      } else {
        document.getElementById("nextButton").style.visibility = "visible";
      }
      initJsonLD(data.cards);
    });
}

function previousPage() {
  curPage--;
  if (curPage === 1) {
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

async function getCardInfo(card) {
  var cardsArray = [];
  cardsArray.push(card);
  var cardsListInfo = await getInfoCards(cardsArray, false);
  var cardInfo = cardsListInfo.cards[0];

  return cardInfo;
}
