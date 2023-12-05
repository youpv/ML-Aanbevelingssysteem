# Machine Learning Aanbevelingssysteem 🧠

## Inleiding 🚀
Dit project is een machine learning aanbevelingssysteem dat gebruikmaakt van Flask om een API te bieden. Het systeem is ontworpen om productaanbevelingen te doen op basis van productgegevens (content-based filtering).
Het systeem is ontworpen om te worden gebruikt met het [Shopify](https://www.shopify.com/) e-commerce platform 🛍️. Het systeem is echter niet afhankelijk van Shopify en kan worden gebruikt met andere e-commerce platforms.

> **Opmerking📝:** Dit project is nog in ontwikkeling en is nog niet klaar voor productie. In de toekomst wordt het systeem uitgebreid met collaborative filtering en feedback loops.
>
> Het bestand `product_data.csv` bevat productgegevens van [Shopify](https://www.shopify.com/). De gegevens worden ingeladen als fallback wanneer er geen verbinding kan worden gemaakt met de database.

## Installatie 💾

1. **Kloon de Repository** 👨‍💻
   ```
   git clone https://github.com/youpv/Python.git
   cd Python
   ```

2. **Installeer Vereisten** 📦
   Installeer de benodigde Python-pakketten.
   ```
   pip install -r requirements.txt
   ```

3. **Configureer de Database** 🗄️
   - Zorg ervoor dat je een PostgreSQL-database hebt.
   - Kopieer het `.env.example` bestand naar een nieuw bestand genaamd `.env`.
   - Bewerk het `.env` bestand en voeg je database URL toe:
     ```
     DATABASE_URL=postgres://user:password@host:port/database
     ```

4. **Start de Flask Applicatie** 🌟
   ```
   python main.py
   ```

## Gebruik 📋
De API biedt endpoints om aanbevelingen te krijgen voor producten. Gebruik de volgende URL om aanbevelingen te vragen:
```
http://localhost:5137/api/recommendation/<product_handle>/<num_recs>
```
Vervang `<product_handle>` met de identificatie van het product waarvoor je aanbevelingen wilt ontvangen en `<num_recs>` met het aantal aanbevelingen dat je wilt ontvangen.

## Licentie 📜
De licentie voor dit project zal later worden toegevoegd. Vermelding van de auteur is verplicht.

## Bijdragen 👥
Ik accepteer geen bijdragen aan dit project op dit moment. 