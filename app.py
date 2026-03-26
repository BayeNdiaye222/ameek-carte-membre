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
from PIL import Image, ImageDraw, ImageOps, ImageFont
import qrcode
import io
import os
import datetime
import requests

# --- CONFIGURATION PAYTECH ---
PAYTECH_API_KEY = "267bf57a799bd46749bc82949134515b1ea1c3fe1dece4f478a2d24c4f37e1de"
PAYTECH_API_SECRET = "785a0d5093f460a2e8af877f8cc7dc8d76ec144e645e086689fa1dcb28818e88"
PAYTECH_URL = "https://paytech.sn/api/payment/request-payment"

st.set_page_config(page_title="AMEEK - Test Paiement", layout="wide")

if 'etape' not in st.session_state:
    st.session_state['etape'] = 'formulaire'

def initier_paiement_paytech(montant, nom_membre):
    payload = {
        "item_name": f"Adhesion AMEEK - {nom_membre}",
        "item_price": str(montant),
        "currency": "XOF",
        "ref_command": f"AMEEK-{datetime.datetime.now().strftime('%H%M%S')}",
        "command_name": "Carte Membre AMEEK",
        "env": "test",
        "ipn_url": "https://google.com/",
        "success_url": "https://google.com/",
        "cancel_url": "https://google.com/",
        "source": "STML",
        "custom_field": ""
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "API_KEY": PAYTECH_API_KEY,
        "API_SECRET": PAYTECH_API_SECRET
    }
    try:
        response = requests.post(PAYTECH_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        return {"success": -1, "errors": "Erreur Serveur"}
    except Exception as e:
        return {"success": -1, "errors": str(e)}

# --- INTERFACE ---
st.title("🪪 Adhésion AMEEK")

if st.session_state['etape'] == 'formulaire':
    # On crée le formulaire
    with st.form("main_form"):
        col1, col2 = st.columns(2)
        with col1:
            prenom_nom = st.text_input("Prénom et Nom")
            telephone = st.text_input("Téléphone")
            statut = st.selectbox("Statut", ["Étudiant", "Élève", "Enseignant", "Sympathisant"])
        with col2:
            photo = st.file_uploader("Photo", type=['jpg', 'png'])
            st.info("Montant : 5 000 FCFA")
        
        btn_payer = st.form_submit_button("💳 GÉNÉRER LE LIEN DE PAIEMENT")

    # LOGIQUE DE PAIEMENT (Après soumission du formulaire)
    if btn_payer:
        if not prenom_nom or not photo:
            st.error("Veuillez remplir tous les champs et ajouter une photo.")
        else:
            res = initier_paiement_paytech(5000, prenom_nom)
            
            if res.get('success') == 1 or res.get('success') == "1":
                # On stocke les infos temporairement pour ne pas les perdre
                st.session_state['temp_nom'] = prenom_nom
                st.session_state['temp_tel'] = telephone
                st.session_state['temp_photo'] = photo
                st.session_state['pay_url'] = res.get('redirect_url')
            else:
                st.error(f"Erreur PayTech : {res.get('errors')}")

    # AFFICHAGE DU LIEN (En dehors du bouton pour qu'il reste visible)
    if 'pay_url' in st.session_state:
        st.success("✅ Lien de paiement prêt !")
        st.markdown(f"### [👉 CLIQUEZ ICI POUR PAYER SUR PAYTECH]({st.session_state['pay_url']})")
        st.info("Une fois payé sur votre téléphone, cliquez sur le bouton ci-dessous.")
        
        if st.button("🏁 J'ai terminé mon paiement"):
            st.session_state['etape'] = 'carte'
            st.session_state['nom'] = st.session_state['temp_nom']
            st.session_state['tel'] = st.session_state['temp_tel']
            st.session_state['photo'] = st.session_state['temp_photo']
            st.rerun()

# --- ÉTAPE FINALE : AFFICHAGE DE LA CARTE ---
elif st.session_state['etape'] == 'carte':
    st.balloons()
    st.header("🎊 Félicitations, Membre AMEEK !")
    
    # 1. Récupération des données sauvegardées
    nom_membre = st.session_state.get('nom', 'Membre').upper()
    tel_membre = st.session_state.get('tel', '')
    photo_membre = st.session_state.get('photo', None)
    statut_membre = st.session_state.get('statut', 'Sympathisant')

    # 2. Création de la Carte Officielle avec Pillow (PIL)
    from PIL import Image, ImageDraw
    import io

    try:
        # --- A. Création du Fond (Bleu Royal élégant) ---
        largeur, hauteur = 800, 450
        carte = Image.new('RGB', (largeur, hauteur), color=(11, 61, 145)) # Bleu Royal
        dessin = ImageDraw.Draw(carte)

        # Couleurs de texte
        color_gold = (212, 175, 55) # Or
        text_color_white = (255, 255, 255) # Blanc

        # --- B. Intégration de VOTRE LOGO (Fichier logo.png) ---
        try:
            # Chargement du fichier logo.jpeg
            img_logo = Image.open("logo.jpeg")
            # Redimensionnement (ex: 90x90 pixels)
            img_logo = img_logo.resize((90, 90))
            # Placement en haut à gauche (coordonnées x=30, y=20)
            # Le 3ème argument gère la transparence si c'est un PNG transparent
            carte.paste(img_logo, (30, 20), img_logo if img_logo.mode == 'RGBA' else None)
            
            # Texte à côté du logo
            dessin.text((140, 35), "ASSOCIATION AMEEK", fill=color_gold)
            dessin.text((140, 80), "Carte de Membre Officielle", fill=text_color_white)
        except FileNotFoundError:
            st.error("⚠️ Fichier 'logo.png' introuvable dans le dossier.")
            # Texte par défaut si l'image manque
            dessin.text((30, 35), "ASSOCIATION AMEEK", fill=color_gold)

        # --- C. Intégration de VOTRE DRAPEAU (Fichier drapeau.png) ---
        try:
            # Chargement du fichier drapeau.png
            img_flag = Image.open("flag_senegal.jpg")
            # Redimensionnement élégant (ex: 120x80 pixels)
            img_flag = img_flag.resize((120, 80))
            # Placement en haut à droite (x = Largeur - TailleDrapeau - Marge, y=20)
            carte.paste(img_flag, (largeur - 150, 20))
        except FileNotFoundError:
            st.error("⚠️ Fichier 'flag_senegal.jpg' introuvable dans le dossier.")

        # --- D. PHOTO DU MEMBRE (Avec contour Or) ---
        if photo_membre:
            img_photo = Image.open(photo_membre)
            # Redimensionnement élégant de la photo de profil
            img_photo = img_photo.resize((220, 260))
            # Positionnement à gauche sous le logo
            x_photo, y_photo = 30, 140
            carte.paste(img_photo, (x_photo, y_photo))
            
            # Dessin du contour doré autour de la photo
            dessin.rectangle([x_photo-5, y_photo-5, x_photo+225, y_photo+265], outline=color_gold, width=3)

        # --- E. TEXTES ET INFOS (À droite de la photo) ---
        x_texte = 300
        y_label = 170
        line_height = 55 # Espace entre les lignes
        
        # Labels en Or, Valeurs en Blanc
        
        # Ligne Nom
        dessin.text((x_texte, y_label), "NOM :", fill=color_gold)
        dessin.text((x_texte + 90, y_label), nom_membre, fill=text_color_white)
        
        # Ligne Téléphone
        dessin.text((x_texte, y_label + line_height), "TÉL :", fill=color_gold)
        dessin.text((x_texte + 90, y_label + line_height), tel_membre, fill=text_color_white)
        
        # Ligne Date
        dessin.text((x_texte, y_label + 2*line_height), "DATE :", fill=color_gold)
        dessin.text((x_texte + 90, y_label + 2*line_height), datetime.date.today().strftime('%d/%m/%Y'), fill=text_color_white)
        
        # --- F. BADGE DE STATUT (Rectangle Vert de succès) ---
        badg_x, badg_y = x_texte, 350
        dessin.rectangle([badg_x, badg_y, badg_x+320, badg_y+55], fill=(40, 167, 69)) # Vert Succès
        dessin.text((badg_x+15, badg_y+15), f"STATUT : {statut_membre.upper()}", fill=text_color_white)

        # --- G. AFFICHAGE DANS L'APPLICATION ---
        st.image(carte, caption="Votre carte officielle AMEEK à présenter", use_container_width=True)

        # --- H. BOUTON DE TÉLÉCHARGEMENT DE L'IMAGE UNIQUE ---
        buf = io.BytesIO()
        carte.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="💾 TÉLÉCHARGER MA CARTE OFFICIELLE",
            data=byte_im,
            file_name=f"Carte_AMEEK_{nom_membre}.png",
            mime="image/png"
        )

    except Exception as e:
        st.error(f"Erreur technique lors de la création de la carte : {e}")
        st.info("Vérifiez que les fichiers 'logo.png' et 'drapeau.png' sont bien dans le dossier du script.")

    # Bouton pour revenir au formulaire
    if st.button("🔄 Créer une nouvelle adhésion"):
        # Nettoyage de la mémoire
        for key in ['etape', 'nom', 'tel', 'photo', 'temp_nom', 'temp_tel', 'temp_photo', 'pay_url', 'statut']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()