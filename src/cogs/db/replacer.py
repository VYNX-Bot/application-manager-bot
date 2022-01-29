import os

os.chdir('../')

for cogs in os.listdir():
    try:
        print(cogs)
        with open(cogs) as fp:
            con = fp.read()
        con.replace(
            """
if ctx.author.guild_permissions.administrator == False:
            for role in ctx.author.roles:
                if role.id in db[str(ctx.guild.id)]["setting_roles"]:
                    no_perm = False
                    break
                else:
                    no_perm = True
            """,
            """
            if ctx.author.guild_permissions.administrator == False:
            for role in ctx.author.roles:
                if role.id in db[str(ctx.guild.id)]["setting_roles"]:
                    no_perm = False
                    break
                else:
                    no_perm = True
            else:
                no_perm = False
            """
        )
        with open(cogs,'w') as fp:
            fp.write(con)
    except IsADirectoryError:
        continue