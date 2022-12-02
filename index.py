from discord import app_commands, Intents, Client, Interaction
import requests

print("\n".join([
    "Привет, добро пожаловать в бота для получения значка активного разработчика.",
    "Пожалуйста, введите токен вашего бота ниже, чтобы продолжить.",
    "",
    "Не закрывайте данное приложение после ввода токена."
    "Но вы можете закрыть его после приглашения бота и выполнения команды."
]))


while True:
    token = input("> ")

    r = requests.get("https://discord.com/api/v10/users/@me", headers={
        "Authorization": f"Bot {token}"
    })

    data = r.json()
    if data.get("id", None):
        break

    print("\nПохоже, вы ввели неверный токен. Попробуйте еще раз.")


class FunnyBadge(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """ Это вызывается при загрузке бота для настройки глобальных команд. """
        await self.tree.sync(guild=None)


client = FunnyBadge(intents=Intents.none())


@client.event
async def on_ready():
    """ Это вызывается, когда бот готов и имеет соединение с Discord
        Он также пишет URL-адрес инвайта бота, который автоматически использует ваш
        Идентификатор клиента, чтобы убедиться, что вы приглашаете правильного бота с правильными областями.
    """
    print("\n".join([
        f"Вы вошли как {client.user} (ID: {client.user.id})",
        "",
        f"Используйте этот URL, чтобы пригласить {client.user} на ваш сервер:",
        f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot"
    ]))


async def _init_command_response(interaction: Interaction) -> None:
    """ Это вызывается при запуске команды
        Причина, по которой команда находится вне командной функции
        это потому, что есть два способа запустить команду и команды с косой чертой
        изначально не поддерживают псевдонимы, поэтому нам приходится их подделывать.
    """


    print(f"> {interaction.user} used the command.")

    await interaction.response.send_message("\n".join([
        f"Привет **{interaction.user}**, спасибо, что поздоровались со мной.",
        "",
        "__**Где мой значок?**__",
        "Право на получение значка периодически проверяется Discord., "
        "в данный момент рекомендуется подождать 24 часа.",
        "",
        "__**Прошло 24 часа, как мне получить значок?**__",
        "Если уже прошло 24 часа, вы можете отправиться в "
        "https://discord.com/developers/active-developer и заполнить 'форму' там.",
        "",
        "__**Обновление значка активного разработчика**__",
        "Обновления, касающиеся значка активного разработчика, можно найти в "
        "Дискорд сервер разработчиков -> discord.gg/discord-developers - в #active-dev-badge канале.",
    ]))


@client.tree.command()
async def hello(interaction: Interaction):
    """ Скажите привет или еще что-то """
    await _init_command_response(interaction)


@client.tree.command()
async def givemebadge(interaction: Interaction):
    """ Говорите привет или что-то в этом роде, но под другим именем аккаунта """
    await _init_command_response(interaction)


client.run(token)