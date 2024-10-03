import discord
from discord import app_commands
import fileout as fo
import searchCase as sc
import json
import os
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def getToken():
    with open("token.json",mode="r") as f:
        data=json.load(f)
    if "discord" not in data.keys():
        raise Exception("discordのトークンが設定されていません")
    if "token" not in data["discord"].keys():
        raise Exception("tokenが設定されていません")
    return data["discord"]["token"]


class testCaseModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="テストケースを入力",
            timeout=None,
        )
        searchCase = sc.main()[1]
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

        self.add_item(self.contest_type)
        self.add_item(self.contest_number)
        self.add_item(self.contest_set)
        self.add_item(self.contest_case)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        fo.printf(interaction.user.name,">>>modal submit",self.contest_type.value,self.contest_number.value,self.contest_set.value,self.contest_case.value)
        query=[]
        query.append(self.contest_type.value)
        query.append(self.contest_number.value)
        query.append(self.contest_set.value)
        query.append(self.contest_case.value)
        await interaction.response.defer()
        testPath=sc.main(query)
        if testPath[0]==False:
            await interaction.followup.send(testPath[1],ephemeral=True)
            return
        case_file=[]
        case_file.append(discord.File(testPath[1]))
        case_file.append(discord.File(testPath[2]))
        file_name=testPath[1].split(os.sep)
        icon={"abc":":blue_circle:","arc":":green_circle:","agc":":orange_circle:"}
        await interaction.followup.send("## "+icon[query[0]]+file_name[1].upper()+" :regional_indicator_"+file_name[2].lower()+":"+" の入力ファイル("+file_name[4]+")を送信中...:")
        await interaction.followup.send(file=case_file[0])
        await interaction.followup.send("## "+icon[query[0]]+file_name[1].upper()+" :regional_indicator_"+file_name[2].lower()+":"+" の出力ファイル("+file_name[4]+")を送信中...:")
        await interaction.followup.send(file=case_file[1])

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
    fo.printf(interaction.user.name,">>>/c")
    # await interaction.response.defer()
    testCase=testCaseModal()
    await interaction.response.send_modal(testCase)

@tree.command(name='case', description='テストケースのファイルを返すよ')
@app_commands.describe(contest_type="コンテストの種類",contest_number="コンテストの番号",question_set="A~H",test_case="テストケースの番号",in_or_out="入力ファイルはin、出力ファイルはout(未記入の場合はin)")
async def contest(interaction: discord.Interaction,contest_type:str,contest_number:str,question_set:str,test_case:str,in_or_out:str=""):
    fo.printf(interaction.user.name,">>>/case",contest_type,contest_number,question_set,test_case,in_or_out)
    await interaction.response.defer()
    testPath=[]
    searched=sc.main([contest_type,contest_number,question_set,test_case])
    if searched[0]==False:#テストケースが見つからなかった場合そのままエラーを返す
        await interaction.followup.send(searched[1])
        return
    if in_or_out=="":
        testPath.append(searched[1])
        testPath.append(searched[2])
    elif in_or_out=="in":
        testPath.append(searched[1])
    elif in_or_out=="out":
        testPath.append(searched[2])
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
