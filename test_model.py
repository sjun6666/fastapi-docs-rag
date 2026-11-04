from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
texts = ["路径参数怎么声明", "URL 里的变量怎么获取", "怎么连接数据库"]
vectors = model.encode(texts, normalize_embeddings=True)

print(vectors.shape)       # 预期 (3, 512)
print(vectors @ vectors.T) # 两两之间的相似度，3 × 3 的表