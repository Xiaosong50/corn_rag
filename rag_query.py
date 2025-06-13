from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

# 1. 嵌入模型
model_name = "BAAI/bge-large-zh-v1.5"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# 2. 加载向量库
vectorstore = FAISS.load_local("corn_vectorstore", embeddings, allow_dangerous_deserialization=True)

# 3. DeepSeek LLM 挂载
llm = ChatOpenAI(
    openai_api_key="sk-1bb535fafae7492b8e1ea724e4bade9c",
    openai_api_base="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0.1
)

# 4. 开始自定义RAG流程
while True:
    query = input("请输入你的问题（输入 exit 退出）：")
    if query.lower() in ["exit", "quit", "q"]:
        print("程序已退出")
        break

    # 4.1 向量召回
    results = vectorstore.similarity_search_with_score(query, k=3)

    # 4.2 把召回结果图片信息显示出来
    context = ""
    print("\n【召回内容】：")
    for doc, score in results:
        meta = doc.metadata
        print("\n===========================")
        print(f"标题：{meta.get('title')}")
        print(f"类型：{meta.get('type')}")
        images = meta.get('image') or meta.get('images')
        if isinstance(images, list):
            image_info = f"相关图片文件：{', '.join(images)}"
            print(f"图片文件：{', '.join(images)}")
        else:
            image_info = f"相关图片文件：{images}"
            print(f"图片文件：{images}")
        print(f"知识片段：\n{doc.page_content[:3000]}...")
        context += doc.page_content + "\n" + image_info + "\n"

    # 4.3 把召回内容拼成 RAG上下文
    full_prompt = f"根据以下资料回答问题：\n{context}\n问题：{query}\n请用简明准确的中文回答。"

    # 4.4 调用大模型生成最终答案
    response = llm.invoke(full_prompt)

    print("\n【生成回答】：")
    print(response.content)