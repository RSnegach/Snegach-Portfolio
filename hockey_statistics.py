import json
class Stats:

    def __init__(self, file:str):
        self.file = file
        with open(self.file, 'r') as file:
            data = file.read()

        self.players = json.loads(data)

    def print_player(self, player):
        name = player["name"]
        team = player["team"]
        assists = int(player["assists"])
        goals = int(player["goals"])
        points = assists + goals

        if points < 10:
            point_spaces = "   "
        elif points >= 10:
            point_spaces = "  "
        elif points >= 100:
            point_spaces = " "

        if assists < 10:
            assist_spaces = "  "
        elif assists >= 10:
            assist_spaces = " "
        print(f"{name:21}{team:5}{goals:>2} +{assist_spaces}{assists:1>} ={point_spaces}{points}")

    def search_for_player(self, name:str):
        player = list(filter(lambda player: player["name"] == name, self.players))[0]
        self.print_player(player)

    def teams(self):
        teams_list = sorted(set(map(lambda player:player["team"], self.players)))
        for team in teams_list:
            print(team)
        
    def countries(self):
        countries_list = sorted(set(map(lambda player:player["nationality"], self.players)))
        for country in countries_list:
            print(country)

    def players_in_team(self, team:str):
        players = list(filter(lambda player: player["team"] == team, self.players))
        sorted_by_points = sorted(players, key= lambda player: player["goals"] + player["assists"], reverse = True)

        for player in sorted_by_points:
            self.print_player(player)

    def players_from_country(self, country:str):
        players = list(filter(lambda player: player["nationality"] == country, self.players))
        sorted_by_points = sorted(players, key= lambda player: player["goals"] + player["assists"], reverse = True)

        for player in sorted_by_points:
            self.print_player(player)

    def most_points(self, amount:int):
        sorted_by_points = sorted(self.players, key= lambda player: (player["goals"] + player["assists"],player["goals"]), reverse = True)

        count = 0
        while count < amount:
            self.print_player(sorted_by_points[count])
            count +=1

    def most_goals(self, amount:int):
        sorted_by_goals = sorted(self.players, key= lambda player: (player["goals"],player["games"]*-1), reverse = True)

        count = 0
        while count < amount:
            self.print_player(sorted_by_goals[count])
            count +=1

class Application:

    def __init__(self):
        self.stats = None
    
    def help(self):
        print("commands:")
        print("0 quit")
        print("1 search for player")
        print("2 teams")
        print("3 countries")
        print("4 players in team")
        print("5 players from country")
        print("6 most points")
        print("7 most goals")

    def search_for_player(self):
        name = input("name: ")
        self.stats.search_for_player(name)

    def teams(self):
        self.stats.teams()

    def countries(self):
        self.stats.countries()

    def players_in_team(self):
        team = input("team:")
        self.stats.players_in_team(team)

    def players_from_country(self):
        country = input("country:")
        self.stats.players_from_country(country)

    def most_points(self):
        amount = int(input("how many:"))
        self.stats.most_points(amount)

    def most_goals(self):
        amount = int(input("how many:"))
        self.stats.most_goals(amount)

    def execute(self):
        filename = input("file name:")
        self.stats = Stats(filename)
        print(f"read the data of {len(self.stats.players)} players\n")

        while True:
            self.help()
            command = int(input("command:"))
            if command == 1:
                self.search_for_player()
            elif command == 2:
                self.teams()
            elif command == 3:
                self.countries()
            elif command == 4:
                self.players_in_team()
            elif command == 5:
                self.players_from_country()
            elif command == 6:
                self.most_points()
            elif command == 7:
                self.most_goals()
            elif command == 0:
                return
            else:
                continue
        
t = Application()
t.execute()
