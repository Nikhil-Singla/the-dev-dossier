function doMath(x, y)
{
    const choice = Math.floor(Math.random()*4);
    if(choice == 1)
    return x*y;
    else if(choice == 2)
    return x+y;
    else if(choice == 3)
    return Math.abs(x-y);
    else
    return x%y;
}

const result = doMath(Math.floor(Math.random()*10),Math.floor(Math.random()*20));
console.log(result);