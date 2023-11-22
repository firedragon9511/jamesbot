import discord, uuid


class PollHandler:
    class Poll:
        def __init__(self, guid: str, title: str, options: list, owner: str) -> None:
            self.guid = guid
            self.title = title
            self.owner = owner

            print(f'Enquete {title} criada por {self.owner}')
            
            self.options = {

            }

            self.voters = []

            for o in options:
                self.options[o] = 0

            pass

        def has_option(self, option):
            return option in self.options


        def get_string(self):
            text = ['Para votar nas opções abaixo utilize o comando vote <title> <option>','']
            for o in self.options:
                text.append(o)
            return '\n'.join(text)
            
            
        def user_voted(self, username):
            return username in self.voters
        

        def vote(self, username, option):
            if self.user_voted(username):
                return
            
            self.options[option] += 1
            self.voters.append(username)


        def get_results(self):
            text = ['Resultado:']
            for key, value in self.options.items():
                text.append(f'{key} teve {value} votos')

            return '\n'.join(text)


    def __init__(self) -> None:
        self.polls: dict = {}
        pass

    def poll_exists(self, guild: str, title: str):
        return guild + title in self.polls


    def get_poll(self, guild: str, title: str) -> Poll:
        print(self.polls)
        return self.polls[guild + title]
    

    def is_owner(self, poll: Poll, username: str):
        return username == poll.owner
    

    def finalize_poll(self, guild: str, title: str):
        poll = self.get_poll(guild, title)
        result = poll.get_results()
        del self.polls[guild + title]
        return result


    def create_poll(self, guild: str, title: str, options: list, owner: str) -> Poll:
        self.polls[guild + title] = self.Poll(guild, title, options, owner)
        return self.polls[guild + title]

   