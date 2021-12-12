# Projet Nosql

Anne-Sophie Besnard et Agathe Da Costa


## Démarrage du projet

Pour lancer le projet : 
```
git clone https://gitlab.pedago.ensiie.fr/anne-sophie.besnard/projet-nosql.git
cd projet-nosql
docker-compose up -d --build
```

Pour arrêter le projet : 
```
docker-compose down
```

## Structure

Nous avons un site web fait à l'aide du framework Flask (facile et pratique d'utilisation) et de bootstrap pour le CSS.

Les technologies utilisées pour les bases de données sont :
- Mongodb
pour vérifier la persistance des données de mongodb :
```
docker exec -it mongo-nosql mongo
```
- Postegres-sql
pour vérifier la persistance des données en postgres :
```
docker exec -it xxx
```



