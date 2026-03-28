# import streamlit as st
# from PIL import Image, ImageDraw, ImageOps, ImageFont
# # Si qrcode n'est pas installé, faites : pip install qrcode
# import qrcode
# import io
# import os
# import datetime
# import requests

# # --- CONFIGURATION PAYTECH (COLLEZ VOS CLÉS ICI) ---
# # Assurez-vous qu'il n'y a pas d'espaces avant ou après les clés
# PAYTECH_API_KEY = "267bf57a799bd46749bc82949134515b1ea1c3fe1dece4f478a2d24c4f37e1de"
# PAYTECH_API_SECRET = "785a0d5093f460a2e8af877f8cc7dc8d76ec144e645e086689fa1dcb28818e88"
# PAYTECH_URL = "https://paytech.sn/api/payment/request-payment"

# # --- CONFIGURATION DE LA PAGE ---
# st.set_page_config(page_title="AMEEK - Test Paiement", layout="wide")

# # On utilise le session_state pour garder la trace du paiement
# if 'etape' not in st.session_state:
#     st.session_state['etape'] = 'formulaire'

# # --- FONCTION DE PAIEMENT ---
# def initier_paiement_paytech(montant, nom_membre):
#     # --- NIVEAU 1 (4 espaces) ---
#     payload = {
#         "item_name": f"Adhesion AMEEK - {nom_membre}",
#         "item_price": str(montant),
#         "currency": "XOF",
#         "ref_command": f"AMEEK-{datetime.datetime.now().strftime('%H%M%S')}",
#         "command_name": "Carte Membre AMEEK",
#         "env": "test",
#         "ipn_url": "https://google.com/",
#         "success_url": "https://google.com/",
#         "cancel_url": "https://google.com/",
#         "source": "STML",
#         "custom_field": ""
#     }

#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json",
#         "API_KEY": PAYTECH_API_KEY,
#         "API_SECRET": PAYTECH_API_SECRET
#     }

#     try:
#         response = requests.post(PAYTECH_URL, json=payload, headers=headers)
#         print(f"DEBUG PAYTECH: {response.status_code} - {response.text}")
        
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"success": -1, "errors": "Erreur Serveur"}
            
#     except Exception as e:
#         print(f"ERREUR CONNEXION: {str(e)}")
#         return {"success": -1, "errors": str(e)}

#     # Ce return final sert de sécurité si tout le reste échoue
#     return {"success": -1, "errors": "Erreur inconnue"}
#     # TRÈS IMPORTANT : Ce return doit être aligné tout à gauche de la fonction
#     return resultat_final
# # --- INTERFACE ---
# st.title("🪪 Adhésion AMEEK")

# if st.session_state['etape'] == 'formulaire':
#     with st.form("main_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             prenom_nom = st.text_input("Prénom et Nom")
#             telephone = st.text_input("Téléphone")
#             statut = st.selectbox("Statut", ["Étudiant", "Élève", "Enseignant", "Sympathisant"])
#         with col2:
#             photo = st.file_uploader("Photo", type=['jpg', 'png'])
#             st.info("Montant : 5 000 FCFA")
        
#         btn_payer = st.form_submit_button("💳 PAYER ET GÉNÉRER")

#     if btn_payer:
#         if not prenom_nom or not photo:
#             st.error("Champs manquants !")
#         else:
#             res = initier_paiement_paytech(5000, prenom_nom)
            
#             # Correction ici : PayTech renvoie 1 pour le succès
#             # --- FIN DU BLOC DE PAIEMENT ---
#         if res.get('success') == 1 or res.get('success') == "1":
#             url = res.get('redirect_url')
#             st.success("✅ Lien de paiement prêt !")
#             st.markdown(f"### [👉 CLIQUEZ ICI POUR PAYER SUR PAYTECH]({url})")
            
#             st.info("Après avoir validé le paiement sur Wave/Orange Money, cliquez ci-dessous :")
            
#             if st.button("🏁 J'ai terminé le paiement"):
#                 st.session_state['etape'] = 'carte'
#                 st.session_state['nom'] = prenom_nom
#                 st.session_state['tel'] = telephone
#                 st.session_state['photo'] = photo
#                 st.rerun()
#         else:
#             st.error(f"Erreur : {res.get('errors', 'Problème de connexion')}")

# # --- LE BLOC QUI CHANGE TOUT (HORS DU FORMULAIRE) ---
# elif st.session_state['etape'] == 'carte':
#     st.balloons()
#     st.header("🎊 Félicitations, Membre AMEEK !")
    
#     # Récupération des données sauvegardées
#     nom_membre = st.session_state.get('nom', 'Membre')
#     tel_membre = st.session_state.get('tel', '')
#     photo_membre = st.session_state.get('photo', None)

#     # Affichage de la carte
#     st.write(f"### Carte officielle de : {nom_membre}")
    
#     # Ici, on affiche la photo si elle existe
#     if photo_membre:
#         st.image(photo_membre, caption="Photo du membre", width=150)
    
#     st.info(f"Numéro de téléphone enregistré : {tel_membre}")
    
#     # Bouton pour revenir au début si besoin
#     if st.button("🔄 Créer une nouvelle adhésion"):
#         st.session_state['etape'] = 'formulaire'
#         st.rerun()
import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageOps, ImageFont
import io
import qrcode
import datetime

# --- 1. CONFIGURATION SÉCURISÉE DES CLÉS ---
# --- 1. CONFIGURATION SÉCURISÉE DES CLÉS ---
if "PAYTECH_API_KEY" not in st.secrets or "PAYTECH_API_SECRET" not in st.secrets:
    st.error("❌ Erreur de configuration des Secrets !")
    st.write("Clés détectées actuellement :", list(st.secrets.keys()))
    st.info("""
    **Comment régler ça ?**
    1. Si tu es sur **Streamlit Cloud** : Va dans `Settings` > `Secrets` et colle ceci :
       ```toml
       PAYTECH_API_KEY = "votre_cle"
       PAYTECH_API_SECRET = "votre_secret"
       ```
    2. Si tu es en **Local** : Crée le fichier `.streamlit/secrets.toml`.
    """)
    st.stop()

PAYTECH_API_KEY = st.secrets["PAYTECH_API_KEY"]
PAYTECH_API_SECRET = st.secrets["PAYTECH_API_SECRET"]

PAYTECH_URL = "https://paytech.sn/api/payment/request-payment"

# --- 2. FONCTION DE PAIEMENT PAYTECH ---
# --- 2. FONCTION DE PAIEMENT PAYTECH ---
def initier_paiement(nom_complet):
    payload = {
        "item_name": f"Adhésion AMEEK - {nom_complet}",
        "item_price": "5000",
        "currency": "XOF",
        "ref_command": f"AMEEK_{int(datetime.datetime.now().timestamp())}",
        "command_name": "Carte de Membre Officielle",
        "env": "test", 
        "ipn_url": "https://ameek-adhesion.streamlit.app", # <-- AJOUTE CETTE LIGNE
        "success_url": "https://ameek-adhesion.streamlit.app",
        "cancel_url": "https://ameek-adhesion.streamlit.app",
    }
    # ... le reste de ton code ne change pas
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "API_KEY": PAYTECH_API_KEY,
        "API_SECRET": PAYTECH_API_SECRET
    }
    try:
        response = requests.post(PAYTECH_URL, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- 3. INTERFACE STREAMLIT ---
st.set_page_config(page_title="AMEEK - Adhésion", layout="centered")

if 'etape' not in st.session_state:
    st.session_state['etape'] = 'formulaire'

# --- ÉTAPE 1 : FORMULAIRE ---
if st.session_state['etape'] == 'formulaire':
    st.image("logo.jpeg", width=100)
    st.title("Formulaire d'Adhésion AMEEK")
    
    with st.form("inscription"):
        prenom = st.text_input("Prénom")
        noms = st.text_input("Noms")
        tel = st.text_input("Téléphone")
        statut = st.radio("Statut", ["ÉTUDIANT", "ÉLÈVE"])
        photo = st.file_uploader("Votre Photo", type=['jpg', 'jpeg', 'png'])
        
        valider = st.form_submit_button("VALIDER ET PAYER (5 000 FCFA)")

    if valider:
        if not prenom or not noms or not photo:
            st.warning("Veuillez remplir tous les champs.")
        else:
            res = initier_paiement(f"{prenom} {noms}")
            if "redirect_url" in res:
                st.session_state['pay_url'] = res['redirect_url']
                st.session_state['temp_data'] = {
                    "prenom": prenom, "noms": noms, "tel": tel, 
                    "statut": statut, "photo": photo.read()
                }
                st.session_state['etape'] = 'paiement'
                st.rerun()
            else:
                st.error(f"Erreur PayTech : {res.get('error', 'Inconnue')}")

# --- ÉTAPE 2 : ATTENTE PAIEMENT ---
elif st.session_state['etape'] == 'paiement':
    st.info("ℹ️ Cliquez sur le lien ci-dessous pour effectuer votre paiement.")
    st.markdown(f"### [👉 CLIQUEZ ICI POUR PAYER SUR PAYTECH]({st.session_state['pay_url']})")
    
    st.warning("⚠️ Une fois le paiement validé sur votre téléphone, cliquez sur le bouton ci-dessous.")
    if st.button("✅ J'AI PAYÉ, GÉNÉRER MA CARTE"):
        st.session_state['etape'] = 'carte'
        st.rerun()

# --- ÉTAPE 3 : GÉNÉRATION DE LA CARTE (Design test.jpeg) ---
# --- ÉTAPE 3 : GÉNÉRATION DE LA CARTE ---
elif st.session_state['etape'] == 'carte':
    data = st.session_state['temp_data']
    largeur, hauteur = 1000, 600
    carte = Image.new('RGB', (largeur, hauteur), color='white')
    dessin = ImageDraw.Draw(carte)
    color_green = (11, 108, 62)

    try:
        # 1. CHARGEMENT DES POLICES (Noms renommés)
        # Si font.ttf n'est pas trouvé, le code affichera l'erreur en bas
        font_large = ImageFont.truetype("font_bold.ttf", 60) # AMEEK
        font_sub = ImageFont.truetype("font_bold.ttf", 30)   # Amicale...
        font_main = ImageFont.truetype("font.ttf", 38)        # Infos
        font_status = ImageFont.truetype("font_bold.ttf", 42)# Statut

        # 2. LOGOS
        logo = Image.open("logo.jpeg").resize((140, 140))
        carte.paste(logo, (30, 20))
        carte.paste(logo, (largeur-170, 20))

        # 3. TEXTES D'EN-TÊTE CENTRÉS
        # Centrage AMEEK
        bbox1 = dessin.textbbox((0, 0), "AMEEK", font=font_large)
        w1 = bbox1[2] - bbox1[0]
        dessin.text(((largeur - w1) / 2, 35), "AMEEK", fill=color_green, font=font_large)

        # Centrage Sous-titre
        txt2 = "AMICALE DES ÉLÈVES ET ÉTUDIANTS DE KOKI"
        bbox2 = dessin.textbbox((0, 0), txt2, font=font_sub)
        w2 = bbox2[2] - bbox2[0]
        dessin.text(((largeur - w2) / 2, 110), txt2, fill="black", font=font_sub)

        # 4. BARRE VERTE ET TEXTE
        barre_y = 175
        dessin.rectangle([0, barre_y, largeur, barre_y + 75], fill=color_green)
        txt3 = "CARTE MEMBRE DE L'AMEEK"
        bbox3 = dessin.textbbox((0, 0), txt3, font=font_sub)
        w3, h3 = bbox3[2] - bbox3[0], bbox3[3] - bbox3[1]
        dessin.text(((largeur - w3) / 2, barre_y + (75 - h3) / 2 - 5), txt3, fill="white", font=font_sub)

        # 5. PHOTO (Alignée sous la barre verte)
        photo_raw = Image.open(io.BytesIO(data['photo']))
        photo_img = ImageOps.fit(photo_raw, (300, 350))
        carte.paste(photo_img, (40, barre_y + 75))

        # 6. INFOS À DROITE
        x_txt = 380
        y_start = barre_y + 110
        dessin.text((x_txt, y_start), f"Tel : {data['tel']}", fill="black", font=font_main)
        dessin.text((x_txt, y_start + 70), f"Prénom : {data['prenom']}", fill="black", font=font_main)
        dessin.text((x_txt, y_start + 140), f"Noms : {data['noms']}", fill="black", font=font_main)
        
        # Statut Vert
        dessin.text((x_txt, y_start + 230), f"{data['statut']} [ X ]", fill=color_green, font=font_status)

        # 7. QR CODE
        qr = qrcode.make("https://www.ameek.sn").resize((140, 140))
        carte.paste(qr, (largeur-210, 380))
        dessin.text((largeur-190, 525), "VALIDER", fill=color_green, font=font_sub)
        dessin.text((largeur-235, 555), "WWW.AMEEK.SN", fill=color_green, font=font_sub)

        # AFFICHAGE
        st.image(carte, use_container_width=True)
        
        # BOUTON TÉLÉCHARGEMENT
        buf = io.BytesIO()
        carte.save(buf, format="PNG")
        st.download_button("📥 TÉLÉCHARGER MA CARTE", buf.getvalue(), f"Carte_{data['noms']}.png", "image/png")

    except Exception as e:
        st.error(f"Erreur : {e}. Vérifiez que 'font.ttf' et 'font_bold.ttf' sont à la racine de votre GitHub.")