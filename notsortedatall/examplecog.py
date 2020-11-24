#Examplecog

class Example(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def nothing(self, ctx):
		await ctx.send("Okay, i did nothing!")


def setup(client):
	client.add_cog(Example(client))
