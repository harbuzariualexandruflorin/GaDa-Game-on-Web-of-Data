export const API_URL = "http://localhost:5053/";
// export const API_URL = "https://34ee-194-176-167-54.eu.ngrok.io/cards/";
export const QUIZ_API_URL = "https://localhost:7214"

function setGame(nrRounds, handSize) {
  localStorage.setItem("inGame", "true");
  localStorage.setItem("quizStatus", "true");
  localStorage.setItem("currentRound", "1");
  localStorage.setItem("nrRounds", nrRounds);
  localStorage.setItem("handSize", handSize);
  localStorage.setItem("userScore", 0);
  localStorage.setItem("compScore", 0);
}

export function startGame() {
  var nrRounds = document.getElementById("nrRounds").value;
  var handSize = document.getElementById("handSize").value;
  setGame(nrRounds, handSize);
  window.location.replace("game.html");
}
