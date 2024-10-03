import dropbox
import os
import dropbox
import requests
import time
import fileout as fo
import searchCase as sc
import indexList as iL
import json
#毎日実行するプログラム

def getToken():
    with open("token.json",mode="r") as f:
        data=json.load(f)
    if "dropbox" not in data.keys():
        raise Exception("dropboxのトークンが設定されていません")
    if "app_key" not in data["dropbox"].keys():
        raise Exception("app_keyが設定されていません")
    if "app_seacret" not in data["dropbox"].keys():
        raise Exception("app_seacretが設定されていません")
    if "reflesh" not in data["dropbox"].keys():
        raise Exception("reflesh(リフレッシュトークン)が設定されていません")
    return data["dropbox"]["app_key"],data["dropbox"]["app_seacret"],data["dropbox"]["reflesh"]


# リフレッシュトークンを使用して新しいアクセストークンを取得する関数
def get_access_token():
    url = "https://api.dropbox.com/oauth2/token"
    keys=getToken()
    data = {
        "grant_type": "refresh_token",
        "client_id": keys[0],
        "client_secret": keys[1],
        "refresh_token": keys[2],
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token_info = response.json()
        return token_info["access_token"]
    else:
        raise Exception(f"Error refreshing token: {response.content}")
def get_shared_folder_list(shared_link):
    # アクセストークンでDropboxクライアントを初期化
    try:
        # 共有リンクのメタデータを取得
        shared_link_metadata = dbx.sharing_get_shared_link_metadata(url=shared_link)
        # メタデータのパスがNoneの場合、ルートフォルダとみなす
        if shared_link_metadata.path_lower is None:
            # 共有リンクオブジェクトを作成
            link = dropbox.files.SharedLink(url=shared_link)
            
            # 空のパスでフォルダ内容を取得
            result = dbx.files_list_folder('', shared_link=link)
        else:
            # 通常のフォルダパスを使用してフォルダ内容を取得
            result = dbx.files_list_folder(shared_link_metadata.path_lower)
        
        # フォルダ名だけを抽出してリストに格納
        folders = [entry.name for entry in result.entries if isinstance(entry, dropbox.files.FolderMetadata)]
        
        return folders
    
    except dropbox.exceptions.ApiError as err:
        fo.printf(f"エラー: {err}")
        return None
def download_shared_folder(shared_link, folder_name, local_download_path): # フォルダをダウンロード
    try:
        # 共有リンクのメタデータを取得
        shared_link_metadata = dbx.sharing_get_shared_link_metadata(url=shared_link)
        link = dropbox.files.SharedLink(url=shared_link)
        # ダウンロード先のディレクトリがなければ作成
        if not os.path.exists(local_download_path):
            os.makedirs(local_download_path)
        # フォルダのパスを構築
        folder_path = shared_link_metadata.path_lower if shared_link_metadata.path_lower else ''
        folder_path = os.path.join(folder_path, folder_name)
        # フォルダの内容を取得
        process_folder(dbx, link, folder_path, local_download_path)
    except dropbox.exceptions.ApiError as err:
        fo.printf(f"エラー: {err}")
        return None
def process_folder(dbx, link, folder_path, local_download_path): # フォルダからファイルパスを取得
    # フォルダの内容をリストアップ
    result = dbx.files_list_folder(path=folder_path, shared_link=link)
    for entry in result.entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            # ファイルのダウンロードパスを作成
            local_file_path = os.path.join(local_download_path, entry.name)
            file_path=folder_path+"/"+entry.name
            # ファイルをダウンロード
            # with open(local_file_path, 'wb') as f:
            # dbx.files_download_to_file(local_file_path,folder_path)
            time.sleep(1)
            while True:
                try:
                    dbx.sharing_get_shared_link_file_to_file(download_path=local_file_path,url=link.url,path=file_path)
                    break
                except:#回線切れたりとかしてやり直す時
                        fo.printf("_Download filed:",local_download_path,">reconnection 10 seconds...",end=".............>")
                        time.sleep(10)
                        fo.printf("_reconnection")
                continue
            fo.printf(f"_Downloaded: {entry.name}")
        else:
            # サブフォルダのダウンロード先ディレクトリを作成
            subfolder_path = os.path.join(local_download_path, entry.name)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
            # サブフォルダのパスを構築
            subfolder_full_path = folder_path+"/"+entry.name
            # サブフォルダを再帰的に処理
            process_folder(dbx, link, subfolder_full_path, subfolder_path)
def isTarget(name:str): # ファイル名が対象かどうか
    if name.startswith("abc"):
        return True
    elif name.startswith("ABC"):
        return True
    elif name.startswith("arc"):
        return True
    elif name.startswith("ARC"):
        return True
    elif name.startswith("agc"):
        return True
    elif name.startswith("AGC"):
        return True
    else:
        return False
def file_list(): # ファイル一覧を取得
    result=set()
    for i in os.listdir("out"):
        if isTarget(i):
            result.add(i)
    return result
def filter_abc(mypc:set,dropbox:list): # PCにすでにないファイルのみ抽出
    result=[]
    for i in range(len(dropbox)):
        if isTarget(dropbox[i]) and dropbox[i].lower() not in mypc:
            result.append(dropbox[i])
    return result



# 共有リンクを指定してファイル一覧を取得
# アクセストークンを取得
while True:
    doing_file=""
    try:

        ACCESS_TOKEN = get_access_token()
        # Dropbox APIクライアントの初期化
        dbx = dropbox.Dropbox(ACCESS_TOKEN)

        shared_link = "https://www.dropbox.com/sh/nx3tnilzqz7df8a/AAAYlTq2tiEHl5hsESw6-yfLa?e=1&dl=0"
        dropbox_folders = get_shared_folder_list(shared_link)#dropboxのフォルダリスト
        pc_folders= file_list()#PCのフォルダリスト
        files = filter_abc(pc_folders,dropbox_folders)
        files.sort()
        files.reverse()
        fo.printf("start",time.time())
        i=0
        while i<len(files): 
        # for i in range(len(files)):
            # try:
            doing_file=files[i]
            ACCESS_TOKEN = get_access_token()
            dbx = dropbox.Dropbox(ACCESS_TOKEN)
            download_shared_folder(shared_link, "/"+files[i], os.path.join("out",files[i]).lower())
            fo.printf(f"Downloaded: {files[i]}") if i%500==0 else None
            i+=1
        fo.printf("fin",time.time())

        file_structure=sc.getFileStructure("out")
        iL.dump("indexList.json",file_structure)
    except:
        fo.printf(doing_file,"cruppsted 10 seconds...")
        time.sleep(10)
        fo.printf("go next")
        continue





