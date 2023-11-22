from jinja2 import Template

class Strings:
    def __init__(self) -> None:
        self.string_success = 'Sucesso!'
        self.string_error = 'Erro!'
        self.string_inexistent_user = 'O usuário {{ user }} não existe!'
        self.string_calc_result = 'O resultado é: {{ result }}'
        self.string_invalid_video = 'Vídeo inválido'

        pass

    def render(self, src, params):
        return Template(src).render(params)

    def user_dont_exists(self, user):
        return self.render(self.string_inexistent_user, {'user': user})
        pass

if __name__ == "__main__":
    print(Strings().user_dont_exists("0xp1p3 {{7*7}}"))
    pass