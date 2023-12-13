# Machine Learning Aanbevelingssysteem 🧠

## Inleiding 🚀
Dit project is een machine learning aanbevelingssysteem dat gebruikmaakt van Flask om een API te bieden. Het systeem is ontworpen om productaanbevelingen te doen op basis van productgegevens (content-based filtering) en orderdata (collaborative filtering).
Het systeem is ontworpen om te worden gebruikt met het [Shopify](https://www.shopify.com/) e-commerce platform 🛍️. Het systeem is echter niet afhankelijk van Shopify en kan worden gebruikt met andere e-commerce platforms.
> **⚠️** Andere e-commerce platforms vereisen mogelijk een andere implementatie van product- en bestelgegevens. De huidige implementatie is specifiek voor Shopify.

## Opmerkingen 📝
- Dit project is nog in ontwikkeling. Mogelijk ontbreken er nog functies die met doorontwikkeling worden toegevoegd.
- Het bestand `product_data.csv` bevat productgegevens van Shopify. De gegevens worden ingeladen als fallback wanneer er geen verbinding kan worden gemaakt met de database. De fallback is uit de nieuwe engine-code gehaald.

## Installatie 💾

1. **Kloon de Repository** 👨‍💻
   ```
   git clone https://github.com/youpv/ML-Aanbevelingssysteem.git
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
http://localhost:5137/api/recommendation/<product_handle>/<num_recs>/<customer_id>
```
Vervang `<product_handle>` met de identificatie van het product waarvoor je aanbevelingen wilt ontvangen, `<num_recs>` met het aantal aanbevelingen dat je wilt ontvangen en `<customer_id>` met de identificatie van de klant die de aanbevelingen ontvangt.
Hierbij is `<num_recs>` en `<customer_id>` optioneel. Als je geen waarde voor `<num_recs>` opgeeft, wordt er hetzelfde aantal aanbevelingen gegeven als het aantal producten in de database. Als je geen waarde voor `<customer_id>` opgeeft, verandert er op dit moment niets aan de aanbevelingen. In de toekomst zal dit worden gebruikt om aanbevelingen verder te personaliseren.

## Licentie 📜
Dit project is gelicenseerd onder de CC BY-NC-SA 4.0 licentie - zie de [LICENSE](LICENSE) bestand voor details.

## Bijdragen 👥
Ik accepteer geen bijdragen aan dit project op dit moment. 