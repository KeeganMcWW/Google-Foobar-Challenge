def solution(xs):
    positive_xs = []
    negative_xs = []
    new_xs = 1
    #if nothing is input, output zero
    if not xs:
        return(str(0))
    #if a single zero is input, return zero
    if len(xs) == 1 and xs[0] == 0:
        return(str(0))
    #if lots of zeros are input, return zero
    if all(x == 0 for x in xs):
        return(str(0))
    #sort into positive and negative values
    for x in xs:
        if x>0:
            positive_xs.append(x)
        if x==0:
            pass
        if x<0:
            negative_xs.append(x)
    #if there are no negative numbers return product of all positive numbers
    if len(negative_xs) == 0:
        for x in positive_xs:
            new_xs = new_xs * x
        return str(new_xs)
    #if there are negative values
    if len(negative_xs) > 0:
        #sort negative values in their list
        negative_xs.sort()
        #if even negatives, make positive and append to other positive_xs
        if len(negative_xs)%2 == 0:
            for x in negative_xs:
                positive_xs.append(-x)
        #if odd, non singluar negative, make positive and append all but last to other positive xs
        if len(negative_xs)%2 == 1 and len(negative_xs) != 1:
            for x in negative_xs[:-1]:
                positive_xs.append(-x)
        # if only value in input is a single negative value - return value
        if len(negative_xs) == 1 and len(xs) == 1:
            return(str(xs[0]))
        # if only one negative number and no positives - return zero
        if len(negative_xs) == 1 and not positive_xs:
            return(str(0))
        # calculate positive x list which now has all postivie values and pairs of (now positive) negative values
        for x in positive_xs:
            new_xs = new_xs * x        

    return str(new_xs)