import json
fil = [
    {
        "本論文永久網址:": " 複製永久網址\nTwitterTwitter"
    }]
a = {}
a['1'] = fil
print(a)

json_data = json.dumps(a,ensure_ascii=False, indent=4)
with open("table_datasss.json", "w", encoding="utf-8") as f:
    f.write(json_data)

print("Data written to table_data.txt")