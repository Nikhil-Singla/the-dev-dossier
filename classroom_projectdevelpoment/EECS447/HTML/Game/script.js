// Define variables
let level = 1;
let gold = 0;
let Starthealth = 10;
let health = 10;
let equippedItem = 0;
let itemPrice = 10;
let damage = 1;

// Define functions
function clamp(num, min, max) 
{
    return num <= min 
        ? min 
        : num >= max 
            ? max 
            : num
  }


function fight() 
{    
    health -= damage;
    if (health <= 0) {
        gold += level;
        level++;
        Starthealth = Math.round(Starthealth*1.2);
        health = Starthealth;
    }

    updateStats();
}

function buy() 
{
    if(damge === 100)
    {
        document.getElementById("item-message").innerText = "Damage Capped Out! All Items Bought";
    }
    else if (gold >= itemPrice) 
    {
        gold -= itemPrice;
        equippedItem += 1;
        itemPrice = Math.round(itemPrice*1.5);
        damage = clamp(damage*2, 1, 100);
        updateStats();
    } 
    else 
    {
        document.getElementById("item-message").innerText = "Not enough gold!";
    }
}

function updateStats() 
{
    document.getElementById("level").innerText = level;
    document.getElementById("gold").innerText = gold;
    document.getElementById("health").innerText = health;
    document.getElementById("buytext").innerText = "Buy: " + itemPrice;
    document.getElementById("dmg").innerText = "Current Damage: " + damage;
}

  
function idleGold() 
{
    gold += level;
}

function clearText()
{
    document.getElementById("item-message").innerText = "";
}

// call idleGold every 10 seconds
setInterval(function() 
{
    idleGold();
    clearText();
}, 5000);  

// Main Game Loop every 0.5 seconds
setInterval(function() 
{
    updateStats();
}, 500);
  

