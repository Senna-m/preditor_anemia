import streamlit as st
import pandas as pd
from catboost import CatBoostClassifier

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Preditor de Anemia",
    page_icon="🩸",
    layout="centered"
)

# ============================================================
# CARREGAR MODELO
# ============================================================
@st.cache_resource
def load_model():
    m = CatBoostClassifier()
    m.load_model("modelo_anemia.cbm")
    return m

modelo = load_model()

# ============================================================
# REGRA DA OMS
# ============================================================
def diagnostico_oms(hemoglobina: float, sexo: int) -> dict:
    if sexo == 1:
        limite = 13.0
        grupo = "Homens"
    else:
        limite = 12.0
        grupo = "Mulheres"

    anemico = hemoglobina < limite

    return {
        "anemico": anemico,
        "grupo": grupo,
        "limite": limite,
        "hemoglobina": hemoglobina
    }

def diagnostico_mcv(mcv: float) -> dict:
    if mcv < 80:
        classificacao = "Microcítico"
        descricao = "Volume corpuscular abaixo do normal"
        alerta = True
    elif mcv <= 100:
        classificacao = "Normocítico"
        descricao = "Volume corpuscular dentro do esperado"
        alerta = False
    else:
        classificacao = "Macrocítico"
        descricao = "Volume corpuscular acima do normal"
        alerta = True
    return {"classificacao": classificacao, "descricao": descricao, "alerta": alerta, "mcv": mcv}

# ============================================================
# INTERFACE
# ============================================================
st.title("🩸 Preditor de Anemia")
st.markdown("Insira os dados do paciente para análise.")

st.divider()

# --- Entradas do usuário ---
col1, col2 = st.columns(2)

with col1:
    sexo_label = st.selectbox("Sexo", ["Feminino", "Masculino"])
    sexo = 1 if sexo_label == "Masculino" else 0

    hemoglobina = st.number_input(
        "Hemoglobina (g/dL)",
        min_value=1.0, max_value=25.0, value=13.0, step=0.1,
        help="Referência OMS: Homens ≥ 13 g/dL | Mulheres ≥ 12 g/dL"
    )

with col2:
    mch = st.number_input(
        "MCH (pg)",
        min_value=1.0, max_value=50.0, value=29.0, step=0.1,
        help="Hemoglobina Corpuscular Média. Referência: 27–33 pg"
    )
    mchc = st.number_input(
        "MCHC (g/dL)",
        min_value=1.0, max_value=50.0, value=34.0, step=0.1,
        help="Concentração de Hemoglobina Corpuscular Média. Referência: 32–36 g/dL"
    )
    mcv = st.number_input(
        "MCV (fL)",
        min_value=1.0, max_value=150.0, value=88.0, step=0.1,
        help="Volume Corpuscular Médio. Referência: 80–100 fL"
    )

st.divider()

# --- Botão de análise ---
if st.button("🔍 Analisar", use_container_width=True):

    # Previsão do modelo
    X = pd.DataFrame({
        "Gender":     [sexo],
        "Hemoglobin": [hemoglobina],
        "MCH":        [mch],
        "MCHC":       [mchc],
        "MCV":        [mcv]
    })

    pred_modelo = int(modelo.predict(X)[0])
    prob = modelo.predict_proba(X)[0]
    confianca = prob[pred_modelo] * 100

    # Diagnósticos
    oms = diagnostico_oms(hemoglobina, sexo)
    mcv_resultado = diagnostico_mcv(mcv)

    # --- Exibir resultados lado a lado ---
    st.subheader("Resultado da Análise")

    col_modelo, col_oms, col_mcv = st.columns(3)

    with col_modelo:
        st.markdown("**🤖 Modelo preditivo (CatBoost)**")
        if pred_modelo == 1:
            st.error(f"🔴 Anêmico\nConfiança: {confianca:.1f}%")
        else:
            st.success(f"🟢 Não Anêmico\nConfiança: {confianca:.1f}%")

    with col_oms:
        st.markdown(f"**🏥 Critério OMS ({oms['grupo']})**")
        if oms["anemico"]:
            st.error(
                f"🔴 Abaixo do limite\n"
                f"Hemoglobina: {hemoglobina} g/dL\n"
                f"Limite OMS: {oms['limite']} g/dL"
            )
        else:
            st.success(
                f"🟢 Dentro do esperado\n"
                f"Hemoglobina: {hemoglobina} g/dL\n"
                f"Limite OMS: {oms['limite']} g/dL"
            )

    with col_mcv:
        st.markdown("**🔬 Análise MCV**")
        if mcv_resultado["alerta"]:
            st.error(
                f"🔴 {mcv_resultado['classificacao']}\n"
                f"{mcv_resultado['descricao']}\n"
                f"MCV: {mcv} fL"
            )
        else:
            st.success(
                f"🟢 {mcv_resultado['classificacao']}\n"
                f"{mcv_resultado['descricao']}\n"
                f"MCV: {mcv} fL"
            )

    st.divider()

    # --- Conclusão final ---
    st.subheader("Conclusão")

    modelo_anemico = pred_modelo == 1
    oms_anemico = oms["anemico"]

    if modelo_anemico and oms_anemico:
        st.error(
            "⚠️ **Alta probabilidade de anemia.**\n\n"
            "Tanto o modelo preditivo quanto o critério da OMS indicam anemia. "
            "Recomenda-se avaliação médica."
        )
    elif not modelo_anemico and not oms_anemico:
        st.success(
            "✅ **Sem indicativo de anemia.**\n\n"
            "Tanto o modelo preditivo quanto o critério da OMS estão dentro do esperado."
        )
    elif modelo_anemico and not oms_anemico:
        st.warning(
            "🟡 **Resultado divergente.**\n\n"
            "O modelo preditivo indica anemia, mas a hemoglobina está acima do limite da OMS. "
            "Os outros marcadores (MCH, MCHC, MCV) podem estar alterados. "
            "Recomenda-se avaliação médica para investigação."
        )
    else:
        st.warning(
            "🟡 **Resultado divergente.**\n\n"
            "A hemoglobina está abaixo do limite da OMS, mas o modelo preditivo "
            "não identificou padrão de anemia nos demais marcadores. "
            "Recomenda-se avaliação médica."
        )

    st.divider()

    # --- Tabela de referência OMS ---
    st.subheader("📋 Valores de Referência OMS")
    tabela_oms = pd.DataFrame({
        "Grupo":        ["Homens", "Mulheres", "Gestantes", "Crianças"],
        "Hemoglobina":  ["< 13 g/dL", "< 12 g/dL", "< 11 g/dL", "Varia por idade"]
    })
    st.table(tabela_oms)

st.caption("⚠️ Este app é uma ferramenta de apoio e não substitui avaliação médica.")