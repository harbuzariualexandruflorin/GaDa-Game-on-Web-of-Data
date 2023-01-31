import { QUESTION_BONUS, QUESTION_FAIL } from "./macros.js";
import { API_URL, QUIZ_API_URL } from "../index.js";

var userCardsNames = [];
var questions = [];
var quizScore = 0;

const quizContainer = document.getElementById('quiz');
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

  if(n === questions.length) {
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

export function initQuiz() {
  
  localStorage.setItem("inQuestions", true);
  userCardsNames = JSON.parse(localStorage.getItem("userCardsNames"));
  console.log(userCardsNames);

  fetch(`${QUIZ_API_URL}/api/question/getQuestions`, {
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

  var correctAnswers = 0, wrongAnswers = 0;

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

  fetch(`${QUIZ_API_URL}/api/question/answer`, {
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
            correctAnswers++;
          } 
          else if (data.options[a_option].checked && !data.options[a_option].isCorrect) {
            answerContainer.querySelector(`input[name=${q_option}]`).parentElement.style.color = 'red';
            wrongAnswers++;
          }
          else if (!data.options[a_option].checked && data.options[a_option].isCorrect) {
            correctAnswers++;
          }
          else if (!data.options[a_option].checked && !data.options[a_option].isCorrect) {
            wrongAnswers++;
          }
        }
      }
    }
    computeQuestionScore(correctAnswers, wrongAnswers);
    const myTimeout = setTimeout(showNextSlide, 2000);
  });
}

export function endQuiz() {
  var pointsToReceive = 0;
  var quizPassed =  quizScore >= Math.round(0.5 * questions.length * QUESTION_BONUS);
  localStorage.setItem("quizStatus", quizPassed);

  if(!quizPassed) {
    localStorage.setItem(
      "compScore",
      parseInt(localStorage.getItem("compScore")) + QUESTION_FAIL
    );
    pointsToReceive = -QUESTION_FAIL;
    alert("You lost the quiz! Points lost: ".concat(pointsToReceive));
  } else {
    alert("You won the quiz! Points received: ".concat(quizScore));
    pointsToReceive = quizScore;
    console.log("POINTS TO RECEIVE: " + pointsToReceive);
  }

  var userScore = parseInt(localStorage.getItem("userScore")) + pointsToReceive;
  if (userScore < 0) {
    userScore = 0;
  }
  localStorage.setItem("userScore", userScore);
  localStorage.removeItem("inQuestions");
  localStorage.removeItem("inQuiz");

  window.location.replace("game.html");
}

// score computed for a scingle question
function computeQuestionScore(correctChecks, wrongChecks) {
  console.log("WRONG CHECKS: " + wrongChecks);
  console.log("CORECT CHECKS: " + correctChecks);

  if(wrongChecks === 0) {
    quizScore += QUESTION_BONUS;
  }
  else if(correctChecks === 0) {
    quizScore -= QUESTION_FAIL;
  }
  else if(wrongChecks - correctChecks > 0){
    quizScore -= Math.round(QUESTION_FAIL / 3);

  } else {
    quizScore += Math.round(QUESTION_BONUS / 2);
  }
}