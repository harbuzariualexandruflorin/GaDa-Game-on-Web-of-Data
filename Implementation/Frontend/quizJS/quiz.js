import { QUESTION_BONUS, QUESTION_FAIL } from "./macros.js";
import { API_URL, QUIZ_API_URL } from "../index.js";

var userCardsNames = [];
var questions = [];

const quizContainer = document.getElementById('quiz');
const resultsContainer = document.getElementById('results');
const checkButton = document.getElementById('check');

var slides = [];
let currentSlide = 0;

function buildQuiz(){

  const output = [];

  questions.forEach(
    (currentQuestion, questionNumber) => {

      console.log("Current question is....");
      console.log(currentQuestion);

      const answers = [];

      for(var option in currentQuestion.options){

        answers.push(
          `<label>
            <input type="checkbox" name="${option}" value="${option}">
            ${option} :
            ${currentQuestion.options[option]}
          </label>`
        );
      }
      output.push(
        `<div class="slide">
          <div class="question"> ${currentQuestion.question} </div>
          <div class="answers"> ${answers.join("")} </div>
        </div>`
      );
    }
  );

  quizContainer.innerHTML = output.join('');
}

function showSlide(n) {

  if(currentSlide === questions.length - 1) {
    endQuiz();
  } else {
    slides[currentSlide].classList.remove('active-slide');
    slides[n].classList.add('active-slide');
    currentSlide = n;
  }  
}

function showNextSlide() {
  showSlide(currentSlide + 1);
}

function showPreviousSlide() {
  showSlide(currentSlide - 1);
}

export function initQuiz() {
  
  localStorage.setItem("inQuestions", true);
  userCardsNames = JSON.parse(localStorage.getItem("userCardsNames"));
  console.log(userCardsNames);

  fetch(`${QUIZ_API_URL}/api/Question/getQuestion`, {
    method: "POST",
    body: JSON.stringify({
      characters: userCardsNames
    }),
    headers: {
      "Content-type": "application/json"
    }
  })
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
    questions = data;
    buildQuiz();
    slides = document.querySelectorAll(".slide");
    showSlide(currentSlide);
  });
}

export function checkAnswer() {

  var nrOfCorrectChecks = 0;

  const answerToSend = new Object();

  const answerContainers = quizContainer.querySelectorAll('.answers');

  const answerContainer = answerContainers[currentSlide];

  var currentQuestion = questions[currentSlide];

  answerToSend.question = currentQuestion.question;
  answerToSend.subject = currentQuestion.subject;
  answerToSend.options = [];

  for(var option in currentQuestion.options){

    const input = answerContainer.querySelector(`input[name=${option}]`);

    answerToSend.options.push({
      value: currentQuestion.options[option],
      checked: input.checked
    });
  }
  console.log(answerToSend);

  fetch(`${QUIZ_API_URL}/api/Question/answer`, {
    method: "POST",
    body: JSON.stringify(answerToSend),
    headers: {
      "Content-type": "application/json"
    }
  })
  .then((response) => response.json())
  .then((data) => {
    console.log(data);

    for(var q_option in currentQuestion.options) {
      for(var a_option in data.options) {
        if (currentQuestion.options[q_option] === data.options[a_option].value) {
          if (data.options[a_option].checked && data.options[a_option].isCorrect) {
            answerContainer.querySelector(`input[name=${q_option}]`).parentElement.style.color = 'green';
            // nrOfCorrectChecks++;
          } 
          else if (data.options[a_option].checked && !data.options[a_option].isCorrect) {
            answerContainer.querySelector(`input[name=${q_option}]`).parentElement.style.color = 'red';
            // nrOfCorrectChecks++;
          }
        }
      }
    }
    const myTimeout = setTimeout(showNextSlide, 3000);
  });
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

checkButton.addEventListener("click", checkAnswer);
