import numpy as np

class CDMA:
    def __init__(self):
        self.wtable = None
        self.copy = None
        self.channel_sequence = None

    def setUp(self, data, num_stations):
        self.wtable = np.zeros((num_stations, num_stations), dtype=int)
        self.copy = np.zeros((num_stations, num_stations), dtype=int)
 
        self.buildWalshTable(num_stations, 0, num_stations - 1, 0, num_stations - 1, False)
        self.showWalshTable(num_stations)
 
        for i in range(num_stations):
            for j in range(num_stations):
                self.copy[i][j] = self.wtable[i][j]
                self.wtable[i][j] *= data[i]
 
        self.channel_sequence = np.zeros(num_stations, dtype=int)
        for i in range(num_stations):
            for j in range(num_stations):
                self.channel_sequence[i] += self.wtable[j][i]

    def listenTo(self, sourceStation, num_stations): 
        innerProduct = 0
        for i in range(num_stations):
            innerProduct += self.copy[sourceStation][i] * self.channel_sequence[i]
        print("The data received is:", innerProduct // num_stations)

    def buildWalshTable(self, length, i1, i2, j1, j2, isBar):
        # Base case: length = 2
        if length == 2:
            if not isBar:
                self.wtable[i1][j1] = 1
                self.wtable[i1][j2] = 1
                self.wtable[i2][j1] = 1
                self.wtable[i2][j2] = -1
            else:
                self.wtable[i1][j1] = -1
                self.wtable[i1][j2] = -1
                self.wtable[i2][j1] = -1
                self.wtable[i2][j2] = 1
            return

        midi = (i1 + i2) // 2
        midj = (j1 + j2) // 2

        self.buildWalshTable(length // 2, i1, midi, j1, midj, isBar)
        self.buildWalshTable(length // 2, i1, midi, midj + 1, j2, isBar)
        self.buildWalshTable(length // 2, midi + 1, i2, j1, midj, isBar)
        self.buildWalshTable(length // 2, midi + 1, i2, midj + 1, j2, not isBar)

    def showWalshTable(self, num_stations): 
        print("\nWalsh Table:")
        for i in range(num_stations):
            for j in range(num_stations):
                print(self.wtable[i][j], end=" ")
            print()
        print("-------------------------\n")


def main():
    # Get user input for data bits
    data = []
    num_stations = 4  # Number of stations (you can change this if needed)
    
    for i in range(num_stations):
        bit = int(input(f"Enter the data bit for Station {i+1} (-1 or 1): "))
        while bit not in [-1, 1]:
            print("Invalid input. Please enter -1 or 1.")
            bit = int(input(f"Enter the data bit for Station {i+1} (-1 or 1): "))
        data.append(bit)
    
    # Initialize the CDMA object and set up the system
    channel = CDMA()
    channel.setUp(data, num_stations)

    # Station you want to listen to
    sourceStation = int(input(f"Enter the station to listen to (1-{num_stations}): ")) - 1
    while sourceStation < 0 or sourceStation >= num_stations:
        print("Invalid station number.")
        sourceStation = int(input(f"Enter the station to listen to (1-{num_stations}): ")) - 1

    # Listen to the selected station
    channel.listenTo(sourceStation, num_stations)

if __name__ == "__main__":
    main()
