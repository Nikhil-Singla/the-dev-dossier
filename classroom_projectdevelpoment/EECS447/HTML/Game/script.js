// Define variables
let level = Number(document.querySelector('meta[name="levelStart"]').content);
let gold = Number(document.querySelector('meta[name="goldStart"]').content);
let Starthealth = Number(document.querySelector('meta[name="healthStart"]').content);
let health = Starthealth;
let equippedItem = 0;
let itemPrice = Number(document.querySelector('meta[name="buytextStart"]').content); 
let damage = Number(document.querySelector('meta[name="dmgStart"]').content);



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
    if(damage == 100)
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

// Save Progress every 60 seconds
//setInterval(function() 
//{
//    write();
//}, 60000);  

// Main Game Loop every 0.5 seconds
setInterval(function() 
{
    updateStats();
}, 500);
  

