import { showLoading, setVisible, cleanLocalStorage } from "./utils.js";

import {
  dealCards,
  getInfoCards,
  getCards,
  getCardTable,
  getCardPlaceholder,
  isCardStrongerThan,
  battleCards,
  getGreenSelectedCard,
  getChainScore,
} from "./cards.js";

export function testme() {
  alert("nice");
}

var userCardsArray = [];
var userCardsNames = [];
var compCardsArray = [];
var compCardsNames = [];
var selectedCards = [];
var gameCards = [];
var userScore = 0;
var compScore = 0;

function clickUserCardHandler() {
  var cards = document.getElementsByClassName("cardTable");
  for (let i = 0; i < cards.length; i++) {
    if (cards[i].getAttribute("id") != "cardTableChain") {
      if (
        this.getAttribute("data-card") == cards[i].getAttribute("data-card")
      ) {
        if (cards[i].classList.contains("selectCardTable")) {
          return;
        }
        cards[i].classList.add("selectCardTable");
        setVisible("game-play", true);
        updateSelectedCardInfo(cards[i].getAttribute("data-card"));
      } else {
        cards[i].classList.remove("selectCardTable");
      }
    }
  }
}

function updateSelectedCardInfo(cardName) {
  if (cardName == undefined) {
    document.getElementById("selectedCardName").innerHTML = "";
    document.getElementById("selectedCardScore").innerHTML = "";

    if (selectedCards.length > 0) {
      document.getElementById("topCardInfoName").innerHTML =
        selectedCards[selectedCards.length - 1].name;
      document.getElementById("topCardInfoScore").innerHTML =
        selectedCards[selectedCards.length - 1].score;
    } else {
      document.getElementById("topCardInfoName").innerHTML = "";
      document.getElementById("topCardInfoScore").innerHTML = "";
      document.getElementById("totalChainScore").innerHTML =
        "Total Chain Score: 0";
    }
    return;
  }

  var selectedCard = userCardsArray.filter((c) => c["name"] == cardName)[0];
  document.getElementById("selectedCardName").innerHTML = selectedCard.name;

  var battleScore1 = selectedCard.score;
  if (selectedCards.length > 0) {
    battleScore1 += battleCards(
      selectedCard,
      selectedCards[selectedCards.length - 1]
    );
  }
  document.getElementById("selectedCardScore").innerHTML = battleScore1;

  if (selectedCards.length > 0) {
    document.getElementById("topCardInfoName").innerHTML =
      selectedCards[selectedCards.length - 1].name;

    var battleScore2 =
      selectedCards[selectedCards.length - 1].score +
      battleCards(selectedCards[selectedCards.length - 1], selectedCard);
    document.getElementById("topCardInfoScore").innerHTML = battleScore2;

    setVisible(
      "game-play",
      battleScore1 > battleScore2 || selectedCards.length % 2 == 1
    );
  }
}

function updateSelectedCards(cardName, isPlayer) {
  if (cardName == undefined) {
    return;
  }
  var selectedCard = undefined;
  if (isPlayer) {
    selectedCard = userCardsArray.filter((c) => c["name"] == cardName)[0];
    userCardsArray = userCardsArray.filter((c) => c.name != cardName);
  } else {
    selectedCard = compCardsArray.filter((c) => c["name"] == cardName)[0];
    compCardsArray = compCardsArray.filter((c) => c.name != cardName);
  }
  selectedCards.push(selectedCard);
  document.getElementById("totalChainScore").innerHTML =
    "Total Chain Score: ".concat(getChainScore(selectedCards));
  renderSelectedCards(isPlayer);
}

function renderSelectedCards(isPlayer) {
  document
    .getElementById("chainColumn")
    .insertAdjacentHTML(
      "afterend",
      getCardTable(selectedCards[selectedCards.length - 1], "Chain").concat(
        "<br><br>"
      )
    );

  if (isPlayer) {
    renderUserCards(selectedCards[selectedCards.length - 1]);
  } else {
    renderComputerCards();
  }
  updateSelectedCardInfo(undefined);
}

function renderComputerCards() {
  var cards = document.getElementsByClassName("compCard");
  if (cards.length > 0) {
    cards[0].remove();
  }
}

function renderUserCards(popCard) {
  var cards = document.getElementsByClassName("cardTable");
  for (let i = 0; i < cards.length; i++) {
    if (cards[i].getAttribute("id") != "cardTableChain") {
      if (popCard["name"] == cards[i].getAttribute("data-card")) {
        cards[i].remove();
        setVisible("game-play", false);
        break;
      }
    }
  }
}

function computerLogic(forceEnd) {
  checkChainStatus(forceEnd);
  var chainTopCard = undefined;
  if (selectedCards.length > 0) {
    chainTopCard = selectedCards[selectedCards.length - 1];
  }

  var compChosenCardName = undefined;
  compCardsArray.sort((a, b) => (a.score > b.score ? 1 : -1));
  if (chainTopCard == undefined && compCardsArray.length > 0) {
    compChosenCardName = compCardsArray[0].name;
  } else {
    for (let i = 0; i < compCardsArray.length; i++) {
      if (isCardStrongerThan(compCardsArray[i], chainTopCard)) {
        compChosenCardName = compCardsArray[i].name;
        break;
      }
    }
    if (compChosenCardName == undefined && compCardsArray.length > 0) {
      if (selectedCards.length % 2 == 1) {
        compChosenCardName = compCardsArray[0].name;
      }
    }
  }
  updateSelectedCards(compChosenCardName, false);
  checkChainStatus(compChosenCardName == undefined);
}

function initScores() {
  userScore = localStorage.getItem("userScore");
  if (userScore == undefined) {
    userScore = 0;
  } else {
    userScore = parseInt(userScore);
  }
  compScore = localStorage.getItem("compScore");
  if (compScore == undefined) {
    compScore = 0;
  } else {
    compScore = parseInt(compScore);
  }
  localStorage.setItem("compScore", compScore);
}

async function initGame(deckSize) {
  var currentRound = localStorage.getItem("currentRound");
  if (currentRound == undefined) {
    currentRound = 1;
  } else {
    currentRound = parseInt(currentRound);
  }

  localStorage.setItem("currentRound", currentRound);
  document.getElementById("game-info").innerHTML = "Current Round: ".concat(
    currentRound
  );
  if (localStorage.getItem("quizStatus") == undefined) {
    localStorage.setItem("quizStatus", true);
  }
  setVisible("game-play", false);
  setVisible("game-skip", false);
  initScores();
  updateScores();

  if (localStorage.getItem("currentRound") == "1") {
    gameCards = await getCards(deckSize);
    localStorage.setItem("gameCards", JSON.stringify(gameCards));
  } else {
    gameCards = JSON.parse(localStorage.getItem("gameCards"));
  }

  localStorage.setItem("inRound", true);
}

export async function loadRound() {
  localStorage.removeItem("inQuiz");
  localStorage.removeItem("inQuestions");

  var nrRounds = localStorage.getItem("nrRounds");
  if (nrRounds == undefined) {
    nrRounds = 2;
  } else {
    nrRounds = parseInt(nrRounds);
  }
  localStorage.setItem("nrRounds", nrRounds);
  var handSize = localStorage.getItem("handSize");
  if (handSize == undefined) {
    handSize = 2;
  } else {
    handSize = parseInt(handSize);
  }
  localStorage.setItem("handSize", handSize);

  await initGame(2 * handSize * nrRounds);
  showLoading(true);

  userCardsArray = [];
  userCardsNames = [];
  compCardsArray = [];
  compCardsNames = [];
  selectedCards = [];

  var currentHand = await dealCards(
    gameCards,
    handSize,
    localStorage.getItem("quizStatus")
  );
  await initJsonLD(currentHand);
  var userDealtCards = await getInfoCards(currentHand, false);

  var tempCardsArray = [];
  for (var card in userDealtCards["cards"]) {
    tempCardsArray.push(userDealtCards["cards"][card]);
  }

  for (var card in tempCardsArray) {
    userCardsArray.push(tempCardsArray[card]);
    userCardsNames.push(tempCardsArray[card].name);

    document
      .getElementById("userColumn")
      .insertAdjacentHTML(
        "afterend",
        getCardTable(tempCardsArray[card], card).concat("<br><br>")
      );

    document
      .getElementById(`cardTable${card}`)
      .addEventListener("click", clickUserCardHandler);
  }

  var currentHand = await dealCards(
    gameCards,
    handSize,
    !localStorage.getItem("quizStatus")
  );
  var computerDealtCards = await getInfoCards(currentHand, false);

  tempCardsArray = [];
  for (var card in computerDealtCards["cards"]) {
    tempCardsArray.push(computerDealtCards["cards"][card]);
  }
  for (var card in tempCardsArray) {
    compCardsArray.push(tempCardsArray[card]);
    compCardsNames.push(tempCardsArray[card].name);

    document
      .getElementById("compColumn")
      .insertAdjacentHTML("afterend", getCardPlaceholder().concat("<br><br>"));
  }

  checkFirstTurn();
  showLoading(false);
}

function checkFirstTurn() {
  if (localStorage.getItem("quizStatus") == "true") {
    return;
  }

  computerLogic(false);
  setVisible(
    "game-skip",
    selectedCards.length > 0 && selectedCards.length % 2 == 0
  );
  return;
}

export function skipTurn() {
  computerLogic(true);
  setVisible(
    "game-skip",
    selectedCards.length > 0 && selectedCards.length % 2 == 0
  );

  var card = getGreenSelectedCard();
  if (card == undefined) {
    return;
  }
  updateSelectedCardInfo(card.getAttribute("data-card"));
  setVisible("game-play", selectedCards.length % 2 == 1);
}

export function playCard() {
  var selectedCard = getGreenSelectedCard();
  if (selectedCard == undefined) {
    return;
  }
  updateSelectedCards(selectedCard.getAttribute("data-card"), true);
  setVisible("game-play", false);

  computerLogic(false);
  setVisible(
    "game-skip",
    selectedCards.length > 0 && selectedCards.length % 2 == 0
  );
}

function checkChainStatus(forceEnd) {
  if (selectedCards.length == 0 || selectedCards.length % 2 == 1) {
    return;
  }

  if (
    !forceEnd &&
    isCardStrongerThan(
      selectedCards[selectedCards.length - 1],
      selectedCards[selectedCards.length - 2]
    ) &&
    !isRoundEnd()
  ) {
    return;
  }

  var chainScore = getChainScore(selectedCards);
  var winnerCard = selectedCards[selectedCards.length - 2];
  if (
    isCardStrongerThan(
      selectedCards[selectedCards.length - 1],
      selectedCards[selectedCards.length - 2]
    )
  ) {
    winnerCard = selectedCards[selectedCards.length - 1];
  }

  if (isPlayerChainWinner(winnerCard)) {
    userScore += chainScore;
    alert("You won the chain! Score received: ".concat(chainScore));
  } else {
    alert("You lost the chain! Computer received: ".concat(chainScore));
    compScore += chainScore;
  }
  updateScores();
  cleanChain();
}

function isPlayerChainWinner(winnerCard) {
  if (userCardsNames.includes(winnerCard.name)) {
    return true;
  }
  if (compCardsNames.includes(winnerCard.name)) {
    return false;
  }
  return false;
}

function updateScores() {
  document.getElementById("userScore").innerHTML = "User Score: ".concat(
    userScore
  );
  document.getElementById("compScore").innerHTML = "Computer Score: ".concat(
    compScore
  );
}

function cleanChain() {
  selectedCards = [];
  var cards = document.getElementsByClassName("cardTable");

  var found = true;
  while (found == true) {
    found = false;
    for (let i = 0; i < cards.length; i++) {
      if (cards[i].getAttribute("id") == "cardTableChain") {
        cards[i].remove();
        found = true;
      }
    }
  }
  updateSelectedCardInfo(undefined);
  checkRoundEnd();
}

function isRoundEnd() {
  return userCardsArray.length == 0 && compCardsArray.length == 0;
}

function checkRoundEnd() {
  if (isRoundEnd()) {
    localStorage.setItem("userScore", userScore);
    localStorage.setItem("compScore", compScore);

    if (gameCards.length == 0) {
      alert("No cards left! Game ended!");
      localStorage.setItem("inSubmit", true);
      window.location.replace("submit.html");
    } else {
      alert("Round Ended! Starting the quiz stage...");
      localStorage.setItem(
        "currentRound",
        parseInt(localStorage.getItem("currentRound")) + 1
      );
      localStorage.setItem("gameCards", JSON.stringify(gameCards));
      localStorage.setItem("inRound", false);

      localStorage.setItem("inQuiz", true);
      localStorage.removeItem("inQuestions");
      localStorage.setItem("userCardsNames", JSON.stringify(userCardsNames));
      window.location.replace("quiz.html");
    }
  }
}

async function initJsonLD(jsonldCards) {
  var jsonlds = await getInfoCards(jsonldCards, true);
  document.getElementById("dynamicJSONLD").innerHTML = JSON.stringify(
    jsonlds.cards
  );
}
