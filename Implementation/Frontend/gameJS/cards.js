import { objectToString, shuffleArray, popRandoms } from "./utils.js";
import { API_URL } from "../index.js";
import {
  BATTLE_TYPE_BONUS,
  CHAIN_AVG_MULTIPLIER,
  CHAIN_LEN_MULTIPLIER,
} from "./macros.js";

export async function getInfoCards(cardsData, jsonld) {
  var names = [];
  cardsData.forEach((card) => {
    names.push(card.name);
  });

  return fetch(`${API_URL}/gada_card_deck/info?jsonld=${jsonld}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      cards: names,
    }),
  })
    .then((resp) => {
      return resp.json();
    })
    .then((data) => {
      return data;
    })

    .catch((error) => console.log(error));
}

export async function getCards(deck_size) {
  return fetch(
    `${API_URL}/gada_card_deck/generate?deck_offset=0&deck_size=${deck_size}&randomize=True`
  )
    .then((resp) => {
      return resp.json();
    })
    .then((data) => {
      return data.cards;
    })
    .catch((error) => console.log(error));
}

export function getCardInfoCell(prop, card) {
  if (prop == "avatar") {
    return `
      <img src=${card[prop]} style="vertical-align: bottom;" width="100%" height="100%"> 
    `;
  }

  return objectToString(card[prop]);
}

export function getCardTable(card, index) {
  var htmlTable = `<table id='cardTable${index}' class='cardTable' style='width:100%' data-card=${JSON.stringify(
    card["name"]
  )}>`;

  for (var prop in card) {
    htmlTable = htmlTable.concat("<tr>");
    htmlTable = htmlTable.concat("<td>");
    htmlTable = htmlTable.concat(prop);
    htmlTable = htmlTable.concat("</td>");

    htmlTable = htmlTable.concat("<td>");
    htmlTable = htmlTable.concat(getCardInfoCell(prop, card));
    htmlTable = htmlTable.concat("</td>");
    htmlTable = htmlTable.concat("</tr>");
  }

  return htmlTable.concat("</table>");
}

export function getCardPlaceholder() {
  return `
    <img src=resources/placeholder.png class="compCard" style="vertical-align: bottom;" width="100%" height="100%"> 
  `;
}

export async function dealCards(gameCards, handSize, quizWon) {
  if (quizWon == false) {
    var currentHand = popRandoms(gameCards, handSize);
    return currentHand;
  }

  gameCards.sort((a, b) => (a.score > b.score ? 1 : -1));
  var middleIndex = Math.ceil(gameCards.length / 2);
  var smallHalf = shuffleArray(gameCards.splice(0, middleIndex));
  var bigHalf = shuffleArray(gameCards.splice(-middleIndex));

  var currentHand = popRandoms(bigHalf, Math.floor(handSize / 2));
  if (currentHand.length < handSize) {
    currentHand = currentHand.concat(
      popRandoms(smallHalf, handSize - currentHand.length)
    );
  }
  gameCards.push(...smallHalf.concat(bigHalf));
  return currentHand;
}

function getCardTypes(card) {
  if (card.types == undefined) {
    return [];
  }
  var types = [];
  for (var o in card.types) {
    types.push(card.types[o].name);
  }
  return types;
}

export function battleCards(cardA, cardB) {
  if (cardA.types == undefined || cardB.types == undefined) {
    return 0;
  }

  var battleScore = 0;
  var cardTypesB = getCardTypes(cardB);
  for (var o in cardA.types) {
    for (var d in cardA.types[o].defeats) {
      if (cardTypesB.includes(cardA.types[0].defeats[d])) {
        battleScore += BATTLE_TYPE_BONUS;
      }
    }
  }
  return battleScore;
}

export function isCardStrongerThan(cardA, cardB) {
  return (
    cardA.score + battleCards(cardA, cardB) >
    cardB.score + battleCards(cardB, cardA)
  );
}

export function getGreenSelectedCard() {
  var cards = document.getElementsByClassName("cardTable");
  for (let i = 0; i < cards.length; i++) {
    if (cards[i].getAttribute("id") != "cardTableChain") {
      if (cards[i].classList.contains("selectCardTable")) {
        return cards[i];
      }
    }
  }
  return undefined;
}

export function getChainScore(chain) {
  var totalScore = 0;
  for (var index in chain) {
    totalScore += chain[index].score;
  }
  var averageScore = totalScore / chain.length;
  var chainScore =
    averageScore * CHAIN_AVG_MULTIPLIER + chain.length * CHAIN_LEN_MULTIPLIER;
  return Math.floor(chainScore);
}
