# CSGO Cases Code Extractor

Ce projet combine le téléchargement automatique d'images depuis Instagram et l'extraction de codes promo à partir de ces images.

## Installation

1. Installez les dépendances :
```bash
pip install -r requirements.txt
```

2. Installez Tesseract OCR :
   - Windows : Téléchargez depuis https://github.com/UB-Mannheim/tesseract/wiki
   - Assurez-vous que le chemin vers tesseract.exe est correct dans le code

3. Configurez vos credentials Instagram :
   - Créez un fichier `.env` à la racine du projet
   - Ajoutez vos credentials :
   ```
   INSTAGRAM_USERNAME=votre_email@gmail.com
   INSTAGRAM_PASSWORD=votre_mot_de_passe
   ```

## Utilisation

### Script principal (recommandé)
```bash
python main.py
```

Ce script va :
1. Télécharger automatiquement la dernière image du compte @csgocasescom
2. Extraire le code promo de l'image
3. Sauvegarder le code dans `downloaded_images/latest_code.txt`

### Scripts individuels

#### Téléchargement d'image uniquement
```bash
python download_image.py
```

#### Extraction de code uniquement
```bash
python extraire_code.py [chemin_vers_image]
```

## Structure des fichiers

- `main.py` : Script principal combinant téléchargement et extraction
- `download_image.py` : Script de téléchargement d'images Instagram
- `extraire_code.py` : Script d'extraction de codes promo
- `requirements.txt` : Dépendances Python
- `.env` : Variables d'environnement (à créer)
- `downloaded_images/` : Dossier contenant les images téléchargées et codes extraits

## Sécurité

⚠️ **Important** : Ne partagez jamais votre fichier `.env` qui contient vos credentials Instagram. Ce fichier est automatiquement ignoré par Git.

## Fonctionnalités

- Téléchargement automatique depuis Instagram
- Extraction de codes promo avec OCR (Tesseract)
- Multiple prétraitements d'images pour améliorer la reconnaissance
- Gestion des erreurs et logging
- Sauvegarde automatique des codes extraits 



pour facebook

https://github.com/hikaruAi/FacebookBot
https://chatgpt.com/c/6868606d-f50c-8009-b6f3-fa1a845b5904