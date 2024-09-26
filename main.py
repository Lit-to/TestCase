import discord
from discord import app_commands
import fileout as fo
import searchCase as sc
import json
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def getToken():
    with open("setting.json",mode="r") as f:
        data=json.load(f)
    return data["discord"]["token"]


class testCaseModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="テストケースを入力",
            timeout=None,
        )
        searchCase = sc.main([False])
        searchCase=list(map(lambda x:discord.SelectOption(label=x),searchCase))
        self.contest_type = discord.ui.TextInput(
            label="コンテストの種類",
            placeholder="ABC,ARC,AGC(大文字小文字区別なし)",
            required=True,
            max_length=3,
            min_length=3,
            style=discord.TextStyle.short
        )
        self.contest_number = discord.ui.TextInput(
            label="コンテスト番号(3桁)",
            placeholder="334",
            required=True,
            max_length=3,
            min_length=3,
            style=discord.TextStyle.short
        )
        self.contest_set = discord.ui.TextInput(
            label="問題セット",
            placeholder="A,B,C,D,E,F,G,H,X",
            required=True,
            max_length=1,
            min_length=1,
            style=discord.TextStyle.short
        )
        self.contest_case = discord.ui.TextInput(
            label="テストケース",
            placeholder="1,sample_01.txt",
            required=True,
            max_length=32,
            min_length=1,
            style=discord.TextStyle.short
        )
        self.contest_set="Ex" if self.contest_set=="X" else self.contest_set#Xの場合はExに変換
        self.add_item(self.contest_type)
        self.add_item(self.contest_number)
        self.add_item(self.contest_set)
        self.add_item(self.contest_case)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        query=[]
        query.append(self.contest_type.value)
        query.append(self.contest_number.value)
        query.append(self.contest_set.value)
        query.append(self.contest_case.value)
        testPath=[]
        await interaction.response.defer()
        testPath.append(sc.main(query,"in"))
        testPath.append(sc.main(query,"out"))
        case_file=[]
        for i in testPath:
            case_file.append(discord.File(i))
        if False in testPath:
            await interaction.followup.send("テストケースが存在しません "+query[0]+" "+query[1]+" "+query[2]+" "+query[3],ephemeral=True)
        else:
            await interaction.followup.send(query[0]+" "+query[1]+" "+query[2]+" "+query[3]+" の入力ファイル:",ephemeral=True)
            await interaction.followup.send(files=case_file[0])
            await interaction.followup.send(query[0]+" "+query[1]+" "+query[2]+" "+query[3]+" の出力ファイル:",ephemeral=True)
            await interaction.followup.send(files=case_file[1])

#起動
@client.event
async def on_ready():
    # アクティビティを設定
    new_activity = "精進"
    fo.printf("Bot","is ready")
    await client.change_presence(activity=discord.Game(new_activity))
    # スラッシュコマンドを同期
    await tree.sync()



@tree.command(name="c", description="テストケース選択画面を出すよ")
async def test_case(interaction: discord.Interaction):
    # await interaction.response.defer()
    testCase=testCaseModal()
    await interaction.response.send_modal(testCase)



@tree.command(name='case', description='テストケースのファイルを返すよ')
@app_commands.describe(contest_type="コンテストの種類",contest_number="コンテストの番号",question_set="A~H",test_case="テストケースの番号",in_or_out="入力ファイルはin、出力ファイルはout(未記入の場合はin)")
async def contest(interaction: discord.Interaction,contest_type:str,contest_number:str,question_set:str,test_case:str,in_or_out:str=""):
    await interaction.response.defer()
    testPath=[]
    if in_or_out=="":
        testPath.append(sc.main([contest_type,contest_number,question_set,test_case],"in"))
        testPath.append(sc.main([contest_type,contest_number,question_set,test_case],"out"))
    elif in_or_out=="in":
        testPath.append(sc.main([contest_type,contest_number,question_set,test_case],"in"))
    elif in_or_out=="out":
        testPath.append(sc.main([contest_type,contest_number,question_set,test_case],"out"))
    else:
        await interaction.followup.send("in_or_outにはinかoutを入力してください")
    case_file=[]
    for i in testPath:
        case_file.append(discord.File(i))
    if False in testPath:
        await interaction.followup.send("テストケースが存在しません"+contest_type+contest_number+question_set+test_case)
    else:
        await interaction.followup.send(files=case_file)




client.run(getToken())
