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
from PIL import Image, ImageDraw, ImageFont
import io
import qrcode
import datetime

# --- 1. CONFIGURATION SÉCURISÉE DES CLÉS ---
try:
    PAYTECH_API_KEY = st.secrets["PAYTECH_API_KEY"]
    PAYTECH_API_SECRET = st.secrets["PAYTECH_API_SECRET"]
except:
    st.error("⚠️ Clés API manquantes dans les Secrets Streamlit !")
    st.stop()

PAYTECH_URL = "https://paytech.sn/api/payment/request-payment"

# --- 2. FONCTION DE PAIEMENT PAYTECH ---
def initier_paiement(nom_complet):
    payload = {
        "item_name": f"Adhésion AMEEK - {nom_complet}",
        "item_price": "5000",
        "currency": "XOF",
        "ref_command": f"AMEEK_{int(datetime.datetime.now().timestamp())}",
        "command_name": "Carte de Membre Officielle",
        "env": "test", # Changez en 'prod' quand vous serez prêt
        "success_url": "https://ameek-adhesion.streamlit.app",
        "cancel_url": "https://ameek-adhesion.streamlit.app",
    }
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
elif st.session_state['etape'] == 'carte':
    data = st.session_state['temp_data']
    
    # Création de l'image
    largeur, hauteur = 1000, 600
    carte = Image.new('RGB', (largeur, hauteur), color='white')
    dessin = ImageDraw.Draw(carte)
    
    color_green = (11, 108, 62)
    
    try:
        # Logos aux deux coins
        logo = Image.open("logo.jpeg").resize((120, 120))
        carte.paste(logo, (30, 20))
        carte.paste(logo, (largeur-150, 20))
        
        # En-tête
        dessin.text((380, 40), "AMEEK", fill=color_green, font=None) # Utilise defaut si pas de .ttf
        dessin.text((250, 110), "AMICALE DES ÉLÈVES ET ÉTUDIANTS DE KOKI", fill="black")
        
        # Bandeau vert
        dessin.rectangle([0, 160, largeur, 230], fill=color_green)
        dessin.text((320, 175), "CARTE MEMBRE DE L'AMEEK", fill="white")
        
        # Photo du membre
        photo_img = Image.open(io.BytesIO(data['photo'])).resize((300, 350))
        carte.paste(photo_img, (40, 250))
        
        # Infos Texte
        x_txt = 450
        y_txt = 260
        dessin.text((x_txt, y_txt), f"Tel : {data['tel']}", fill="black")
        dessin.text((x_txt, y_txt+60), f"Prénom : {data['prenom']}", fill="black")
        dessin.text((x_txt, y_txt+120), f"Noms : {data['noms']}", fill="black")
        
        # Statut (Case à cocher)
        status_txt = f"{data['statut']} [ X ]"
        dessin.text((x_txt, y_txt+200), status_txt, fill=color_green)
        
        # QR Code
        qr = qrcode.make("https://www.ameek.sn").resize((150, 150))
        carte.paste(qr, (largeur-200, 350))
        dessin.text((largeur-180, 510), "VALIDER", fill=color_green)
        dessin.text((largeur-210, 540), "WWW.AMEEK.SN", fill=color_green)
        
        st.image(carte, use_container_width=True)
        
        # Download
        buf = io.BytesIO()
        carte.save(buf, format="PNG")
        st.download_button("📥 TÉLÉCHARGER MA CARTE", buf.getvalue(), "carte_ameek.png", "image/png")
        
    except Exception as e:
        st.error(f"Erreur d'image : {e}")