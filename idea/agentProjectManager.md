# 概要

プロジェクトに関するQAボットとして、仕様やコーディング規約を人間のProjectManagerの代わりに答えてくれる。といいな。

# 目的

- PMへの質問の内、既に決定している事項を人間の代わりに回答させる
- 設計などの意思決定は行わない
- Github, Backlog, Notion等のドキュメントからRAGして、根拠（リンク等）を添えて回答させる
- 根拠を示せない場合は未確定の旨を回答させる

# 背景

- 人間への質問はレスポンスに時間（最悪N時間）がかかる
- 何度も質問するのはお互い時間的に無駄がある
- なら知識ベースで回答できるものはBotが回答してくれればいいよね

# 参考
- RAG（Retrieval-Augmented Generation）
  ![RAG](https://blogs.nvidia.com/wp-content/uploads/2023/11/NVIDIA-RAG-diagram-scaled.jpg)