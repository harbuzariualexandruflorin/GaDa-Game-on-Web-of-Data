
**Project progress**

Week 6 (31st of October - 6th of November)
 - Formed the group and discussed the topic of the project. (Together)
 - Agreed on a high-level structure and flow of the APIs. (Together)
 - Created a draft document for the project requirements. (Together)
 - Discussed the Database structure. (Florin)

  
Week 7 (7th of November - 13th of November)
 - Describe the main modules. (Stefan)
 - [UML Diagrams](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/Software%20Architecture/Class%20Diagram) (Florin)
 - [Use-case Diagrams](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/Software%20Architecture/Use%20Case%20Diagram) (Andrei)
 - Formulated a potential RDF schema. (Together)

  
Week 8 (14th of November - 20th of November)
 - [OpenAPI specification](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/Open%20API) (Florin)
 - [JsonLD models](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/JSON%20Models) (Andrei)
 - [ScholarlyHTML](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/Scholarly%20HTML) introduction, proposed solution, architecture sections. (Stefan)

  
Week 9 (21st of November - 27th of November)
 - [ScholarlyHTML](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/Scholarly%20HTML) UI section. (Stefan)
 - [ScholarlyHTML](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/blob/main/Documentation/Software%20Architecture/architecture/architecture.jpg) Architecture diagram. (Florin)
 - [ScholarlyHTML](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/Scholarly%20HTML) Data modelling section. (Andrei)
 - [Project progress document](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/blob/main/Documentation/gada_project_progress.md) (Stefan)


Week 10 (28th of November - 4th of December)
- [Studying the structure of the external APIs](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/External%20APIs/Sample%20Calls) used for building the GaDa ontology. (Florin)


Week 11 (5th of December - 11th of December)
- Extract necessary information from the APIs: Marvel, Pokemon, Star Trek, Star Wars. (Florin)


Week 12 (12th of December - 18th of December)
- Extract additional information using other APIs: DuckDuckGo for avatars and SuperHero API for Marvel characters. (Florin)
- [Process the data obtained](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/External%20APIs/Processed%20JSONs) (calculate the score for each card, get an avatar image for all cards). (Florin)
- Building the Quiz API structure (Andrei)


Week 13 (19th of December - 23rd of December)
- Research existing vocabularies that can be used for the GaDa ontology. (Florin)
- Constructing the [GaDa ontology](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/blob/main/Documentation/Ontology/Full%20Ontology/gada_ontology.ttl). (Florin)
- Start working with [dotNetRDF](https://dotnetrdf.org/) for making Sparql queries in the Quiz API. (Andrei)


Winter vacation (24th of December - 8th of January)
- Choose a triplestore database and populate it with the ontology created as a turtle file. (Florin)
- Research how to implement the frontend architecture. (Stefan)
- Implementation of the [Quiz API](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Implementation/Backend/QuizAPI). (Andrei)


Week 14 (9nd of January - 15th of January)
- [JSON-LD generation](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/JSON%20Models) and parsing method to convert them to normal JSON. (Florin)
- User management functionalities for their scores: [relational database](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/blob/main/Documentation/Software%20Architecture/Relational%20Database%20Schema/db_schema.png) using SQLITE. (Florin)
- The main page and card game of the frontend (HTML & CSS). (Stefan)
- [API Gateway](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Implementation/Backend/ApiGateway) implementation. (Andrei)

Week 15 (16th of January - 22nd of January)
- [Finalizing](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/Open%20API) the GaDa card API. (Florin)
- Finalizing Quiz API and API Gateway. (Andrei)
- Deployment of the final application on ngrok (using nginx). (Florin)
- Help with [integrating and fetching data](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/blob/main/Implementation/Frontend/gameJS/cards.js) from the cards API and using them in the frontend interface. (Florin)
- Javascript [game logic](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/blob/main/Implementation/Frontend/gameJS/game.js) for the card game. (Stefan)
- Implementing the main flow for the frontend application. (Stefan)
- Implementation of quiz, user high scores and wiki components on Frontend and integrating them with Card and Quiz APIs. (Andrei)


Week 16/17 (23rd of January - 1st of February)
- Designing the end screen for the frontend application. (Stefan)
- [ScholarlyHTML](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/Scholarly%20HTML): Updated the Introduction, Proposed Solution, Card Game Logic, UI, References sections. (Stefan)
- [ScholarlyHTML](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/Scholarly%20HTML): Updated the Introduction, Proposed Solution, Architecture, SPARQL Queries, Technologies Used, References sections. Created the: User Management, Game Cards Management, Use of External Data sections. (Florin)
- [[ScholarlyHTML](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/Scholarly%20HTML)]: Updated OpenApi, Architecture, UI, Game Quiz Management, UML Diagram, SPARQL Queries, Technologies Used, References sections and finishing formatting the document. (Andrei)
- [UserGuide](https://github.com/harbuzariualexandruflorin/GaDa-Game-on-Web-of-Data/tree/main/Documentation/User%20Guide%20HTML): (Stefan)


#project #infoiasi #wade #web
