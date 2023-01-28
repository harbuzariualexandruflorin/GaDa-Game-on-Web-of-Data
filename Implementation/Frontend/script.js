// Get the card data
const names = [];
var resp = await fetch("http://localhost:5053/gada_card_deck/generate?deck_offset=0&deck_size=5&randomize=True");
resp = await resp.json();
resp.cards.forEach((card) => {
  names.push(card.name);
});
resp = await fetch("http://localhost:5053/gada_card_deck/info?jsonld=False", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    cards: names,
  }),
});
resp = await resp.json();

// Create the elements for each card
var opponentDeck = document.getElementById("opponent-deck");
resp.cards.forEach((card) => {
  var cardDiv = document.createElement("div");
  cardDiv.classList.add("card");

  var name = document.createElement("p");
  name.innerHTML = card.name;
  cardDiv.appendChild(name);

  var score = document.createElement("p");
  score.innerHTML = card.score;
  cardDiv.appendChild(score);

  var avatar = document.createElement("img");
  avatar.src = card.avatar;
  cardDiv.appendChild(avatar);

  opponentDeck.appendChild(cardDiv);
});

// Create the elements for the player-deck
var playerDeck = document.getElementById("player-deck");
resp.cards.forEach((card) => {
  var cardDiv= document.createElement("div");
  cardDiv.classList.add("card");
  
  var name = document.createElement("p");
  name.innerHTML = card.name;
  cardDiv.appendChild(name);
  
  var score = document.createElement("p");
  score.innerHTML = card.score;
  cardDiv.appendChild(score);
  
  var avatar = document.createElement("img");
  avatar.src = card.avatar;
  cardDiv.appendChild(avatar);
  
  playerDeck.appendChild(cardDiv);
  });
