import { QUESTION_BONUS, QUESTION_FAIL } from "./macros.js";
import { API_URL } from "../index.js";

var userCardsNames = [];

export function initQuiz() {
  localStorage.setItem("inQuestions", true);
  userCardsNames = JSON.parse(localStorage.getItem("userCardsNames"));
  console.log(userCardsNames);
}

export function endQuiz() {
  var nrCorrect = parseInt(document.getElementById("nrCorrect").value);
  var QUESTIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

  var quizScore = 0;
  if (nrCorrect >= QUESTIONS.length / 2) {
    quizScore = nrCorrect * QUESTION_BONUS;
    alert("You won the quiz! Points received: ".concat(quizScore));
  } else {
    quizScore = -QUESTION_FAIL;
    alert("You lost the quiz! Points lost: ".concat(QUESTION_FAIL));
    localStorage.setItem(
      "compScore",
      parseInt(localStorage.getItem("compScore")) + QUESTION_FAIL
    );
  }

  localStorage.setItem("quizStatus", nrCorrect >= QUESTIONS.length / 2);
  quizScore = parseInt(localStorage.getItem("userScore")) + quizScore;
  if (quizScore < 0) {
    quizScore = 0;
  }
  localStorage.setItem("userScore", quizScore);
  localStorage.removeItem("inQuestions");
  localStorage.removeItem("inQuiz");

  window.location.replace("game.html");
}
