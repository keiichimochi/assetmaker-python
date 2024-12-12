import streamlit as st
from PIL import Image, ImageDraw
import io
import openai
from openai import OpenAI
import base64

# タイトルとスタイル設定
st.set_page_config(page_title="16x16 RPGアセットメーカー", layout="wide")
st.title("16x16 RPGアセットメーカー 🎮")
st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# OpenAI APIキーの設定
api_key = st.sidebar.text_input("OpenAI APIキー", type="password")
if api_key:
    client = OpenAI(api_key=api_key)

def generate_asset_prompt(asset_type):
    prompts = {
        "草原": "16x16 pixel art of a green grassland tile for RPG, top-down view, simple",
        "森": "16x16 pixel art of a forest tile with trees for RPG, top-down view, simple",
        "山": "16x16 pixel art of a mountain tile for RPG, top-down view, simple",
        "高い山": "16x16 pixel art of a tall snow-capped mountain tile for RPG, top-down view, simple",
        "川": "16x16 pixel art of a river tile for RPG, top-down view, simple blue water",
        "海": "16x16 pixel art of an ocean tile for RPG, top-down view, simple blue water",
        "城": "16x16 pixel art of a castle tile for RPG, top-down view, simple grey structure",
        "街": "16x16 pixel art of a town tile for RPG, top-down view, simple houses"
    }
    return prompts[asset_type]

def generate_pixel_art(asset_type, pixel_size):
    if not api_key:
        st.error("OpenAI APIキーを入力してください！")
        return None
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=generate_asset_prompt(asset_type),
            size="1024x1024",  # DALL-E 3は1024x1024のみサポート
            quality="standard",
            n=1,
        )
        
        # 画像URLを取得
        image_url = response.data[0].url
        
        # 画像をダウンロードしてPIL Imageに変換
        import requests
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content))
        
        # 指定されたサイズにリサイズ
        img = img.resize((pixel_size, pixel_size), Image.Resampling.NEAREST)
        
        return img
    
    except Exception as e:
        st.error(f"エラーが発生したナリ！: {str(e)}")
        return None

def convert_to_bytes(img):
    if img is None:
        return None
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

# メインアプリケーション
st.markdown("### アセットタイプとサイズを選択するナリ！ 🎨")

col1, col2 = st.columns(2)
with col1:
    asset_type = st.selectbox(
        "作成したいアセットを選ぶナリ！",
        ["草原", "森", "山", "高い山", "川", "海", "城", "街"]
    )
with col2:
    pixel_size = st.selectbox(
        "ピクセルサイズを選ぶナリ！",
        [16, 32, 64],
        format_func=lambda x: f"{x}x{x}"
    )

if st.button("アセットを生成するナリ！ 🚀"):
    with st.spinner("生成中..."):
        img = generate_pixel_art(asset_type, pixel_size)
        if img:
            # 画像を大きく表示（表示サイズは256pxに固定）
            resized_img = img.resize((256, 256), Image.Resampling.NEAREST)
            st.image(resized_img, caption=f"{asset_type}のアセット ({pixel_size}x{pixel_size})", use_column_width=False)
            
            # ダウンロードボタン
            btn = st.download_button(
                label="PNGをダウンロードするナリ！ 💾",
                data=convert_to_bytes(img),
                file_name=f"rpg_asset_{asset_type}_{pixel_size}x{pixel_size}.png",
                mime="image/png"
            )

st.markdown("""
### 使い方ナリ！ 📝
1. サイドバーにOpenAI APIキーを入力するナリ！
2. アセットタイプとサイズを選択するナリ！
3. 「アセットを生成するナリ！」ボタンをクリックするナリ！
4. 気に入ったら「PNGをダウンロードするナリ！」ボタンでダウンロードするナリ！
""")
