// Define variables
let level = 1;
let gold = 0;
let Starthealth = 10;
let health = 10;
let equippedItem = null;

// Define functions
function fight() 
{
    let damage = 1;
    if (equippedItem === "sword") {
        damage++;
    }
    health -= damage;
    if (health <= 0) {
        level++;
        gold += level;
        Starthealth *= 1.2;
        Starthealth = Math.round(Starthealth);
        health = Starthealth;
    }
    updateStats();
}

function equip(item) {
    equippedItem = item;
    updateStats();
}

function discard(item) {
    if (equippedItem === item) {
        equippedItem = null;
    }
    updateStats();
}

let swordPrice = 10;

function buySword() {
    if (gold >= swordPrice) {
        gold -= swordPrice;
        equippedItem = "sword";
        swordPrice *= 2;
        updateStats();
        document.getElementById("buy-sword").disabled = true;
        document.getElementById("sword-price").innerText = swordPrice;
        document.getElementById("sword-message").innerText = "You bought the sword!";
        document.getElementById("sword").classList.add("equipped");
    } else {
        document.getElementById("sword-message").innerText = "Not enough gold!";
    }
}

function updateStats() {
    document.getElementById("level").innerText = level;
    document.getElementById("gold").innerText = gold;
    document.getElementById("health").innerText = health;
    if (equippedItem === "sword") {
        document.getElementById("sword").classList.add("equipped");
    } else {
        document.getElementById("sword").classList.remove("equipped");
    }
    if (equippedItem === "sword") {
        document.getElementById("sword").classList.add("equipped");
        document.getElementById("buy-sword").disabled = true;
        document.getElementById("sword-message").innerText = "";
        document.getElementById("sword-price").innerText = "N/A";
    } else {
        document.getElementById("sword").classList.remove("equipped");
        document.getElementById("buy-sword").disabled = false;
        document.getElementById("sword-message").innerText = "";
        document.getElementById("sword-price").innerText = swordPrice;
    }
}

  
  function updateGold() {
    gold += level;
  }
  
  // Main Game Loop every 0.5 seconds
  setInterval(function() {
    updateStats();
  }, 500);
  
  // call updateGold every 10 seconds
  setInterval(function() {
    updateGold();
  }, 10000);
