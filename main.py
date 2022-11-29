import asyncio 
import sqlite3
import os
import datetime
import maskpass


middle  = 46*" "
gap_len = 76


def format_input(ques) : 
    string  = middle + "| " + ques  + " "*(((gap_len*2)-1)-(len(ques))) +  "|\n" + middle  + "| -" 
    output = input(string)
    return output

async def redirect(redirect):
    for i in range(3,0,-1):
        title = "Redirecting to {redirect} in {i}...".format(redirect=redirect,i=i)
        symbol = " "
        gap = str(symbol)*(gap_len-int((len(title)/2)))
        gap2 = str(symbol)*((gap_len*2)- len(title) - len(gap))
        print(( middle + "|" + gap + title + gap2 + "|"),end='\r') 
        await asyncio.sleep(1)   

def int_check(answer,input ="Enter a number -" ) :
    answer = str(answer).strip()
    integer = -1
    while integer < 1 :
        try : 
            int(answer)
            integer = int(answer)
        except : 
            centre("Please enter a valid integer !")
            answer = format_input(input) 
            continue
    return int(answer)

def centre(title,symbol=" ",str_end="\n") :
    #aligns the title in centre with symbols around it
    gap = str(symbol)*(gap_len-int((len(title)/2)))
    gap2 = str(symbol)*((gap_len*2)- len(title) - len(gap))
    print(( middle + "|" + gap + title + gap2 + "|" + "\n" + middle + "|" + (gap_len*2)*" " + "|"),end=str_end)

def ans_check(option_list) :


    #prints and detetcs the answers and returns the choose answer
    centre("-","-")
    for i in option_list : 
        centre(symbol=" ", title=(str(option_list.index(i) + 1) + ".) " + str(i)))
    centre("-","-")
    ques = "Choose a option"
    string  = middle + "| " + ques  + " "*(((gap_len*2)-1)-(len(ques))) +  "|\n" + middle  + "| -" 
    answer = input(string)
    answer = answer.strip()
    answer = int_check(answer)
    while int(answer) > len(option_list) :
            centre("Not a valid answer !")
            answer = format_input("Choose a option")
            try :
                int(answer) 
            except  :
                answer = int_check(answer)
        
    return option_list[int(answer) - 1]

async def homescreen(search) :
    os.system('cls')
    centre("=","=")
    centre(f"Searching in {search}")
    centre("What task do you wish to perform?")
    option_list = [
        "Search for matches on a speicific date",
        "Search for matches on a speicific venue",
        "Search for matches of 2 teams",
        "Predict a match outcome",
        "View history of a team",
        "Enter new data",
        "Back"
        ]
    answer = ans_check(option_list=option_list)

    if answer == option_list[0] :
        await spe_date(search)

    elif answer == option_list[1] :
        await venue(search)

    elif answer == option_list[2]:
        await teams_vs(search)

    elif answer == option_list[3] :
        await predict(search)   

    elif answer == option_list[4] :
        await team(search)

    elif answer == option_list[5] :
        await enter_data(search)

async def teams_vs(search) :
    os.system('cls')
    centre('=', '=')
    conn = sqlite3.connect(str(search) + ".sqlite")
    cur = conn.cursor()

    cur.execute('SELECT match FROM "table"')
    matches = cur.fetchall()

    team_list = []
    for match in matches :
        match = match[0] 
        teams = str(match).split('vs')
        for team in teams : 
            team = team.strip()
            if team not in team_list :
                team_list.append(team)

    centre('Select TEAM 1')
    team_1 = ans_check(option_list=team_list)
    team_list.remove(team_1)
    os.system('cls')
    centre('=', '=')
    centre(f'TEAM 1 - {team_1}')

    centre('Select TEAM 2')
    team_2 = ans_check(option_list=team_list)
 
    string = team_1 + ' vs ' + team_2

    cur.execute(f'SELECT * FROM "table" WHERE "match" = "{string}"')
    data1 = cur.fetchall()

    string = team_2 + ' vs ' + team_1
    
    cur.execute(f'SELECT * FROM "table" WHERE "match" = "{string}"')
    data2 = cur.fetchall()

    for i in data2 : 
        data1.append(i)

    if data1 != [] :
        os.system('cls')
        centre('=', '=')
        centre(f'All the matches of {string} : ')
        team_1_wins = 0
        team_2_wins = 0 
        ties = 0 
        for data in data1 :

            date = data[0]
            venue = data[2]
            winner = data[3] 

            if (team_1 + " won") in winner :
                team_1_wins += 1

            elif (team_2 + " won") in winner :
                team_2_wins += 1
            
            else : 
                ties += 1

            centre(f"date : {date} | venue : {venue} | result : {winner}")
        centre(f'Total matches : {len(data1)}')
        centre(f"{team_1} wins : {team_1_wins} | {team_2} wins : {team_2_wins} | Ties : {ties}")
            
    else : 
        centre(f'No matches of {string}')
    
    ans_check(option_list=['back'])
    await homescreen(search)

async def spe_date(search) :
    os.system('cls')
    centre('=', '=')
    conn = sqlite3.connect(str(search) + ".sqlite")
    cur = conn.cursor()

    centre('DAY INPUT',"-")
    day = format_input('Enter the day')
    day = int_check(day, input='Enter the day')
    while not (1 <= day <= 31) :
        day = int_check(str(day) + ".", input='Enter the day')
    if (len(str(day))) < 2 :
        day = "0" + str(day) 

    centre('MONTH INPUT',"-")
    month = format_input('Enter the month')
    month = int_check(month, input='Enter the month')
    while not (1 <= month <= 12) :
        month = int_check(str(month) + ".",input='Enter the month')

    if (len(str(month))) < 2 :
        month = "0" + str(month) 

    centre('YEAR INPUT',"-")
    cur_year = datetime.date.today().year
    year = format_input('Enter the day')
    year = int_check(year, input='Enter the day')
    while(len(str(year))) < 4 or not (1877 < year <= cur_year) :
        year = int_check(str(year) + ".",input='Enter the day')

    date = f'{year}-{month}-{day}'
    norm_date = f'{day}-{month}-{year}'

    cur.execute(f'SELECT match, venue, winner FROM "table" WHERE "date" = "{date}" ')
    data = cur.fetchall()

    if data != [] :
        os.system('cls')
        centre('=', '=')
        centre(f'List of matches on {norm_date}')
        for i in data :
            match = i[0]
            venue = i[1]
            winner = i[2] 
            centre(f"match : {match} | venue : {venue} | result : {winner}")
    else : 
        centre(f'No {search} matches took place on {norm_date}')
         
    ans_check(option_list=['back'])
    await homescreen(search)

async def team(search) :
    os.system('cls')
    centre('=', '=')
    conn = sqlite3.connect(str(search) + ".sqlite")
    cur = conn.cursor()

    cur.execute('SELECT match FROM "table"')
    matches = cur.fetchall()

    team_list = []
    for match in matches :
        match = match[0] 
        teams = str(match).split('vs')
        for team in teams : 
            team = team.strip()
            if team not in team_list :
                team_list.append(team) 

    team = ans_check(option_list=team_list)

    cur.execute('SELECT * FROM "table"')
    data = cur.fetchall()

    filtered_data = []
    for i in data :
        if team in i[1] :
            filtered_data.append(i)

    if filtered_data != [] :
        os.system('cls')
        centre('=', '=')
        centre(f'All the matches of {team} : ')

        wins = 0
        loses = 0 
        ties = 0 
        for data in filtered_data :
            date = data[0]
            match = data[1]
            venue = data[2]
            winner = data[3]
            
            if (team + " won") in winner :
                wins += 1

            elif 'Tie' in winner :
                ties += 1
            
            else : 
                loses += 1
                 
            centre(f"date : {date} | match : {match} | venue : {venue} | result : {winner}")
        centre(f'Total matches : {len(filtered_data)}')
        centre(f" wins : {wins} | loeses : {loses} | Ties : {ties}")
    else :
        centre('No matches of this team found')
    
    ans_check(option_list=['back'])
    await homescreen(search)

async def enter_data(search):
    os.system('cls')
    centre('=', '=')

    pass_ = '123456'

    #checking pass
    pass_trials = 2
    ques = "Enter your password"
    string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
    input_pass = maskpass.advpass(prompt=string, mask="*")
    if input_pass.lower() != pass_ :

        while input_pass != pass_ and pass_trials > 0 : 

            centre("incorrect password ! you have {trials} trials left ".format(trials=pass_trials))
            ques = "Enter your password"
            string  = middle + "| " + ques  + " "*(127-(len(ques))) +  "|\n" + middle  + "| -" 
            input_pass = maskpass.advpass(prompt=string, mask="*")
            pass_trials -= 1
            if input_pass == pass_ :
                break 
    if pass_trials >= 0 and input_pass == pass_ :

        os.system('cls')
        centre('=', '=')
        conn = sqlite3.connect(str(search) + ".sqlite")
        cur = conn.cursor()

        centre('DATE INPUT','-')

        centre('DAY INPUT',"-")
        day = format_input('Enter the day')
        day = int_check(day, input='Enter the day')
        while not (1 <= day <= 31) :
            day = int_check(str(day) + ".", input='Enter the day')
        if (len(str(day))) < 2 :
            day = "0" + str(day) 

        centre('MONTH INPUT',"-")
        month = format_input('Enter the month')
        month = int_check(month, input='Enter the month')
        while not (1 <= month <= 12) :
            month = int_check(str(month) + ".",input='Enter the month')

        if (len(str(month))) < 2 :
            month = "0" + str(month) 

        centre('YEAR INPUT',"-")
        cur_year = datetime.date.today().year
        year = format_input('Enter the day')
        year = int_check(year, input='Enter the day')
        while(len(str(year))) < 4 or not (1877 < year <= cur_year) :
            year = int_check(str(year) + ".",input='Enter the day')

        date = f'{year}-{month}-{day}'
        norm_date = f'{day}-{month}-{year}'

        os.system('cls')
        centre('=', '=')

        centre(f'Input date : {norm_date}'  )

        centre('=', '=')

        centre('VENUE INPUT')
        venue = format_input('Enter a city name')
        venue = venue.capitalize()

        os.system('cls')
        centre('=', '=')

        centre(f'Input date : {norm_date}'  )
        centre(f'Venue input : {venue}')

        centre('=', '=')

        centre('TEAM SELECTION')
        cur.execute('SELECT match FROM "table"')
        matches = cur.fetchall()

        team_list = []
        for match in matches :
            match = match[0] 
            teams = str(match).split('vs')
            for team in teams : 
                team = team.strip()
                if team not in team_list :
                    team_list.append(team)

        centre('Select TEAM 1')
        team_1 = ans_check(option_list=team_list)
        team_list.remove(team_1)

        os.system('cls')
        centre('=', '=')
        centre(f'TEAM 1 - {team_1}')

        centre('Select TEAM 2')
        team_2 = ans_check(option_list=team_list)

        match = f"{team_1} vs {team_2}"

        os.system('cls')
        centre('=', '=')

        centre(f'Input date : {norm_date}'  )
        centre(f'Input venue : {venue}')
        centre(f'Input match : {match}')

        centre('=', '=')

        centre('SELECT WINNER')
        winner = ans_check(option_list=[team_1,team_2, 'Tie'])

        if winner != 'Tie' :
            centre('SELECT WINNING SITUATION')
            win_sit = ans_check(option_list=['Wickets',"Runs"])

            centre('ENTER THE MARGIN')
            win_mar = format_input('Enter a number')
            win_mar = int_check(win_mar)
            if win_sit == "Wickets" :
                while win_mar > 11 :
                    centre('Invalid ! wickets can only be less than 10')
                    win_mar = int_check(str(win_mar) + '.')
            
            result = f'{winner} won by {win_mar} {win_sit}'

        else : 
            result = 'Tie'

        os.system('cls')
        centre('=', '=')

        centre(f'date : {norm_date} | venue : {venue} | match : {match} | winner : {result}')
        ans = ans_check(option_list=['Confirm','Cancel'])

        if ans == 'Confirm' :

            cur.execute(f'INSERT INTO "table" VALUES ( "{date}", "{match}", "{venue}", "{result}")')
            centre('Data saved')

        else :

            centre('Cancelled')
        
        cur.close()
        await redirect('Homescreen')
        await homescreen(search)

async def venue(search):
    os.system('cls')
    centre('=', '=')
    conn = sqlite3.connect(str(search) + ".sqlite")
    cur = conn.cursor()

    cur.execute('SELECT venue FROM "table"')
    venues = cur.fetchall()

    venue_list = []
    for venue in venues :
        venue = venue[0] 
        if venue not in venue_list :
            venue_list.append(venue) 

    venue = ans_check(option_list=venue_list)

    cur.execute(f'SELECT * FROM "table" WHERE "venue" = "{venue}"')
    data = cur.fetchall()

    if data != [] :
        os.system('cls')
        centre('=', '=')
        centre(f'List of matches in {venue}')
        for i in data :
            date = i[0]
            match = i[1]
            venue = i[2]
            winner = i[3] 
            centre(f"date : {date} | match : {match} | result : {winner}")
    else : 
        centre(f'No {search} matches took place in {venue}')
         
    ans_check(option_list=['back'])
    await homescreen(search)

async def predict(search):
    os.system('cls')
    centre('=', '=')
    conn = sqlite3.connect(str(search) + ".sqlite")
    cur = conn.cursor()
    
    cur.execute('SELECT match FROM "table"')
    matches = cur.fetchall()

    team_list = []
    for match in matches :
        match = match[0] 
        teams = str(match).split('vs')
        for team in teams : 
            team = team.strip()
            if team not in team_list :
                team_list.append(team)

    centre('Select TEAM 1')
    team_1 = ans_check(option_list=team_list)
    team_list.remove(team_1)
    os.system('cls')
    centre('=', '=')
    centre(f'TEAM 1 - {team_1}')

    centre('Select TEAM 2')
    team_2 = ans_check(option_list=team_list)
 
    string = team_1 + ' vs ' + team_2

    cur.execute(f'SELECT * FROM "table" WHERE "match" = "{string}"')
    data1 = cur.fetchall()

    string = team_2 + ' vs ' + team_1
    
    cur.execute(f'SELECT * FROM "table" WHERE "match" = "{string}"')
    data2 = cur.fetchall()

    for i in data2 : 
        data1.append(i)

    if data1 != [] :
        os.system('cls')
        for i in loading_list :
            print(i,end='\r')
            #await asyncio.sleep(2)
        os.system('cls')
        centre('=', '=')
        team_1_wins = 0
        team_2_wins = 0 
        ties = 0 
        for data in data1 :

            winner = data[3] 

            if (team_1 + " won") in winner :
                team_1_wins += 1

            elif (team_2 + " won") in winner :
                team_2_wins += 1
            
            else : 
                ties += 1

        matches = len(data1) - ties 

        win_per_1 = int((team_1_wins/matches)*100)
        win_per_2 = int((team_2_wins/matches)*100)
    else : 
        win_per_1 = 50
        win_per_2 = 50
    centre(f'Win probability of {team_1} vs {team_2}')
    win_str = win_per_1*"■" + win_per_2*"□"
    centre(win_str)
    gap = " "*(88 - len(team_1) - len(team_2))
    matches_str = f"{team_1} ({win_per_1}%){gap}{team_2} ({win_per_2}%)"
    centre(matches_str)
    ans_check(option_list=['back'])
    await homescreen(search)



file = open("design.txt",encoding= "utf8")
lines = file.readlines()
file.close()



file = open("loading.txt", "r+",encoding='utf8')
loading = file.readlines()
file.close()
loading_list = []
string = ""
for i in loading :
    try : 
        int(i.strip('\n'))
        loading_list.append(string.rstrip("\n"))
        string = ""
    except :
        gap = " "*(gap_len*2 - int((len(i))) - 50)
        string += middle + "|" + " "*(50)  +  i.strip("\n") +  gap + "|\n"



while True :
    os.system('cls')
    for i in  lines : 
        print(middle + i.strip('\n'))
    centre("Where do you wish to search ?")
    search = ans_check(option_list=["ODI", "IPL", "T20",'EXIT'])
    if search != 'EXIT' :
        asyncio.run(homescreen(search))
    else :
        break

    
  