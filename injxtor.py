import os, json, platform
from PIL import Image

class ImageTextInjectorAL:
    def __init__(self, imageFile: str):
        with open('syntax.json', 'r') as f:
            self.encoding = json.load(f)
        self.totalEncodingChars = len(self.encoding.keys())
            
        self.file = imageFile
        
        self.image = Image.open(imageFile)
        self.pixels = self.image.load()
        self.size = self.image.size

        self.encodingValues = []

        self.width = []
        self.height = []
    
    def encode(self, encode: str):
        self.text = encode.lower()
        
        for character in self.text:
            self.encodingValues.append(self.encoding[character])
        count = 0
        for height in range(0, self.size[0]):
            for width in range(0, self.size[1]):
                R = self.pixels[height, width][0]
                G = self.pixels[height, width][1]
                B = self.pixels[height, width][2]
                A = self.pixels[height, width][3]
                if A >= 220 and A > self.totalEncodingChars:
                    self.pixels[height, width] = (R,G,B, A-self.totalEncodingChars)
                if count < len(self.encodingValues):
                    self.pixels[height, width] = (R,G,B, int(self.encodingValues[count]))
                    count += 1
        self.image.save('output.png')
    
    def decode(self):
        self.decodedText = []
        for height in range(0, self.size[0]):
            for width in range(0, self.size[1]):
                A = self.pixels[height, width][3]
                if A < 220:
                    continue
                self.decodedText.append(list(self.encoding.keys())[list(self.encoding.values()).index(str(A))])
        self.decodedText = "".join(self.decodedText)
        return self.decodedText

def logo(style):
    prefix = "\033[32m"
    suffix = "\033[0m\n\n"
    if style == "poisonBig":
        return f"{prefix}@@@  @@@  @@@       @@@  @@@  @@@  @@@@@@@   @@@@@@   @@@@@@@\n@@@  @@@@ @@@       @@@  @@@  @@@  @@@@@@@  @@@@@@@@  @@@@@@@@\n@@!  @@!@!@@@       @@!  @@!  !@@    @@!    @@!  @@@  @@!  @@@\n!@!  !@!!@!@!       !@!  !@!  @!!    !@!    !@!  @!@  !@!  @!@\n!!@  @!@ !!@!       !!@   !@@!@!     @!!    @!@  !@!  @!@!!@!\n!!!  !@!  !!!       !!!    @!!!      !!!    !@!  !!!  !!@!@!\n!!:  !!:  !!!       !!:   !: :!!     !!:    !!:  !!!  !!: :!!\n:!:  :!:  !:!  !!:  :!:  :!:  !:!    :!:    :!:  !:!  :!:  !:!\n ::   ::   ::  ::: : ::   ::  :::     ::    ::::: ::  ::   :::\n:    ::    :    : :::     :   ::      :      : :  :    :   : :{suffix}"
    elif style == "poisonSmall":
        return f"{prefix} @@@ @@@  @@@     @@@ @@@  @@@ @@@@@@@  @@@@@@  @@@@@@@ \n @@! @@!@!@@@     @@! @@!  !@@   @@!   @@!  @@@ @@!  @@@\n !!@ @!@@!!@!     !!@  !@@!@!    @!!   @!@  !@! @!@!!@! \n !!: !!:  !!! .  .!!   !: :!!    !!:   !!:  !!! !!: :!! \n :   ::    :  ::.::   :::  :::    :     : :. :   :   : :{suffix}"
    elif style == "ghost":
        return f"{prefix} ██▓ ███▄    █  ▄▄▄██▀▀▀▒██   ██▒▄▄▄█████▓ ▒█████   ██▀███  \n▓██▒ ██ ▀█   █    ▒██   ▒▒ █ █ ▒░▓  ██▒ ▓▒▒██▒  ██▒▓██ ▒ ██▒\n▒██▒▓██  ▀█ ██▒   ░██   ░░  █   ░▒ ▓██░ ▒░▒██░  ██▒▓██ ░▄█ ▒\n░██░▓██▒  ▐▌██▒▓██▄██▓   ░ █ █ ▒ ░ ▓██▓ ░ ▒██   ██░▒██▀▀█▄  \n░██░▒██░   ▓██░ ▓███▒   ▒██▒ ▒██▒  ▒██▒ ░ ░ ████▓▒░░██▓ ▒██▒\n░▓  ░ ▒░   ▒ ▒  ▒▓▒▒░   ▒▒ ░ ░▓ ░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░\n ▒ ░░ ░░   ░ ▒░ ▒ ░▒░   ░░   ░▒ ░    ░      ░ ▒ ▒░   ░▒ ░ ▒░\n ▒ ░   ░   ░ ░  ░ ░ ░    ░    ░    ░      ░ ░ ░ ▒    ░░   ░ \n ░           ░  ░   ░    ░    ░               ░ ░     ░     {suffix}"
    elif style == "terra":
        return f"{prefix} ▄▀▀█▀▄    ▄▀▀▄ ▀▄        ▄█  ▄▀▀▄  ▄▀▄  ▄▀▀▀█▀▀▄  ▄▀▀▀▀▄   ▄▀▀▄▀▀▀▄ \n█   █  █  █  █ █ █  ▄▀▀▀█▀ ▐ █    █   █ █    █  ▐ █      █ █   █   █ \n▐   █  ▐  ▐  █  ▀█ █    █    ▐     ▀▄▀  ▐   █     █      █ ▐  █▀▀█▀  \n    █       █   █  ▐    █         ▄▀ █     █      ▀▄    ▄▀  ▄▀    █  \n ▄▀▀▀▀▀▄  ▄▀   █     ▄   ▀▄      █  ▄▀   ▄▀         ▀▀▀▀   █     █   \n█       █ █    ▐      ▀▀▀▀     ▄▀  ▄▀   █                  ▐     ▐   \n▐       ▐ ▐                   █    ▐    ▐                            {suffix}"

# Main Program
titlePrefix = "\u001b[34m"+"[*] "+"\u001b[0m"
infoPrefix = "\u001b[37m"+"["+"\u001b[0m"+  "\u001b[35m"+"?"+"\u001b[0m"  +"\u001b[37m"+"] "+"\u001b[0m"
errorPrefix = "\u001b[37m"+"["+"\u001b[0m"+  "\u001b[31m"+"!"+"\u001b[0m"  +"\u001b[37m"+"] "+"\u001b[0m"

currentOS = platform.platform()
if currentOS.lower().startswith("windows"):
    default = logo("ghost")
else:
    default = logo("ghost")
    
if currentOS.lower().startswith("windows") == False and currentOS.lower().startswith("linux") == False:
    print(errorPrefix+"Error, unsupported OS.")
    exit()
else:
    if currentOS.lower().startswith("windows"):
        os.system("cls")
    else:
        os.system("clear")
    print(default)

while True:
    try:
        command = input("\u001b[37m"+"injxtor~$ "+"\u001b[0m")
        
        try:
            if command == "clear":
                if currentOS.lower().startswith("windows"):
                    os.system("cls")
                else:
                    os.system("clear")
                print(default)
            elif command.startswith("encode"):
                command = command.removeprefix("encode ")
                parameters = command.split(" ")

                image = parameters[0]
                text = " ".join(parameters[1:])
                
                ImageTextInjectorAL(image, text).encode()
            elif command.startswith("decode"):
                command = command.removeprefix("decode ")
                parameters = command
                
                image = parameters[0]
                text = ImageTextInjectorAL(image).decode()
                
                with open(image.split(".")[0]+".txt", "w") as f:
                    f.write(text)

            if command != "" and command != "clear":
                print()
        except:
            print(errorPrefix+f"Error, Command '{command}' could not be executed. Check the syntax of the command\n")
    except:
        if currentOS.lower().startswith("windows"):
            os.system("cls")
        else:
            os.system("clear")
        print(default)