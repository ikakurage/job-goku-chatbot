import streamlit as st
import random

# --- 設定値 ---
# チャットボットの名前
BOT_NAME = "ジョブゴク"

# 冒頭の挨拶文
INITIAL_GREETING = "ジョブゴクです、あなたに合った理想のお仕事を紹介いたします。何か求人をお探しですか？"

# ブラック企業にありがちなフレーズのリスト
BLACK_PHRASES = [
    "やりがいのある仕事です！",
    "未経験者大歓迎！",
    "急成長企業で一緒に成長しませんか？",
    "ヤル気・諦めない粘り強さ・夢を実現！",
    "ノルマ無し（実質はあります）", # 皮肉を込めたコメント
    "20代~30代がメインで活躍中！",
    "即戦力として活躍できます！",
    "少数精鋭な組織です",
    "短期間で幹部候補に！",
    "アットホームな職場で、あなたの個性を活かせます！",
    "充実した研修制度でスキルアップ！",
    "風通しの良い職場環境です！",
    "社員の成長を全力でサポートします！",
    "夢を追いかけるあなたを応援します！",
    "成果は正当に評価します！",
    "常に変化に対応できる柔軟性のある方、歓迎！",
    "チームワークを重視し、協調性のある方！",
    "チャレンジ精神旺盛な方を求めています！",
    "ワークライフバランスを重視しています！（建前）",
    "残業は個人の裁量に任せています！（実質強制）",
    "社員の意見を尊重する社風です！（聞くだけ）"
]

# ネガティブなキーワード（カタカナ）
NEGATIVE_KEYWORDS = [
    "ジゴク", "アクム", "シュラ", "マオウ", "ヨミ", "ゲキツウ", "ムゲン", "ゼツボウ", "キョウフ",
    "アビス", "カオス", "デス", "ドゥーム", "ヘル", "イビル", "ダーク", "クライシス",
    "ザンコク", "ハイキョ", "フメツ", "オワリ", "サイアク", "コンラン", "ハカイ", "キョウアク"
]

# 業種名とそれに対応する企業名の接尾語
INDUSTRY_SUFFIXES = {
    "建築": ["建築", "建設", "工務店", "組", "土木"],
    "介護": ["福祉会", "ケアサービス", "介護施設", "ヘルプ", "ナーシング"],
    "金融": ["銀行", "金融", "証券", "キャピタル", "ファンド"],
    "IT": ["システム", "テクノロジー", "ラボ", "デジタル", "ソリューションズ"],
    "飲食": ["フード", "ダイニング", "キッチン", "レストラン", "カフェ"],
    "サービス": ["サービス", "コンサルティング", "エージェント", "サポート", "プロデュース"],
    "製造": ["製作所", "工業", "ファクトリー", "マニュファクチャリング", "重工"],
    "物流": ["ロジスティクス", "運送", "輸送", "デリバリー", "カーゴ"],
    "医療": ["クリニック", "ホスピタル", "メディカル", "ヘルスケア", "薬局"],
    "教育": ["学園", "塾", "アカデミー", "スクール", "教育"],
    "小売": ["ストア", "ショップ", "販売", "流通", "マーケット"],
    "不動産": ["不動産", "エステート", "開発", "住建", "リアルティ"]
}

# 備考欄のバリエーションを増やすためのフレーズ
REMARKS_VARIATIONS = [
    "我々はあなたの「夢」を応援します！（ただし、会社が定める夢に限る）",
    "社員の成長が会社の成長に直結します！（個人の犠牲の上に成り立つ）",
    "若手でも活躍できる環境です！（ベテランは使い潰されます）",
    "あなたのアイデアが会社を動かします！（採用されるとは言っていない）",
    "残業代は「みなし」ですが、頑張りはしっかり評価します！（評価基準は不明）",
    "休日出勤は滅多にありません！（ただし繁忙期は除く）",
    "社員の健康を第一に考えています！（健康診断は自己責任）",
    "退職金制度あり！（勤続30年以上が条件）",
    "社員間のコミュニケーションが活発です！（飲み会強制参加）",
    "成果を出せば、すぐに昇進できます！（成果の定義は曖昧）",
    "入社後すぐに即戦力として活躍できます！（研修はOJTのみ）",
    "あなたの頑張りが、そのまま給与に反映されます！（微々たるものです）",
    "転勤は基本的にありません！（ただし辞令が出れば別）",
    "服装は自由です！（ただし常識の範囲内で）",
    "福利厚生も充実！（聞いたことがないものばかり）",
    "社員旅行は海外！（積立金は給与天引き）",
    "社員の声を大切にしています！（聞くだけ）",
    "チームで目標達成を目指します！（個人の責任にされる）",
    "未経験でも安心のサポート体制！（放置される可能性あり）",
    "あなたの情熱を仕事にぶつけてください！（プライベートは犠牲に）"
]

# --- 関数定義 ---
def generate_job_posting(user_query):
    """
    ユーザーのクエリに基づいてブラックな求人票を生成します。
    """
    # ユーザーのクエリから業種を特定
    matched_industry = "その他"
    for industry, suffixes in INDUSTRY_SUFFIXES.items():
        if industry in user_query or any(s in user_query for s in suffixes):
            matched_industry = industry
            break
    
    # 企業名の生成
    negative_prefix = random.choice(NEGATIVE_KEYWORDS)
    if matched_industry in INDUSTRY_SUFFIXES:
        industry_suffix = random.choice(INDUSTRY_SUFFIXES[matched_industry])
    else:
        # マッチしない場合は一般的な業種名からランダムに選択
        all_suffixes = [s for sublist in INDUSTRY_SUFFIXES.values() for s in sublist]
        industry_suffix = random.choice(all_suffixes)
        
    company_name = f"株式会社{negative_prefix}{industry_suffix}"

    # 給与の生成 (年収250万〜1000万の範囲でランダムに設定)
    min_salary = random.randint(250, 400) # 下限を少し狭める
    max_salary = random.randint(min_salary + 200, 1000) # 上限を広げる
    salary_range = f"年収{min_salary}万円〜{max_salary}万円"

    # ブラックフレーズの選択 (3〜5個ランダムに選択)
    num_phrases = random.randint(3, 5)
    selected_black_phrases = random.sample(BLACK_PHRASES, num_phrases)
    
    # 備考欄のフレーズ選択 (2〜4個ランダムに選択)
    num_remarks = random.randint(2, 4)
    selected_remarks = random.sample(REMARKS_VARIATIONS, num_remarks)

    # 求人票の作成
    job_posting = f"""
### 【求人】{company_name} - {matched_industry}業界の未来を担う人材募集！
---
**企業名**: {company_name}
**業種**: {matched_industry}

**給与**: {salary_range}
    ※あなたの能力とヤル気次第で、上限は青天井です！

**仕事内容**:
    多岐にわたる業務をお任せします。
    あなたの成長が会社の成長に直結します！
    （具体的な業務内容は入社後に説明します）

**求める人材**:
"""
    for phrase in selected_black_phrases:
        job_posting += f"    - {phrase}\n"
    job_posting += """
**待遇・福利厚生**:
    社会保険完備（たぶん）
    交通費支給（上限あり）
    昇給あり（実績による）
    社員旅行あり（強制参加）

**備考**:
"""
    for remark in selected_remarks:
        job_posting += f"    - {remark}\n"
    job_posting += "---"
    
    return job_posting

# --- Streamlit アプリの本体 ---
st.title(f"{BOT_NAME}（職業紹介所）")

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 冒頭の挨拶
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": INITIAL_GREETING})

# チャット履歴の表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ユーザーからの入力
user_input = st.chat_input("ここに希望の業種などを入力してください")

if user_input:
    # ユーザーのメッセージを履歴に追加
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # アシスタント（ジョブゴク）の返答を生成
    with st.chat_message("assistant"):
        with st.spinner("求人情報を検索中です..."):
            # ここでLLMを呼び出す代わりに、自作の関数で求人票を生成
            job_offer = generate_job_posting(user_input)
            st.write(job_offer)
            st.write("いかがでしょうか？この求人、あなたの「やりがい」を刺激するでしょう？")
        
    # アシスタントのメッセージを履歴に追加
    st.session_state.messages.append({"role": "assistant", "content": job_offer + "\nいかがでしょうか？この求人、あなたの「やりがい」を刺激するでしょう？"})

