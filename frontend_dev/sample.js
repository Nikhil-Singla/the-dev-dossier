function doMath(x, y)
{
    choice = Math.floor(Math.random()*4);
    if(choice == 1)
    {
        process.stdout.write("1: ");
        return x*y;
    }
    else if(choice == 2)
    {
        process.stdout.write("2: ");
        return x+y;
    }
    else if(choice == 3)
    {
        process.stdout.write("3: ");
        return Math.abs(x-y);
    }
    else
    {
        process.stdout.write("4: ");
        return x%y;
    }
}
result = doMath(Math.floor(Math.random()*10), Math.floor(Math.random()*20));
console.log(result);