export function timeout(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function objectToString(obj) {
  if (typeof obj != "object") {
    return JSON.stringify(obj);
  }

  var str = "";
  if (Array.isArray(obj)) {
    for (var i in obj) {
      str = str.concat(objectToString(obj[i])).concat("<br>");
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

export function shuffleArray(array) {
  let shuffled = array
    .map((value) => ({ value, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map(({ value }) => value);
  return shuffled;
}

function popRandom(array) {
  let i = (Math.random() * array.length) | 0;
  return array.splice(i, 1)[0];
}

export function popRandoms(array, handSize) {
  var pops = [];
  for (let i = 0; i < handSize; i++) {
    var popped = popRandom(array);
    if (popped == undefined) {
      break;
    }
    pops.push(popped);
  }
  return pops;
}

export function setVisible(id, status) {
  if (typeof status === "string" || status instanceof String) {
    status = status === "true";
  }

  if (status == true) {
    document.getElementById(id).style.display = "block";
    document.getElementById(id).classList.remove("forceHide");
    document.getElementById(id).classList.add("forceShow");
  } else {
    document.getElementById(id).style.display = "none";
    document.getElementById(id).classList.remove("forceShow");
    document.getElementById(id).classList.add("forceHide");
  }
}

export function showLoading(status) {
  if (status == true) {
    setVisible("loader", true);
  } else {
    setVisible("loader", false);
  }
}

export function cleanLocalStorage() {
  localStorage.removeItem("inGame");
  localStorage.removeItem("inRound");
  localStorage.removeItem("inQuiz");
  localStorage.removeItem("inQuestions");
  localStorage.removeItem("inSubmit");
  localStorage.removeItem("quizStatus");
  localStorage.removeItem("userCardsNames");

  localStorage.removeItem("currentRound");
  localStorage.removeItem("gameCards");
  localStorage.removeItem("nrRounds");
  localStorage.removeItem("handSize");
  localStorage.removeItem("userScore");
  localStorage.removeItem("compScore");
}

function checkGameContext() {
  var inRound = localStorage.getItem("inRound");
  if (inRound === "true") {
    cleanLocalStorage();
    window.location.replace("index.html");
  }

  var inGame = localStorage.getItem("inGame");
  if (inGame == undefined || inGame == "false") {
    cleanLocalStorage();
    window.location.replace("index.html");
  }
}

function checkQuizContext() {
  var inQuestions = localStorage.getItem("inQuestions");
  if (inQuestions === "true") {
    cleanLocalStorage();
    window.location.replace("index.html");
  }

  var inQuiz = localStorage.getItem("inQuiz");
  if (inQuiz == undefined || inQuiz == "false") {
    cleanLocalStorage();
    window.location.replace("index.html");
  }
}

function checkSubmitContext() {
  var inSubmit = localStorage.getItem("inSubmit");
  if (inSubmit == undefined || inSubmit == "false") {
    cleanLocalStorage();
    window.location.replace("index.html");
  }
}

export function checkPageContext(currentPage) {
  if (currentPage == "game") {
    checkGameContext();
  } else if (currentPage == "main") {
    cleanLocalStorage();
  } else if (currentPage == "quiz") {
    checkQuizContext();
  } else if (currentPage == "submit") {
    checkSubmitContext();
  } else if (currentPage == "leaderboard") {
    cleanLocalStorage();
  } else if (currentPage == "wiki") {
    cleanLocalStorage();
  }
}

export function exitGame() {
  cleanLocalStorage();
  window.location.replace("index.html");
}
