# Начало программы должно начинаться только с program var #
program var

# Объявление переменных идет после program var #
% x, y, z, a, b, i, j

begin
    let x = 5;
    y = x + 3;
    z = 1;
    

    
    input(a b z);

    
    output(a);

    do while
        x = y
        output(a)
    loop;

    if 
        x > 10
    then 
        let z = x * 2
    end_else;

    if 
        y < 5
    then 
        output(x)
    else
        let z = x + 1
    end_else;

    if 
        y < 5
    then 
        output(x)
    else 
        let z = x + 1
    else
        let z = x + 1
    end_else;
    
    do while
        x = y
        if 
            y < 5
        then 
            let z = x + 1
        else 
            let z = x + 1
        end_else
    loop;

    for 
    ( x >= 0 ; x <= 5 ; x = x + 1 )
        for 
            ( x >= 0 ; x <= 5 ; x = x + 1 )
                do while
                    x = y
                    if 
                        y < 5
                    then 
                        let z = x + 1
                    else 
                        let z = x + 1
                    end_else
                loop

end.
