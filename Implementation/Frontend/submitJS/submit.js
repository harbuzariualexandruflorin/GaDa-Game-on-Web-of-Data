import { API_URL } from "../index.js";

function setVisible(id, status) {
  if (status == true) {
    document.getElementById(id).style.display = "block";
  } else {
    document.getElementById(id).style.display = "none";
  }
}

export async function postUserScore(userName, userScore) {
  return fetch(`${API_URL}high_scores`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_name: userName,
      score: userScore,
    }),
  })
    .then(function (data) {
      if (data !== undefined) {
        if (data.status == 400) {
          alert("User already exists! Enter a different name.");
        } else if (data.status == 200) {
          alert("Score added!");
          window.location.replace("index.html");
        }
      }
    })
    .catch(function (error) {
      console.log(error);
    });
}

export function submitScore() {
  var userName = document.getElementById("userName").value;
  if (userName == undefined || userName.length == 0) {
    alert("Invalid user name!");
    return;
  }
  postUserScore(userName, parseInt(localStorage.getItem("userScore")));
}

export function setGameResult() {
  var userScore = parseInt(localStorage.getItem("userScore"));
  var compScore = parseInt(localStorage.getItem("compScore"));

  if (userScore == undefined) {
    userScore = 0;
  }
  if (compScore == undefined) {
    compScore = 0;
  }
  document.getElementById("finalUserScore").innerHTML = userScore;
  document.getElementById("finalCompScore").innerHTML = compScore;
  if (userScore == compScore) {
    document.getElementById("finalResult").innerHTML = "DRAW";
    setVisible("drawImg", true);
  } else if (userScore > compScore) {
    document.getElementById("finalResult").innerHTML = "YOU WON";
    setVisible("winImg", true);
  } else {
    document.getElementById("finalResult").innerHTML = "YOU LOST";
    setVisible("loseImg", true);
  }
}
