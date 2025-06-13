import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# 加载 bge-large-zh-v1.5 嵌入模型
model_name = "BAAI/bge-large-zh-v1.5"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# 读取已抽取好的结构化数据
with open("data/structured_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []
metadatas = []

# 病虫害部分
for record in data['pests']:
    chunk = f"名称：{record['title']}\n"

    if record['symptom_field']:
        chunk += f"{record['symptom_field']}：{record['symptom_content']}\n"
    if record['rule_field']:
        chunk += f"{record['rule_field']}：{record['rule_content']}\n"
    if record['control_field']:
        chunk += f"{record['control_field']}：{record['control_content']}\n"    
    if record['image']:
        chunk += f"\n相关图片文件：{record['image']}"
    documents.append(chunk)
    metadatas.append({"title": record['title'], "type": "病虫害", "image": record['image']})

# 杂草防除部分
weed_images = data['weed'].get('images', [])
image_info = f"\n相关图片文件：{', '.join(weed_images)}" if weed_images else ""
weed_chunk = f"名称：{data['weed']['title']}\n{data['weed']['content']}{image_info}"
documents.append(weed_chunk)
metadatas.append({"title": data['weed']['title'], "type": "杂草防除", "images": weed_images})

# 使用 LangChain 的 FAISS 统一建库
vectorstore = FAISS.from_texts(texts=documents, embedding=embeddings, metadatas=metadatas)
vectorstore.save_local("corn_vectorstore")

print("✅ LangChain 知识库建库完成！")