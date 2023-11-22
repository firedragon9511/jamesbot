import discord, re, random, string, traceback
import jinja2
from strings import Strings
import sqlite3
from video_player import VideoPlayer

from database_handler import DatabaseHandler
from poll_handler import PollHandler
from image_handler import ImageHandler
from download_handler import DownloadHandler

class CommandHandler:
    def __init__(self, client) -> None:
        self.client = client
        self.prefix = '!'

        self.strings = Strings()
        self.database_handler = DatabaseHandler()

        self.poll_handler = PollHandler()

        self.download_handler = DownloadHandler()
        pass

    def get_args(self, command):
        matches = re.findall(r'"(.*?)"|\'(.*?)\'|(\S+)', command)
        return [match[0] or match[1] or match[2] for match in matches]
    

    def calc(self, expression):
        return eval(expression)
    

    def random_string(self, size):
        try:
            return ''.join([random.choice(string.ascii_letters) for x in range(int(size))])
        except Exception as e:
            return traceback.format_exc()


    def create_embed(self, title, text):
        embed=discord.Embed(title=title, description=text)
        return embed


    async def handle_welcome(self, member: discord.Member):
        result = self.database_handler.get_guild_messages(member.guild.id)
        if result is not None:
            await self.send(member)


    async def send_file(self, channel, file: discord.File):
        await channel.send(file=file)


    async def send(self, channel, message):
        await channel.send(message)


    async def send_embed(self, channel, message):
        await channel.send(embed=message)


    async def help_embed(self, channel):
        embed=discord.Embed(title="Comandos gerais", description="James, o seu assistente do Discord")
        embed.add_field(name="!help", value="Mostra esta mensagem", inline=True)
        embed.add_field(name="!play", value="Tocar uma música, <url>", inline=True)
        embed.add_field(name="!avatar", value="Mostrar avatar de um usuário", inline=True)
        embed.add_field(name="!userinfo", value="Mostrar informações de um usuário", inline=True)
        await channel.send(embed=embed)

        embed=discord.Embed(title="Administração", description="Administração do servidor")
        embed.add_field(name="!setmessages", value="Alterar mensagens, <channel> <welcome> <goodbye>", inline=True)
        embed.add_field(name="!ban", value="Banir um usuário", inline=True)
        embed.add_field(name="!kick", value="Kickar usuário", inline=True)
        await channel.send(embed=embed)

        embed=discord.Embed(title="Diversos", description="Comandos diversos")
        embed.add_field(name="!calc", value="Calcula uma empressão", inline=True)
        embed.add_field(name="!say", value="Fazer o bot falar algo", inline=True)
        embed.add_field(name="!custom", value="Criar um comando customizável <comando> <mensagem>", inline=True)
        embed.add_field(name="!poll", value="Criar uma enquete. '<title>' '<option1,option2,option3...>'", inline=True)
        embed.add_field(name="!vote", value="Votar em uma enquete criada '<title>' '<option>'", inline=True)
        embed.add_field(name="!fpoll", value="Finalizar enquete '<title>'", inline=True)
        embed.add_field(name="!random", value="Gerar caracteres aleatórios. <size>", inline=True)
        embed.add_field(name="!imagegrey", value="Pega uma imagem e transforma em preto e branco. <url>", inline=True)
        await channel.send(embed=embed)


    def is_command(self, arg0, cmd ):
        return arg0 == f'{self.prefix}{cmd}'
        

    async def handle(self, message: discord.Message):
        if not message.content.strip().startswith(self.prefix):
            return
        
        args = self.get_args(message.content)
        invalid_command = True

        if args[0] == f'{self.prefix}help':
            invalid_command = False
            await self.help_embed(message.channel)

        if args[0] == f'{self.prefix}calc':
            invalid_command = False
            await self.send(
                message.channel, 
                self.strings.render(self.strings.string_calc_result, {'result' : self.calc(args[1])})
            )

        if args[0] == f'{self.prefix}custom':
            invalid_command = False
            self.database_handler.insert_custom_command(message.guild.id, args[1], args[2]) 
            

        if args[0] == f'{self.prefix}play':
            invalid_command = False
            if not VideoPlayer.is_video(args[1]):
                await self.send_embed(message.channel, self.create_embed(self.strings.string_error, self.strings.string_invalid_video))


        if self.is_command(args[0], 'poll'):
            if not self.poll_handler.poll_exists(str(message.guild.id), args[1]):
                poll: PollHandler.Poll = self.poll_handler.create_poll(str(message.guild.id), args[1], args[2].split(','), message.author.name)
                await self.send_embed(message.channel, self.create_embed(f'Enquete criada por {message.author}!', poll.get_string()))
            else:
                await self.send_embed(message.channel, self.create_embed(self.strings.string_error, 'Enquete já existe!'))
            pass

        if self.is_command(args[0], 'vote'):
            if self.poll_handler.poll_exists(str(message.guild.id), args[1]):      
                poll = self.poll_handler.get_poll(str(message.guild.id), args[1])
                if not poll.user_voted(message.author.name):
                    if poll.has_option(args[2]):
                        poll.vote(message.author.name, args[2])
                        await self.send_embed(message.channel, self.create_embed(self.strings.string_success, f'Você votou em \'{args[2]}\' na enquete \'{args[1]}\''))
                    else:
                        await self.send_embed(message.channel, self.create_embed(self.strings.string_error, f'A opção \'{args[2]}\' não existe na enquete \'{args[1]}\''))
                else:
                        await self.send_embed(message.channel, self.create_embed(self.strings.string_error, f'Você já votou nessa enquete!'))
            else:
                await self.send_embed(message.channel,  self.create_embed(self.strings.string_error, 'Enquete não existe!'))
            pass

        if self.is_command(args[0], 'fpoll'):
            if self.poll_handler.poll_exists(str(message.guild.id), args[1]):
                if self.poll_handler.is_owner(self.poll_handler.get_poll(str(message.guild.id), args[1]), message.author.name):
                    result = self.poll_handler.finalize_poll(str(message.guild.id), args[1])
                    await self.send_embed(message.channel, self.create_embed(self.strings.string_success, result))
                else:
                    await self.send_embed(message.channel, self.create_embed(self.strings.string_error, 'Você precisa ser o dono para finalizar esta enquete!'))

            else:
                await self.send_embed(message.channel, self.create_embed(self.strings.string_error, 'Enquete não existe!'))
            pass


        if self.is_command(args[0], 'random'):
            await self.send(message.channel, f'O resultado é: {self.random_string(args[1])}')
            pass

        if self.is_command(args[0], 'imagegrey'):
            path = self.download_handler.download_file(args[1], 'tmp', type_verify='image')
            image_handler = ImageHandler(str(message.author.id), path)
            image_handler.greyscale()
            await self.send_file(message.channel, image_handler.get_output())
            
            image_handler.delete_output()
            #await self.send(message.channel, f'O resultado é: {self.random_string(args[1])}')
            pass


        if invalid_command:
            try_cmd = self.database_handler.get_custom_command(str(message.guild.id), args[0].replace(self.prefix, ''))
            if try_cmd is not None:
                await self.send(message.channel, try_cmd)


if __name__ == "__main__":
    #print(CommandHandler(None).get_args("!say \"oi aaa\" oi oi"))
    #print(CommandHandler(None).random_string('3'))
    #print(eval('__import__(\'os\').system(\'dir\')'))
    pass