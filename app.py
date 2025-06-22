# app.py

import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
import gradio as gr

# Load the trained model
lmodel = joblib.load("loan_model.pkl")

# Prediction function
def predict_loan(Age, Income, Family, CCAvg, Education, Mortgage, Securities_Account, CD_Account):
    education_map = {"Undergraduate": 1, "Graduate": 2, "Advanced": 3}
    Education = education_map.get(Education, 1)
    
    features = np.array([[Age, Income, Family, CCAvg, Education, Mortgage,
                          int(Securities_Account), int(CD_Account)]])
    
    prediction = lmodel.predict(features)[0]
    return (
        "<div style='background-color:#d1fae5; padding:15px; font-size:20px; color:green; border-radius:10px;'>✅ Loan Approved</div>"
        if prediction == 1
        else "<div style='background-color:#fee2e2; padding:15px; font-size:20px; color:red; border-radius:10px;'>❌ Loan Not Approved</div>"
    )

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft(primary_hue="teal", secondary_hue="indigo")) as demo:
    gr.Markdown("""
    <div style='text-align:center; padding:20px;'>
        <h1 style='color:#0f172a;'>🏦 Indian Bank Loan Approval Predictor 🇮🇳</h1>
        <p style='font-size:16px;'>Enter customer details below to predict whether a bank loan will be approved.</p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column():
            Age = gr.Number(label="🔢 Age")
            Income = gr.Number(label="💵 Annual Income (₹ in Lakhs)")
            Family = gr.Slider(minimum=1, maximum=5, label="👨‍👩‍👧‍👦 Family Members")
            CCAvg = gr.Number(label="💳 Avg Credit Card Spend (₹ in Lakhs/month)")
        with gr.Column():
            Education = gr.Dropdown(choices=["Undergraduate", "Graduate", "Advanced"], label="🎓 Education Level")
            Mortgage = gr.Number(label="🏠 Mortgage Amount (₹ in Lakhs)")
            Securities_Account = gr.Checkbox(label="📈 Has Securities Account")
            CD_Account = gr.Checkbox(label="💽 Has CD Account")

    with gr.Row():
        submit_btn = gr.Button("🚀 Predict Now", variant="primary")

    with gr.Row():
        output = gr.HTML(label="🔍 Prediction")

    submit_btn.click(
        fn=predict_loan,
        inputs=[Age, Income, Family, CCAvg, Education, Mortgage, Securities_Account, CD_Account],
        outputs=output
    )

demo.launch(debug=True, inbrowser=True)
