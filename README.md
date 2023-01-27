<h1 align="center">💎 Terra - Python Discord Bot 💎</h1>

> # **Shortcuts**
- > [About](#-about)
- > [Features](#-features)
- > [Planned Features](#-planned-features)
- > [Contributing](#-contributing)
- > [Support](#-support)
- > [Requirements](#-requirements)
- > [How To Migrate (Update) DB](#-how-to-migrate-update-db)

---
<h1 align="center"><b>👋 About</b></h1>

`Terra` is growing open-source Discord bot that have some useful stuff.</br>
We aiming to implement as many useful bot functionality as we can.

> Note: This project was created mainly for our portfolio, so **please do not create pool requests**, **sorry**. Please check out our [Contributing](#-contributing) section for more information.

If you want to try it out by yourself, you can invite it to your Discord server by clicking [Here](https://discordapp.com/oauth2/authorize?client_id=769398326532898856&permissions=8&scope=bot)!

---
<h1 align="center"><b>🌟 Features</b></h1>

> Commands syntax: **`command`** **&lt;`required`&gt;** **[`optional`]**

<details>
    <summary>General commands</summary>

    help - Shows help message. If command name is specified, shows help message for that command.
        Syntax: help [Command Name]
</details>

<details>
    <summary>User's commands</summary>

    profile - Shows user's profile.
        Syntax: profile [Server Member]
</details>

<details>
    <summary>Fun commands</summary>

    8ball - Ask the magic 8 ball a question.
        Syntax: 8ball <Question>
        Aliases: 8b, magic8ball, magic8b

    coinflip - Flip a coin and guess which side (heads or tails) it will land on.
        Syntax: coinflip <Coin Side>
</details>

<details>
    <summary>Util commands</summary>

    first-message - Shows first message in channel.
        Syntax: first-message
        Aliases: firstmsg, fmsg
</details>

---
<h1 align="center"><b>📅 Planned Features</b></h1>

You can find current updates plan in [TODO.md](https://github.com/TerraFaster/Terra/blob/master/TODO.md) file!

---
<h1 align="center"><b>🤝 Contributing</b></h1>

As it was described in [About](#-about) section, this project was created mainly for our portfolio, so **please do not create pool requests**, **sorry**.

> But your ideas, suggestions and bug reports are welcome! Feel free to check out our [issues page](https://github.com/TerraFaster/Terra/issues) to find out what you could do!

---
<h1 align="center"><b>💖 Support</b></h1>

You can support us by:
- > Joining to our discord [Support Server](https://discord.gg/tbUe7Hg7Ep).
- > Adding our bot to your server ([Click here](https://discordapp.com/oauth2/authorize?client_id=769398326532898856&permissions=8&scope=bot)).
- > Starring this repository.

---
<h1 align="center"><b>📜 Requirements</b></h1>

These are the requirements for the bot.

- > Python 3.10 (Required packages listed in requirements.txt)
- > Set environment variable `DISCORD_BOT_TOKEN` with your bot token OR replace `"YOUR_TOKEN_HERE"` in `config.py` with your bot token (keep quotes).

---
<h1 align="center"><b>🧾 How To Migrate (Update) DB</b></h1>

What is migration?</br>
**Migration is a way to update database structure without losing data.**</br>
In this project we are using [Aerich](https://github.com/tortoise/aerich) to manage migrations.

> Note: All migrations are stored in `migrations` folder.

To migrate database, you need to do the following steps:
1. > Be sure that you have installed all required packages from `requirements.txt`
2. > Run these commands:
    ```
    >>> aerich migrate --name YOUR_MIGRATION_NAME
    >>> aerich upgrade
    ```
