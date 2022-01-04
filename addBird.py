import pyodbc

def main():

    print('\n')
    theObj = []
    # Get The Bird Info
    bird = input('Bird:  ')
    theObj.append(bird)
    category = input('Category:  ')
    theObj.append(category)
    categoryAlt = input('Category Alt:  ')
    theObj.append(categoryAlt)
    state = input('State:  ')
    theObj.append(state)
    city = input('City:  ')
    theObj.append(city)
    date = input('Date (YYY/MM/DD):  ')
    theObj.append(date)
    details = input('Details:  ')
    theObj.append(details)
    WasLifeBird = input('LifeBird? (1 or 0):  ')
    theObj.append(WasLifeBird)

    # Verify:
    for item in theObj:
        print(f'------>{item}<------')

 
    


if __name__ == '__main__':
    main()