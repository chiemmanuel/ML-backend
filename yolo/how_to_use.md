- Add the best.pt (weight) of the model you want to integrate to the "models" directory

- For easier identification, rename the weight to what purpose it serves or the model it comes from e.g : yolo\models\team_chambe_3L_fine_tune.pt

- Update the path to the weight in the custom control model in the control_models directory e.g: model_path = "team_chambe_3L_fine_tune.pt"

- Launch Docker app

- Run "docker-compose up --build"

- In label studio, add model in the model section in settings

     - connect model

     - enter model name

     - enter backend url : localhost:9090
     
     - validate and save


- NOTES
1 - The classes in label studio should be same as the classes in the model 
2 - The label type should be rectangle labels in label studio and custom control model

##########################################################################################################################

- Ajouter le best.pt (poids) du modèle que vous souhaitez intégrer dans le répertoire "models"

- Pour une identification plus simple, renommer le fichier de poids selon son utilité ou le modèle d’origine
ex : yolo\models\team_chambe_3L_fine_tune.pt

- Mettre à jour le chemin vers le poids dans le modèle de contrôle personnalisé dans le répertoire control_models
ex : model_path = "team_chambe_3L_fine_tune.pt"

- Lancer l’application Docker

- Exécuter : docker-compose up --build

- Dans Label Studio, ajouter le modèle dans la section Models des paramètres

    - Connect model

    - Entrer le nom du modèle

    - Entrer l’URL du backend : localhost:9090

    - Valider et enregistrer

NOTES
1 - Les classes dans Label Studio doivent être identiques à celles du modèle
2 - Le type de label doit être rectangle labels dans Label Studio et dans le modèle de contrôle personnalisé