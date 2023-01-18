import random

from discord.ext import commands

from extensions._base_types import BaseCog


class FunCog(BaseCog):
    @commands.command(name="8ball", aliases=["8b", "magic8ball", "magic8b"])
    async def magic_8_ball(self, ctx: commands.Context, question: str) -> None:
        """
        Ask the magic 8 ball a question.
        """
        answers = [
            "It is certain 😉",
            "It is decidedly so.",
            "Without a doubt 😎",
            "Yes — definitely 👍",
            "You may rely on it 😏",
            "As I see it, yes 😮",
            "Most likely 👌",
            "Outlook good 😊",
            "Yes.",
            "Signs point to yes 🃏",
            "Reply hazy, try again 🤔",
            "Ask again later 🕒",
            "Better not tell you now 🤫",
            "Cannot predict now ¯\_(ツ)_/¯",
            "Concentrate and ask again.",
            "Don't count on it 😒",
            "My reply is no 👎",
            "My sources say no 🕵️‍♂️",
            "Outlook not so good 😕",
            "Very doubtful 😔"
        ]

        await ctx.send(f"Question: {question}\nAnswer: {random.choice(answers)}")

    @commands.command()
    async def coinflip(self, ctx: commands.Context, guess: str) -> None:
        """
        Flip a coin.
        """
        if guess.lower() not in ["heads", "tails"]:
            await ctx.send("❌ Please choose either `heads` or `tails`.")
            return

        result = random.choice(["heads", "tails"])

        await ctx.send(
            f"The coin landed on {result}. "
            "Luckily for you, you guessed correctly! 🎉" if guess == result else 
            "Unfortunately, your guess was wrong. 😔"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(FunCog(bot))
