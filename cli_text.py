from PIL import Image
import pprint

class Textify():
    def __init__(self):
        self.letters = "abcdefghijklmnopqrstuvwxyz_"
        self.letters_dict = {}
        for x in self.letters:
            self.letters_dict[x] = Image.open(".//cli_icons//{}.png".format(x))
    def parse_letter(self,letter):
        image = self.letters_dict.get(letter)
        return_string = ""
        return_list = []
        for y in range(image.size[1]):
            temp_list = ""
            for x in range(image.size[0]):
                #print(image.getpixel((x,y)))
                if(image.getpixel((x,y))) == (0,0,0,255):
                    temp_list += "*"
                else:temp_list += " "
            return_list.append(temp_list)
        return return_list
    def print_string(self,string):
        total = []
        for letter in string:
            total.append(self.parse_letter(letter))
        return_string = ""
        for x in range(33):
            for letter in total:
                return_string += letter[x]
            return_string += "\n"
        return return_string


