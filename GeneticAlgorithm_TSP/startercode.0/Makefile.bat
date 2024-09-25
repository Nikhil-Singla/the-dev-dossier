@echo off
setlocal EnableDelayedExpansion

REM Run loop
for /L %%q in (50, 20, 500) do (
    echo fixedQuant=%%q
    python -u "c:\Users\Nikhil Singla\Desktop\Fall 2024\CSCI 561 AI\Homework 1\startercode.0\inputGenerator.py" --fixedQuant=%%q
    set counter=0

    :loop
    if !counter! lss 10 (
        echo Try !counter!
        python -u "c:\Users\Nikhil Singla\Desktop\Fall 2024\CSCI 561 AI\Homework 1\startercode.0\timingHomework.py"
        set /a counter+=1
        goto loop
    ) else (
        echo Finished processing for fixedQuant=%%q
    )
)

endlocal
pause
