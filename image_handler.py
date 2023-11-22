from PIL import Image
import discord
import os

class ImageHandler:
    def __init__(self, requester_id: str, path: str) -> None:
        self.requester = requester_id
        self.path = path
        self.extension = path.rsplit('.',1)[1]
        self.output_name = self.path + requester_id + '.output.' + self.extension
        self.image = Image.open(self.path)
        pass

    def greyscale(self):
        output = self.image.convert('L')
        output.save(self.output_name)
        return self.output_name
    
    
    def get_output(self):
        return discord.File(self.output_name)
    

    def delete_output(self):
        os.remove(self.output_name)


if __name__ == "__main__":
    #print("aa.da/test.png".rsplit('.',1)[1])
    ImageHandler('1111111', 'tmp/dog.jpg').greyscale()