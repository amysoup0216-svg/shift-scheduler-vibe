import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gemini 權限檢查", page_icon="🔍")

st.title("🔍 檢查我的 Gemini 模型權限")
api_key = st.text_input("輸入你的 API Key", type="password", help="請輸入從 Google AI Studio 取得的 API Key")

if api_key:
    # 檢查是否包含空白字元（常見的複製貼上錯誤）
    api_key = api_key.strip()
    
    try:
        genai.configure(api_key=api_key)
        st.write("---")
        st.subheader("✅ 認證成功！你的帳號可用模型：")
        
        # 取得模型列表
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append(m.name)
        
        if models:
            # 使用列表呈現，視覺上更清晰
            st.success(f"目前共支援 {len(models)} 個生成模型：")
            for model_name in sorted(models):
                st.code(model_name)
        else:
            st.warning("認證成功，但找不到任何支援生成內容的模型。")
                
    except Exception as e:
        # 根據錯誤訊息提供更友善的提示
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg:
            st.error("❌ API Key 錯誤：這把鑰匙無效或已被停用。請去 Google AI Studio 重新申請。")
        elif "quota" in error_msg.lower():
            st.error("❌ 配額問題：你的 API Key 已達到使用上限。")
        else:
            st.error(f"❌ 查詢失敗：{error_msg}")
